"""Test CLI."""
from unittest.mock import patch

from click.testing import CliRunner
from pytest import mark

from semvergit.app import SemverGit
from semvergit.cli import cli


@mark.parametrize("quiet, dry_run", [(True, True), (True, False), (False, True), (False, False)])
@mark.parametrize("bump_type", ["major", "minor", "patch", "prerelease"])
def test_cli(quiet: bool, dry_run: bool, bump_type: str) -> None:
    """Test CLI."""
    runner = CliRunner()
    args = []
    if quiet:
        args.append("--quiet")
    if dry_run:
        args.append("--dry_run")
    args.append("--bump_type")
    args.append(bump_type)
    with patch.object(SemverGit, "update", spec=SemverGit) as mock_update:
        result = runner.invoke(cli, args)
    mock_update.assert_called_once()
    assert not result.exception
    assert result.exit_code == 0


def test_cli_debug() -> None:
    """Test CLI debug."""
    runner = CliRunner()
    args = ["--debug"]
    args.append("--bump_type")
    args.append("patch")

    with patch.object(SemverGit, "update", spec=SemverGit) as mock_update:
        result = runner.invoke(cli, args)
    mock_update.assert_called_once()
    assert result.exit_code == 0
