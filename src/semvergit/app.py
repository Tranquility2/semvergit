"""SemverGit application module."""

from enum import Enum
from importlib import metadata
from typing import List

import semver
from loguru import logger

from semvergit.git_utils import get_active_branch, get_repo, get_tags_with_prefix, pull_remote


class BumpType(str, Enum):
    """BumpType."""

    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    PRERELEASE = "prerelease"

    def __str__(self) -> str:
        return self.value


class SemverGit:  # pylint: disable=too-few-public-methods
    """SemverGit."""

    def __init__(self, pull_branch: bool = True) -> None:
        """Init."""
        logger.success(f"SemverGit: {metadata.version('semvergit')}")
        self.current_repo = get_repo()
        if pull_branch:
            pull_remote(self.current_repo)
        self.branch = get_active_branch(repo=self.current_repo)
        logger.info(f"Active branch: {self.branch.name}")
        self.versions = self.get_versions()
        self.latest_version = max(self.versions)

    def get_versions(self, version_prefix: str = "v") -> List[semver.VersionInfo]:
        """Get versions."""
        current_repo = get_repo()
        pull_remote(current_repo)
        tags = get_tags_with_prefix(repo=current_repo, prefix=version_prefix)
        clean_tags = [self.remove_prefix(tag, version_prefix) for tag in tags]
        versions = [semver.VersionInfo.parse(tag) for tag in clean_tags]
        return versions

    @staticmethod
    def remove_prefix(text: str, prefix: str) -> str:
        """Remove prefix."""
        if text.startswith(prefix):
            return text[len(prefix) :]
        return text

    def update(self, bump_type: str, token: str = "dev") -> str:
        """Update."""
        new_version = self.latest_version.next_version(part=bump_type, prerelease_token=token)
        logger.info(f"Update from {self.latest_version} with {bump_type} to {new_version}")
        return str(new_version)
