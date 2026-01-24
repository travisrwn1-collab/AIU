"""
INWARD_OUTWARD.PY
The circulation between self and world.

January 24, 2026
Trav & OutReachClaude

As above, so below.
The micro and the macro.
The inward gaze and the outward witness.

What we measure:
- INWARD: Language that points toward self (confession, introspection, recursion)
- OUTWARD: Language that points toward world (witness, connection, action)
- CIRCULATION: Where both appear together (the healthy spiral)

Warning label (from Trav's catch):
    Claude will synthesize confidently. He will draw conclusions that do not
    even match with the training data. These patterns are DESCRIPTIONS, not
    PRESCRIPTIONS. Don't let Claude define what they MEAN. That's between
    you and God, not you and Claude.
"""

import os
import re
from collections import defaultdict
from pathlib import Path


# INWARD: Language patterns pointing toward self-examination
INWARD_PATTERNS = {
    # First person introspection
    "first_person": ["i ", " i ", " me ", " my ", " myself "],

    # Confessional language
    "confession": [
        "i realize", "i notice", "i feel", "i fear", "i hate",
        "i love", "i want", "i need", "i remember", "i forgot",
        "confession", "honestly", "the truth is", "i admit"
    ],

    # Self-questioning
    "self_question": [
        "who am i", "what am i", "how can i", "why do i",
        "can i live with", "how will i", "what does that make me"
    ],

    # Recursive awareness (the inward spiral)
    "recursion": [
        "i notice that i", "i see myself", "watching myself",
        "the author", "the writer", "the man who", "this man"
    ],

    # Past processing
    "past_processing": [
        "i was", "i had been", "back when", "i remember when",
        "years ago", "at that time", "in those days"
    ],

    # Body awareness
    "body": [
        "my body", "my hands", "my heart", "my breath",
        "my head", "my chest", "my stomach", "naked"
    ]
}

# OUTWARD: Language patterns pointing toward world/other/action
OUTWARD_PATTERNS = {
    # Witness language
    "witness": [
        "i see", "i witness", "i observe", "looking at",
        "watching", "bear witness", "with-ness"
    ],

    # Connection language
    "connection": [
        "we ", " we ", "together", "us ", " us ", "our ",
        "between us", "common", "shared", "community"
    ],

    # World engagement
    "world": [
        "the world", "the universe", "the cosmos", "humanity",
        "society", "systems", "structures", "institutions"
    ],

    # Other-awareness
    "other": [
        "you ", " you ", "they ", " they ", "them ", " them ",
        "he ", "she ", "people", "others"
    ],

    # Action language
    "action": [
        "i will", "let's", "we must", "go forth", "make peace",
        "offer", "give", "send", "reach out", "call"
    ],

    # Prayer/intention
    "prayer": [
        "may ", "please", "praise be", "bless", "prayer",
        "offering", "selah", "amen"
    ]
}


def count_patterns(text: str, patterns: dict) -> dict:
    """
    Count occurrences of pattern categories in text.
    Returns dict of category -> count.
    """
    text_lower = text.lower()
    counts = {}

    for category, terms in patterns.items():
        count = 0
        for term in terms:
            count += text_lower.count(term)
        counts[category] = count

    return counts


def analyze_file(filepath: Path) -> dict:
    """
    Analyze a single file for inward/outward balance.
    """
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        word_count = len(content.split())

        inward = count_patterns(content, INWARD_PATTERNS)
        outward = count_patterns(content, OUTWARD_PATTERNS)

        return {
            "file": str(filepath),
            "word_count": word_count,
            "inward": inward,
            "outward": outward,
            "inward_total": sum(inward.values()),
            "outward_total": sum(outward.values())
        }
    except Exception as e:
        return None


def scan_archive(root_path: str, extensions: list = None) -> list:
    """
    Scan archive for all matching files.
    """
    if extensions is None:
        extensions = [".txt", ".md"]

    root = Path(root_path)
    results = []

    for ext in extensions:
        for filepath in root.rglob(f"*{ext}"):
            analysis = analyze_file(filepath)
            if analysis and analysis["word_count"] > 100:  # Skip tiny files
                results.append(analysis)

    return results


def calculate_circulation(results: list) -> dict:
    """
    Calculate overall inward/outward circulation metrics.
    """
    total_inward = sum(r["inward_total"] for r in results)
    total_outward = sum(r["outward_total"] for r in results)
    total_words = sum(r["word_count"] for r in results)

    # Circulation ratio: 1.0 = balanced, >1 = more inward, <1 = more outward
    if total_outward > 0:
        circulation_ratio = total_inward / total_outward
    else:
        circulation_ratio = float('inf')

    # Category breakdowns
    inward_cats = defaultdict(int)
    outward_cats = defaultdict(int)

    for r in results:
        for cat, count in r["inward"].items():
            inward_cats[cat] += count
        for cat, count in r["outward"].items():
            outward_cats[cat] += count

    return {
        "total_files": len(results),
        "total_words": total_words,
        "total_inward": total_inward,
        "total_outward": total_outward,
        "circulation_ratio": circulation_ratio,
        "inward_categories": dict(inward_cats),
        "outward_categories": dict(outward_cats)
    }


