import json

class TestHomePage:
    """
    All tests related to typefight's home page
    """
    def test_route_get(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/' page is requested (GET)
        THEN check that the response is valid
        """
        response = test_client.get("/")

        assert response.status_code == 200
        assert response.headers.get("Content-Type") == "text/html; charset=utf-8"

        assert b"Typefight!" in response.data
        assert b"Compete against players around the world to see who's the fastest typist!" in response.data

    def test_bad_request(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/' page is posted to (POST)
        THEN check that a '405' status code is returned
        """
        response = test_client.post("/")

        assert response.status_code == 405
        assert b"Typefight!" not in response.data
        assert response.status == "405 METHOD NOT ALLOWED"

class TestHighscores:
    """All tests related to the /highscores route"""
    def test_get_highscores(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/highscores' route is requested (GET)
        THEN check that the stored highscores are returned
        """
        response = test_client.get("/highscores")
        test_score = {
            "country": "test",
            "player_name": "test",
            "score": 13.37
        }

        assert response.status_code == 200
        assert test_score in json.loads(response.data.decode("utf-8"))
        assert response.headers.get("Content-Type") == "application/json"
    
    def test_bad_request(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/highscores' route is posted to (POST)
        THEN check that a '405' status code is returned
        """
        response = test_client.post("/highscores")

        assert response.status_code == 405
        assert response.status == "405 METHOD NOT ALLOWED"

class TestQuotes:
    """All tests related to the /quote route"""
    def test_get_quote(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/quote' route is requested (GET)
        THEN check that the stored quotes are returned
        """
        response = test_client.get("/quote")

        assert response.status_code == 200
        assert json.loads(response.data.decode("utf-8"))["quote"] # quote is random, can't check for specific one
        assert response.headers.get("Content-Type") == "application/json"

    def test_bad_request(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/quote' route is posted to (POST)
        THEN check that a '405' status code is returned
        """
        response = test_client.post("/quote")

        assert response.status_code == 405
        assert response.status == "405 METHOD NOT ALLOWED"
