from nselib.libutil import header
from nselib.libutil import default_header
import logging
import numpy as np
import pandas as pd
import zipfile
import requests
from datetime import datetime, timedelta
from io import BytesIO
from typing import Optional

from nselib.constants import ddmmyy
from nselib.derivatives.get_func import (
    cleaning_nse_symbol,
    dd_mm_yyyy,
    derive_from_and_to_date,
    future_price_volume_data_column,
    get_business_growth_fo_segment_daily,
    get_business_growth_fo_segment_monthly,
    get_business_growth_fo_segment_yearly,
    get_future_price_volume_data,
    get_nse_option_chain,
    get_option_price_volume_data,
    indices_list,
    nse_urlfetch,
    validate_date_param,
    validate_param_from_list,
)
from nselib.errors import (
    DerivativeInstrumentNotFoundError,
    NSEdataNotFound,
    NSEApiError,
)

logger = logging.getLogger(__name__)


def future_price_volume_data(
    symbol: str,
    instrument: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    period: Optional[str] = None,
):
    """
    Fetch the contract-wise future price and volume data set.

    Args:
        symbol (str): The NSE symbol (e.g., 'SBIN' or 'BANKNIFTY').
        instrument (str): The instrument type (e.g., 'FUTIDX' or 'FUTSTK').
        from_date (str, optional): The start date in 'dd-mm-YYYY' format (e.g., '17-03-2022').
        to_date (str, optional): The end date in 'dd-mm-YYYY' format (e.g., '17-06-2023').
        period (str, optional): A predefined time period to fetch data for.
            Must be one of {'1D': last day, '1W': last 7 days, '1M': last month, '3M': last 3 months, '6M': last 6 months}.

    Returns:
        pd.DataFrame: A DataFrame containing the future price volume data.

    Raises:
        ValueError: If the parameters or dates are formatted incorrectly.

    Example:
        >>> from nselib import derivatives
        >>> df = derivatives.future_price_volume_data(symbol='SBIN', instrument='FUTSTK', period='1M')
    """
    validate_date_param(from_date, to_date, period)
    logger.debug(
        f"Fetching future price volume data (aggregated) for symbol: {symbol}, instrument: {instrument}, period: {period}"
    )
    symbol, instrument = cleaning_nse_symbol(symbol=symbol), instrument.upper()
    if instrument not in ["FUTIDX", "FUTSTK"]:
        raise DerivativeInstrumentNotFoundError(
            f"{instrument} is not a future instrument"
        )

    from_date, to_date = derive_from_and_to_date(
        from_date=from_date, to_date=to_date, period=period
    )
    nse_df = pd.DataFrame(columns=future_price_volume_data_column)
    from_date = datetime.strptime(from_date, dd_mm_yyyy)
    to_date = datetime.strptime(to_date, dd_mm_yyyy)
    load_days = (to_date - from_date).days
    while load_days > 0:
        if load_days > 90:
            end_date = (from_date + timedelta(90)).strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        else:
            end_date = to_date.strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        data_df = get_future_price_volume_data(
            symbol=symbol, instrument=instrument, from_date=start_date, to_date=end_date
        )
        from_date = from_date + timedelta(91)
        load_days = (to_date - from_date).days
        if nse_df.empty:
            nse_df = data_df
        else:
            nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    logger.debug(f"Aggregated {len(nse_df)} records for {symbol} futures.")
    return nse_df


def option_price_volume_data(
    symbol: str,
    instrument: str,
    option_type: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    period: Optional[str] = None,
) -> pd.DataFrame:
    """
    Fetch the contract-wise option price and volume data set.
    Note: Collecting more than 90 days of data may take a significantly longer time.

    Args:
        symbol (str): The NSE symbol (e.g., 'SBIN' or 'BANKNIFTY').
        instrument (str): The instrument type (e.g., 'OPTIDX' or 'OPTSTK').
        option_type (str, optional): The option type (e.g., 'PE' or 'CE').
        from_date (str, optional): The start date in 'dd-mm-YYYY' format.
        to_date (str, optional): The end date in 'dd-mm-YYYY' format.
        period (str, optional): A predefined time period to fetch data for.
            Must be one of {'1D': last day, '1W': last 7 days, '1M': last month, '3M': last 3 months, '6M': last 6 months}.

    Returns:
        pd.DataFrame: A DataFrame containing the option price volume data.

    Raises:
        ValueError: If the parameters or dates are formatted incorrectly.

    Example:
        >>> from nselib import derivatives
        >>> df = derivatives.option_price_volume_data(symbol='NIFTY', instrument='OPTIDX', option_type='CE', period='1M')
    """
    validate_date_param(from_date, to_date, period)
    logger.debug(
        f"Fetching option price volume data (aggregated) for symbol: {symbol}, instrument: {instrument}, option_type: {option_type}"
    )
    symbol, instrument = cleaning_nse_symbol(symbol=symbol), instrument.upper()
    if instrument not in ["OPTIDX", "OPTSTK"]:
        raise DerivativeInstrumentNotFoundError(
            f"{instrument} is not a future instrument"
        )

    if option_type and option_type not in ["PE", "CE"]:
        raise DerivativeInstrumentNotFoundError(
            f"{option_type} is not a valid option type"
        )

    option_type = [option_type] if option_type else ["PE", "CE"]
    from_date, to_date = derive_from_and_to_date(
        from_date=from_date, to_date=to_date, period=period
    )
    nse_df = pd.DataFrame(columns=future_price_volume_data_column)
    from_date = datetime.strptime(from_date, dd_mm_yyyy)
    to_date = datetime.strptime(to_date, dd_mm_yyyy)
    load_days = (to_date - from_date).days
    while load_days > 0:
        if load_days > 90:
            end_date = (from_date + timedelta(90)).strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        else:
            end_date = to_date.strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        for opt_typ in option_type:
            data_df = get_option_price_volume_data(
                symbol=symbol,
                instrument=instrument,
                option_type=opt_typ,
                from_date=start_date,
                to_date=end_date,
            )
            if nse_df.empty:
                nse_df = data_df
            else:
                nse_df = pd.concat([nse_df, data_df], ignore_index=True)
        from_date = from_date + timedelta(91)
        load_days = (to_date - from_date).days

    logger.debug(f"Aggregated {len(nse_df)} records for {symbol} options.")
    return nse_df


