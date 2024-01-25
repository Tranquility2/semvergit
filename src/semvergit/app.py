"""SemverGit application module."""

import sys
from enum import Enum
from importlib import metadata
from typing import List, Optional

from loguru import logger
from semver import VersionInfo

from semvergit.git_utils import (
    get_active_branch,
    get_repo,
    get_tags_with_prefix,
    new_commit,
    pull_remote,
    push_remote,
    set_tag,
)


class BumpType(str, Enum):
    """BumpType."""

    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    PRERELEASE = "prerelease"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def print_options(cls) -> str:
        """Print options."""
        return f"{[str(bump_type) for bump_type in list(cls)]}"


class SemverGit:  # pylint: disable=too-few-public-methods
    """SemverGit."""

    prerelease_token: str = "dev"
    version_prefix: str = "v"

    def __init__(self, pull_branch: bool = False) -> None:
        """Init."""
        logger.success(f"SemverGit: {metadata.version('semvergit')}")
        self.current_repo = get_repo()
        self.branch = get_active_branch(repo=self.current_repo)
        logger.debug(f"Active branch: {self.branch.name}")
        if pull_branch:
            logger.info("Pulling...")
            pull_remote(self.current_repo)
        self.versions = self.get_versions()
        self.latest_version = max(self.versions)

    def get_versions(self) -> List[VersionInfo]:
        """Get versions."""
        current_repo = get_repo()
        tags = get_tags_with_prefix(repo=current_repo, prefix=self.version_prefix)
        clean_tags = [self.remove_prefix(tag, self.version_prefix) for tag in tags]
        versions = [VersionInfo.parse(tag) for tag in clean_tags]
        return versions

    @staticmethod
    def remove_prefix(text: str, prefix: str) -> str:
        """Remove prefix."""
        if text.startswith(prefix):
            return text[len(prefix) :]
        return text

    def update(self, bump_type: str, dry_run: bool, commit_message: Optional[str], auto_message: bool) -> str:
        """Update."""
        new_version = self.latest_version.next_version(part=bump_type, prerelease_token=self.prerelease_token)
        new_version_str = str(new_version)
        logger.info(f"Update from {self.latest_version} with {bump_type} to {new_version}")
        new_tag_str = f"{self.version_prefix}{new_version}"

        if dry_run:
            logger.warning("Dry run (no tag set or pushed)")

        if auto_message:
            commit_message = f"New version: {new_version_str}"
        if auto_message or commit_message:
            logger.info("Committing...")
            new_commit(repo=self.current_repo, message=commit_message, dry_run=dry_run)
        else:
            logger.debug("No commit message")

        set_tag(repo=self.current_repo, tag=new_tag_str, dry_run=dry_run)
        logger.info("Pushing...")
        push_remote(repo=self.current_repo, tag_str=new_tag_str, dry_run=dry_run)

        logger.success(f"New version tag: {new_tag_str}")
        sys.stdout.write(new_version_str)
        return str(new_version_str)
