from decimal import Decimal

def decimal_type_handler(decimal_value):
    if isinstance(decimal_value, Decimal):
        return str(decimal_value)
    raise TypeError