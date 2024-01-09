"""Git utilities."""
from typing import List

from git import Head, Repo
from loguru import logger


def get_repo(search_parent_directories: bool = True) -> Repo:
    """Get repo."""
    repo = Repo(search_parent_directories=search_parent_directories)
    logger.debug(f"Working on Repository: {repo.working_tree_dir}")
    return repo


def get_active_branch(repo: Repo) -> Head:
    """Get active branch."""
    branch = repo.active_branch
    return branch


def pull_remote(repo: Repo) -> None:
    """Pull remote."""
    remote = repo.remotes.origin
    remote.pull()
    logger.debug(f"Pulled remote {remote.name}")


def get_tags_with_prefix(repo: Repo, prefix: str = "v") -> List[str]:
    """Get tags as list of strings."""
    tags = repo.tags
    results = [tag.name for tag in tags if tag.name.startswith(prefix)]
    logger_detail = f"with prefix -{prefix}-" if prefix else "no prefix"
    logger.debug(f"Fetched tags: {results} ({logger_detail})")
    return results