def fno_bhav_copy(trade_date: str) -> pd.DataFrame:
    """
    Fetch the new CM-UDiFF Common NSE future and options bhav copy.
    Valid from 2018 onwards.

    Args:
        trade_date (str): The trade date in 'dd-mm-YYYY' format (e.g., '20-06-2023').

    Returns:
        pd.DataFrame: A DataFrame containing the F&O Bhavcopy data.

    Raises:
        NSEdataNotFound: If no data is found for the given date.

    Example:
        >>> from nselib import derivatives
        >>> df = derivatives.fno_bhav_copy(trade_date='17-02-2025')
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    logger.debug(
        f"Fetching F&O Bhavcopy for trade date: {trade_date.strftime('%d-%m-%Y')}"
    )
    url = "https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_"
    payload = f"{str(trade_date.strftime('%Y%m%d'))}_F_0000.csv.zip"
    request_bhav = nse_urlfetch(url + payload)
    bhav_df = pd.DataFrame()
    if request_bhav.status_code == 200:
        zip_bhav = zipfile.ZipFile(BytesIO(request_bhav.content), "r")
        for file_name in zip_bhav.filelist:
            if file_name:
                bhav_df = pd.read_csv(zip_bhav.open(file_name))
    elif request_bhav.status_code == 403:
        url2 = (
            "https://www.nseindia.com/api/reports?archives="
            "%5B%7B%22name%22%3A%22F%26O%20-%20Bhavcopy(csv)%22%2C%22type%22%3A%22archives%22%2C%22category%22"
            f"%3A%22derivatives%22%2C%22section%22%3A%22equity%22%7D%5D&date={str(trade_date.strftime('%d-%b-%Y'))}"
            f"&type=equity&mode=single"
        )
        request_bhav = nse_urlfetch(url2)
        if request_bhav.status_code == 200:
            zip_bhav = zipfile.ZipFile(BytesIO(request_bhav.content), "r")
            for file_name in zip_bhav.filelist:
                if file_name:
                    bhav_df = pd.read_csv(zip_bhav.open(file_name))
        elif request_bhav.status_code == 403:
            logger.error(
                f"F&O Bhavcopy data not found for {trade_date.strftime('%d-%m-%Y')}"
            )
            raise NSEdataNotFound("Data not found, change the date...")
    # bhav_df = bhav_df[['INSTRUMENT', 'SYMBOL', 'EXPIRY_DT', 'STRIKE_PR', 'OPTION_TYP', 'OPEN', 'HIGH', 'LOW',
    #                    'CLOSE', 'SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH', 'OPEN_INT', 'CHG_IN_OI', 'TIMESTAMP']]
    logger.debug(f"Successfully retrieved F&O Bhavcopy with {len(bhav_df)} records.")
    return bhav_df


def participant_wise_open_interest(trade_date: str) -> pd.DataFrame:
    """
    Fetch FII, DII, Pro, and Client-wise participant Open Interest (OI) data for a given trade date.

    Args:
        trade_date (str): The trade date in 'dd-mm-YYYY' format (e.g., '20-06-2023').

    Returns:
        pd.DataFrame: A DataFrame containing participant-wise open interest data.

    Raises:
        NSEdataNotFound: If the OI data is not available for the given date.

    Example:
        >>> from nselib import derivatives
        >>> df = derivatives.participant_wise_open_interest(trade_date='16-09-2024')
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    logger.debug(
        f"Fetching participant-wise open interest for trade date: {trade_date.strftime('%d-%m-%Y')}"
    )
    url = f"https://nsearchives.nseindia.com/content/nsccl/fao_participant_oi_{str(trade_date.strftime('%d%m%Y'))}.csv"
    # payload = f"{str(for_date.strftime('%d%m%Y'))}.csv"
    file_chk = nse_urlfetch(url)
    if file_chk.status_code == 404:
        url = f"https://archives.nseindia.com/content/nsccl/fao_participant_oi_{str(trade_date.strftime('%d%m%Y'))}.csv"
        file_chk = nse_urlfetch(url)
    if file_chk.status_code != 200:
        logger.error(
            f"Participant-wise open interest data not found for {trade_date.strftime('%d-%m-%Y')}"
        )
        raise NSEdataNotFound(f"No data available for : {trade_date}")
    try:
        # data_df = pd.read_csv(url, engine='python', sep=',', quotechar='"', on_bad_lines='skip', skiprows=1)
        data_df = pd.read_csv(
            BytesIO(file_chk.content), on_bad_lines="skip", skiprows=1
        )
    except Exception as e:
        logger.error(
            f"Error while fetching participant wise open interest data: {e}",
            exc_info=e,
        )
        data_df = pd.read_csv(
            BytesIO(file_chk.content), on_bad_lines="skip", skiprows=1
        )
        data_df.drop(data_df.tail(1).index, inplace=True)
        data_df.columns = [name.replace("\t", "") for name in data_df.columns]
    return data_df


