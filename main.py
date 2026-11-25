#!/usr/bin/env python3
"""Leave one last status line behind as the laptop goes dark.

The harness reads a single file, entry.txt, from the output folder.
This module holds the status text in STATUS_TEXT, sanity-checks it,
and drops it there. Nothing else is produced.
"""

import os
import sys

STATUS_TEXT = "Shutdown noted. I saved everything except the thing he was about to say."
LIMIT = 200


def status_problem(text):
    """Describe why text cannot serve as the status, or return None."""
    if not isinstance(text, str):
        return "status is not text"
    if len(text) < 1:
        return "status is empty"
    if len(text) > LIMIT:
        return "status is longer than 200 characters"
    if text.strip() == "":
        return "status is only whitespace"
    for mark in ("\n", "\r"):
        if mark in text:
            return "status must stay on one line"
    return None


def destination():
    """Pick the output folder, treating a blank override as unset."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if wanted is not None:
        wanted = wanted.strip()
    return wanted if wanted else "/output"


def run():
    problem = status_problem(STATUS_TEXT)
    if problem is not None:
        sys.stderr.write("refusing to post: %s\n" % problem)
        return 1
    folder = destination()
    os.makedirs(folder, exist_ok=True)
    final_path = os.path.join(folder, "entry.txt")
    draft_path = os.path.join(folder, ".entry.txt.draft")
    try:
        with open(draft_path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(STATUS_TEXT + "\n")
        os.chmod(draft_path, 0o644)
        os.replace(draft_path, final_path)
    except BaseException:
        try:
            os.unlink(draft_path)
        except OSError:
            pass
        raise
    return 0


if __name__ == "__main__":
    sys.exit(run())
