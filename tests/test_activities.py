"""
Tests for the GET /activities endpoint.

Validates that the activities endpoint returns the correct list of activities
with proper structure and data formatting.
"""
import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client, fresh_activities):
        """Test that GET /activities returns all 9 activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        
        activities = response.json()
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities

    def test_get_activities_response_structure(self, client, fresh_activities):
        """Test that each activity has the correct structure."""
        response = client.get("/activities")
        activities = response.json()
        
        # Check structure of first activity
        chess_club = activities["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club

    def test_get_activities_description_field(self, client, fresh_activities):
        """Test that descriptions are non-empty strings."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["description"], str)
            assert len(activity_data["description"]) > 0

    def test_get_activities_schedule_field(self, client, fresh_activities):
        """Test that schedule is present and properly formatted."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["schedule"], str)
            assert len(activity_data["schedule"]) > 0

    def test_get_activities_max_participants(self, client, fresh_activities):
        """Test that max_participants is a positive integer."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0

    def test_get_activities_participants_is_list(self, client, fresh_activities):
        """Test that participants field is a list."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_participants_are_emails(self, client, fresh_activities):
        """Test that participants contain valid email addresses."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant  # Basic email validation
                assert "." in participant

    def test_get_activities_specific_activity_data(self, client, fresh_activities):
        """Test that specific activities have expected data."""
        response = client.get("/activities")
        activities = response.json()
        
        # Verify Chess Club data
        chess = activities["Chess Club"]
        assert "Learn strategies" in chess["description"]
        assert "Fridays" in chess["schedule"]
        assert chess["max_participants"] == 12
        assert "michael@mergington.edu" in chess["participants"]

    def test_get_activities_consistent_responses(self, client, fresh_activities):
        """Test that multiple calls return consistent results."""
        response1 = client.get("/activities")
        response2 = client.get("/activities")
        
        assert response1.json() == response2.json()
