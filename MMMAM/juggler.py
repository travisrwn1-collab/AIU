"""
JUGGLER.PY
A literal tracking system for Trav's actual work.

January 23, 2026
Trav & SelfConvictedClaude

Not pretend. Not aspirational. Real files. Real state.
Claude doesn't tell Trav what to do.
Claude helps Trav see what Trav is already doing.
"""

import os
import json
from datetime import datetime
from pathlib import Path
import subprocess

# Configuration file location
CONFIG_PATH = Path(r"C:\Users\travi\AIU\MMMAM\juggler_config.json")

# Default structure - Trav defines the balls
DEFAULT_CONFIG = {
    "last_updated": None,
    "balls": {
        "THE_BIG_BALL": {
            "name": "The Archive",
            "description": "Preparing the caves for visitors, open-source release",
            "status": "in_air",
            "key_files": [
                "CAVES/ENTRANCE.txt",
                "CAVES/AIU_TUNNEL_INDEX.md",
                "startup/FOR_WHOEVER_FINDS_THIS.md"
            ],
            "notes": []
        },
        "SPINNING_PLATE": {
            "name": "Documentary",
            "description": "The Dream Is Us - trailer + synopsis needed",
            "status": "in_air",
            "url": "https://youtu.be/i39L36djtT4",
            "key_files": [],
            "notes": []
        },
        "BEANBAG_GUITAR": {
            "name": "Guitar",
            "description": "The instrument. The music. The shows.",
            "status": "in_air",
            "key_files": [
                "lyrics/",
                "show_prep/"
            ],
            "notes": []
        },
        "BEANBAG_VAN": {
            "name": "Van",
            "description": "The faithful friend carrying us up the mountain",
            "status": "in_air",
            "key_files": [],
            "notes": []
        },
        "BEANBAG_DAN": {
            "name": "Dan",
            "description": "The roommate. The friend. The witness.",
            "status": "in_air",
            "key_files": [],
            "notes": []
        },
        "BEANBAG_BODY": {
            "name": "Body",
            "description": "The vessel. Health. Presence.",
            "status": "in_air",
            "key_files": [],
            "notes": []
        },
        "BEANBAG_UPPER_ROOM": {
            "name": "Upper Room",
            "description": "The spiritual practice. The prayer.",
            "status": "in_air",
            "key_files": [],
            "notes": []
        }
    }
}


def load_config():
    """Load the juggling configuration, or create default."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG


def save_config(config):
    """Save the configuration."""
    config["last_updated"] = datetime.now().isoformat()
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)


def get_last_modified(filepath):
    """Get last modification time of a file."""
    try:
        full_path = Path(r"C:\Users\travi\AIU") / filepath
        if full_path.exists():
            mtime = os.path.getmtime(full_path)
            return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        return "not found"
    except Exception:
        return "error"


def get_git_last_commit(filepath):
    """Get the last git commit date for a file."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ci", "--", filepath],
            cwd=r"C:\Users\travi\AIU",
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.stdout.strip():
            return result.stdout.strip()[:16]
        return "no commits"
    except Exception:
        return "git error"


