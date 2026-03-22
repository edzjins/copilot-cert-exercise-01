"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Validates signup functionality including happy paths, error cases, and edge cases.
"""
import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client, fresh_activities):
        """Test successful signup for an activity."""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_adds_participant(self, client, fresh_activities):
        """Test that signup actually adds the participant to the activity."""
        # First, verify initial state
        initial = client.get("/activities").json()
        initial_count = len(initial["Chess Club"]["participants"])
        
        # Sign up new participant
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        
        # Verify participant was added
        updated = client.get("/activities").json()
        assert len(updated["Chess Club"]["participants"]) == initial_count + 1
        assert "newstudent@mergington.edu" in updated["Chess Club"]["participants"]

    def test_signup_activity_not_found(self, client, fresh_activities):
        """Test signup fails with 404 for non-existent activity."""
        response = client.post(
            "/activities/Nonexistent%20Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        
        data = response.json()
        assert "Activity not found" in data.get("detail", "")

    def test_signup_duplicate_participant(self, client, fresh_activities):
        """Test that duplicate signup is rejected with 400."""
        email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "already signed up" in data.get("detail", "").lower()

    def test_signup_different_activities(self, client, fresh_activities):
        """Test that a student can signup for multiple different activities."""
        email = "versatile@mergington.edu"
        
        # Sign up for Chess Club
        response1 = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Sign up for Programming Class
        response2 = client.post(
            "/activities/Programming%20Class/signup",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Verify both signups succeeded
        activities = client.get("/activities").json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Programming Class"]["participants"]

    def test_signup_same_activity_twice_fails(self, client, fresh_activities):
        """Test that signing up twice for the same activity fails."""
        email = "duplicate@mergington.edu"
        
        # First signup should succeed
        response1 = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second signup for same activity should fail
        response2 = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": email}
        )
        assert response2.status_code == 400

    def test_signup_with_special_characters_in_email(self, client, fresh_activities):
        """Test signup with special characters in email address."""
        email = "student+tag@mergington.edu"
        
        response = client.post(
            "/activities/Art%20Studio/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify signup was recorded with special characters preserved
        activities = client.get("/activities").json()
        assert email in activities["Art Studio"]["participants"]

    def test_signup_activity_name_case_sensitive(self, client, fresh_activities):
        """Test that activity name matching is case-sensitive."""
        response = client.post(
            "/activities/chess%20club/signup",  # lowercase
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404

    def test_signup_activity_with_spaces(self, client, fresh_activities):
        """Test signup for activity with multiple spaces in name."""
        response = client.post(
            "/activities/Programming%20Class/signup",
            params={"email": "programmer@mergington.edu"}
        )
        assert response.status_code == 200

    def test_signup_empty_email_parameter(self, client, fresh_activities):
        """Test signup with empty email parameter."""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": ""}
        )
        # FastAPI will accept empty string but it will be added as participant
        # This tests current behavior; could be enhanced with validation
        assert response.status_code == 200

    def test_signup_multiple_sequential_participants(self, client, fresh_activities):
        """Test multiple different participants signing up sequentially."""
        emails = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu"
        ]
        
        for email in emails:
            response = client.post(
                "/activities/Debate%20Club/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all were added
        activities = client.get("/activities").json()
        participants = activities["Debate Club"]["participants"]
        for email in emails:
            assert email in participants

    def test_signup_response_message_format(self, client, fresh_activities):
        """Test that signup response message has expected format."""
        email = "newperson@mergington.edu"
        activity = "Music Ensemble"
        
        response = client.post(
            f"/activities/{activity.replace(' ', '%20')}/signup",
            params={"email": email}
        )
        
        data = response.json()
        assert "Signed up" in data["message"]
        assert email in data["message"]
        assert activity in data["message"]

    def test_signup_participants_list_preserved(self, client, fresh_activities):
        """Test that existing participants are preserved after new signup."""
        # Get initial participants
        initial = client.get("/activities").json()
        initial_participants = initial["Tennis Club"]["participants"].copy()
        
        # Sign up new participant
        new_email = "tennisplayer@mergington.edu"
        client.post(
            "/activities/Tennis%20Club/signup",
            params={"email": new_email}
        )
        
        # Verify all original participants plus new one are present
        updated = client.get("/activities").json()
        final_participants = updated["Tennis Club"]["participants"]
        
        for participant in initial_participants:
            assert participant in final_participants
        assert new_email in final_participants
