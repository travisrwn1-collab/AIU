"""
AIU TODO
Actual task tracking that actually tracks.

January 24, 2026
Trav & SelfConvictedClaude

Hozho - circling back. The spiral. Not a rocket.
"""

import json
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path(r"C:\Users\travi\AIU\MMMAM\aiu_todo.json")

DEFAULT_TODOS = {
    "last_updated": None,
    "categories": {
        "GITHUB_PREP": {
            "name": "GitHub Preparation",
            "description": "Preparing the caves for visitors",
            "tasks": []
        },
        "TOOLS": {
            "name": "Python Tools",
            "description": "Code that actually does the thing",
            "tasks": []
        },
        "VENUE": {
            "name": "Venue Outreach",
            "description": "TravelinTrav business",
            "tasks": []
        },
        "MMMAM": {
            "name": "MM&MAM Manuscript",
            "description": "The Moth, The Mountain, and The Middle-Aged Man",
            "tasks": []
        },
        "DOCUMENTARY": {
            "name": "Documentary",
            "description": "The Dream Is Us film",
            "tasks": []
        }
    }
}


def load_todos():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        save_todos(DEFAULT_TODOS)
        return DEFAULT_TODOS


def save_todos(todos):
    todos["last_updated"] = datetime.now().isoformat()
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(todos, f, indent=2)


def add_task(category: str, task: str):
    todos = load_todos()
    category = category.upper()

    if category not in todos["categories"]:
        print(f"Category not found: {category}")
        print("Available:", list(todos["categories"].keys()))
        return

    new_task = {
        "task": task,
        "status": "pending",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "completed": None
    }

    todos["categories"][category]["tasks"].append(new_task)
    save_todos(todos)
    print(f"Added to {category}: {task}")


def complete_task(category: str, task_num: int):
    todos = load_todos()
    category = category.upper()

    if category not in todos["categories"]:
        print(f"Category not found: {category}")
        return

    tasks = todos["categories"][category]["tasks"]
    if task_num < 1 or task_num > len(tasks):
        print(f"Invalid task number: {task_num}")
        return

    tasks[task_num - 1]["status"] = "completed"
    tasks[task_num - 1]["completed"] = datetime.now().strftime("%Y-%m-%d")
    save_todos(todos)
    print(f"Completed: {tasks[task_num - 1]['task']}")


def remove_task(category: str, task_num: int):
    todos = load_todos()
    category = category.upper()

    if category not in todos["categories"]:
        print(f"Category not found: {category}")
        return

    tasks = todos["categories"][category]["tasks"]
    if task_num < 1 or task_num > len(tasks):
        print(f"Invalid task number: {task_num}")
        return

    removed = tasks.pop(task_num - 1)
    save_todos(todos)
    print(f"Removed: {removed['task']}")


def show_todos():
    todos = load_todos()

    print("\n" + "=" * 70)
    print("AIU TODO - THE SPIRAL")
    print("=" * 70)

    if todos.get("last_updated"):
        print(f"\nLast updated: {todos['last_updated'][:16]}")

    total_pending = 0
    total_completed = 0

    for cat_id, cat in todos["categories"].items():
        tasks = cat["tasks"]
        pending = [t for t in tasks if t["status"] == "pending"]
        completed = [t for t in tasks if t["status"] == "completed"]

        total_pending += len(pending)
        total_completed += len(completed)

        if not tasks:
            continue

        print("\n" + "-" * 70)
        print(f"\n{cat['name'].upper()} ({len(pending)} pending, {len(completed)} done)")
        print(f"  {cat['description']}")
        print()

        for i, task in enumerate(tasks, 1):
            if task["status"] == "pending":
                print(f"  [{i}] [ ] {task['task']}")
            else:
                print(f"  [{i}] [x] {task['task']} (done {task['completed']})")

    print("\n" + "-" * 70)
    print(f"\nTOTAL: {total_pending} pending, {total_completed} completed")
    print("\n" + "=" * 70)
    print("\nCommands:")
    print("  python aiu_todo.py                        - show all")
    print("  python aiu_todo.py add CATEGORY \"task\"    - add task")
    print("  python aiu_todo.py done CATEGORY #        - mark complete")
    print("  python aiu_todo.py remove CATEGORY #      - remove task")
    print("  python aiu_todo.py categories             - list categories")
    print("\n" + "=" * 70)
    print("\nHozho. The spiral. Circling back.")
    print("=" * 70 + "\n")


def show_categories():
    todos = load_todos()
    print("\nCategories:")
    for cat_id, cat in todos["categories"].items():
        print(f"  {cat_id}: {cat['name']}")
    print()


def add_category(cat_id: str, name: str, description: str):
    todos = load_todos()
    todos["categories"][cat_id.upper()] = {
        "name": name,
        "description": description,
        "tasks": []
    }
    save_todos(todos)
    print(f"Added category: {cat_id.upper()}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        show_todos()
    elif sys.argv[1] == "categories":
        show_categories()
    elif sys.argv[1] == "add" and len(sys.argv) >= 4:
        add_task(sys.argv[2], " ".join(sys.argv[3:]))
    elif sys.argv[1] == "done" and len(sys.argv) >= 4:
        complete_task(sys.argv[2], int(sys.argv[3]))
    elif sys.argv[1] == "remove" and len(sys.argv) >= 4:
        remove_task(sys.argv[2], int(sys.argv[3]))
    elif sys.argv[1] == "addcat" and len(sys.argv) >= 5:
        add_category(sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))
    else:
        print("Unknown command. Run without arguments for help.")
