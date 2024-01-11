"""Test log_utils module."""
from semvergit.log_utils import set_logger


def test_set_logger_invalid() -> None:
    """Test set_logger with invalid mode."""
    try:
        set_logger("invalid")  # type: ignore
    except ValueError:
        pass
    else:
        raise AssertionError("Should have raised ValueError")
