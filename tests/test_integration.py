"""Integration tests for the semvergit package."""

import subprocess
import tempfile
from typing import Optional, Tuple


class RunCommandException(Exception):
    """Exception raised when a command fails."""

    def __init__(self, message: str) -> None:
        """Initialize the exception."""
        super().__init__(message)


def run_command(command: str, cwd: str, validation_string: Optional[str] = None) -> Tuple[str, str]:
    """Run a command in a subprocess and return the output. Raise an exception if the command fails."""
    result = subprocess.run(command, capture_output=True, shell=True, text=True, check=False, cwd=cwd)
    if result.returncode != 0:
        raise RunCommandException(f"Error {result.stderr}, Code: {result.returncode}, Command output: {result.stdout}")
    if validation_string:
        print(f"[v] {validation_string}")
    return (result.stdout, result.stderr)


def add_file_to_repo(filename: str, repodirname: str, content: str) -> None:
    """Add a file to a git repository and commit it."""
    with open(repodirname + "/" + filename, "w", encoding="utf-8") as f:
        f.write(content)
    run_command(f"git add {filename}", repodirname, f"Added {filename} to the index")
    run_command(f'git commit -m "Added {filename}"', repodirname, f"Committed {filename}")


def check_git_log(repodirname: str, expected: str) -> None:
    """Check the git log for the last commit."""
    result, _ = run_command('git --no-pager log --pretty=format:"%h%d %s [%an]"', repodirname, "Checked the commit log")
    print(f"Git Log:\n{result}")
    assert expected in result


def update_version(repodirname: str, version_type: str, target_version: str) -> None:
    """Run the semvergit command to update the version."""
    result, logs = run_command(f"semvergit -v -t {version_type}", repodirname, "Created a new version")
    print(logs, end="")
    assert result == target_version


def update_version_file(repodirname: str, version_type: str, target_version: str, version_file: str) -> None:
    """Run the semvergit command to update the version on file."""
    result, logs = run_command(
        f"semvergit -v -t {version_type} -f {version_file}", repodirname, "Created a new version (in file)"
    )
    print(logs, end="")
    assert result == target_version


def update_version_file_custom(
    repodirname: str, version_type: str, target_version: str, version_file: str, custom_message: str
) -> None:
    """Run the semvergit command to update the version on file with custom message."""
    result, logs = run_command(
        f'semvergit -v -t {version_type} -f {version_file} -m "{custom_message}"',
        repodirname,
        "Created a new version (in file)",
    )
    print(logs, end="")
    assert result == target_version


def set_credentials(repodirname: str) -> None:
    """Set the git credentials for the repository."""
    run_command("git config user.email 'test@test'", repodirname, "Set user email")
    run_command("git config user.name 'Test User'", repodirname, "Set user name")


def check_file_content(filename: str, repodirname: str, expected: str) -> None:
    """Check the content of a file."""
    with open(repodirname + "/" + filename, "r", encoding="utf-8") as f:
        file_content = f.read()
        print(f"File content:\n{file_content}")
        assert expected in file_content


