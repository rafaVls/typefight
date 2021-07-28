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

    def test_route_post(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/' page is posted to (POST)
        THEN check that a '405' status code is returned
        """
        response = test_client.post("/")

        assert response.status_code == 405
        assert b"Typefight!" not in response.data
