"""Test app."""

from semvergit.app import SemverGit


def test_app() -> None:
    """Test app."""
    app = SemverGit()
    assert app is not None
