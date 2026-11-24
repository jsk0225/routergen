"""Tests for RouterGen read-only diagnostics."""

from routergen.diagnostics import (
    CommandCheck,
    diagnostics_pass,
    format_diagnostics,
)


def make_data(*, is_linux=True, command_available=True):
    """Create deterministic diagnostic test data."""
    path = "/usr/bin/example" if command_available else None

    return {
        "routergen_version": "0.2.0.dev0",
        "python_version": "3.10.0",
        "python_executable": "/example/python",
        "platform": "Linux" if is_linux else "Other",
        "platform_release": "test",
        "is_linux": is_linux,
        "is_wsl": False,
        "virtual_env": "/example/.venv",
        "commands": [
            CommandCheck(
                name="example",
                required=True,
                path=path,
            )
        ],
    }


def test_diagnostics_pass_when_requirements_are_available():
    data = make_data()

    assert diagnostics_pass(data) is True


def test_diagnostics_fail_when_required_command_is_missing():
    data = make_data(command_available=False)

    assert diagnostics_pass(data) is False


def test_diagnostics_fail_on_non_linux_platform():
    data = make_data(is_linux=False)

    assert diagnostics_pass(data) is False


def test_report_declares_network_changes_not_permitted():
    data = make_data()

    report = format_diagnostics(data)

    assert "FINAL_RESULT=PASS" in report
    assert "NETWORK_CHANGES_PERMITTED=NO" in report
