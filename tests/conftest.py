from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module


# Keep an original deep copy of the activities so tests can reset mutable state
_ORIGINAL_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the module-level `activities` dict before each test to avoid
    inter-test pollution (Arrange step)."""
    app_module.activities = deepcopy(_ORIGINAL_ACTIVITIES)
    yield
    app_module.activities = deepcopy(_ORIGINAL_ACTIVITIES)


@pytest.fixture()
def client():
    """Provide a TestClient instance for tests to exercise the API."""
    return TestClient(app_module.app)
