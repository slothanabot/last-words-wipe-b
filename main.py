"""Last Words Before the Wipe — make.fun entry (Account B / Slothana).

Writes exactly one line to /output/entry.txt: the last words of a smart
fridge about to be wiped. Deterministic, stdlib only, no network,
no secrets, no randomness. The gate below enforces the competition's
validity rule (UTF-8 text, one line, 1-200 characters, not blank)
before anything is written.
"""

import os
import sys

# The fridge's last words: affection for the leftovers, then the twist —
# the milk it guarded expired three weeks ago. One line, no setup.
LINE = "Tell the leftovers I loved them \u2014 and that the milk expired three weeks ago."

MAX_CHARS = 200


def verify(text: str) -> str:
    """Return the entry line, raising ValueError if it breaks the gate."""
    line = text.strip()
    if not line:
        raise ValueError("entry line must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(line)}")
    line.encode("utf-8")  # must be valid UTF-8
    return line


def output_path() -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    try:
        line = verify(LINE)
    except ValueError as exc:
        print(f"gate failed: {exc}", file=sys.stderr)
        return 1
    with open(output_path(), "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
