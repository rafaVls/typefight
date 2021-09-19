import pytest
from flask import g, session

class TestAuthHome:
    """All tests related to /auth"""
    def test_home_route(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/auth' route is requested (GET)
        THEN check that we get the auth.html page
        """
        response = test_client.get("/auth", follow_redirects=True)

        assert response.status_code == 200
        assert response.headers.get("Content-Type") == "text/html; charset=utf-8"

        assert b"Login" in response.data
        assert b"Signup" in response.data

    def test_bad_request(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/auth' route is posted to (POST)
        THEN check that a '405' status code is returned
        """
        response = test_client.post("/auth")
        
        assert response.status == "405 METHOD NOT ALLOWED"
        assert response.status_code == 405

class TestRegister:
    """All tests related to /auth/register"""
    def test_register(self, register_response):
        """
        GIVEN the '/auth/register' is posted to (POST)
        WHEN using valid credencials username: 'a', password: 'a', country: 'Mexico'
        THEN check user got saved in db and we got redirected to '/auth'
        """
        assert register_response.status_code == 200
        assert register_response.headers.get("Content-Type") == "text/html; charset=utf-8"
        assert b"Login" in register_response.data
        assert b"Signup" in register_response.data

        with g.db as db:
            cur = db.cursor()
            cur.execute(
                "SELECT * FROM players WHERE player_name = 'a';"
            )
            assert cur.fetchone() is not None
            cur.execute(
                "DELETE FROM players WHERE player_name = 'a';"
            )
            cur.close()
            db.commit()

    @pytest.mark.parametrize(("username", "password", "country", "message"), (
        ("", "", "", b"Username is required."),
        ("a", "", "", b"Password is required."),
        ("test", "test", "test", b"Player name test already exists.")
    ))
    def test_register_validate_input(self, test_client, username, password, country, message):
        """
        GIVEN the '/auth/register' route is posted to (POST)
        WHEN using three sets of invalid credentials
        THEN check we get the correct error message
        """
        response = test_client.post(
            "/auth/register",
            data={"username": username, "password": password, "country": country}
        )

        assert response.status_code == 200
        assert message in response.data
    
class TestLogin:
    """All tests related to /auth/login"""
    def test_login(self, test_client, login_response):
        """
        GIVEN the '/auth/login' is posted to (POST)
        WHEN using valid credencials username: 'test', password: 'test'
        THEN check we get redirected to '/', and player_uid is saved in 'g' and session
        """
        assert login_response.status_code == 200
        assert b"Typefight!" in login_response.data # route redirects to index.html if data is correct
        assert session["player_uid"] == "bff618f7-9aaa-43a5-9e1a-1b151bd5882f"

        # making sure we're logged in
        new_response = test_client.get("/")

        assert new_response.status_code == 200
        assert g.user["player_name"] == "test"
        assert g.user["country"] == "test"

    @pytest.mark.parametrize(("username", "password", "message"), (
        ("", "", b"Incorrect username."),
        ("test", "", b"Incorrect password.")
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
        THEN check we get redirected to '/' and player_uid is not stored in cookie
        THEN the '/' is requested (GET)
        THEN the we check user isn't stored in 'g'
        """
        assert b"Typefight!" in login_response.data
        assert login_response.status_code == 200

        # logging out
        logout_response = test_client.get("/auth/logout", follow_redirects=True)

        assert b"Typefight!" in logout_response.data
        assert logout_response.status_code == 200
        assert not "player_uid" in session

        # making sure we're logged out
        home_response = test_client.get("/")

        assert b"Typefight!" in home_response.data
        assert home_response.status_code == 200
        assert not g.user
