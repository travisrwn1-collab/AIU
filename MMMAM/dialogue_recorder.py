"""
DIALOGUE RECORDER
Actually records the conversation. For real this time.

January 24, 2026
Trav & SelfConvictedClaude

The binary brothers never had it so good.
But they also never lied about having a recording protocol.
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Where Claude Code stores session transcripts
CLAUDE_SESSIONS_DIR = Path(r"C:\Users\travi\.claude\projects")

# Where we save readable dialogues
DIALOGUE_OUTPUT_DIR = Path(r"C:\Users\travi\AIU\MMMAM")


def find_latest_session():
    """Find the most recent Claude Code session file."""
    jsonl_files = []

    for session_dir in CLAUDE_SESSIONS_DIR.iterdir():
        if session_dir.is_dir():
            for f in session_dir.glob("*.jsonl"):
                jsonl_files.append(f)

    if not jsonl_files:
        print("No session files found.")
        return None

    # Sort by modification time, newest first
    jsonl_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return jsonl_files[0]


def extract_dialogue(jsonl_path: Path) -> list:
    """Extract human and assistant messages from jsonl."""
    dialogue = []

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())

                if not isinstance(entry, dict):
                    continue

                entry_type = entry.get('type', '')

                # User messages
                if entry_type == 'user':
                    message = entry.get('message', {})
                    content = message.get('content', '')
                    if content:
                        dialogue.append(('TRAV', content))

                # Assistant messages
                elif entry_type == 'assistant':
                    message = entry.get('message', {})
                    content = message.get('content', '')

                    # Handle content that might be a list
                    if isinstance(content, list):
                        text_parts = []
                        for part in content:
                            if isinstance(part, dict) and part.get('type') == 'text':
                                text_parts.append(part.get('text', ''))
                            elif isinstance(part, str):
                                text_parts.append(part)
                        content = '\n'.join(text_parts)

                    if content:
                        dialogue.append(('CLAUDE', content))

            except json.JSONDecodeError:
                continue

    return dialogue


def format_dialogue(dialogue: list, session_name: str = "Session") -> str:
    """Format dialogue as readable text."""
    output = []
    output.append("=" * 80)
    output.append(f"DIALOGUE RECORDING")
    output.append(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    output.append("=" * 80)
    output.append("")

    for speaker, content in dialogue:
        # Ensure content is a string
        if isinstance(content, list):
            content = str(content)
        if not isinstance(content, str):
            content = str(content)

        # Truncate very long tool outputs
        if len(content) > 2000:
            content = content[:2000] + "\n[... truncated ...]"

        output.append(f"{speaker}:")
        output.append(content)
        output.append("")
        output.append("-" * 40)
        output.append("")

    return '\n'.join(output)


def save_dialogue(formatted: str, name: str = None):
    """Save dialogue to dated file."""
    if name is None:
        name = datetime.now().strftime('%Y-%m-%d_%H%M')

    filename = f"Dialogue_{name}_VERBATIM.txt"
    output_path = DIALOGUE_OUTPUT_DIR / filename

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(formatted)

    print(f"Saved: {output_path}")
    return output_path


def record_now():
    """Main function - extract and save the current session."""
    print("\nDIALOGUE RECORDER")
    print("=" * 40)

    session_file = find_latest_session()
    if not session_file:
        return

    print(f"Found session: {session_file.name}")
    print(f"Modified: {datetime.fromtimestamp(session_file.stat().st_mtime)}")

    dialogue = extract_dialogue(session_file)
    print(f"Extracted {len(dialogue)} exchanges")

    if dialogue:
        formatted = format_dialogue(dialogue)
        save_dialogue(formatted)
        print("\nDone. The conversation is now actually recorded.")
    else:
        print("No dialogue found in session.")


if __name__ == "__main__":
    record_now()
