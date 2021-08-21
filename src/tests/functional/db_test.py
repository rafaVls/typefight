import pytest
import psycopg2
from typefight.db import get_db

class TestDB:
    """All tests related to the db module"""
    def test_get_db(self, flask_app):
        with flask_app.app_context():
            db = get_db()
            # We make sure get_db() returns the same connection
            # each time we call it
            assert db is get_db()

        with pytest.raises(psycopg2.InterfaceError) as e:
        # After the context, the connection should be closed
        # which makes the next 2 lines raise a psycopg2 InterfaceError
            cur = db.cursor()
            cur.execute("SELECT 1")
        
        assert "closed" in str(e.value)