def participant_wise_trading_volume(trade_date: str) -> pd.DataFrame:
    """
    Fetch FII, DII, Pro, and Client-wise participant trading volume data for a given trade date.

    Args:
        trade_date (str): The trade date in 'dd-mm-YYYY' format (e.g., '20-06-2023').

    Returns:
        pd.DataFrame: A DataFrame containing participant-wise trading volume data.

    Raises:
        NSEdataNotFound: If the volume data is not available for the given date.

    Example:
        >>> from nselib import derivatives
        >>> df = derivatives.participant_wise_trading_volume(trade_date='16-09-2024')
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    logger.debug(
        f"Fetching participant-wise trading volume for trade date: {trade_date.strftime('%d-%m-%Y')}"
    )
    url = f"https://nsearchives.nseindia.com/content/nsccl/fao_participant_vol_{str(trade_date.strftime('%d%m%Y'))}.csv"
    # payload = f"{str(for_date.strftime('%d%m%Y'))}.csv"
    file_chk = nse_urlfetch(url)
    if file_chk.status_code != 200:
        logger.error(
            f"Participant-wise trading volume data not found for {trade_date.strftime('%d-%m-%Y')}"
        )
        raise NSEdataNotFound(f"No data available for : {trade_date}")
    try:
        data_df = pd.read_csv(
            BytesIO(file_chk.content), on_bad_lines="skip", skiprows=1
        )
    except Exception as e:
        logger.error(
            f"Error while fetching participant wise trading volume data: {e}",
            exc_info=e,
        )
        data_df = pd.read_csv(
            BytesIO(file_chk.content),
            engine="c",
            sep=",",
            quotechar='"',
            on_bad_lines="skip",
            skiprows=1,
        )
        data_df.drop(data_df.tail(1).index, inplace=True)
        data_df.columns = [name.replace("\t", "") for name in data_df.columns]
    return data_df


def daily_volatility(trade_date: str):
    """
    get F&O daily volatility report as per the traded date provided
    :param trade_date: eg:'20-06-2023'
    :return: pandas dataframe
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    payload = f"FOVOLT_{str(trade_date.strftime('%d%m%Y'))}.csv"
    origin_url = "https://www.nseindia.com/all-reports-derivatives"
    report_urls = [
        f"https://nsearchives.nseindia.com/archives/nsccl/volt/{payload}",
        f"https://archives.nseindia.com/archives/nsccl/volt/{payload}",
        "https://www.nseindia.com/api/reports?archives="
        "%5B%7B%22name%22%3A%22F%26O%20-%20Daily%20Volatility%22%2C%22type%22%3A%22archives%22%2C%22category%22"
        f"%3A%22derivatives%22%2C%22section%22%3A%22equity%22%7D%5D&date={str(trade_date.strftime('%d-%b-%Y'))}"
        f"&type=equity&mode=single",
    ]
    last_status_code = None
    for url in report_urls:
        # NSE archive requests can fail behind stale local proxy settings, so fetch this report
        # with a session that ignores environment proxies while preserving the usual cookie flow.
        r_session = requests.session()
        r_session.trust_env = False
        nse_live = r_session.get(origin_url, headers=default_header)
        cookies = nse_live.cookies
        report = r_session.get(url, headers=header, cookies=cookies)
        last_status_code = report.status_code
        if report.status_code != 200:
            continue
        try:
            data_df = pd.read_csv(BytesIO(report.content), skipinitialspace=True)
        except Exception as exc:
            raise FileNotFoundError(
                f" Daily volatility data not found for : {trade_date.strftime(dd_mm_yyyy)} :: NSE error : {exc}"
            )
        data_df = data_df.dropna(how="all")
        data_df.columns = [column_name.strip() for column_name in data_df.columns]
        return data_df
    raise FileNotFoundError(
        f" No daily volatility data available for : {trade_date.strftime(dd_mm_yyyy)} :: status={last_status_code}"
    )


