#!/usr/bin/env python3
"""
telegram-chunker.py — Split Telegram JSON export into NotebookLM-compatible chunks.

Usage:
    python telegram-chunker.py <input.json> [--words-per-chunk 300000] [--output-dir ./chunks]

NotebookLM limit: 500,000 words per source. Default chunk size: 300,000 words (safe margin).
"""

import json
import argparse
import os
import re
import sys
from pathlib import Path


def count_words(text: str) -> int:
    return len(text.split())


def extract_messages(data: dict) -> list[dict]:
    """Extract messages from Telegram JSON export."""
    messages = data.get("messages", [])
    result = []
    for msg in messages:
        if msg.get("type") != "message":
            continue
        # Handle text that can be string or list of segments
        text_raw = msg.get("text", "")
        if isinstance(text_raw, list):
            text = " ".join(
                segment if isinstance(segment, str) else segment.get("text", "")
                for segment in text_raw
            )
        else:
            text = str(text_raw)
        if not text.strip():
            continue
        date = msg.get("date", "")
        author = msg.get("from") or msg.get("actor") or "Unknown"
        result.append({"date": date, "author": author, "text": text})
    return result


def chunk_messages(messages: list[dict], words_per_chunk: int) -> list[str]:
    """Split messages into chunks respecting word limit."""
    chunks = []
    current_chunk_lines = []
    current_words = 0

    for msg in messages:
        line = f"[{msg['date']}] {msg['author']}: {msg['text']}"
        line_words = count_words(line)

        if line_words > words_per_chunk:
            print(f"  Warning: single message ({line_words:,} words) exceeds chunk size ({words_per_chunk:,} words), adding as-is", file=sys.stderr)

        if current_words + line_words > words_per_chunk and current_chunk_lines:
            chunks.append("\n".join(current_chunk_lines))
            current_chunk_lines = []
            current_words = 0

        current_chunk_lines.append(line)
        current_words += line_words

    if current_chunk_lines:
        chunks.append("\n".join(current_chunk_lines))

    return chunks


def main():
    parser = argparse.ArgumentParser(description="Split Telegram JSON export for NotebookLM")
    parser.add_argument("input", help="Path to Telegram JSON export (result.json)")
    parser.add_argument("--words-per-chunk", type=int, default=300000,
                        help="Words per chunk (default: 300000, max safe: 500000)")
    parser.add_argument("--output-dir", default="./chunks",
                        help="Output directory for chunk files")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Reading {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: {input_path} is not valid JSON. Make sure you exported with format 'Machine-readable JSON'.\n{e}", file=sys.stderr)
            sys.exit(1)

    chat_name = data.get("name", "Telegram Chat")
    chat_name = re.sub(r'[<>:"/\\|?*]', '_', chat_name)
    messages = extract_messages(data)
    total_words = sum(count_words(m["text"]) for m in messages)

    print(f"Chat: {chat_name}")
    print(f"Messages: {len(messages):,}")
    print(f"Total words: {total_words:,}")

    chunks = chunk_messages(messages, args.words_per_chunk)
    print(f"Chunks: {len(chunks)} (at {args.words_per_chunk:,} words each)")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, chunk in enumerate(chunks, 1):
        filename = output_dir / f"{chat_name}_part{i:03d}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {chat_name} — Part {i}/{len(chunks)}\n\n")
            f.write(chunk)
        chunk_words = count_words(chunk)
        print(f"  {filename.name}: {chunk_words:,} words")

    print(f"\nDone! {len(chunks)} files saved to {output_dir}/")
    print(f"Next: use /telegram-to-notebook in Claude Code to upload to NotebookLM")


if __name__ == "__main__":
    main()
