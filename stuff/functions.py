from datetime import datetime

# This function generates a date string based on the current date and arrays of day names.
def get_date(days_names):
    now = datetime.now()
    day_name = days_names[now.weekday()]
    return f"{day_name}, {now.day}. {now.month} {now.year}"
