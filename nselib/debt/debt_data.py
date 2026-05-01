import datetime as dt
import logging
from io import BytesIO

import pandas as pd

from nselib.libutil import nse_urlfetch

logger = logging.getLogger(__name__)


def securities_available_for_trading(trade_date: str) -> pd.DataFrame:
    """
    Get securities available for trading.

    Args:
        trade_date (str): Date in 'dd-mm-YYYY' format (e.g., '17-03-2022').

    Returns:
        pandas.DataFrame: A DataFrame containing securities available for trading.

    Example:
        >>> from nselib import debt
        >>> df = debt.securities_available_for_trading('17-03-2022')
    """
    logger.debug(f"Fetching securities available for trading for date: {trade_date}")
    month = dt.datetime.strptime(trade_date, "%d-%m-%Y").strftime("%b").upper()
    year = dt.datetime.strptime(trade_date, "%d-%m-%Y").strftime("%Y")
    date_str = dt.datetime.strptime(trade_date, "%d-%m-%Y").strftime("%d%m%Y")
    origin_url = "https://www.nseindia.com/all-reports-debt"
    url = f"https://nsearchives.nseindia.com/content/historical/WDM/{year}/{month}/wdmlist_{date_str}.csv"
    file_chk = nse_urlfetch(url, origin_url=origin_url)
    if file_chk.status_code != 200:
        logger.error(f"Failed to fetch data, status code: {file_chk.status_code}")
        raise FileNotFoundError("No data available")
    try:
        data_df = pd.read_csv(BytesIO(file_chk.content))
    except Exception as e:
        logger.error(f"Failed to parse equity list: {e}", exc_info=e)
        raise FileNotFoundError(f" Equity List not found :: NSE error : {e}")

    return data_df
