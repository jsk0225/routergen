"""Tests for the RouterGen command-line interface."""

from routergen import __version__
from routergen.cli import build_parser, main


def test_version_is_current_development_version():
    assert __version__ == "0.2.0.dev0"


def test_parser_program_name():
    parser = build_parser()
    assert parser.prog == "routergen"


def test_cli_main_returns_success(monkeypatch):
    monkeypatch.setattr("sys.argv", ["routergen"])
    assert main() == 0
