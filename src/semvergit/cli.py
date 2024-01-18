"""CLI for semvergit."""
import sys

import click

from semvergit.app import BumpType, SemverGit
from semvergit.log_utils import LogMode, set_logger


def validate_log_level(
    ctx: click.Context, param: click.Parameter, value: str  # pylint: disable=unused-argument
) -> LogMode:
    """Validate log level."""
    try:
        return LogMode(value)
    except ValueError as exp:
        raise click.BadParameter(f"please select from {LogMode.print_options()}") from exp


def validate_bump_type(
    ctx: click.Context, param: click.Parameter, value: str  # pylint: disable=unused-argument
) -> BumpType:
    """Validate bump type."""
    try:
        return BumpType(value)
    except ValueError as exp:
        raise click.BadParameter(f"please select from {BumpType.print_options()}") from exp


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.version_option()
@click.option("--dry_run", "-d", is_flag=True, help="Dry run", default=False)
@click.option(
    "--log_level",
    "-l",
    type=click.UNPROCESSED,
    help=f"Log Level {LogMode.print_options()}",
    callback=validate_log_level,
    default=LogMode.STANDARD,
)
@click.option(
    "--bump_type",
    "-t",
    type=click.UNPROCESSED,
    help=f"Bump Type {BumpType.print_options()}",
    callback=validate_bump_type,
)
def cli(bump_type: str, log_level: LogMode, dry_run: bool) -> None:
    """CLI for semvergit."""
    set_logger(log_mode=log_level)
    quiet = log_level == LogMode.QUIET
    svg = SemverGit()
    svg.update(bump_type=bump_type, quiet=quiet, dry_run=dry_run)
    sys.exit(0)
