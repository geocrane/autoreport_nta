import datetime

# from dateutil.relativedelta import relativedelta
import random


def get_date_from():
    today = datetime.date.today()
    first = today.replace(day=1)
    last_of_previous_month = first - datetime.timedelta(days=1)
    first_of_previous_month = last_of_previous_month.replace(day=1)
    return first_of_previous_month

    # current_date = datetime.date.today()
    # return (current_date - relativedelta(months=7))
