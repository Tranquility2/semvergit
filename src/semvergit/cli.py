"""CLI for semvergit."""
import click
from loguru import logger

from semvergit.app import BumpType, SemverGit


@click.command()
def cli() -> None:
    """CLI for semvergit."""
    svg = SemverGit()
    new_version = svg.update(bump_type=str(BumpType.PATCH))
    logger.success(f"New version: {new_version}")
