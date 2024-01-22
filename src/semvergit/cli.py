"""CLI for semvergit."""
import sys
from typing import Optional

import click

from semvergit.app import BumpType, SemverGit
from semvergit.log_utils import LogLevel, set_logger


def validate_bump_type(
    ctx: click.Context, param: click.Parameter, value: str  # pylint: disable=unused-argument
) -> BumpType:
    """Validate bump type."""
    try:
        return BumpType(value)
    except ValueError as exp:
        raise click.BadParameter(f"Please select from {BumpType.print_options()}") from exp


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.version_option()
@click.option("--dry_run", "-d", is_flag=True, help="Dry run", default=False)
@click.option("--verbose", "-v", count=True, help="Verbose", default=0, type=click.IntRange(0, 2))
@click.option(
    "--bump_type",
    "-t",
    envvar="BUMP_TYPE",
    type=click.UNPROCESSED,
    help=f"Bump Type {BumpType.print_options()}",
    callback=validate_bump_type,
)
@click.option("message", "--message", "-m", envvar="COMMIT_MESSAGE", help="Commit message", default=None)
@click.option("auto_message", "--auto_message", "-am", is_flag=True, help="Auto commit message", default=False)
def cli(bump_type: str, verbose: int, dry_run: bool, message: Optional[str], auto_message: bool) -> None:
    """CLI for semvergit."""
    set_logger(log_level=LogLevel(verbose))
    svg = SemverGit()
    svg.update(bump_type=bump_type, dry_run=dry_run, commit_message=message, auto_message=auto_message)
    sys.exit(0)
