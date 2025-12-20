import datetime as dt
from io import BytesIO, StringIO
import json
from nselib.libutil import *
from nselib.constants import *


def securities_available_for_trading(trade_date):
    """
    get securities available for trading
    trade_date: 17-03-2022' ('dd-mm-YYYY') format
    :return: pandas dataframe
    """
    month = dt.datetime.strptime(trade_date, '%d-%m-%Y').strftime('%b').upper()
    year = dt.datetime.strptime(trade_date, '%d-%m-%Y').strftime('%Y')
    date_str = dt.datetime.strptime(trade_date, '%d-%m-%Y').strftime('%d%m%Y')
    origin_url = "https://www.nseindia.com/all-reports-debt"
    url = f"https://nsearchives.nseindia.com/content/historical/WDM/{year}/{month}/wdmlist_{date_str}.csv"
    file_chk = nse_urlfetch(url, origin_url=origin_url)
    if file_chk.status_code != 200:
        raise FileNotFoundError(f" No data available")
    try:
        data_df = pd.read_csv(BytesIO(file_chk.content))
    except Exception as e:
        raise FileNotFoundError(f' Equity List not found :: NSE error : {e}')
    return data_df


# if __name__ == '__main__':
#     data = securities_available_for_trading('02-12-2025')
#     print(data)