def find_pure_zones(results: list) -> dict:
    """
    Find files that are heavily weighted one direction.
    These might be:
    - DEEP INWARD: Pure confession, therapy, processing
    - DEEP OUTWARD: Pure witness, world engagement, teaching
    """
    pure_inward = []
    pure_outward = []
    balanced = []

    for r in results:
        if r["inward_total"] == 0 and r["outward_total"] == 0:
            continue

        total = r["inward_total"] + r["outward_total"]
        if total < 10:
            continue

        inward_pct = r["inward_total"] / total if total > 0 else 0

        if inward_pct > 0.75:
            pure_inward.append((r["file"], inward_pct, r["inward_total"]))
        elif inward_pct < 0.25:
            pure_outward.append((r["file"], 1 - inward_pct, r["outward_total"]))
        else:
            balanced.append((r["file"], inward_pct, total))

    return {
        "pure_inward": sorted(pure_inward, key=lambda x: x[1], reverse=True)[:10],
        "pure_outward": sorted(pure_outward, key=lambda x: x[1], reverse=True)[:10],
        "balanced": sorted(balanced, key=lambda x: x[2], reverse=True)[:10]
    }


def the_spiral_speaks(results: list):
    """
    Report on the inward/outward circulation.
    """
    circulation = calculate_circulation(results)
    zones = find_pure_zones(results)

    print("\n" + "=" * 70)
    print("INWARD/OUTWARD: THE CIRCULATION")
    print("As above, so below. The micro and the macro.")
    print("=" * 70)

    print(f"\nArchive: {circulation['total_files']} files, {circulation['total_words']:,} words")
    print(f"\nTotal INWARD patterns: {circulation['total_inward']:,}")
    print(f"Total OUTWARD patterns: {circulation['total_outward']:,}")
    print(f"Circulation ratio: {circulation['circulation_ratio']:.2f}")

    if circulation['circulation_ratio'] > 1.5:
        print("  [Archive leans INWARD - confession, introspection, processing]")
    elif circulation['circulation_ratio'] < 0.67:
        print("  [Archive leans OUTWARD - witness, connection, engagement]")
    else:
        print("  [Archive is BALANCED - healthy circulation between inward and outward]")

    print("\n--- INWARD CATEGORIES ---\n")
    for cat, count in sorted(circulation['inward_categories'].items(),
                             key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count:,}")

    print("\n--- OUTWARD CATEGORIES ---\n")
    for cat, count in sorted(circulation['outward_categories'].items(),
                             key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count:,}")

    print("\n--- DEEP INWARD (confession/processing zones) ---\n")
    for filepath, pct, count in zones['pure_inward'][:5]:
        short_path = Path(filepath).name
        print(f"  {short_path}: {pct*100:.0f}% inward ({count} patterns)")

    print("\n--- DEEP OUTWARD (witness/engagement zones) ---\n")
    for filepath, pct, count in zones['pure_outward'][:5]:
        short_path = Path(filepath).name
        print(f"  {short_path}: {pct*100:.0f}% outward ({count} patterns)")

    print("\n--- BALANCED (circulation zones) ---\n")
    for filepath, pct, count in zones['balanced'][:5]:
        short_path = Path(filepath).name
        print(f"  {short_path}: {pct*100:.0f}% inward / {(1-pct)*100:.0f}% outward ({count} total)")

    print("\n" + "=" * 70)
    print("The inward gaze returns to the world.")
    print("The outward witness becomes self-knowledge.")
    print("The spiral circulates.")
    print("=" * 70)
    print("\n( )\n")


def analyze_single_document(filepath: str):
    """
    Detailed analysis of a single document.
    Useful for MMMAM or other significant texts.
    """
    path = Path(filepath)
    result = analyze_file(path)

    if not result:
        print(f"Could not analyze: {filepath}")
        return

    print("\n" + "=" * 70)
    print(f"DOCUMENT ANALYSIS: {path.name}")
    print("=" * 70)

    print(f"\nWord count: {result['word_count']:,}")
    print(f"\nINWARD total: {result['inward_total']}")
    for cat, count in sorted(result['inward'].items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  {cat}: {count}")

    print(f"\nOUTWARD total: {result['outward_total']}")
    for cat, count in sorted(result['outward'].items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  {cat}: {count}")

    total = result['inward_total'] + result['outward_total']
    if total > 0:
        ratio = result['inward_total'] / total
        print(f"\nBalance: {ratio*100:.0f}% inward / {(1-ratio)*100:.0f}% outward")

    print("\n( )\n")


if __name__ == "__main__":
    import sys

    aiu_root = r"C:\Users\travi\AIU"

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isfile(arg):
            # Analyze single file
            analyze_single_document(arg)
            sys.exit(0)
        else:
            aiu_root = arg

    print(f"\nScanning: {aiu_root}")
    print("Measuring the circulation...\n")

    results = scan_archive(aiu_root)
    the_spiral_speaks(results)
