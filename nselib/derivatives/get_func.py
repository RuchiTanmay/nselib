import logging
import pandas as pd
import requests

from nselib.constants import indices_list
from nselib.errors import NSEdataNotFound
from nselib.libutil import (
    cleaning_column_name,
    cleaning_nse_symbol,
    future_price_volume_data_column,
    nse_urlfetch,
    default_header,
    header,
)

logger = logging.getLogger(__name__)


def get_future_price_volume_data(
    symbol: str, instrument: str, from_date: str, to_date: str
) -> pd.DataFrame:
    """
    Fetch historical price and volume data for a specific futures contract.

    Args:
        symbol (str): The ticker symbol of the underlying asset (e.g., 'SBIN', 'NIFTY').
        instrument (str): The type of futures instrument ('FUTIDX' for index futures, 'FUTSTK' for stock futures).
        from_date (str): The start date for the historical data in 'DD-MM-YYYY' format.
        to_date (str): The end date for the historical data in 'DD-MM-YYYY' format.

    Returns:
        pandas.DataFrame: A DataFrame containing the historical OHLCV data and other transaction details.

    Raises:
        ValueError: If the NSE API rejects the parameters or encounters an error during the fetch.

    Example:
        >>> from nselib import derivatives
        >>> df = derivatives.future_price_volume_data(symbol='SBIN', instrument='FUTSTK', period='1M')
    """
    logger.debug(
        f"Fetching future price volume data for symbol: {symbol}, instrument: {instrument}, from: {from_date}, to: {to_date}"
    )
    origin_url = "https://www.nseindia.com/report-detail/fo_eq_security"
    url = "https://www.nseindia.com/api/historicalOR/foCPV?"
    payload = f"from={from_date}&to={to_date}&instrumentType={instrument}&symbol={symbol}&csv=true"

    try:
        logger.debug("Making request to NSE API for future data.")
        data: dict = nse_urlfetch(url + payload, origin_url=origin_url).json()
    except Exception as e:
        logger.error(
            f"Failed to fetch future price volume data. Error: {e}", exc_info=e
        )
        raise ValueError(f" Invalid parameters : NSE error:{e}")

    data_df = pd.DataFrame(data["data"])
    data_df.columns = cleaning_column_name(data_df.columns)
    logger.debug(
        f"Successfully retrieved future price volume data with {len(data_df)} records."
    )
    return data_df


def get_option_price_volume_data(
    symbol: str, instrument: str, option_type: str, from_date: str, to_date: str
) -> pd.DataFrame:
    """
    Fetch historical price and volume data for a specific options contract.

    Args:
        symbol (str): The ticker symbol of the underlying asset (e.g., 'RELIANCE', 'BANKNIFTY').
        instrument (str): The type of options instrument ('OPTIDX' for index options, 'OPTSTK' for stock options).
        option_type (str): The type of option ('CE' for Call European, 'PE' for Put European).
        from_date (str): The start date for the historical data in 'DD-MM-YYYY' format.
        to_date (str): The end date for the historical data in 'DD-MM-YYYY' format.

    Returns:
        pandas.DataFrame: A DataFrame containing the historical OHLCV data for the requested option.

    Raises:
        ValueError: If the provided parameters yield no data, or if the NSE API throws an error.

    Example:
        >>> from nselib import derivatives
        >>> df = derivatives.option_price_volume_data(symbol='NIFTY', instrument='OPTIDX', option_type='CE', period='1M')
    """
    logger.debug(
        f"Fetching option price volume data for symbol: {symbol}, instrument: {instrument}, option type: {option_type}, from: {from_date}, to: {to_date}"
    )
    origin_url = "https://www.nseindia.com/report-detail/fo_eq_security"
    url = "https://www.nseindia.com/api/historicalOR/foCPV?"
    payload = (
        f"from={from_date}&to={to_date}&instrumentType={instrument}&symbol={symbol}"
        f"&optionType={option_type}&csv=true"
    )
    try:
        logger.debug("Making request to NSE API for option data.")
        data_dict = nse_urlfetch(url + payload, origin_url=origin_url).json()
    except Exception as e:
        logger.error(
            f"Failed to fetch option price volume data. Error: {e}", exc_info=e
        )
        raise ValueError(f" Invalid parameters : NSE error : {e}")

    data_df = pd.DataFrame(data_dict["data"])
    if data_df.empty:
        logger.warning(f"No option price volume data returned for symbol: {symbol}")
        raise ValueError("Invalid parameters, Please change the parameters")

    data_df.columns = cleaning_column_name(data_df.columns)
    logger.debug(
        f"Successfully retrieved option price volume data with {len(data_df)} records."
    )
    return data_df[future_price_volume_data_column]