def category_turnover_fo(trade_date: str) -> pd.DataFrame:
    """
    Fetch NSE derivatives category-wise turnover data for a given trade date.

    Args:
        trade_date (str): The trade date in 'dd-mm-YYYY' format (e.g., '07-04-2026').

    Returns:
        pd.DataFrame: A DataFrame containing the category-wise turnover data.

    Raises:
        NSEdataNotFound: If the turnover data cannot be found for the given date.

    Example:
        >>> from nselib import derivatives
        >>> df = derivatives.category_turnover_fo(trade_date='16-09-2025')
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    logger.debug(
        f"Fetching category-wise turnover for trade date: {trade_date.strftime('%d-%m-%Y')}"
    )
    url = f"https://archives.nseindia.com/archives/fo/cat/fo_cat_turnover_{trade_date.strftime(ddmmyy)}.xls"
    file_chk = nse_urlfetch(url)
    if file_chk.status_code != 200:
        logger.error(
            f"Category turnover FO data not found for {trade_date.strftime('%d-%m-%Y')}"
        )
        raise NSEdataNotFound(f"No data available for : {trade_date}")

    raw = pd.read_excel(BytesIO(file_chk.content), header=None, engine="xlrd")
    header_row = None
    for index in range(min(len(raw), 16)):
        first = str(raw.iloc[index, 0]).strip()
        second = str(raw.iloc[index, 1]).strip() if raw.shape[1] > 1 else ""
        if first.lower() == "trade date" and second.lower() in {
            "category",
            "client categories",
        }:
            header_row = index
            break
    if header_row is None:
        logger.error(
            f"Could not locate header row in category turnover data for {trade_date.strftime('%d-%m-%Y')}"
        )
        raise NSEdataNotFound(f"Category turnover FO data not found for : {trade_date}")

    headers = [str(value).strip() for value in raw.iloc[header_row, :4].tolist()]
    end_row = header_row + 1
    while end_row < len(raw.index):
        first_value = raw.iloc[end_row, 0] if raw.shape[1] > 0 else None
        second_value = raw.iloc[end_row, 1] if raw.shape[1] > 1 else None
        first_text = str(first_value).strip() if first_value is not None else ""
        second_text = str(second_value).strip() if second_value is not None else ""
        if (
            first_value is None
            or (isinstance(first_value, float) and pd.isna(first_value))
            or first_text.lower().startswith("note")
            or first_text.lower().startswith("notes")
            or first_text.lower() == "trade date"
            or second_text.lower() in {"category", "client categories"}
        ):
            break
        end_row += 1

    data_df = raw.iloc[header_row + 1 : end_row, :4].copy()
    data_df.columns = headers
    data_df = data_df.rename(
        columns={
            "Trade Date": "Trade Date",
            "Category": "Category",
            "Client Categories": "Category",
            "Buy Value in Rs.Crores": "Buy Value in Rs.Crores",
            "Sell Value in Rs.Crores": "Sell Value in Rs.Crores",
        }
    )
    data_df = data_df[
        [
            column
            for column in [
                "Trade Date",
                "Category",
                "Buy Value in Rs.Crores",
                "Sell Value in Rs.Crores",
            ]
            if column in data_df.columns
        ]
    ].copy()
    data_df["Trade Date"] = pd.to_datetime(data_df["Trade Date"], errors="coerce")
    data_df["Category"] = data_df["Category"].astype(str).str.strip()
    data_df = data_df[data_df["Category"].ne("")].copy()
    for column_name in ["Buy Value in Rs.Crores", "Sell Value in Rs.Crores"]:
        data_df[column_name] = pd.to_numeric(data_df[column_name], errors="coerce")
    data_df = data_df.dropna(subset=["Trade Date", "Category"]).reset_index(drop=True)
    data_df["Net Value in Rs.Crores"] = (
        data_df["Buy Value in Rs.Crores"] - data_df["Sell Value in Rs.Crores"]
    )
    data_df["Trade Date"] = data_df["Trade Date"].dt.strftime("%d-%b-%Y")
    return data_df


def fii_derivatives_statistics(trade_date: str) -> pd.DataFrame:
    """
    Fetch specific FII derivatives statistics for a given trade date.

    Args:
        trade_date (str): The trade date in 'dd-mm-YYYY' format (e.g., '20-06-2023').

    Returns:
        pd.DataFrame: A DataFrame containing the FII derivatives statistics.

    Raises:
        NSEdataNotFound: If the statistics are not available for the given date.

    Example:
        >>> from nselib import derivatives
        >>> df = derivatives.fii_derivatives_statistics(trade_date='16-09-2024')
    """
    t_date = pd.to_datetime(trade_date, format="%d-%m-%Y")
    trade_date = t_date.strftime("%d-%b-%Y")
    logger.debug(f"Fetching FII derivatives statistics for trade date: {trade_date}")
    url = f"https://nsearchives.nseindia.com/content/fo/fii_stats_{trade_date}.xls"
    file_chk = nse_urlfetch(url)
    if file_chk.status_code != 200:
        logger.error(f"FII derivatives statistics not found for {trade_date}")
        raise NSEdataNotFound(f"No data available for : {trade_date}")
    try:
        bhav_df = pd.read_excel(
            BytesIO(file_chk.content), skiprows=3, skipfooter=10
        ).dropna()
        bhav_df.columns = [
            "fii_derivatives",
            "buy_contracts",
            "buy_value_in_Cr",
            "sell_contracts",
            "sell_value_in_Cr",
            "open_contracts",
            "open_contracts_value_in_Cr",
        ]
    except Exception as e:
        logger.error(
            f"Failed to parse FII derivatives statistics for {trade_date}",
            exc_info=e,
        )
        raise NSEdataNotFound(
            f"FII derivatives statistics not found for : {trade_date} :: NSE error : {e}"
        )
    return bhav_df


def expiry_dates_future() -> list:
    """
    Fetch the list of valid expiry dates for futures contracts.

    Returns:
        list: A list of expiration dates in 'dd-MMM-yyyy' format.

    Example:
        >>> from nselib import derivatives
        >>> exp_dates = derivatives.expiry_dates_future()
    """
    origin_url = "https://www.nseindia.com/option-chain"
    logger.debug("Fetching valid expiry dates for futures contracts.")
    payload = nse_urlfetch(
        "https://www.nseindia.com/api/option-chain-contract-info?symbol=TCS",
        origin_url=origin_url,
    ).json()
    return payload["expiryDates"]


def expiry_dates_option_index() -> dict:
    """
    Fetch the valid future and option expiry dates mapped to their underlying stock or index.

    Returns:
        dict: A dictionary mapping index/symbols to their exact list of expiry dates.

    Example:
        >>> from nselib import derivatives
        >>> index_dates_map = derivatives.expiry_dates_option_index()
    """
    # data_df = pd.DataFrame(columns=['index', 'expiry_date'])
    logger.debug("Fetching valid expiry dates for mapped option indices.")
    data_dict = {}
    for ind in indices_list:
        origin_url = "https://www.nseindia.com/option-chain"
        payload = nse_urlfetch(
            f"https://www.nseindia.com/api/option-chain-contract-info?symbol={ind}",
            origin_url=origin_url,
        ).json()
        data_dict.update({ind: payload["expiryDates"]})
    return data_dict


def nse_live_option_chain(
    symbol: str, expiry_date: str = None, oi_mode: str = "full"
) -> pd.DataFrame:
    """
    Fetch the live NSE option chain.

    Args:
        symbol (str): The NSE symbol (e.g., 'SBIN' or 'BANKNIFTY').
        expiry_date (str, optional): The specific expiry date to filter by, in 'dd-mm-YYYY' format.
        oi_mode (str, optional): The detail level of the Open Interest data. Can be 'full' or 'compact'.

    Returns:
        pd.DataFrame: A DataFrame containing the real-time option chain data.

    Example:
        >>> from nselib import derivatives
        >>> chain_df = derivatives.nse_live_option_chain(symbol='TCS', expiry_date='20-06-2023')
    """

    if expiry_date:
        exp_date = pd.to_datetime(expiry_date, format="%d-%m-%Y")
        expiry_date = pd.to_datetime(exp_date, format="%d-%m-%Y").strftime("%d-%b-%Y")
    logger.debug(
        f"Parsing live option chain data for symbol: {symbol}, expiry_date: {expiry_date}, mode: {oi_mode}"
    )
    payload = get_nse_option_chain(symbol, expiry_date).json()
    if oi_mode == "compact":
        col_names = [
            "Fetch_Time",
            "Symbol",
            "Expiry_Date",
            "CALLS_OI",
            "CALLS_Chng_in_OI",
            "CALLS_Volume",
            "CALLS_IV",
            "CALLS_LTP",
            "CALLS_Net_Chng",
            "Strike_Price",
            "PUTS_OI",
            "PUTS_Chng_in_OI",
            "PUTS_Volume",
            "PUTS_IV",
            "PUTS_LTP",
            "PUTS_Net_Chng",
        ]
    else:
        col_names = [
            "Fetch_Time",
            "Symbol",
            "Expiry_Date",
            "CALLS_OI",
            "CALLS_Chng_in_OI",
            "CALLS_Volume",
            "CALLS_IV",
            "CALLS_LTP",
            "CALLS_Net_Chng",
            "CALLS_Bid_Qty",
            "CALLS_Bid_Price",
            "CALLS_Ask_Price",
            "CALLS_Ask_Qty",
            "Strike_Price",
            "PUTS_Bid_Qty",
            "PUTS_Bid_Price",
            "PUTS_Ask_Price",
            "PUTS_Ask_Qty",
            "PUTS_Net_Chng",
            "PUTS_LTP",
            "PUTS_IV",
            "PUTS_Volume",
            "PUTS_Chng_in_OI",
            "PUTS_OI",
        ]

    oi_data = pd.DataFrame(columns=col_names)

    oi_row = {
        "Fetch_Time": None,
        "Symbol": None,
        "Expiry_Date": None,
        "CALLS_OI": 0,
        "CALLS_Chng_in_OI": 0,
        "CALLS_Volume": 0,
        "CALLS_IV": 0,
        "CALLS_LTP": 0,
        "CALLS_Net_Chng": 0,
        "CALLS_Bid_Qty": 0,
        "CALLS_Bid_Price": 0,
        "CALLS_Ask_Price": 0,
        "CALLS_Ask_Qty": 0,
        "Strike_Price": 0,
        "PUTS_OI": 0,
        "PUTS_Chng_in_OI": 0,
        "PUTS_Volume": 0,
        "PUTS_IV": 0,
        "PUTS_LTP": 0,
        "PUTS_Net_Chng": 0,
        "PUTS_Bid_Qty": 0,
        "PUTS_Bid_Price": 0,
        "PUTS_Ask_Price": 0,
        "PUTS_Ask_Qty": 0,
    }

    # print(expiry_date)
    for m in range(len(payload["records"]["data"])):
        if not expiry_date or (
            payload["records"]["data"][m]["expiryDates"] == expiry_date
        ):
            try:
                oi_row["Expiry_Date"] = payload["records"]["data"][m]["expiryDates"]
                oi_row["CALLS_OI"] = payload["records"]["data"][m]["CE"]["openInterest"]
                oi_row["CALLS_Chng_in_OI"] = payload["records"]["data"][m]["CE"][
                    "changeinOpenInterest"
                ]
                oi_row["CALLS_Volume"] = payload["records"]["data"][m]["CE"][
                    "totalTradedVolume"
                ]
                oi_row["CALLS_IV"] = payload["records"]["data"][m]["CE"][
                    "impliedVolatility"
                ]
                oi_row["CALLS_LTP"] = payload["records"]["data"][m]["CE"]["lastPrice"]
                oi_row["CALLS_Net_Chng"] = payload["records"]["data"][m]["CE"]["change"]
                if oi_mode == "full":
                    oi_row["CALLS_Bid_Qty"] = payload["records"]["data"][m]["CE"][
                        "buyQuantity1"
                    ]
                    oi_row["CALLS_Bid_Price"] = payload["records"]["data"][m]["CE"][
                        "buyPrice1"
                    ]
                    oi_row["CALLS_Ask_Price"] = payload["records"]["data"][m]["CE"][
                        "sellPrice1"
                    ]
                    oi_row["CALLS_Ask_Qty"] = payload["records"]["data"][m]["CE"][
                        "sellQuantity1"
                    ]
            except KeyError:
                (
                    oi_row["CALLS_OI"],
                    oi_row["CALLS_Chng_in_OI"],
                    oi_row["CALLS_Volume"],
                    oi_row["CALLS_IV"],
                    oi_row["CALLS_LTP"],
                    oi_row["CALLS_Net_Chng"],
                ) = 0, 0, 0, 0, 0, 0
                if oi_mode == "full":
                    (
                        oi_row["CALLS_Bid_Qty"],
                        oi_row["CALLS_Bid_Price"],
                        oi_row["CALLS_Ask_Price"],
                        oi_row["CALLS_Ask_Qty"],
                    ) = 0, 0, 0, 0
                pass

            oi_row["Strike_Price"] = payload["records"]["data"][m]["strikePrice"]

            try:
                oi_row["PUTS_OI"] = payload["records"]["data"][m]["PE"]["openInterest"]
                oi_row["PUTS_Chng_in_OI"] = payload["records"]["data"][m]["PE"][
                    "changeinOpenInterest"
                ]
                oi_row["PUTS_Volume"] = payload["records"]["data"][m]["PE"][
                    "totalTradedVolume"
                ]
                oi_row["PUTS_IV"] = payload["records"]["data"][m]["PE"][
                    "impliedVolatility"
                ]
                oi_row["PUTS_LTP"] = payload["records"]["data"][m]["PE"]["lastPrice"]
                oi_row["PUTS_Net_Chng"] = payload["records"]["data"][m]["PE"]["change"]
                if oi_mode == "full":
                    oi_row["PUTS_Bid_Qty"] = payload["records"]["data"][m]["PE"][
                        "buyQuantity1"
                    ]
                    oi_row["PUTS_Bid_Price"] = payload["records"]["data"][m]["PE"][
                        "buyPrice1"
                    ]
                    oi_row["PUTS_Ask_Price"] = payload["records"]["data"][m]["PE"][
                        "sellPrice1"
                    ]
                    oi_row["PUTS_Ask_Qty"] = payload["records"]["data"][m]["PE"][
                        "sellQuantity1"
                    ]
            except KeyError:
                (
                    oi_row["PUTS_OI"],
                    oi_row["PUTS_Chng_in_OI"],
                    oi_row["PUTS_Volume"],
                    oi_row["PUTS_IV"],
                    oi_row["PUTS_LTP"],
                    oi_row["PUTS_Net_Chng"],
                ) = 0, 0, 0, 0, 0, 0
                if oi_mode == "full":
                    (
                        oi_row["PUTS_Bid_Qty"],
                        oi_row["PUTS_Bid_Price"],
                        oi_row["PUTS_Ask_Price"],
                        oi_row["PUTS_Ask_Qty"],
                    ) = 0, 0, 0, 0

            # if oi_mode == 'full':
            #     oi_row['CALLS_Chart'], oi_row['PUTS_Chart'] = 0, 0
            if oi_data.empty:
                oi_data = pd.DataFrame([oi_row]).copy()
            else:
                oi_data = pd.concat(
                    [oi_data, pd.DataFrame([oi_row])], ignore_index=True
                )
            oi_data["Symbol"] = symbol
            oi_data["Fetch_Time"] = payload["records"]["timestamp"]
    return oi_data


def fno_security_in_ban_period(trade_date: str) -> list:
    """
    Fetch the list of securities which are banned from the F&O segment for a given trade date.

    Args:
        trade_date (str): The trade date in 'dd-mm-YYYY' format (e.g., '20-06-2023').

    Returns:
        list: A list of security symbols currently in the ban period.

    Example:
        >>> from nselib import derivatives
        >>> banned_securities = derivatives.fno_security_in_ban_period(trade_date='26-03-2025')
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    logger.debug(
        f"Fetching F&O securities in ban period for trade date: {trade_date.strftime('%d-%m-%Y')}"
    )
    url = "https://nsearchives.nseindia.com/archives/fo/sec_ban/fo_secban_"
    payload = f"{str(trade_date.strftime('%d%m%Y'))}.csv"
    request = nse_urlfetch(url + payload)
    securities = []
    if request.status_code == 200:
        lines = request.content.decode("utf-8").strip().split("\n")
        securities = [line.split(",")[1] for line in lines[1:]]
    elif request.status_code == 403:
        url2 = (
            "https://www.nseindia.com/api/reports?archives="
            "%5B%7B%22name%22%3A%22F%26O%20-%20Security%20in%20ban%20period%22%2C%22type%22%3A%22archives%22%2C%22category%22"
            f"%3A%22derivatives%22%2C%22section%22%3A%22equity%22%7D%5D&date={str(trade_date.strftime('%d-%b-%Y'))}"
            f"&type=equity&mode=single"
        )
        request = nse_urlfetch(url2)
        if request.status_code == 200:
            lines = request.content.decode("utf-8").strip().split("\n")
            securities = [line.split(",")[1] for line in lines[1:]]
        elif request.status_code == 403:
            logger.error(
                f"F&O ban period data not found for {trade_date.strftime('%d-%m-%Y')}"
            )
            raise NSEdataNotFound("Data not found, change the date...")
    logger.debug(f"Successfully retrieved {len(securities)} securities in ban period.")
    return securities


