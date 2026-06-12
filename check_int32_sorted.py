#!/usr/bin/env python3
"""Check that an int32 binary file is sorted in nondecreasing order."""

from __future__ import annotations

import argparse
from array import array
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a sorted int32 binary file.")
    parser.add_argument("file", type=Path)
    parser.add_argument("--buffer", type=int, default=100_000)
    args = parser.parse_args()

    previous = None
    total = 0

    with args.file.open("rb") as f:
        while True:
            values = array("i")
            try:
                values.fromfile(f, args.buffer)
            except EOFError:
                pass

            if not values:
                break

            for value in values:
                if previous is not None and value < previous:
                    raise SystemExit(
                        f"Not sorted at index {total}: {value} < {previous}"
                    )
                previous = value
                total += 1

    print(f"OK: {args.file} is sorted, integers checked: {total}")


if __name__ == "__main__":
    main()
