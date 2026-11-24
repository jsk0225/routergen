"""RouterGen command-line interface."""

from __future__ import annotations

import argparse

from routergen import __version__
from routergen.diagnostics import (
    collect_diagnostics,
    diagnostics_pass,
    format_diagnostics,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the RouterGen CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="routergen",
        description=(
            "Safety-first topology compiler for reproducible "
            "Linux router environments."
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"RouterGen {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "diagnose",
        help="Run read-only environment diagnostics.",
    )

    return parser


def main() -> int:
    """RouterGen CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "diagnose":
        data = collect_diagnostics()
        print(format_diagnostics(data))
        return 0 if diagnostics_pass(data) else 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
