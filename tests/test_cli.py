"""Test CLI."""
from unittest.mock import patch

from click.testing import CliRunner
from pytest import mark

from semvergit.app import SemverGit
from semvergit.cli import cli


@mark.parametrize("dry_run", [True, False])
@mark.parametrize("log_level", ["standard", "quiet", "debug"])
@mark.parametrize("bump_type", ["major", "minor", "patch", "prerelease"])
def test_cli(dry_run: bool, bump_type: str, log_level: str) -> None:
    """Test CLI."""
    runner = CliRunner()
    args = []
    args.append("--bump_type")
    args.append(bump_type)
    args.append("--log_level")
    args.append(log_level)
    if dry_run:
        args.append("--dry_run")
    with patch.object(SemverGit, "update", spec=SemverGit) as mock_update:
        result = runner.invoke(cli, args)
    mock_update.assert_called_once()
    assert not result.exception
    assert result.exit_code == 0


@mark.parametrize("arg", ["--bump_type", "-t", "--log_level", "-l"])
def test_cli_invalid_bump_type(arg: str) -> None:
    """Test CLI errors with invalid bump type."""
    runner = CliRunner()
    args = []
    args.append(arg)
    args.append("invalid")
    with patch.object(SemverGit, "update", spec=SemverGit) as mock_update:
        result = runner.invoke(cli, args)
    mock_update.assert_not_called()
    assert result.exception
    assert result.exit_code == 2
