"""
Unit Tests for the Flask Web Application
Run with: pytest tests/ -v
"""
import json
import pytest
from app import create_app


@pytest.fixture
def client():
    """
    Create a test client using Flask's built-in test client.
    The app is configured in TESTING mode so errors propagate
    to the test rather than being swallowed by the error handler.
    """
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Home page tests ───────────────────────────────────────────────────────────

class TestHomePage:
    def test_home_returns_200(self, client):
        """GET / should return HTTP 200 OK."""
        response = client.get("/")
        assert response.status_code == 200

    def test_home_returns_html(self, client):
        """GET / should return an HTML content type."""
        response = client.get("/")
        assert "text/html" in response.content_type

    def test_home_contains_title(self, client):
        """Home page HTML should include the app title."""
        response = client.get("/")
        assert b"CI/CD" in response.data

    def test_home_contains_pipeline_steps(self, client):
        """Home page should describe the CI/CD pipeline stages."""
        response = client.get("/")
        assert b"Docker" in response.data
        assert b"Deploy" in response.data


# ── Health check tests ────────────────────────────────────────────────────────

class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        """GET /health should return HTTP 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_json(self, client):
        """GET /health should return a JSON content type."""
        response = client.get("/health")
        assert "application/json" in response.content_type

    def test_health_status_ok(self, client):
        """GET /health JSON body must contain status: ok."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert data["status"] == "ok"

    def test_health_contains_service_name(self, client):
        """GET /health JSON body must include the service name."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert "service" in data
        assert isinstance(data["service"], str)
        assert len(data["service"]) > 0


# ── 404 test ─────────────────────────────────────────────────────────────────

class TestNotFound:
    def test_unknown_route_returns_404(self, client):
        """Any undefined route should return 404."""
        response = client.get("/this-route-does-not-exist")
        assert response.status_code == 404
