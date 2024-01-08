"""CLI for semvergit."""
import click
from loguru import logger

from semvergit.app import BumpType, SemverGit


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.version_option()
@click.option("--bump_type", "-t", type=click.Choice(list(BumpType)), help="Bump Type")
def cli(bump_type: str) -> None:
    """CLI for semvergit."""
    svg = SemverGit()
    new_version = svg.update(bump_type)
    logger.success(f"New version: {new_version}")
