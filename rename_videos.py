"""
Rename all video files in a folder to sequential numbers: 1.mp4, 2.mkv, 3.mp4 ...

Usage:
    python rename_videos.py
Then answer the prompts (folder path, starting number, etc.).
"""

import os
import uuid

VIDEO_EXTENSIONS = {
    ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
    ".m4v", ".mpg", ".mpeg", ".3gp", ".ts", ".vob", ".ogv",
}


def main():
    folder = input("Folder path: ").strip().strip('"').strip("'")
    if not os.path.isdir(folder):
        print("That folder doesn't exist.")
        return

    start_text = input("Start numbering from (default 1): ").strip()
    start = int(start_text) if start_text else 1

    order = input("Order by [n]ame or [d]ate modified? (default n): ").strip().lower()
    pad = input("Zero-pad numbers like 001, 002? (y/N): ").strip().lower() == "y"

    videos = [
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
        and os.path.splitext(f)[1].lower() in VIDEO_EXTENSIONS
    ]

    if not videos:
        print("No video files found.")
        return

    if order == "d":
        videos.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)))
    else:
        videos.sort(key=str.lower)

    width = len(str(start + len(videos) - 1)) if pad else 0

    plan = []
    for i, name in enumerate(videos, start=start):
        ext = os.path.splitext(name)[1].lower()
        new_name = f"{str(i).zfill(width)}{ext}"
        plan.append((name, new_name))

    # Preview
    print(f"\nFound {len(videos)} videos. Preview:")
    for old, new in plan[:10]:
        print(f"  {old}  ->  {new}")
    if len(plan) > 10:
        print(f"  ... and {len(plan) - 10} more")

    if input("\nGo ahead and rename? (y/N): ").strip().lower() != "y":
        print("Cancelled. Nothing was changed.")
        return

    # Pass 1: rename to unique temp names (avoids clashes like an existing "3.mp4")
    temp_names = []
    for old, new in plan:
        temp = f"__tmp_{uuid.uuid4().hex}{os.path.splitext(old)[1]}"
        os.rename(os.path.join(folder, old), os.path.join(folder, temp))
        temp_names.append((temp, new))

    # Pass 2: rename temp names to final numbers
    for temp, new in temp_names:
        os.rename(os.path.join(folder, temp), os.path.join(folder, new))

    # Save a log so you can see what became what
    log_path = os.path.join(folder, "rename_log.txt")
    with open(log_path, "w", encoding="utf-8") as log:
        for old, new in plan:
            log.write(f"{old} -> {new}\n")

    print(f"Done! Renamed {len(plan)} files. Log saved to {log_path}")


if __name__ == "__main__":
    main()
