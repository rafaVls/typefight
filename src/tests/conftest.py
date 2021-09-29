from decimal import Decimal
from typing import OrderedDict
from typefight import create_app
import pytest

# */ ==========[ Unit test fixtures ]========== */
@pytest.fixture(scope="class")
def highscores_data():
    data = [
        OrderedDict([
            ('score', Decimal('12.53')), 
            ('player_name', 'rafa_vls'), 
            ('country', 'Mexico')
        ]),
        OrderedDict([
            ('score', Decimal(8.90)), 
            ('player_name', 'rafa_vls'), 
            ('country', 'Mexico')
        ]),
        OrderedDict([
            ('score', Decimal('6.14')), 
            ('player_name', 'andu_lpz'), 
            ('country', 'Puerto Rico')
        ])
    ]

    return data

@pytest.fixture(scope="class")
def serialized_data():
    data = [
        {
            "country": "Mexico",
            "player_name": "rafa_vls",
            "score": 12.53
        },
        {
            "country": "Mexico",
            "player_name": "rafa_vls",
            "score": 8.9
        },
        {
            "country": "Puerto Rico",
            "player_name": "andu_lpz",
            "score": 6.14
        }
    ]

    return data

# */ ==========[ Functional test fixtures ]========== */
@pytest.fixture(scope="class")
def flask_app():
    # Create a test client using the Flask application configured for testing
    flask_app = create_app("flask_test.cfg")

    return flask_app

@pytest.fixture(scope="class")
def test_client(flask_app):
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client # this is where the testing happens

@pytest.fixture()
def register_response(test_client, user_info={"username": "test123", "password": "test123", "country": "Mexico"}):
    response = test_client.post(
        "/auth/register",
        data={
            "username": user_info["username"],
            "password": user_info["password"],
            "confirm": user_info["password"],
            "country": user_info["country"]
        },
        follow_redirects=True
    )

    return response

@pytest.fixture()
def login_response(test_client, user_info={"username": "test123", "password": "test123"}):
    response = test_client.post(
        "/auth/login",
        data={
            "username": user_info["username"], 
            "password": user_info["password"]
            },
        follow_redirects=True
        )

    return response