def live_most_active_underlying() -> pd.DataFrame:
    """
    Fetch the most active underlyings in the live market.
    Note: After market hours, this will return data based on the last traded values.
    Source: https://www.nseindia.com/market-data/most-active-underlying

    Returns:
        pd.DataFrame: A DataFrame of the most active underlying assets.

    Raises:
        NSEdataNotFound: If the API resource is unavailable.

    Example:
        >>> from nselib import derivatives
        >>> df = derivatives.live_most_active_underlying()
    """
    origin_url = "https://www.nseindia.com/market-data/most-active-underlying"
    url = "https://www.nseindia.com/api/live-analysis-most-active-underlying"
    logger.debug("Fetching most active underlyings in live market.")
    try:
        data_json = nse_urlfetch(url, origin_url=origin_url).json()
        data_df = pd.DataFrame(data_json["data"])
    except Exception as e:
        logger.error("Failed to fetch live most active underlyings", exc_info=e)
        raise NSEApiError(f"Resource not available MSG: {e}")
    logger.debug(
        f"Successfully retrieved {len(data_df)} records for most active underlyings."
    )
    return data_df


def _normalize_business_growth_fo_segment_financial_year(from_year, to_year):
    if to_year is None and from_year is not None and "-" in str(from_year):
        from_year, to_year = [part.strip() for part in str(from_year).split("-", 1)]
    if from_year is None or to_year is None:
        raise NSEdataNotFound(
            "For monthly data provide from_year and to_year, e.g. from_year='2025', to_year='2026'"
        )
    return str(from_year).strip(), str(to_year).strip()


