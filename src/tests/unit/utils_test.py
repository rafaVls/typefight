from decimal import Decimal
from typing import OrderedDict
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
    def test_use_case(self):
        """
        GIVEN a list of items that could be non-serializable
        WHEN the list needs to be serializable
        THEN we return a list of json-serializable items
        """
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
            ])
        ]

        assert make_serializable(data) == [
            {
                "country": "Mexico",
                "player_name": "rafa_vls",
                "score": 12.53
            },
            {
                "country": "Mexico",
                "player_name": "rafa_vls",
                "score": 8.9
            }
        ]

    def test_empty_list(self):
        """
        GIVEN an empty list (which is the case if there's no records)
        WHEN the list needs to be serializable
        THEN we return an empty list
        """

        data = []
        assert make_serializable(data) == []