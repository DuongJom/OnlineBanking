from datetime import datetime as dt

MAX_CARD_NUMBER_DIGITS = 14

# Filter to format currency
def currency_format(value):
    if value is None:
        value = 0
    return "{:,.2f}".format(float(value))

# Filter to format datetime
def datetime_format(value, format='%Y-%m-%d %H:%M:%S'):
    if isinstance(value, dt):
        return value.strftime(format)
    value = dt.strptime(value, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
    return value

# Filter to format date
def date_format(value):
    return dt.fromisoformat(value).date()

# Filter to strip whitespace
def strip(value):
    return str(value).strip()

# Filter to format date with a custom format
def format_date(value, format="%Y-%m-%d"):
    if value is None:
        return ""
    
    if isinstance(value, str):
        value = dt.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")

    return value.strftime(format)

# Filter to format card number (mask all but the last 4 digits)
def format_card_number(card_number):
    card_number_str = str(card_number)
    
    if len(card_number_str) == MAX_CARD_NUMBER_DIGITS:
        return f"**** **** **** {card_number_str[-4:]}"
    return card_number_str

# Filter to format ID (padded with zeros)
def format_id(id, length):
    return str(id).zfill(length)