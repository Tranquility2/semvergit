"""Test file_utils module."""

import tempfile

from pytest import LogCaptureFixture, mark
from semver import VersionInfo

from semvergit.file_utils import update_verion_file


@mark.parametrize(
    "new_version, expected_version",
    [
        (VersionInfo(0, 0, 5), '__version__ = "0.0.5"\n'),
        (VersionInfo(0, 1, 2), '__version__ = "0.1.2"\n'),
    ],
)
def test_update_verion_file(new_version: VersionInfo, expected_version: str) -> None:
    """Test update_verion_file."""

    with tempfile.TemporaryDirectory() as tmpdirname:
        version_file = f"{tmpdirname}/version.py"
        update_verion_file(version_file, new_version, dry_run=False)
        with open(version_file, "r", encoding="utf-8") as version_file_handle:
            version_file_content = version_file_handle.read()
            assert expected_version in version_file_content


@mark.parametrize(
    "new_version, expected_msg, expected_version",
    [
        (VersionInfo(0, 0, 5), "Dry run, version file content", '__version__ = "0.0.5"\n'),
        (VersionInfo(0, 1, 2), "Dry run, version file content", '__version__ = "0.1.2"\n'),
    ],
)
def test_update_verion_file_dry_run(
    caplog: LogCaptureFixture, new_version: VersionInfo, expected_msg: str, expected_version: str
) -> None:
    """Test update_verion_file dry run."""

    with tempfile.TemporaryDirectory() as tmpdirname:
        version_file = f"{tmpdirname}/version.py"
        update_verion_file(version_file, new_version, dry_run=True)
        assert expected_msg in caplog.text
        assert expected_version in caplog.text
        # check that file was not created
        try:
            with open(version_file, "r", encoding="utf-8") as version_file_handle:
                _ = version_file_handle.read()
                assert False
        except FileNotFoundError:
            assert True
        except Exception:  # pylint: disable=broad-except
            assert False
