import json
from flask import g, session

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
        assert (
            b"Compete against players around the world to see who's the fastest typist!" 
            in response.data
        )

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
        # Terrible workaround for getting the correct quote in g
        quote_id = ""
        while quote_id != "ea9d502e-a9b6-4d67-ab35-5cae050af38b":
            quote_id = json.loads(test_client.get("/quote").data.decode("utf-8"))["quote_id"]

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

class TestSetHighscore:
    """All tests related to the /highscores/score route"""
    def test_set_new_score(self, test_client, login_response):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/highscores/score' route is posted to (POST)
        WHEN the user is logged in and there's no saved score for current quote
        THEN make sure new record is saved and correct message is returned
        """
        quote_id = ""
        while quote_id != "f6c8c2c0-c648-459e-9c08-673383a326b0":
            quote_id = json.loads(test_client.get("/quote").data.decode("utf-8"))["quote_id"]

        highscore_response = test_client.post("/highscores/2.5")
        data = json.loads(highscore_response.data)
        assert data["success"] == True
        assert data["message"] == "Your new score 2.5 has been saved."

        with g.db as db:
            cur = db.cursor()
            cur.execute(
                """
                DELETE FROM scores
                WHERE player_uid = %s
                AND quote_uid = %s;
                """, (session["player_uid"], session["quote"]["quote_id"])
            )
            cur.close()

    def test_update_score(self, test_client, login_response):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/highscores/score' route is posted to (POST)
        WHEN the user is logged in and there's a slower score saved for current quote
        THEN make sure new record is saved and correct message is returned
        """
        quote_id = ""
        while quote_id != "ea9d502e-a9b6-4d67-ab35-5cae050af38b":
            quote_id = json.loads(test_client.get("/quote").data.decode("utf-8"))["quote_id"]

        highscore_response = test_client.post("/highscores/2.5")
        data = json.loads(highscore_response.data)
        assert data["success"] == True
        assert data["message"] == (
            "New record! Your new score was faster than your previous one. "
            "Old score: 13.37 "
            "New score: 2.5"
        )

        # resetting the score
        with g.db as db:
            cur = db.cursor()
            cur.execute(
                """
                UPDATE scores
                SET score = 13.37
                WHERE player_uid = %s;
                """, (session["player_uid"], )
            )
            db.commit()
            cur.close()

    def test_post_slow_score(self, test_client, login_response):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/highscores/score' route is posted to (POST)
        WHEN the user is logged in and there's a faster score saved for current quote
        THEN make sure correct message is returned
        """
        quote_id = ""
        while quote_id != "ea9d502e-a9b6-4d67-ab35-5cae050af38b":
            quote_id = json.loads(test_client.get("/quote").data.decode("utf-8"))["quote_id"]

        highscore_response = test_client.post("/highscores/20.5")
        data = json.loads(highscore_response.data)
        assert data["success"] == True
        assert data["message"] == "Too slow! Best score: 13.37 Current score: 20.5"
