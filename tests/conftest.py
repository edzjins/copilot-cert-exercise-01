"""
Shared test configuration and fixtures for the Mergington High School API tests.
"""
import pytest
from starlette.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient instance for testing the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """
    Provide a fresh copy of the activities database for test isolation.
    
    This fixture resets the in-memory activities database to its initial state
    between tests, ensuring no side effects from previous tests.
    """
    # Store original state
    original_state = {
        name: {
            "description": activity["description"],
            "schedule": activity["schedule"],
            "max_participants": activity["max_participants"],
            "participants": activity["participants"].copy()  # Make a copy of the list
        }
        for name, activity in activities.items()
    }
    
    yield activities
    
    # Restore original state after test
    activities.clear()
    activities.update(original_state)
