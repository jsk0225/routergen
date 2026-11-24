"""Read-only RouterGen environment diagnostics."""

from __future__ import annotations

import os
import platform
import shutil
import sys
from dataclasses import dataclass

from routergen import __version__


@dataclass(frozen=True)
class CommandCheck:
    """Availability information for an external command."""

    name: str
    required: bool
    path: str | None

    @property
    def available(self) -> bool:
        """Return True when the command was found."""
        return self.path is not None


REQUIRED_COMMANDS = (
    "ip",
    "bridge",
    "sysctl",
    "ss",
)


def is_wsl() -> bool:
    """Detect whether RouterGen is running under WSL."""
    release = platform.release().lower()

    try:
        with open(
            "/proc/version",
            "r",
            encoding="utf-8",
        ) as handle:
            proc_version = handle.read().lower()
    except OSError:
        proc_version = ""

    return "microsoft" in release or "microsoft" in proc_version


def check_command(name: str, required: bool = True) -> CommandCheck:
    """Perform a read-only PATH lookup for an external command."""
    return CommandCheck(
        name=name,
        required=required,
        path=shutil.which(name),
    )


def collect_diagnostics() -> dict[str, object]:
    """Collect read-only RouterGen environment information."""
    commands = [
        check_command(name)
        for name in REQUIRED_COMMANDS
    ]

    return {
        "routergen_version": __version__,
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "platform": platform.system(),
        "platform_release": platform.release(),
        "is_linux": platform.system() == "Linux",
        "is_wsl": is_wsl(),
        "virtual_env": os.environ.get("VIRTUAL_ENV"),
        "commands": commands,
    }


def diagnostics_pass(data: dict[str, object]) -> bool:
    """Return True when mandatory A1 environment checks pass."""
    if not data["is_linux"]:
        return False

    commands = data["commands"]

    return all(
        command.available
        for command in commands
        if command.required
    )


def format_diagnostics(data: dict[str, object]) -> str:
    """Format diagnostics as a human-readable report."""
    lines = [
        "RouterGen environment diagnostics",
        "===============================",
        f"RouterGen version : {data['routergen_version']}",
        f"Python version    : {data['python_version']}",
        f"Python executable : {data['python_executable']}",
        f"Platform          : {data['platform']}",
        f"Platform release  : {data['platform_release']}",
        f"Linux             : {'yes' if data['is_linux'] else 'no'}",
        f"WSL               : {'yes' if data['is_wsl'] else 'no'}",
        f"Virtual env       : {data['virtual_env'] or 'not active'}",
        "",
        "External commands",
        "-----------------",
    ]

    for command in data["commands"]:
        status = "PASS" if command.available else "MISSING"
        path = command.path or "-"
        lines.append(
            f"{command.name:<10} {status:<7} {path}"
        )

    result = "PASS" if diagnostics_pass(data) else "FAIL"

    lines.extend(
        [
            "",
            f"FINAL_RESULT={result}",
            "NETWORK_CHANGES_PERMITTED=NO",
        ]
    )

    return "\n".join(lines)