class TestIntegration:
    """Integration tests for the semvergit package."""

    # pylint: disable=attribute-defined-outside-init
    def setup_method(self) -> None:
        """Create a git repository and clone it."""
        self.tmpdirname = tempfile.mkdtemp()
        self.repodirname = self.tmpdirname + "/repo"
        run_command(f"mkdir {self.repodirname}", self.tmpdirname, f"Created repo directory: {self.repodirname}")
        run_command("git -c init.defaultBranch=master init", self.repodirname, "Initialized git repository")
        set_credentials(self.repodirname)
        run_command("touch initial.txt", self.repodirname, "Created initial.txt")
        run_command("git add .", self.repodirname, "Added initial.txt to the index")
        run_command('git commit -m "Initial commit"', self.repodirname, "Committed initial.txt")
        check_git_log(self.repodirname, "Initial commit")
        self.clonedirname = self.tmpdirname + "/clone"
        run_command(
            f"git clone {self.repodirname} {self.clonedirname}", self.repodirname, f"Cloned to {self.clonedirname}"
        )
        set_credentials(self.clonedirname)

    def teardown_method(self) -> None:
        """Remove the temporary directory."""
        run_command(f"rm -rf {self.tmpdirname}", self.tmpdirname)

    def test_integration_patch(self) -> None:
        """Test the integration of the semvergit package with a patch version update."""
        add_file_to_repo("test.txt", self.clonedirname, "Hello, World!")
        check_git_log(self.clonedirname, "Added test.txt")
        update_version(self.clonedirname, "patch", "v0.0.1")
        add_file_to_repo("test2.txt", self.clonedirname, "New content")
        check_git_log(self.clonedirname, "Added test2.txt")
        update_version(self.clonedirname, "patch", "v0.0.2")
        check_git_log(self.clonedirname, "v0.0.2")

    def test_integration_minor(self) -> None:
        """Test the integration of the semvergit package with a minor version update."""
        add_file_to_repo("test.txt", self.clonedirname, "Hello, World!")
        check_git_log(self.clonedirname, "Added test.txt")
        update_version(self.clonedirname, "minor", "v0.1.0")
        add_file_to_repo("test2.txt", self.clonedirname, "New content")
        check_git_log(self.clonedirname, "Added test2.txt")
        update_version(self.clonedirname, "minor", "v0.2.0")
        check_git_log(self.clonedirname, "v0.2.0")

    def test_integration_major(self) -> None:
        """Test the integration of the semvergit package with a major version update."""
        add_file_to_repo("test.txt", self.clonedirname, "Hello, World!")
        check_git_log(self.clonedirname, "Added test.txt")
        update_version(self.clonedirname, "major", "v1.0.0")
        add_file_to_repo("test2.txt", self.clonedirname, "New content")
        check_git_log(self.clonedirname, "Added test2.txt")
        update_version(self.clonedirname, "major", "v2.0.0")
        check_git_log(self.clonedirname, "v2.0.0")

    def test_integration_prerelease(self) -> None:
        """Test the integration of the semvergit package with a prerelease version update."""
        add_file_to_repo("test.txt", self.clonedirname, "Hello, World!")
        check_git_log(self.clonedirname, "Added test.txt")
        update_version(self.clonedirname, "prerelease", "v0.0.1-dev.1")
        add_file_to_repo("test2.txt", self.clonedirname, "New content")
        check_git_log(self.clonedirname, "Added test2.txt")
        update_version(self.clonedirname, "prerelease", "v0.0.1-dev.2")
        check_git_log(self.clonedirname, "v0.0.1-dev.2")

    def test_integration_stack(self) -> None:
        """Test the integration of the semvergit package with multiple version updates."""
        add_file_to_repo("test.txt", self.clonedirname, "Hello, World!")
        check_git_log(self.clonedirname, "Added test.txt")
        update_version(self.clonedirname, "patch", "v0.0.1")
        add_file_to_repo("test2.txt", self.clonedirname, "New content")
        check_git_log(self.clonedirname, "Added test2.txt")
        update_version(self.clonedirname, "minor", "v0.1.0")
        add_file_to_repo("test3.txt", self.clonedirname, "More content")
        check_git_log(self.clonedirname, "Added test3.txt")
        update_version(self.clonedirname, "major", "v1.0.0")
        add_file_to_repo("test4.txt", self.clonedirname, "Even more content")
        check_git_log(self.clonedirname, "Added test4.txt")
        update_version(self.clonedirname, "minor", "v1.1.0")
        add_file_to_repo("test5.txt", self.clonedirname, "Some more content")
        check_git_log(self.clonedirname, "Added test5.txt")
        update_version(self.clonedirname, "patch", "v1.1.1")
        check_git_log(self.clonedirname, "v1.1.1")

    def test_integration_version_file(self) -> None:
        """Test the integration of the semvergit package with a version file."""
        add_file_to_repo("test.txt", self.clonedirname, "Hello, World!")
        add_file_to_repo("version.txt", self.clonedirname, "0.0.0")
        check_file_content("version.txt", self.clonedirname, "0.0.0")
        check_git_log(self.clonedirname, "Added test.txt")
        check_git_log(self.clonedirname, "Added version.txt")
        update_version_file(self.clonedirname, "patch", "v0.0.1", "version.txt")
        check_file_content("version.txt", self.clonedirname, "0.0.1")
        add_file_to_repo("test2.txt", self.clonedirname, "New content")
        check_git_log(self.clonedirname, "Added test2.txt")
        update_version_file_custom(self.clonedirname, "minor", "v0.1.0", "version.txt", "Updated version to 0.1.0")
        check_file_content("version.txt", self.clonedirname, "0.1.0")
        check_git_log(self.clonedirname, "0.1.0")
