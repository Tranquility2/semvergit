"""CLI for semvergit."""
import click
from loguru import logger

from semvergit.app import BumpType, SemverGit
from semvergit.log_utils import set_logger


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.version_option()
@click.option("--debug", "-d", is_flag=True, help="Debug mode")
@click.option("--bump_type", "-t", type=click.Choice(list(BumpType)), help="Bump Type")
def cli(bump_type: str, debug: bool) -> None:
    """CLI for semvergit."""
    set_logger(debug=debug)
    svg = SemverGit()
    new_version = svg.update(bump_type)
    logger.success(f"New version: {new_version}")
