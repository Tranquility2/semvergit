"""SemverGit app module."""

from semvergit.git_utils import get_active_branch, get_repo, get_tags, pull_remote


class SemverGit:  # pylint: disable=too-few-public-methods
    """SemverGit."""

    def test(self) -> None:
        """Test."""
        print("Working")
        repo = get_repo()
        pull_remote(repo)
        branch = get_active_branch(repo)  # pylint: disable=unused-variable
        tags = get_tags(repo)  # pylint: disable=unused-variable
