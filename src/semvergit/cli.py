"""CLI for semvergit."""
import click
from loguru import logger

from semvergit.app import BumpType, SemverGit


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.version_option()
def cli() -> None:
    """CLI for semvergit."""
    svg = SemverGit()
    new_version = svg.update(str(BumpType.PATCH))
    logger.success(f"New version: {new_version}")
