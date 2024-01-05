"""Git utilities."""
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
    logger.debug(f"Active branch: {branch.name}")
    return branch


def pull_remote(repo: Repo) -> None:
    """Pull remote."""
    remote = repo.remotes.origin
    remote.pull()
    logger.debug(f"Pulled remote {remote.name}")


def get_tags(repo: Repo) -> list:
    """Get tags."""
    tags = repo.tags
    logger.debug(f"Fetched tags: {tags}")
    return tags
