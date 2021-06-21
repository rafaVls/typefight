from decimal import Decimal

def decimal_type_handler(decimal_value: Decimal) -> str:
    """
    Used as type handler when using json.dumps.
    It'll take a non json-serializable Decimal type and convert
    it to a json-serializable string type.
    """
    
    if isinstance(decimal_value, Decimal):
        return str(decimal_value)
    raise TypeError