"""CLI for semvergit."""
import sys

import click
from loguru import logger

from semvergit.app import BumpType, SemverGit
from semvergit.log_utils import LogMode, set_logger


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.version_option()
@click.option("--debug", "-d", is_flag=True, help="Debug mode")
@click.option("--quiet", "-q", is_flag=True, help="Quiet mode")
@click.option("--bump_type", "-t", type=click.Choice(list(BumpType)), help="Bump Type")
def cli(bump_type: str, debug: bool, quiet: bool) -> None:
    """CLI for semvergit."""
    if debug:
        set_logger(log_mode=LogMode.DEBUG)
    elif quiet:
        set_logger(log_mode=LogMode.QUIET)
    else:
        set_logger(log_mode=LogMode.STANDARD)
    svg = SemverGit()
    new_version = svg.update(bump_type)
    logger.success(f"New version: {new_version}")
    if quiet:
        sys.stdout.write(new_version)
