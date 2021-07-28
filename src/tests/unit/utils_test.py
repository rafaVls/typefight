from decimal import Decimal
from typefight.utils import decimal_type_handler, make_serializable

class TestDecimalHandler:
    """
    All tests related to decimal_type_handler
    """
    def test_use_case(self):
        """
        GIVEN a decimal type object
        WHEN the object needs to be serializable
        THEN we return a float type object
        """
        decimal_object = Decimal(2.5)
        serializable_object = decimal_type_handler(decimal_object)

        # Check to make sure object is float and not decimal
        assert isinstance(serializable_object, float) == True
        assert isinstance(serializable_object, Decimal) == False

        # Check to make sure the value of the object wasn't altered
        assert serializable_object == decimal_object
        assert serializable_object == 2.5

    def test_object_is_not_decimal(self):
        """
        GIVEN an object that isn't of type decimal
        WHEN the object needs to be serializable
        THEN return the object as is
        """
        assert decimal_type_handler(None) == None
        assert decimal_type_handler(True) == True
        assert decimal_type_handler("help") == "help"
        assert decimal_type_handler([]) == []
        assert decimal_type_handler({}) == {}
    
class TestMakeSerializable:
    """
    All tests related to make_serializable
    """
    def test_use_case(self, highscores_data, serialized_data):
        """
        GIVEN a list of highscore records with scores that could be non-serializable
        WHEN the list needs to be fully serializable
        THEN we return a list of json-serializable items
        """
        assert make_serializable(highscores_data) == serialized_data

    def test_empty_list(self):
        """
        GIVEN a list of highscore records
        WHEN the list is empty (there are no records yet)
        THEN we return an empty list
        """

        data = []
        assert make_serializable(data) == []