"""Test CLI."""
from click.testing import CliRunner

from semvergit.cli import cli


def test_cli() -> None:
    """Test CLI."""
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
