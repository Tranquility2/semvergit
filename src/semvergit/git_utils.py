"""Git utilities."""
from functools import wraps
from typing import Any, Callable, List, Optional

from git import Head, Repo
from loguru import logger
from semver import VersionInfo


def drywrap(func: Callable) -> Callable:
    """Dry run wrapper."""

    @wraps(func)
    def dryfunc(*args: Any, **kwargs: Any) -> Optional[Callable]:
        """Dry run function."""
        dry_run = kwargs.get("dry_run")
        if dry_run is not None and dry_run:
            logger.debug(f"Dry run: {func.__name__}(*{args}, **{kwargs})")
            return None

        if dry_run is not None:
            del kwargs["dry_run"]
        return func(*args, **kwargs)

    return dryfunc


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


@drywrap
def new_commit(repo: Repo, message: str) -> str:
    """New commit."""
    new_commit_id = repo.index.commit(message=message)
    short_commit_id = new_commit_id.hexsha[:7]
    logger.debug(f"Created commit [{short_commit_id}] {message}")
    return short_commit_id


@drywrap
def set_tag(repo: Repo, tag: str) -> VersionInfo:
    """Set tag."""
    new_tag = repo.create_tag(tag)
    logger.debug(f"Created {str(new_tag)}")
    return new_tag


@drywrap
def push_remote(repo: Repo, tag_str: str) -> None:
    """Push remote."""
    remote = repo.remotes.origin
    remote.push(tag_str)
    logger.debug(f"Pushed remote {remote.name}")
