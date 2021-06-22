from decimal import Decimal

def make_serializable(data:list) -> list:
    """
    Returns a json-serializable list that can be 
    used as an http response.
    """

    serialized_list = []

    for raw_row in data:
        processed_row = {}

        for column_value in raw_row:
            processed_row[column_value] = decimal_type_handler(raw_row[column_value])

        serialized_list.append(processed_row)
    
    return serialized_list

def decimal_type_handler(object_to_check: (Decimal | any)) -> (float | any):
    """
    Checks if object_to_check is of type decimal;
    if it is, casts it into a float.
    """

    if isinstance(object_to_check, Decimal):
        return float(object_to_check)

    return object_to_check