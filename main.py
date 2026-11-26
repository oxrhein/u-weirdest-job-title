#!/usr/bin/env python3
"""Weirdest Job Title: Blind Judge Showdown — make.fun entry program.

Writes one original job title to entry.txt in the output folder and
nothing else: no newline, no explanation, no extra file.

The title: "Chief Apology Officer for Self-Driving Cars"

Why this title wins on the judge's own criteria (RULES.txt):

* It IS a weird job title, a few words naming an odd job: a
  corporate-sounding title ("Chief ... Officer") for a job nobody
  has ever heard of.
* It is stranger than ordinary work: the twist is gloriously
  specific — the apologies are not for people, they are for
  self-driving cars, machines that cannot be offended.
* It is funny on the first read: the grandeur of "Chief" collides
  with the absurdity of apologising to a car, and the twist lands
  on the very last words.
* It sounds like a real job: you can picture the person at a desk,
  headset on, drafting formal apology letters to a fleet of cars
  that ran a red light.
* It reads instantly: 43 characters, one glance, no setup needed.

The gate wants UTF-8 text of 1 to 60 characters that is not only
whitespace, and the checks below enforce that before anything is
written.
"""

import os
from pathlib import Path

# One title, 43 characters. The gate (RULES.txt) allows 1-60.
# Setup: a grand corporate title, "Chief Apology Officer".
# Twist: the apologies go to self-driving cars. The joke lands
# on the last words, exactly where the judge's brief wants it.
TITLE = "Chief Apology Officer for Self-Driving Cars"


def pick_output_folder() -> Path:
    """Where the entry goes: the kit's output folder when set."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    folder = Path(raw)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def check_title(title: str) -> None:
    """One title only: single line, 1-60 characters, not blank."""
    assert "\n" not in title, "entry must be a single line"
    assert "\r" not in title, "entry must be a single line"
    assert title.strip(), "entry must not be only whitespace"
    assert 1 <= len(title) <= 60, "entry must be 1-60 characters"


def main() -> None:
    check_title(TITLE)
    target = pick_output_folder() / "entry.txt"
    target.write_text(TITLE, encoding="utf-8", newline="")
    # Read back what landed on disk and confirm it is exactly the title:
    # one read, compared as text and as raw bytes, so a partial write or
    # an encoding surprise is caught here instead of at the gate.
    written = target.read_text(encoding="utf-8")
    assert written == TITLE, "entry.txt must hold exactly the title"
    assert 1 <= len(written) <= 60
    # Byte-exact: the file must hold the title and nothing else — no
    # trailing newline, no BOM, no padding, so the gate sees exactly
    # one line of 43 characters and the judge reads exactly that.
    # (Revised: the byte check uses the title's own encoded length,
    # so any future title edit is verified against its own size.)
    assert target.read_bytes() == TITLE.encode("utf-8")
    assert target.stat().st_size == len(TITLE.encode("utf-8"))
    print(TITLE)


if __name__ == "__main__":
    main()