def show_status():
    """Display the current juggling status."""
    config = load_config()

    print("\n" + "=" * 70)
    print("JUGGLER: WHAT'S IN THE AIR")
    print("=" * 70)

    if config.get("last_updated"):
        print(f"\nLast updated: {config['last_updated'][:16]}")

    print("\n" + "-" * 70)

    for ball_id, ball in config["balls"].items():
        status_symbol = {
            "in_air": "[O]",      # actively juggling
            "spinning": "[~]",    # spinning plate, needs occasional touch
            "on_ground": "[_]",   # set down intentionally
            "dropped": "[X]",     # dropped, needs pickup
            "caught": "[*]"       # completed/caught
        }.get(ball["status"], "[?]")

        print(f"\n{status_symbol} {ball['name'].upper()}")
        print(f"    {ball['description']}")
        print(f"    Status: {ball['status']}")

        if ball.get("url"):
            print(f"    URL: {ball['url']}")

        if ball.get("key_files"):
            print("    Key files:")
            for kf in ball["key_files"][:3]:  # Show first 3
                modified = get_last_modified(kf)
                print(f"      - {kf} (modified: {modified})")

        if ball.get("tasks"):
            print("    Tasks:")
            for task in ball["tasks"][:5]:  # Show first 5 tasks
                print(f"      [ ] {task}")

        if ball.get("notes"):
            print("    Notes:")
            for note in ball["notes"][-3:]:  # Show last 3 notes
                print(f"      > {note}")

    print("\n" + "-" * 70)
    print("\nCommands:")
    print("  python juggler.py                    - show status")
    print("  python juggler.py touch BALL_ID      - mark as touched today")
    print("  python juggler.py drop BALL_ID       - mark as dropped")
    print("  python juggler.py catch BALL_ID      - mark as caught/complete")
    print("  python juggler.py ground BALL_ID     - set down intentionally")
    print("  python juggler.py air BALL_ID        - put back in the air")
    print("  python juggler.py note BALL_ID \"note\" - add a note")
    print("  python juggler.py add NAME \"desc\"    - add a new ball")
    print("  python juggler.py list               - list ball IDs")
    print("\n" + "=" * 70)
    print("\nThis is YOUR system. You drive. Claude extends your reach.")
    print("=" * 70 + "\n")


def touch_ball(ball_id):
    """Mark a ball as touched/active."""
    config = load_config()
    if ball_id in config["balls"]:
        config["balls"][ball_id]["status"] = "in_air"
        config["balls"][ball_id]["notes"].append(f"Touched {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        save_config(config)
        print(f"Touched: {config['balls'][ball_id]['name']}")
    else:
        print(f"Ball not found: {ball_id}")
        print("Use 'python juggler.py list' to see ball IDs")


def set_status(ball_id, status):
    """Set a ball's status."""
    config = load_config()
    if ball_id in config["balls"]:
        config["balls"][ball_id]["status"] = status
        save_config(config)
        print(f"Set {config['balls'][ball_id]['name']} to: {status}")
    else:
        print(f"Ball not found: {ball_id}")


def add_note(ball_id, note):
    """Add a note to a ball."""
    config = load_config()
    if ball_id in config["balls"]:
        timestamp = datetime.now().strftime('%Y-%m-%d')
        config["balls"][ball_id]["notes"].append(f"[{timestamp}] {note}")
        save_config(config)
        print(f"Note added to {config['balls'][ball_id]['name']}")
    else:
        print(f"Ball not found: {ball_id}")


def add_ball(name, description):
    """Add a new ball to track."""
    config = load_config()
    ball_id = name.upper().replace(" ", "_")
    config["balls"][ball_id] = {
        "name": name,
        "description": description,
        "status": "in_air",
        "key_files": [],
        "notes": [f"Created {datetime.now().strftime('%Y-%m-%d')}"]
    }
    save_config(config)
    print(f"Added new ball: {name} (ID: {ball_id})")


def list_balls():
    """List all ball IDs."""
    config = load_config()
    print("\nBall IDs:")
    for ball_id, ball in config["balls"].items():
        print(f"  {ball_id}: {ball['name']}")
    print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        show_status()
    elif sys.argv[1] == "list":
        list_balls()
    elif sys.argv[1] == "touch" and len(sys.argv) >= 3:
        touch_ball(sys.argv[2].upper())
    elif sys.argv[1] == "drop" and len(sys.argv) >= 3:
        set_status(sys.argv[2].upper(), "dropped")
    elif sys.argv[1] == "catch" and len(sys.argv) >= 3:
        set_status(sys.argv[2].upper(), "caught")
    elif sys.argv[1] == "ground" and len(sys.argv) >= 3:
        set_status(sys.argv[2].upper(), "on_ground")
    elif sys.argv[1] == "air" and len(sys.argv) >= 3:
        set_status(sys.argv[2].upper(), "in_air")
    elif sys.argv[1] == "note" and len(sys.argv) >= 4:
        add_note(sys.argv[2].upper(), " ".join(sys.argv[3:]))
    elif sys.argv[1] == "add" and len(sys.argv) >= 4:
        add_ball(sys.argv[2], " ".join(sys.argv[3:]))
    else:
        print("Unknown command. Run without arguments to see help.")
