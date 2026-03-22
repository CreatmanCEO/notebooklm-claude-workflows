#!/bin/bash
# nlm-auth-check.sh — Check NotebookLM auth and notify if expired

LOG_FILE="$HOME/Documents/scripts/nlm-auth.log"
mkdir -p "$(dirname "$LOG_FILE")"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Check auth by listing notebooks
RESULT=$(PYTHONIOENCODING=utf-8 nlm notebook list 2>&1)

if echo "$RESULT" | grep -q '"id"'; then
    COUNT=$(echo "$RESULT" | grep -c '"id"')
    echo "[$TIMESTAMP] AUTH OK — $COUNT notebooks accessible" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] AUTH EXPIRED — run: nlm login" >> "$LOG_FILE"
    # Windows toast notification (try BurntToast first, fallback to MessageBox)
    powershell.exe -Command "
        try {
            New-BurntToastNotification -Text 'NotebookLM Auth', 'Cookies expired! Run: nlm login'
        } catch {
            Add-Type -AssemblyName PresentationFramework
            [System.Windows.MessageBox]::Show('NotebookLM cookies expired! Run: nlm login', 'NotebookLM Auth', 'OK', 'Warning')
        }
    " 2>/dev/null
fi
