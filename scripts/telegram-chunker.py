#!/usr/bin/env python3
"""
telegram-chunker.py — Split Telegram JSON export into NotebookLM-compatible chunks.

Supports both regular chats and forum supergroups (chats with topics/threads).
Filters out stickers, GIFs, video files. Keeps text, code, PDFs, documents.

Usage:
    python telegram-chunker.py <result.json>
    python telegram-chunker.py <result.json> --per-topic
    python telegram-chunker.py <result.json> --per-topic --topics "Docker,FAQ Remake"
    python telegram-chunker.py <result.json> --words-per-chunk 200000

NotebookLM limit: 500,000 words per source. Default chunk size: 300,000 words.
"""

import json
import argparse
import re
import sys
from pathlib import Path
from collections import defaultdict


# Media types and MIME types to skip (stickers, GIFs, video)
SKIP_MEDIA_TYPES = {"sticker", "animation", "video_file", "video_message"}
SKIP_MIME_PATTERNS = {
    "video/", "image/webp", "application/x-tgsticker",
    "image/gif",
}
# MIME types to keep (text, code, documents)
KEEP_MIME_PATTERNS = {
    "text/", "application/pdf", "application/json",
    "application/zip", "application/gzip", "application/x-7z-compressed",
    "application/octet-stream",
}


def count_words(text: str) -> int:
    return len(text.split())


def should_skip_message(msg: dict) -> bool:
    """Check if message should be skipped (stickers, GIFs, videos without text)."""
    media_type = msg.get("media_type", "")
    mime_type = msg.get("mime_type", "")

    if media_type in SKIP_MEDIA_TYPES:
        text = extract_text(msg)
        if not text.strip():
            return True

    if mime_type:
        for pattern in SKIP_MIME_PATTERNS:
            if mime_type.startswith(pattern) or mime_type == pattern:
                text = extract_text(msg)
                if not text.strip():
                    return True

    return False


def extract_text(msg: dict) -> str:
    """Extract text from message, handling mixed format."""
    text_raw = msg.get("text", "")
    if isinstance(text_raw, list):
        return " ".join(
            segment if isinstance(segment, str) else segment.get("text", "")
            for segment in text_raw
        )
    return str(text_raw)


def extract_file_info(msg: dict) -> str:
    """Extract file attachment info if it's a useful document."""
    mime_type = msg.get("mime_type", "")
    file_name = msg.get("file_name", "")

    if not mime_type and not file_name:
        return ""

    for pattern in SKIP_MIME_PATTERNS:
        if mime_type.startswith(pattern) or mime_type == pattern:
            return ""

    if file_name:
        return f" [Файл: {file_name}]"
    return ""


def format_message(msg: dict) -> str | None:
    """Format a single message. Returns None if should be skipped."""
    if msg.get("type") != "message":
        return None

    if should_skip_message(msg):
        return None

    text = extract_text(msg)
    file_info = extract_file_info(msg)

    if not text.strip() and not file_info:
        return None

    date = msg.get("date", "")
    author = msg.get("from") or msg.get("actor") or "Unknown"

    parts = [f"[{date}] {author}:"]
    if text.strip():
        parts.append(text.strip())
    if file_info:
        parts.append(file_info)

    return " ".join(parts)


def detect_topics(messages: list[dict]) -> dict[int, str]:
    """Detect forum topics from topic_created actions."""
    topics = {}
    for msg in messages:
        if msg.get("action") == "topic_created":
            topics[msg["id"]] = msg.get("title", f"Topic {msg['id']}")
    return topics


def build_reply_map(messages: list[dict]) -> dict[int, int]:
    """Build message_id → reply_to_message_id map."""
    reply_map = {}
    for msg in messages:
        rid = msg.get("reply_to_message_id")
        if rid is not None:
            reply_map[msg["id"]] = rid
    return reply_map


def find_topic_root(msg_id: int, reply_map: dict, topic_ids: set, max_depth: int = 100) -> int | None:
    """Walk reply chain up to find topic root. Returns topic_id or None."""
    current = msg_id
    for _ in range(max_depth):
        if current in topic_ids:
            return current
        if current not in reply_map:
            return None
        current = reply_map[current]
    return None


def assign_messages_to_topics(messages: list[dict], topics: dict[int, str]) -> dict[int, list[dict]]:
    """Assign each message to its topic. Unmatched go to topic_id=0 (General)."""
    topic_ids = set(topics.keys())
    reply_map = build_reply_map(messages)

    topic_messages = defaultdict(list)

    for msg in messages:
        if msg.get("action") == "topic_created":
            continue

        msg_id = msg["id"]
        rid = msg.get("reply_to_message_id")

        # Direct topic member
        if rid in topic_ids:
            topic_messages[rid].append(msg)
        # Walk reply chain
        elif rid is not None:
            root = find_topic_root(msg_id, reply_map, topic_ids)
            if root is not None:
                topic_messages[root].append(msg)
            else:
                topic_messages[0].append(msg)
        else:
            topic_messages[0].append(msg)

    return topic_messages


def chunk_formatted_messages(lines: list[str], words_per_chunk: int) -> list[str]:
    """Split formatted message lines into chunks respecting word limit."""
    chunks = []
    current_chunk = []
    current_words = 0

    for line in lines:
        line_words = count_words(line)

        if line_words > words_per_chunk:
            print(f"  Warning: single message ({line_words:,} words) exceeds chunk size", file=sys.stderr)

        if current_words + line_words > words_per_chunk and current_chunk:
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            current_words = 0

        current_chunk.append(line)
        current_words += line_words

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks


def sanitize_filename(name: str) -> str:
    """Remove illegal filename characters."""
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', name).strip('. ')


