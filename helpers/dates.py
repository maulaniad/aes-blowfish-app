from datetime import datetime, timedelta

# Helpers to generate dates and it's string formatted form.

def d_end_date():
    return datetime(year=3000, month=12, day=12, hour=12).date()

def dt_end_date():
    return datetime(year=3000, month=12, day=12, hour=12)

def d_now():
    return datetime.now().date()

def dt_now():
    return datetime.now()

def d_yesterday():
    return (datetime.now() - timedelta(days=1)).date()

def dt_yesterday():
    return (datetime.now() - timedelta(days=1))