def get_nse_option_chain(symbol: str, expiry_date: str):
    """
    Fetch the complete live option chain for a given symbol and expiry date.

    Args:
        symbol (str): The underlying symbol (e.g., 'TCS', 'NIFTY'). The function automatically determines if it's an index or equity.
        expiry_date (str): The exact expiration date in 'DD-MMM-YYYY' format (e.g., '25-Dec-2025').

    Returns:
        requests.Response: The HTTP response from the NSE API containing the option chain data payload.

    Example:
        >>> from nselib import derivatives
        >>> chain = derivatives.nse_live_option_chain(symbol='TCS', expiry_date='27-03-2026')
    """
    logger.debug(
        f"Fetching NSE option chain for symbol: {symbol}, expiry date: {expiry_date}"
    )
    symbol = cleaning_nse_symbol(symbol)
    origin_url = "https://www.nseindia.com/option-chain"

    if any(x in symbol for x in indices_list):
        logger.debug(f"Symbol '{symbol}' identified as an index.")
        url = f"https://www.nseindia.com/api/option-chain-v3?type=Indices&symbol={symbol}&expiry={expiry_date}"
    else:
        logger.debug(f"Symbol '{symbol}' identified as equity.")
        url = f"https://www.nseindia.com/api/option-chain-v3?type=Equity&symbol={symbol}&expiry={expiry_date}"

    logger.debug("Making request to NSE API for option chain data.")
    chain = nse_urlfetch(url, origin_url=origin_url)
    logger.debug("Successfully retrieved option chain data.")
    return chain


def _get_business_growth_fo_segment_data(api_path: str) -> dict:
    """
    Internal helper to fetch business growth data for the F&O segment from NSE.

    Establishes a fresh session with the NSE origin page to obtain cookies,
    then makes the actual API request.

    Args:
        api_path (str): The relative API path to query (e.g., '/api/historicalOR/fo/tbg/yearly').

    Returns:
        dict: The parsed JSON response from the NSE API.

    Raises:
        NSEdataNotFound: If the NSE API is unreachable or returns an error.
    """
    logger.debug(f"Fetching business growth F&O segment data from path: {api_path}")
    origin_url = "https://www.nseindia.com/market-data/business-growth-fo-segment"
    url = f"https://www.nseindia.com{api_path}"
    try:
        r_session = requests.session()
        r_session.trust_env = False
        nse_live = r_session.get(origin_url, headers=default_header)
        cookies = nse_live.cookies
        data_json = r_session.get(url, headers=header, cookies=cookies).json()
    except Exception as e:
        logger.error(
            f"Failed to fetch business growth F&O data. Error: {e}", exc_info=e
        )
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    logger.debug("Successfully retrieved business growth F&O segment data.")
    return data_json


def get_business_growth_fo_segment_yearly() -> dict:
    """
    Fetch yearly business growth data for the NSE F&O segment.

    Returns:
        dict: The JSON response containing yearly F&O business growth statistics.

    Example:
        >>> from nselib import derivatives
        >>> df = derivatives.business_growth_fo_segment(data_type='yearly')
    """
    logger.debug("Fetching yearly business growth F&O segment data.")
    return _get_business_growth_fo_segment_data("/api/historicalOR/fo/tbg/yearly")


def get_business_growth_fo_segment_monthly(from_year: str, to_year: str) -> dict:
    """
    Fetch monthly business growth data for the NSE F&O segment for a given financial year.

    Args:
        from_year (str): The starting year of the financial year (e.g., '2025').
        to_year (str): The ending year of the financial year (e.g., '2026').

    Returns:
        dict: The JSON response containing monthly F&O business growth statistics.

    Example:
        >>> from nselib import derivatives
        >>> df = derivatives.business_growth_fo_segment(data_type='monthly', from_year='2025', to_year='2026')
    """
    logger.debug(
        f"Fetching monthly business growth F&O segment data for FY {from_year}-{to_year}."
    )
    return _get_business_growth_fo_segment_data(
        f"/api/historicalOR/fo/tbg/monthly?from={from_year}&to={to_year}"
    )


def get_business_growth_fo_segment_daily(month: str, year: str) -> dict:
    """
    Fetch daily business growth data for the NSE F&O segment for a given month and year.

    Args:
        month (str): The 3-letter abbreviated month name (e.g., 'Mar').
        year (str): The full year (e.g., '2026').

    Returns:
        dict: The JSON response containing daily F&O business growth statistics.

    Example:
        >>> from nselib import derivatives
        >>> df = derivatives.business_growth_fo_segment(data_type='daily', month='Mar', year='2026')
    """
    logger.debug(f"Fetching daily business growth F&O segment data for {month} {year}.")
    return _get_business_growth_fo_segment_data(
        f"/api/historicalOR/fo/tbg/daily?month={month}&year={year}"
    )