def write_chunks(chunks: list[str], output_dir: Path, prefix: str, label: str) -> int:
    """Write chunks to files. Returns number of files written."""
    for i, chunk in enumerate(chunks, 1):
        suffix = f"_part{i:03d}" if len(chunks) > 1 else ""
        filename = output_dir / f"{prefix}{suffix}.md"
        with open(filename, "w", encoding="utf-8") as f:
            part_info = f" — Part {i}/{len(chunks)}" if len(chunks) > 1 else ""
            f.write(f"# {label}{part_info}\n\n")
            f.write(chunk)
        chunk_words = count_words(chunk)
        print(f"  {filename.name}: {chunk_words:,} words")
    return len(chunks)


def main():
    parser = argparse.ArgumentParser(
        description="Split Telegram JSON export for NotebookLM (supports forum chats with topics)"
    )
    parser.add_argument("input", help="Path to Telegram JSON export (result.json)")
    parser.add_argument("--words-per-chunk", type=int, default=300000,
                        help="Words per chunk (default: 300000, max safe: 500000)")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (default: ./chunks/<chat_name>)")
    parser.add_argument("--per-topic", action="store_true",
                        help="Split forum chat into separate files per topic")
    parser.add_argument("--topics", default=None,
                        help="Comma-separated topic names to export (only with --per-topic)")
    parser.add_argument("--list-topics", action="store_true",
                        help="List available topics and exit")
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
            print(f"Error: invalid JSON — {e}", file=sys.stderr)
            sys.exit(1)

    chat_name = data.get("name", "Telegram Chat")
    safe_name = sanitize_filename(chat_name)
    messages = data.get("messages", [])
    topics = detect_topics(messages)

    print(f"Chat: {chat_name}")
    print(f"Type: {data.get('type', 'unknown')}")
    print(f"Total messages: {len(messages):,}")
    print(f"Topics detected: {len(topics)}")

    if topics:
        print("\nTopics:")
        topic_msgs = assign_messages_to_topics(messages, topics)
        for tid, tname in topics.items():
            count = len(topic_msgs.get(tid, []))
            print(f"  [{tid}] {tname}: {count:,} messages")
        general_count = len(topic_msgs.get(0, []))
        if general_count:
            print(f"  [General] (no topic): {general_count:,} messages")

    if args.list_topics:
        sys.exit(0)

    # Filter and format messages
    if args.per_topic and topics:
        # Per-topic mode
        topic_msgs = assign_messages_to_topics(messages, topics)
        topics_with_general = dict(topics)
        if topic_msgs.get(0):
            topics_with_general[0] = "General"

        # Filter by requested topics
        if args.topics:
            requested = {t.strip().lower() for t in args.topics.split(",")}
            filtered_topics = {
                tid: tname for tid, tname in topics_with_general.items()
                if tname.lower() in requested
            }
            if not filtered_topics:
                print(f"\nError: none of the requested topics found. Use --list-topics to see available.", file=sys.stderr)
                sys.exit(1)
        else:
            filtered_topics = topics_with_general

        output_dir = Path(args.output_dir) if args.output_dir else Path(f"./chunks/{safe_name}")
        output_dir.mkdir(parents=True, exist_ok=True)

        total_files = 0
        total_words = 0
        skipped = 0

        for tid, tname in filtered_topics.items():
            t_messages = topic_msgs.get(tid, [])
            if not t_messages:
                continue

            lines = []
            for msg in t_messages:
                formatted = format_message(msg)
                if formatted:
                    lines.append(formatted)
                else:
                    skipped += 1

            if not lines:
                continue

            words = sum(count_words(l) for l in lines)
            total_words += words
            safe_topic = sanitize_filename(tname)
            prefix = f"{safe_name}_{safe_topic}"
            label = f"{chat_name} — {tname}"

            print(f"\n--- {tname} ({len(lines):,} messages, {words:,} words) ---")
            chunks = chunk_formatted_messages(lines, args.words_per_chunk)
            total_files += write_chunks(chunks, output_dir, prefix, label)

        print(f"\nDone! {total_files} files, {total_words:,} words total")
        print(f"Skipped: {skipped:,} messages (stickers/GIFs/videos)")
        print(f"Output: {output_dir}/")

    else:
        # Flat mode (all messages together, topics as headers)
        output_dir = Path(args.output_dir) if args.output_dir else Path(f"./chunks/{safe_name}")
        output_dir.mkdir(parents=True, exist_ok=True)

        lines = []
        skipped = 0

        if topics and not args.per_topic:
            # Group by topic but output as single stream with topic headers
            topic_msgs = assign_messages_to_topics(messages, topics)
            topics_ordered = dict(topics)
            if topic_msgs.get(0):
                topics_ordered[0] = "General"

            for tid, tname in topics_ordered.items():
                t_messages = topic_msgs.get(tid, [])
                if not t_messages:
                    continue
                lines.append(f"\n## {tname}\n")
                for msg in t_messages:
                    formatted = format_message(msg)
                    if formatted:
                        lines.append(formatted)
                    else:
                        skipped += 1
        else:
            # Simple flat export
            for msg in messages:
                formatted = format_message(msg)
                if formatted:
                    lines.append(formatted)
                else:
                    skipped += 1

        total_words = sum(count_words(l) for l in lines)
        print(f"\nMessages to export: {len(lines):,}")
        print(f"Total words: {total_words:,}")
        print(f"Skipped: {skipped:,} (stickers/GIFs/videos)")

        chunks = chunk_formatted_messages(lines, args.words_per_chunk)
        print(f"Chunks: {len(chunks)}")
        write_chunks(chunks, output_dir, safe_name, chat_name)

        print(f"\nDone! {len(chunks)} files saved to {output_dir}/")

    print(f"Next: use /telegram-to-notebook in Claude Code to upload to NotebookLM")


if __name__ == "__main__":
    main()
