from typefight import create_app

class TestFactory:
    """All tests related to the factory app"""
    def test_config(self, flask_app):
        """
        GIVEN two Flask applications
        WHEN one is configured for testing and the other is not
        THEN make sure they have the corresponding testing property
        """
        assert not create_app().testing
        assert flask_app.testing