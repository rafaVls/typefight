import os, json
from decimal import Decimal

def make_serializable(data:list) -> list:
    """
    Returns a json-serializable list that can be 
    used as an http response.
    """

    serialized_list = []

    # raw_row is a table row from the db. It's a RealDictRow object that looks like:
    # raw_row["country"] = "Mexico" and raw_row["score"] = Decimal("12.53")
    for raw_row in data:
        # processed_row is a table row as a dictionary that looks like:
        # processed_row = {"score": 12.53, 'player_name': 'rafa_vls', 'country': 'Mexico'}
        processed_row = {}

        # column_value is the column title of the db table. 
        # e.g. "country", "player_name" and "score"
        for column_value in raw_row:
            processed_row[column_value] = decimal_type_handler(raw_row[column_value])

        serialized_list.append(processed_row)
    
    return serialized_list

def decimal_type_handler(object_to_check):
    """
    Checks if object_to_check is of type decimal;
    if it is, casts it into a float.
    """

    if isinstance(object_to_check, Decimal):
        return float(object_to_check)

    return object_to_check

def get_countries_path() -> str:
    return os.path.join(
        os.path.dirname(__file__), 
        "static", 
        "countries.json"
        )

def get_countries_list(filepath: str) -> list:
    try:
        with open(filepath, "r") as f:
            countries = json.loads(f.read())
            f.close()
        return countries
    except FileNotFoundError:
        raise FileNotFoundError(f"File ${filepath} not found")

def validate_country(input: str):
    """
    Checks if country exists in country's input options,
    if it does, return country string, else return None.
    """
    countries_filepath = get_countries_path()
    countries = get_countries_list(countries_filepath)

    if input in countries:
        return input
    else:
        return None
