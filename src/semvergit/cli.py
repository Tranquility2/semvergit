"""CLI for semvergit."""
import click

from semvergit.app import SemverGit


@click.command()
def cli() -> None:
    """CLI for semvergit."""
    smg = SemverGit()
    smg.test()
