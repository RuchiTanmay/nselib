import os
from datetime import datetime, timedelta, date
import requests
import numpy as np
import pandas as pd
from nselib.constants import *
import pandas_market_calendars as mcal

default_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

header = {
            "referer": "https://www.nseindia.com/",
             "Connection": "keep-alive",
             "Cache-Control": "max-age=0",
             "DNT": "1",
             "Upgrade-Insecure-Requests": "1",
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
             "Sec-Fetch-User": "?1",
             "Accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
             "Sec-Fetch-Site": "none",
             "Sec-Fetch-Mode": "navigate",
             "Accept-Language": "en-US,en;q=0.9,hi;q=0.8"
            }

nse_calendar = mcal.get_calendar("NSE")


class CalenderNotFound(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(CalenderNotFound, self).__init__(message)


class NSEdataNotFound(Exception):
    def __init__(self, message):
        super(NSEdataNotFound, self).__init__(message)


def validate_param_from_list(value: str, static_options_list: list):
    if value not in static_options_list:
        raise ValueError(f"'{value}' not a valid parameter :: select from {static_options_list}")
    else:
        pass


def validate_date_param(from_date: str, to_date: str, period: str):
    if not period and (not from_date or not to_date):
        raise ValueError(' Please provide the valid parameters')
    elif period and period.upper() not in equity_periods:
        raise ValueError(f'period = {period} is not a valid value')

    try:
        if not period:
            from_date = datetime.strptime(from_date, dd_mm_yyyy)
            to_date = datetime.strptime(to_date, dd_mm_yyyy)
            time_delta = (to_date - from_date).days
            if time_delta < 1:
                raise ValueError(f'to_date should greater than from_date ')
    except Exception as e:
        print(e)
        raise ValueError(f'either or both from_date = {from_date} || to_date = {to_date} are not valid value')


def subtract_months(dt, months):
    # calculate target year and month
    year = dt.year
    month = dt.month - months

    # adjust year and month when month < 1
    while month <= 0:
        month += 12
        year -= 1

    # maximum days in each month
    month_days = [31,
                  29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,
                  31, 30, 31, 30,
                  31, 31, 30, 31, 30, 31]

    # adjust the day if current date > max days in target month
    day = min(dt.day, month_days[month - 1])

    return date(year, month, day)


def derive_from_and_to_date(from_date: str = None, to_date: str = None, period: str = None):
    if not period:
        return from_date, to_date
    today = date.today()
    conditions = [period.upper() == '1D',
                  period.upper() == '1W',
                  period.upper() == '1M',
                  period.upper() == '6M',
                  period.upper() == '1Y'
                  ]
    value = [today - timedelta(days=1),
             today - timedelta(weeks=1),
             subtract_months(today, 1),
             subtract_months(today, 6),
             subtract_months(today, 12)]

    f_date = np.select(conditions, value, default=(today - timedelta(days=1)))
    f_date = pd.to_datetime(str(f_date))
    while True:
        date_chk = nse_calendar.schedule(start_date=f_date, end_date=f_date)
        if not date_chk.empty:  # If market was open on this day
            break  # Stop the loop
        f_date -= timedelta(days=1)
    from_date = f_date.strftime(dd_mm_yyyy)
    today = today.strftime(dd_mm_yyyy)
    return from_date, today


def cleaning_column_name(col: list):
    unwanted_str_list = ['FH_', 'EOD_', 'HIT_']
    new_col = col
    for unwanted in unwanted_str_list:
        new_col = [name.replace(f'{unwanted}', '') for name in new_col]
    return new_col


def cleaning_nse_symbol(symbol):
    symbol = symbol.replace('&', '%26')  # URL Parse for Stocks Like M&M Finance
    return symbol.upper()


def nse_urlfetch(url, origin_url="http://nseindia.com"):
    r_session = requests.session()
    nse_live = r_session.get(origin_url, headers=default_header)
    cookies = nse_live.cookies
    return r_session.get(url, headers=header, cookies=cookies)


def get_nselib_path():
    """
    Extract isap file path
    """
    mydir = os.getcwd()
    return mydir.split(r'\nselib', 1)[0]


def get_month_from_date(trade_date):
    """
    get the month
    :param trade_date:
    :return: 'Dec'
    """
    return datetime.strptime(trade_date, '%Y-%m-%d').strftime('%b')


def trading_holiday_calendar():
    data_df = pd.DataFrame(columns=['Product', 'tradingDate', 'weekDay', 'description', 'Sr_no'])
    url = "https://www.nseindia.com/api/holiday-master?type=trading"
    try:
        data_dict = nse_urlfetch(url).json()
    except Exception as e:
        raise CalenderNotFound(" Calender data Not found try after some time ")
    for prod in data_dict:
        h_df = pd.DataFrame(data_dict[prod])
        h_df['Product'] = prod
        data_df = pd.concat([data_df, h_df])
    condition = [data_df['Product'] == 'CBM', data_df['Product'] == 'CD', data_df['Product'] == 'CM',
                 data_df['Product'] == 'CMOT', data_df['Product'] == 'COM', data_df['Product'] == 'FO',
                 data_df['Product'] == 'IRD', data_df['Product'] == 'MF', data_df['Product'] == 'NDM',
                 data_df['Product'] == 'NTRP', data_df['Product'] == 'SLBS']
    value = ['Corporate Bonds', 'Currency Derivatives', 'Equities', 'CMOT', 'Commodity Derivatives', 'Equity Derivatives',
             'Interest Rate Derivatives', 'Mutual Funds', 'New Debt Segment', 'Negotiated Trade Reporting Platform',
             'Securities Lending & Borrowing Schemes']
    data_df['Product'] = np.select(condition, value, default='Unknown')
    return data_df


if __name__ == '__main__':
    # data = derive_from_and_to_date('6M')
    print(trading_holiday_calendar())