def _normalize_business_growth_fo_segment_daily_args(month, year):
    if year is None and month is not None and "-" in str(month):
        month, year = [part.strip() for part in str(month).split("-", 1)]
    if month is None or year is None:
        raise NSEdataNotFound(
            "For daily data provide month and year, e.g. month='Mar', year='2026'"
        )

    month = str(month).strip()
    try:
        month = datetime.strptime(month[:3].title(), "%b").strftime("%b")
    except ValueError as exc:
        raise NSEdataNotFound(
            "Month should be a valid month name like 'Mar' or 'March'"
        ) from exc

    year = str(year).strip()
    if len(year) == 2 and year.isdigit():
        year = f"20{year}"
    return month, year


def _business_growth_fo_segment_dataframe(data_json):
    records = [row.get("data", row) for row in data_json.get("data", [])]
    data_df = pd.DataFrame(records)
    if data_df.empty:
        return data_df

    data_df = data_df.replace({r"\r": ""}, regex=True)
    preserve_columns = {"type", "TYPE", "date"}
    null_map = {
        "": np.nan,
        "-": np.nan,
        "--": np.nan,
        "None": np.nan,
        "nan": np.nan,
        "NaN": np.nan,
    }

    for column_name in data_df.columns:
        if column_name in preserve_columns:
            continue
        if pd.api.types.is_datetime64_any_dtype(data_df[column_name]):
            continue
        cleaned_series = (
            data_df[column_name]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        normalized_series = cleaned_series.replace(null_map)
        numeric_series = pd.to_numeric(normalized_series, errors="coerce")
        if numeric_series.notna().sum() == normalized_series.notna().sum():
            data_df[column_name] = numeric_series
        else:
            data_df[column_name] = normalized_series

    meta_keys = [key for key in data_json.keys() if key != "data"]
    if meta_keys:
        data_df.attrs["metadata"] = {key: data_json[key] for key in meta_keys}
    return data_df


def business_growth_fo_segment(
    data_type: str = "yearly",
    from_year: str = None,
    to_year: str = None,
    month: str = None,
    year: str = None,
):
    """
    Fetch historical business growth data for the NSE F&O segment.

    Args:
        data_type (str): The frequency of data to fetch. Must be one of {'yearly', 'monthly', 'daily'}. Defaults to 'yearly'.
        from_year (str): Required for monthly data. The starting year of the financial year (e.g., '2025' for FY 2025-2026).
        to_year (str): Required for monthly data. The ending year of the financial year (e.g., '2026' for FY 2025-2026).
        month (str): Required for daily data. The 3-letter abbreviated month name (e.g., 'Mar', 'March', or 'Mar-26').
        year (str): Required for daily data. The 4-digit or 2-digit year (e.g., '2026' or '26').

    Returns:
        pandas.DataFrame: A DataFrame containing the historical business growth F&O data.

    Raises:
        ValueError: If the required parameters for the specified `data_type` are missing or improperly formatted.

    Example:
        >>> from nselib import derivatives
        >>> df_yearly = derivatives.business_growth_fo_segment(data_type='yearly')
        >>> df_monthly = derivatives.business_growth_fo_segment(data_type='monthly', from_year='2025', to_year='2026')
    """
    logger.debug(
        f"Fetching historical business growth data for F&O segment, frequency: {data_type}"
    )
    static_options_list = ["yearly", "monthly", "daily"]
    validate_param_from_list(data_type, static_options_list)

    if data_type == "yearly":
        data_json = get_business_growth_fo_segment_yearly()
    elif data_type == "monthly":
        from_year, to_year = _normalize_business_growth_fo_segment_financial_year(
            from_year, to_year
        )
        data_json = get_business_growth_fo_segment_monthly(
            from_year=from_year, to_year=to_year
        )
    else:
        month, year = _normalize_business_growth_fo_segment_daily_args(month, year)
        data_json = get_business_growth_fo_segment_daily(month=month, year=year)

    return _business_growth_fo_segment_dataframe(data_json)


# if __name__ == '__main__':
# df = future_price_volume_data("BANKNIFTY", "FUTIDX", from_date='01-11-2025', to_date='08-12-2025', period='6M')
# df = option_price_volume_data('NIFTY', 'OPTIDX', period='1W')
# df = nse_live_option_chain(symbol='TCS', expiry_date='02-01-2026')
# df = fii_derivatives_statistics(trade_date='16-09-2024')
# df = participant_wise_trading_volume(trade_date='16-09-2024')
# df = fno_security_in_ban_period(trade_date='26-03-2025')
# df = expiry_dates_option_index()
# df = expiry_dates_future()
# df = fno_bhav_copy('17-02-2025')
# df = live_most_active_underlying()
# df = category_turnover_fo(trade_date='16-09-2025')
# df = business_growth_fo_segment(data_type='yearly')
# df = business_growth_fo_segment(data_type='monthly', from_year='2025', to_year='2026')
# df = business_growth_fo_segment(data_type='daily', month='Mar', year='2026')
# print(df)
# print(df.columns)
# print(df[df['EXPIRY_DT']=='27-Jul-2023'])
