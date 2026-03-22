"""
Tests for the GET / (root) endpoint.

Validates that the root endpoint redirects to the static index.html file.
"""
import pytest


class TestRootRedirect:
    """Test suite for GET / endpoint."""

    def test_root_redirect_to_index(self, client, fresh_activities):
        """Test that GET / redirects to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        
        # Should return a redirect status (307 or 302)
        assert response.status_code in [307, 302]

    def test_root_redirect_location_header(self, client, fresh_activities):
        """Test that redirect location is /static/index.html."""
        response = client.get("/", follow_redirects=False)
        
        assert "location" in response.headers or "Location" in response.headers
        location = response.headers.get("location") or response.headers.get("Location")
        assert "/static/index.html" in location

    def test_root_redirect_followed(self, client, fresh_activities):
        """Test that following redirect resolves to static index."""
        response = client.get("/", follow_redirects=True)
        
        # After following redirect, should get 200 and HTML content
        assert response.status_code == 200

    def test_root_path_normalization(self, client, fresh_activities):
        """Test that root path is recognized as /."""
        response = client.get("/", follow_redirects=False)
        
        # Should be recognized and redirect (not 404)
        assert response.status_code != 404
        assert response.status_code in [307, 302]
