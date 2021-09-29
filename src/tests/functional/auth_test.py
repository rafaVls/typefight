import pytest
from flask import g, session

class TestRegister:
    """All tests related to /auth/register"""
    def test_register(self, register_response):
        """
        GIVEN the '/auth/register' is posted to (POST)
        WHEN using valid credencials username: 'test123', password: 'test123', country: 'Mexico'
        THEN check user got saved in db and we got redirected to '/auth'
        """
        assert register_response.status_code == 200
        assert register_response.headers.get("Content-Type") == "text/html; charset=utf-8"
        assert b"Login" in register_response.data
        assert b"Signup" in register_response.data

        with g.db as db:
            cur = db.cursor()
            cur.execute(
                """
                SELECT * 
                FROM players 
                WHERE player_name = 'test123';
                """
            )
            assert cur.fetchone() is not None

    @pytest.mark.parametrize(("username", "password", "country", "message"), (
        ("", "", "", b"A username is required"),
        ("a", "", "", b"A password is required"),
        ("test123", "test123", "Mexico", b'Player name &#34;test123&#34; already exists')
    ))
    def test_register_validate_input(self, test_client, username, password, country, message):
        """
        GIVEN the '/auth/register' route is posted to (POST)
        WHEN using three sets of invalid credentials
        THEN check we get the correct error message
        """
        response = test_client.post(
            "/auth/register",
            data={
                "username": username,
                "password": password, 
                "confirm": password,
                "country": country
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert message in response.data
    
class TestLogin:
    """All tests related to /auth/login"""
    def test_login(self, test_client, login_response):
        """
        GIVEN the '/auth/login' is posted to (POST)
        WHEN using valid credencials username: 'test123', password: 'test123'
        THEN check we get redirected to '/', and player is saved in 'g'
        """
        assert login_response.status_code == 200
        assert b"Typefight!" in login_response.data # route redirects to index.html if data is correct
        assert session["session_hash"]

        # making sure we're logged in
        new_response = test_client.get("/")

        assert new_response.status_code == 200
        assert g.user["player_name"] == "test123"
        assert g.user["country"] == "Mexico"

    @pytest.mark.parametrize(("username", "password", "message"), (
        ("", "", b"A username is required"),
        ("test", "", b"A password is required")
    ))
    def test_login_validate_input(self, test_client, username, password, message):
        """
        GIVEN the '/auth/login' is posted to (POST)
        WHEN using two sets of invalid credentials
        THEN check we get the correct error message
        """
        response = test_client.post(
            "/auth/login",
            data={"username": username, "password": password}
        )

        assert response.status_code == 200
        assert message in response.data

class TestLogout:
    """All tests related to /auth/logout"""
    def test_logout(self, login_response, test_client):
        """
        GIVEN the '/auth/login' is posted to (POST)
        WHEN using valid credentials
        THEN check we get redirected to '/'
        THEN the '/auth/logout' is requested (GET)
        THEN check we get redirected to '/' and session is not stored in cookie
        THEN the '/' is requested (GET)
        THEN the we check user isn't stored in 'g'
        """
        assert b"Typefight!" in login_response.data
        assert login_response.status_code == 200
        assert "session_hash" in session
        assert g.user

        # logging out
        logout_response = test_client.get("/auth/logout", follow_redirects=True)

        assert b"Typefight!" in logout_response.data
        assert logout_response.status_code == 200
        assert not "session_hash" in session
        assert not g.user

        # making sure we're logged out
        home_response = test_client.get("/")

        assert b"Typefight!" in home_response.data
        assert home_response.status_code == 200
