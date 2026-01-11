import datetime as dt
import zipfile
import xml.etree.ElementTree as ET
from nselib.capital_market.get_func import *


# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("urllib3").setLevel(logging.WARNING)


def price_volume_and_deliverable_position_data(symbol: str, from_date: str = None, to_date: str = None,
                                               period: str = None):
    """
    get Security wise price volume & Deliverable position data set. use get_nse_symbols() to get all symbols
    :param symbol: symbol eg: 'SBIN'
    :param from_date: '17-03-2022' ('dd-mm-YYYY')
    :param to_date: '17-06-2023' ('dd-mm-YYYY')
    :param period: use one {'1D': last day data,'1W': for last 7 days data,
                            '1M': from last month same date, '6M': last 6 month data, '1Y': from last year same date)
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    validate_date_param(from_date, to_date, period)
    symbol = cleaning_nse_symbol(symbol=symbol)
    from_date, to_date = derive_from_and_to_date(from_date=from_date, to_date=to_date, period=period)
    nse_df = pd.DataFrame(columns=price_volume_and_deliverable_position_data_columns)
    from_date = datetime.strptime(from_date, dd_mm_yyyy)
    to_date = datetime.strptime(to_date, dd_mm_yyyy)
    load_days = (to_date - from_date).days
    while load_days > 0:
        if load_days > 365:
            end_date = (from_date + dt.timedelta(364)).strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        else:
            end_date = to_date.strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        data_df = get_price_volume_and_deliverable_position_data(symbol=symbol, from_date=start_date, to_date=end_date)
        from_date = from_date + dt.timedelta(365)
        load_days = (to_date - from_date).days
        if not data_df.empty:
            # Drop all-NaN columns from both frames
            data_df = data_df.fillna('-')
            nse_df = nse_df.fillna('-')
            data_df = data_df.dropna(axis=1, how='all')
            nse_df = nse_df.dropna(axis=1, how='all')
            if not data_df.empty:
                nse_df = pd.concat([nse_df, data_df], ignore_index=True)

    nse_df["TotalTradedQuantity"] = pd.to_numeric(nse_df["TotalTradedQuantity"].astype(str).str.replace(",", ""), errors="coerce")
    nse_df["TurnoverInRs"] = pd.to_numeric(nse_df["TurnoverInRs"].astype(str).str.replace(",", ""), errors="coerce")
    nse_df["No.ofTrades"] = pd.to_numeric(nse_df["No.ofTrades"].astype(str).str.replace(",", ""), errors="coerce")
    nse_df["DeliverableQty"] = pd.to_numeric(nse_df["DeliverableQty"].astype(str).str.replace(",", ""), errors="coerce")
    return nse_df


def price_volume_data(symbol: str, from_date: str = None, to_date: str = None, period: str = None):
    """
    get Security wise price volume data set.
    :param symbol: symbol eg: 'SBIN'
    :param from_date: '17-03-2022' ('dd-mm-YYYY')
    :param to_date: '17-06-2023' ('dd-mm-YYYY')
    :param period: use one {'1D': last day data,'1W': for last 7 days data,
                            '1M': from last month same date, '6M': last 6 month data, '1Y': from last year same date)
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    validate_date_param(from_date, to_date, period)
    symbol = cleaning_nse_symbol(symbol=symbol)
    from_date, to_date = derive_from_and_to_date(from_date=from_date, to_date=to_date, period=period)
    nse_df = pd.DataFrame(columns=price_volume_data_columns)
    from_date = datetime.strptime(from_date, dd_mm_yyyy)
    to_date = datetime.strptime(to_date, dd_mm_yyyy)
    load_days = (to_date - from_date).days
    while load_days > 0:
        if load_days > 365:
            end_date = (from_date + dt.timedelta(364)).strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        else:
            end_date = to_date.strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        data_df = get_price_volume_data(symbol=symbol, from_date=start_date, to_date=end_date)
        from_date = from_date + dt.timedelta(365)
        load_days = (to_date - from_date).days
        if nse_df.empty:
            nse_df = data_df
        else:
            nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def deliverable_position_data(symbol: str, from_date: str = None, to_date: str = None, period: str = None):
    """
    get Security wise deliverable position data set.
    :param symbol: symbol eg: 'SBIN'
    :param from_date: '17-03-2022' ('dd-mm-YYYY')
    :param to_date: '17-06-2023' ('dd-mm-YYYY')
    :param period: use one {'1D': last day data,
                            '1W': for last 7 days data,
                            '1M': from last month same date,
                            '6M': last 6 month data,
                            '1Y': from last year same date)
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    validate_date_param(from_date, to_date, period)
    symbol = cleaning_nse_symbol(symbol=symbol)
    from_date, to_date = derive_from_and_to_date(from_date=from_date, to_date=to_date, period=period)
    nse_df = pd.DataFrame(columns=deliverable_data_columns)
    from_date = datetime.strptime(from_date, dd_mm_yyyy)
    to_date = datetime.strptime(to_date, dd_mm_yyyy)
    load_days = (to_date - from_date).days
    while load_days > 0:
        if load_days > 365:
            end_date = (from_date + dt.timedelta(364)).strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        else:
            end_date = to_date.strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        data_df = get_deliverable_position_data(symbol=symbol, from_date=start_date, to_date=end_date)
        from_date = from_date + dt.timedelta(365)
        load_days = (to_date - from_date).days
        if nse_df.empty:
            nse_df = data_df
        else:
            nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def india_vix_data(from_date: str = None, to_date: str = None, period: str = None):
    """
    get india vix spot data  set for the specific time period.
    :param from_date: '17-03-2022' ('dd-mm-YYYY')
    :param to_date: '17-06-2023' ('dd-mm-YYYY')
    :param period: use one {'1D': last day data,'1W': for last 7 days data,
                            '1M': from last month same date, '6M': last 6 month data, '1Y': from last year same date)
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    validate_date_param(from_date, to_date, period)
    from_date, to_date = derive_from_and_to_date(from_date=from_date, to_date=to_date, period=period)
    nse_df = pd.DataFrame(columns=india_vix_data_column)
    from_date = datetime.strptime(from_date, dd_mm_yyyy)
    to_date = datetime.strptime(to_date, dd_mm_yyyy)
    load_days = (to_date - from_date).days
    while load_days > 0:
        if load_days > 365:
            end_date = (from_date + dt.timedelta(364)).strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        else:
            end_date = to_date.strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        data_df = get_india_vix_data(from_date=start_date, to_date=end_date)
        from_date = from_date + dt.timedelta(365)
        load_days = (to_date - from_date).days
        if nse_df.empty:
            nse_df = data_df
        else:
            nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def index_data(index: str, from_date: str = None, to_date: str = None, period: str = None):
    """
    get historical index data set for the specific time period.
    apply the index name as per the nse india site
    :param index: 'NIFTY 50'/'NIFTY BANK'
    :param from_date: '17-03-2022' ('dd-mm-YYYY')
    :param to_date: '17-06-2023' ('dd-mm-YYYY')
    :param period: use one {'1D': last day data,'1W': for last 7 days data,
                            '1M': from last month same date, '6M': last 6 month data, '1Y': from last year same date)
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    validate_date_param(from_date, to_date, period)
    from_date, to_date = derive_from_and_to_date(from_date=from_date, to_date=to_date, period=period)
    nse_df = pd.DataFrame()
    from_date = datetime.strptime(from_date, dd_mm_yyyy)
    to_date = datetime.strptime(to_date, dd_mm_yyyy)
    load_days = (to_date - from_date).days
    while load_days > 0:
        if load_days > 365:
            end_date = (from_date + dt.timedelta(364)).strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        else:
            end_date = to_date.strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        data_df = get_index_data(index=index, from_date=start_date, to_date=end_date)
        from_date = from_date + dt.timedelta(365)
        load_days = (to_date - from_date).days
        if nse_df.empty:
            nse_df = data_df
        else:
            nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def bulk_deal_data(from_date: str = None, to_date: str = None, period: str = None):
    """
    get bulk deal data set.
    :param from_date: '17-03-2022' ('dd-mm-YYYY')
    :param to_date: '17-06-2023' ('dd-mm-YYYY')
    :param period: use one {'1D': last day data,
                            '1W': for last 7 days data,
                            '1M': from last month same date,
                            '6M': last 6 month data,
                            '1Y': from last year same date)
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    validate_date_param(from_date, to_date, period)
    from_date, to_date = derive_from_and_to_date(from_date=from_date, to_date=to_date, period=period)
    nse_df = pd.DataFrame(columns=bulk_deal_data_columns)
    from_date = datetime.strptime(from_date, dd_mm_yyyy)
    to_date = datetime.strptime(to_date, dd_mm_yyyy)
    load_days = (to_date - from_date).days
    while load_days > 0:
        if load_days > 365:
            end_date = (from_date + dt.timedelta(364)).strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        else:
            end_date = to_date.strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        data_df = get_bulk_deal_data(from_date=start_date, to_date=end_date)
        from_date = from_date + dt.timedelta(365)
        load_days = (to_date - from_date).days
        if nse_df.empty:
            nse_df = data_df
        else:
            nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def block_deals_data(from_date: str = None, to_date: str = None, period: str = None):
    """
    get block deals data set.
    :param from_date: '17-03-2022' ('dd-mm-YYYY')
    :param to_date: '17-06-2023' ('dd-mm-YYYY')
    :param period: use one {'1D': last day data,
                            '1W': for last 7 days data,
                            '1M': from last month same date,
                            '6M': last 6 month data,
                            '1Y': from last year same date)
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    validate_date_param(from_date, to_date, period)
    from_date, to_date = derive_from_and_to_date(from_date=from_date, to_date=to_date, period=period)
    nse_df = pd.DataFrame(columns=block_deals_data_columns)
    from_date = datetime.strptime(from_date, dd_mm_yyyy)
    to_date = datetime.strptime(to_date, dd_mm_yyyy)
    load_days = (to_date - from_date).days
    while load_days > 0:
        if load_days > 365:
            end_date = (from_date + dt.timedelta(364)).strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        else:
            end_date = to_date.strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        data_df = get_block_deals_data(from_date=start_date, to_date=end_date)
        from_date = from_date + dt.timedelta(365)
        load_days = (to_date - from_date).days
        if nse_df.empty:
            nse_df = data_df
        else:
            nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def short_selling_data(from_date: str = None, to_date: str = None, period: str = None):
    """
    get short selling data set.
    :param from_date: '17-03-2022' ('dd-mm-YYYY')
    :param to_date: '17-06-2023' ('dd-mm-YYYY')
    :param period: use one {'1D': last day data,
                            '1W': for last 7 days data,
                            '1M': from last month same date,
                            '6M': last 6 month data,
                            '1Y': from last year same date)
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    validate_date_param(from_date, to_date, period)
    from_date, to_date = derive_from_and_to_date(from_date=from_date, to_date=to_date, period=period)
    nse_df = pd.DataFrame(columns=short_selling_data_columns)
    from_date = datetime.strptime(from_date, dd_mm_yyyy)
    to_date = datetime.strptime(to_date, dd_mm_yyyy)
    load_days = (to_date - from_date).days
    while load_days > 0:
        if load_days > 365:
            end_date = (from_date + dt.timedelta(364)).strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        else:
            end_date = to_date.strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        data_df = get_short_selling_data(from_date=start_date, to_date=end_date)
        from_date = from_date + dt.timedelta(365)
        load_days = (to_date - from_date).days
        if nse_df.empty:
            nse_df = data_df
        else:
            nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def bhav_copy_with_delivery(trade_date: str):
    """
    get the NSE bhav copy with delivery data as per the traded date
    :param trade_date: eg:'20-06-2023'
    :return: pandas data frame
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    use_date = trade_date.strftime(ddmmyyyy)
    url = f'https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{use_date}.csv'
    request_bhav = nse_urlfetch(url)
    if request_bhav.status_code == 200:
        bhav_df = pd.read_csv(BytesIO(request_bhav.content))
    else:
        raise FileNotFoundError(f' Data not found, change the trade_date...')
    bhav_df.columns = [name.replace(' ', '') for name in bhav_df.columns]
    bhav_df['SERIES'] = bhav_df['SERIES'].str.replace(' ', '')
    bhav_df['DATE1'] = bhav_df['DATE1'].str.replace(' ', '')
    return bhav_df


def bhav_copy_equities(trade_date: str):
    """
    get new CM-UDiFF Common Bhavcopy Final as per the traded date provided
    :param trade_date:
    :return: pandas dataframe
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    url = 'https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_'
    payload = f"{str(trade_date.strftime('%Y%m%d'))}_F_0000.csv.zip"
    request_bhav = nse_urlfetch(url + payload)
    bhav_df = pd.DataFrame()
    if request_bhav.status_code == 200:
        zip_bhav = zipfile.ZipFile(BytesIO(request_bhav.content), 'r')
        for file_name in zip_bhav.filelist:
            if file_name:
                bhav_df = pd.read_csv(zip_bhav.open(file_name))
    elif request_bhav.status_code == 403:
        raise FileNotFoundError(f' Data not found, change the trade_date...')
    # bhav_df = bhav_df[['SYMBOL', 'SERIES', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST', 'PREVCLOSE', 'TOTTRDQTY',
    #                    'TOTTRDVAL', 'TIMESTAMP', 'TOTALTRADES']]
    return bhav_df


def bhav_copy_indices(trade_date: str):
    """
    get nse bhav copy as per the traded date provided
    :param trade_date: eg:'20-06-2023'
    :return: pandas dataframe
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    url = f"https://nsearchives.nseindia.com/content/indices/ind_close_all_{str(trade_date.strftime('%d%m%Y').upper())}.csv"
    file_chk = nse_urlfetch(url)
    if file_chk.status_code != 200:
        raise FileNotFoundError(f" No data available for : {trade_date}")
    try:
        bhav_df = pd.read_csv(BytesIO(file_chk.content))
    except Exception as e:
        raise FileNotFoundError(f' Bhav copy indices not found for : {trade_date} :: NSE error : {e}')
    return bhav_df


def bhav_copy_sme(trade_date: str):
    """
    get the NSE bhav copy for SME data as per the traded date
    :param trade_date: eg:'20-06-2023'
    :return: pandas data frame
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    use_date = trade_date.strftime(ddmmyy)
    url = f'https://nsearchives.nseindia.com/archives/sme/bhavcopy/sme{use_date}.csv'
    request_bhav = nse_urlfetch(url)
    if request_bhav.status_code == 200:
        bhav_df = pd.read_csv(BytesIO(request_bhav.content))
    else:
        raise FileNotFoundError(f' Data not found, change the trade_date...')
    bhav_df.columns = [name.replace(' ', '') for name in bhav_df.columns]
    return bhav_df


def equity_list():
    """
    get list of all equity available to trade in NSE
    :return: pandas data frame
    """
    origin_url = "https://nsewebsite-staging.nseindia.com"
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    file_chk = nse_urlfetch(url, origin_url=origin_url)
    if file_chk.status_code != 200:
        raise FileNotFoundError(f" No data equity list available")
    try:
        data_df = pd.read_csv(BytesIO(file_chk.content))
    except Exception as e:
        raise FileNotFoundError(f' Equity List not found :: NSE error : {e}')
    data_df = data_df[['SYMBOL', 'NAME OF COMPANY', ' SERIES', ' DATE OF LISTING', ' FACE VALUE']]
    return data_df


def fno_equity_list():
    """
    get a dataframe of all listed derivative equity list with the recent lot size to trade
    :return: pandas data frame
    """
    origin_url = "https://www.nseindia.com/products-services/equity-derivatives-list-underlyings-information"
    url = "https://www.nseindia.com/api/underlying-information"
    data_obj = nse_urlfetch(url, origin_url=origin_url)
    if data_obj.status_code != 200:
        raise NSEdataNotFound(f" Resource not available for fno_equity_list")
    data_dict = data_obj.json()
    data_df = pd.DataFrame(data_dict['data']['UnderlyingList'])
    return data_df


def fno_index_list():
    """
    get a dataframe of all listed derivative index list with the recent lot size to trade
    :return: pandas data frame
    """
    origin_url = "https://www.nseindia.com/products-services/equity-derivatives-list-underlyings-information"
    url = "https://www.nseindia.com/api/underlying-information"
    data_obj = nse_urlfetch(url, origin_url=origin_url)
    if data_obj.status_code != 200:
        raise NSEdataNotFound(f" Resource not available for fno_equity_index_list")
    data_dict = data_obj.json()
    data_df = pd.DataFrame(data_dict['data']['IndexList'])
    return data_df


def nifty50_equity_list():
    """
    list of all equities under NIFTY 50 index
    :return: pandas data frame
    """
    url = "https://nsearchives.nseindia.com/content/indices/ind_nifty50list.csv"
    file_chk = nse_urlfetch(url)
    if file_chk.status_code != 200:
        raise FileNotFoundError(f" No data equity list available")
    try:
        data_df = pd.read_csv(BytesIO(file_chk.content))
    except Exception as e:
        raise FileNotFoundError(f' equities under NIFTY 50 index not found :: NSE error : {e}')
    data_df = data_df[['Company Name', 'Industry', 'Symbol']]
    return data_df


def niftynext50_equity_list():
    """
    list of all equities under NIFTY NEXT 50 index
    :return: pandas data frame
    """
    try:
        data_df = pd.read_csv("https://archives.nseindia.com/content/indices/ind_niftynext50list.csv")
    except Exception as e:
        raise FileNotFoundError(f' equities under NIFTY NEXT 50 index not found :: NSE error : {e}')
    data_df = data_df[['Company Name', 'Industry', 'Symbol']]
    return data_df


def niftymidcap150_equity_list():
    """
    list of all equities under NIFTY MIDCAP 150 index
    :return: pandas data frame
    """
    try:
        data_df = pd.read_csv("https://archives.nseindia.com/content/indices/ind_niftymidcap150list.csv")
    except Exception as e:
        raise FileNotFoundError(f' equities under NIFTY MIDCAP 150 index not found :: NSE error : {e}')
    data_df = data_df[['Company Name', 'Industry', 'Symbol']]
    return data_df


def niftysmallcap250_equity_list():
    """
    list of all equities under NIFTY SMALLCAP 250 index
    :return: pandas data frame
    """
    try:
        data_df = pd.read_csv("https://archives.nseindia.com/content/indices/ind_niftysmallcap250list.csv")
    except Exception as e:
        raise FileNotFoundError(f' equities under NIFTY SMALLCAP 250 index not found :: NSE error : {e}')
    data_df = data_df[['Company Name', 'Industry', 'Symbol']]
    return data_df


def market_watch_all_indices():
    """
    Market Watch - Indices of the day in data frame
    :return: pd.DataFrame
    """
    origin_url = "https://nsewebsite-staging.nseindia.com"
    url = "https://www.nseindia.com/api/allIndices"
    data_json = nse_urlfetch(url, origin_url=origin_url).json()
    data_df = pd.DataFrame(data_json['data'])
    print(data_df.columns)
    return data_df[['key', 'index', 'indexSymbol', 'last', 'variation', 'percentChange', 'open', 'high', 'low',
                    'previousClose', 'yearHigh', 'yearLow', 'pe', 'pb', 'dy', 'declines', 'advances', 'unchanged',
                    'perChange365d', 'perChange30d', 'previousDay', 'oneWeekAgoVal', 'oneMonthAgoVal', 'oneYearAgoVal']]


def fii_dii_trading_activity():
    """
    FII and DII trading activity of the day in data frame
    :return: pd.DataFrame
    """
    url = "https://www.nseindia.com/api/fiidiiTradeReact"
    data_json = nse_urlfetch(url).json()
    data_df = pd.DataFrame(data_json)
    return data_df


def var_begin_day(trade_date: str):
    """
    get the VaR Begin Day data as per the traded date
    :param trade_date: eg:'20-06-2023'
    :return: pandas data frame
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    use_date = trade_date.strftime(ddmmyyyy)
    url = f'https://nsearchives.nseindia.com/archives/nsccl/var/C_VAR1_{use_date}_1.DAT'
    request_nse = nse_urlfetch(url)
    if request_nse.status_code == 200:
        var_df = pd.read_csv(BytesIO(request_nse.content), skiprows=1)
    else:
        raise FileNotFoundError(f' Data not found, change the trade_date...')
    var_df.columns = var_columns
    return var_df


def var_1st_intra_day(trade_date: str):
    """
    get the VaR 1st Intra Day data as per the traded date
    :param trade_date: eg:'20-06-2023'
    :return: pandas data frame
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    use_date = trade_date.strftime(ddmmyyyy)
    url = f'https://nsearchives.nseindia.com/archives/nsccl/var/C_VAR1_{use_date}_2.DAT'
    request_nse = nse_urlfetch(url)
    if request_nse.status_code == 200:
        var_df = pd.read_csv(BytesIO(request_nse.content), skiprows=1)
    else:
        raise FileNotFoundError(f' Data not found, change the trade_date...')
    var_df.columns = var_columns
    return var_df


def var_2nd_intra_day(trade_date: str):
    """
    get the VaR 2nd Intra Day data as per the traded date
    :param trade_date: eg:'20-06-2023'
    :return: pandas data frame
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    use_date = trade_date.strftime(ddmmyyyy)
    url = f'https://nsearchives.nseindia.com/archives/nsccl/var/C_VAR1_{use_date}_3.DAT'
    request_nse = nse_urlfetch(url)
    if request_nse.status_code == 200:
        var_df = pd.read_csv(BytesIO(request_nse.content), skiprows=1)
    else:
        raise FileNotFoundError(f' Data not found, change the trade_date...')
    var_df.columns = var_columns
    return var_df


def var_3rd_intra_day(trade_date: str):
    """
    get the VaR 3rd Intra Day data as per the traded date
    :param trade_date: eg:'20-06-2023'
    :return: pandas data frame
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    use_date = trade_date.strftime(ddmmyyyy)
    url = f'https://nsearchives.nseindia.com/archives/nsccl/var/C_VAR1_{use_date}_4.DAT'
    request_nse = nse_urlfetch(url)
    if request_nse.status_code == 200:
        var_df = pd.read_csv(BytesIO(request_nse.content), skiprows=1)
    else:
        raise FileNotFoundError(f' Data not found, change the trade_date...')
    var_df.columns = var_columns
    return var_df


def var_4th_intra_day(trade_date: str):
    """
    get the VaR 4th Intra Day data as per the traded date
    :param trade_date: eg:'20-06-2023'
    :return: pandas data frame
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    use_date = trade_date.strftime(ddmmyyyy)
    url = f'https://nsearchives.nseindia.com/archives/nsccl/var/C_VAR1_{use_date}_5.DAT'
    request_nse = nse_urlfetch(url)
    if request_nse.status_code == 200:
        var_df = pd.read_csv(BytesIO(request_nse.content), skiprows=1)
    else:
        raise FileNotFoundError(f' Data not found, change the trade_date...')
    var_df.columns = var_columns
    return var_df


def var_end_of_day(trade_date: str):
    """
    get the VaR End of Day data as per the traded date
    :param trade_date: eg:'20-06-2023'
    :return: pandas data frame
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    use_date = trade_date.strftime(ddmmyyyy)
    url = f'https://nsearchives.nseindia.com/archives/nsccl/var/C_VAR1_{use_date}_6.DAT'
    request_nse = nse_urlfetch(url)
    if request_nse.status_code == 200:
        var_df = pd.read_csv(BytesIO(request_nse.content), skiprows=1)
    else:
        raise FileNotFoundError(f' Data not found, change the trade_date...')
    var_df.columns = var_columns
    return var_df


def sme_bhav_copy(trade_date: str):
    """
    get the SME bhav copy data as per the traded date
    :param trade_date: eg:'20-06-2023'
    :return: pandas data frame
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    use_date = trade_date.strftime(ddmmyy)
    url = f'https://nsearchives.nseindia.com/archives/sme/bhavcopy/sme{use_date}.csv'
    request_bhav = nse_urlfetch(url)
    if request_bhav.status_code == 200:
        bhav_df = pd.read_csv(BytesIO(request_bhav.content))
    else:
        raise FileNotFoundError(f' Data not found, change the trade_date...')
    bhav_df.columns = [name.replace(' ', '') for name in bhav_df.columns]
    return bhav_df


def sme_band_complete(trade_date: str):
    """
    get the SME Band Complete data as per the traded date
    :param trade_date: eg:'20-06-2023'
    :return: pandas data frame
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    use_date = trade_date.strftime(ddmmyyyy)
    url = f'https://nsearchives.nseindia.com/sme/content/price_band/archieves/sme_bands_complete_{use_date}.csv'
    request_sme = nse_urlfetch(url)
    if request_sme.status_code == 200:
        sme_df = pd.read_csv(BytesIO(request_sme.content))
    else:
        raise FileNotFoundError(f' Data not found, change the trade_date...')
    sme_df.columns = [name.replace(' ', '') for name in sme_df.columns]
    return sme_df


def week_52_high_low_report(trade_date: str):
    """
    get the 52-Week High Low Report data as per the traded date
    :param trade_date: eg:'20-06-2023'
    :return: pandas data frame
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    use_date = trade_date.strftime(ddmmyyyy)
    url = f'https://nsearchives.nseindia.com/content/CM_52_wk_High_low_{use_date}.csv'
    request_nse = nse_urlfetch(url)
    if request_nse.status_code == 200:
        high_low_df = pd.read_csv(BytesIO(request_nse.content), skiprows=2)
    else:
        raise FileNotFoundError(f' Data not found, change the trade_date...')
    high_low_df.columns = [name.replace(' ', '') for name in high_low_df.columns]
    return high_low_df


def financial_results_for_equity(from_date: str = None,
                                 to_date: str = None,
                                 period: str = None,
                                 fo_sec: bool = False,
                                 fin_period: str = 'Quarterly'):

    """
    get audited and un-auditable financial results for equities. as per
    https://www.nseindia.com/companies-listing/corporate-filings-financial-results
    :param fin_period: Quaterly/ Half-Yearly/ Annual/ Others
    :param fo_sec: True/False
    :param from_date: '17-03-2022' ('dd-mm-YYYY')
    :param to_date: '17-06-2023' ('dd-mm-YYYY')
    :param period: use one {'1D': last day data,
                            '1W': for last 7 days data,
                            '1M': from last month same date,
                            '6M': last 6 month data,
                            '1Y': from last year same date)
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    master_data_df, headers, ns, keys_to_extract = get_financial_results_master(from_date, to_date, period,
                                                                                fo_sec, fin_period)
    fin_df, df = pd.DataFrame(), pd.DataFrame()
    for row in master_data_df.itertuples(index=False):
        try:
            # Fetch the XML content
            response_ = requests.get(row.xbrl, headers=headers)
            response_.raise_for_status()  # Check for HTTP errors

            # Parse the XML content
            root = ET.fromstring(response_.content)

            # Extract values
            extracted_data = {}
            for key in keys_to_extract:
                elem_ = root.find(f".//in-bse-fin:{key}", ns)
                extracted_data[key] = elem_.text if elem_ is not None else None

            # Convert to Pandas DataFrame
            df = pd.DataFrame([extracted_data])
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Request failed: {e}") from e
        except ET.ParseError as e:
            raise ET.ParseError(f"XML parsing failed: {e}") from e
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}") from e

        if fin_df.empty:
            fin_df = df
        else:
            fin_df = pd.concat([fin_df, df], ignore_index=True)
    return fin_df


def corporate_bond_trade_report(trade_date: str):
    """
    get the NSE corporate bond trade report as per the traded date
    :param trade_date: eg:'20-06-2023'
    :return: pandas data frame
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    use_date = trade_date.strftime(ddmmyy)
    url = f'https://nsearchives.nseindia.com/archives/equities/corpbond/corpbond{use_date}.csv'
    request_bhav = nse_urlfetch(url)
    if request_bhav.status_code == 200:
        bond_df = pd.read_csv(BytesIO(request_bhav.content))
    else:
        raise FileNotFoundError(f' Data not found, change the trade_date...')
    bond_df.columns = [name.replace(' ', '') for name in bond_df.columns]
    bond_df['SERIES'] = bond_df['SERIES'].str.replace(' ', '')
    return bond_df


def pe_ratio(trade_date: str):
    """
    get the NSE pe ratio for all NSE equities data as per the traded date
    :param trade_date: eg:'20-06-2023'
    :return: pandas data frame
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    use_date = trade_date.strftime(ddmmyy)
    url = f'https://nsearchives.nseindia.com/content/equities/peDetail/PE_{use_date}.csv'
    request_bhav = nse_urlfetch(url)
    if request_bhav.status_code == 200:
        pe_df = pd.read_csv(BytesIO(request_bhav.content))
    else:
        raise FileNotFoundError(f' Data not found, change the trade_date...')
    pe_df.columns = [name.replace(' ', '') for name in pe_df.columns]
    return pe_df


def corporate_actions_for_equity(from_date: str = None,
                                 to_date: str = None,
                                 period: str = None,
                                 fno_only: bool = False):

    """
    get corporate actions for equities as per
    https://www.nseindia.com/companies-listing/corporate-filings-actions
    :param fno_only: True/False
    :param from_date: '17-03-2022' ('dd-mm-YYYY')
    :param to_date: '17-06-2023' ('dd-mm-YYYY')
    :param period: use one {'1D': last day data,
                            '1W': for last 7 days data,
                            '1M': from last month same date,
                            '6M': last 6 month data,
                            '1Y': from last year same date)
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    validate_date_param(from_date, to_date, period)
    from_date, to_date = derive_from_and_to_date(from_date=from_date, to_date=to_date, period=period)
    origin_url = "https://www.nseindia.com/companies-listing/corporate-filings-actions"
    url_ = "https://www.nseindia.com/api/corporates-corporateactions?index=equities&"
    if fno_only:
        payload = f'from_date={from_date}&to_date={to_date}&fo_sec=true'
    else:
        payload = f'from_date={from_date}&to_date={to_date}'
    data_text = nse_urlfetch(url_ + payload, origin_url=origin_url)
    if data_text.status_code != 200:
        raise NSEdataNotFound(f" Resource not available for financial data with these parameters")
    json_str = data_text.content.decode("utf-8")
    data_list = json.loads(json_str)
    master_data_df = pd.DataFrame(data_list)
    master_data_df.columns = [name.replace(' ', '') for name in master_data_df.columns]
    return master_data_df


def event_calendar_for_equity(from_date: str = None,
                              to_date: str = None,
                              period: str = None,
                              fno_only: bool = False):

    """
    get event calendar for equities as per
    https://www.nseindia.com/companies-listing/corporate-filings-event-calendar
    :param fno_only: True/False
    :param from_date: '17-03-2022' ('dd-mm-YYYY')
    :param to_date: '17-06-2023' ('dd-mm-YYYY')
    :param period: use one {'1D': last day data,
                            '1W': for last 7 days data,
                            '1M': from last month same date,
                            '6M': last 6 month data,
                            '1Y': from last year same date)
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    validate_date_param(from_date, to_date, period)
    from_date, to_date = derive_from_and_to_date(from_date=from_date, to_date=to_date, period=period)
    origin_url = "https://www.nseindia.com/companies-listing/corporate-filings-event-calendar"
    url_ = "https://www.nseindia.com/api/event-calendar?index=equities&"
    if fno_only:
        payload = f'from_date={from_date}&to_date={to_date}&fo_sec=true'
    else:
        payload = f'from_date={from_date}&to_date={to_date}'
    data_text = nse_urlfetch(url_ + payload, origin_url=origin_url)
    if data_text.status_code != 200:
        raise NSEdataNotFound(f" Resource not available for financial data with these parameters")
    json_str = data_text.content.decode("utf-8")
    data_list = json.loads(json_str)
    master_data_df = pd.DataFrame(data_list)
    master_data_df.columns = [name.replace(' ', '') for name in master_data_df.columns]
    return master_data_df


def top_gainers_or_losers(to_get: str = 'gainers'):
    """
    get top gainers or losers on live market, after market hour it will get as per last traded value
    :param to_get: gainers/loosers
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    static_options_list = ['gainers', 'loosers']
    validate_param_from_list(to_get, static_options_list)
    data_json = get_top_gainers_or_losers(to_get)
    legends_dict = {item[0]: item[1] for item in data_json['legends']}
    gainers_losers_df = pd.DataFrame()
    for i in legends_dict.keys():
        data_df = pd.DataFrame(data_json[i]['data'])
        data_df['legend'] = i
        if gainers_losers_df.empty:
            gainers_losers_df = data_df
        else:
            gainers_losers_df = pd.concat([gainers_losers_df, data_df])
    return gainers_losers_df


def most_active_equities(fetch_by: str = 'value'):
    """
    to get most active equities fetched by value/volume in live market, after market hour it will get as per last traded value
    link : https://www.nseindia.com/market-data/most-active-equities
    :param fetch_by: select any volume/value
    :return: pandas dataframe
    """
    static_options_list = ['volume', 'value']
    validate_param_from_list(fetch_by, static_options_list)
    origin_url = "https://www.nseindia.com/market-data/most-active-equities"
    url = f"https://www.nseindia.com/api/live-analysis-most-active-securities?index={fetch_by}"
    try:
        data_json = nse_urlfetch(url, origin_url=origin_url).json()
        data_df = pd.DataFrame(data_json['data'])
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    return data_df


def total_traded_stocks():
    """
    to get all total traded stocks detail in live market, after market hour it will get as per last traded value
    summary_dict - has the live market summary for the stocks in dictionary format
    detail_df - has all detail available in the current market in dataframe format
    link : https://www.nseindia.com/market-data/stocks-traded
    :return: summary_dict, detail_df
    """
    origin_url = "https://www.nseindia.com/market-data/stocks-traded"
    url = f"https://www.nseindia.com/api/live-analysis-stocksTraded"
    try:
        data_json = nse_urlfetch(url, origin_url=origin_url).json()
        summary_dict = data_json['total']['count']
        detail_df = pd.DataFrame(data_json['total']['data'])
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    return summary_dict, detail_df


# if __name__ == '__main__':
    # data = pe_ratio(trade_date='11-09-2024')  # trade_date='11-09-2024'
    # data = index_data(index='NIFTY 50', period='1W')
    # data = block_deals_data(period='1W')
    # data = bulk_deal_data(period='1W')
    # data = india_vix_data(period='1W')
    # data = short_selling_data(period='1W')
    # data = index_data(index='NIFTY 50', from_date='21-10-2024', to_date='30-10-2024')
    # data = deliverable_position_data(symbol='SBIN', from_date='23-03-2024', to_date='23-06-2024')
    # data = market_watch_all_indices()
    # data = fno_equity_list()
    # data = price_volume_and_deliverable_position_data(symbol='SBIN',  from_date='23-03-2024', to_date='23-06-2024')
    # data = price_volume_and_deliverable_position_data(symbol='SBIN', period='1M')
    # data = price_volume_data(symbol='SBIN', from_date='20-06-2023', to_date='20-07-2023')
    # data = financial_results_for_equity(from_date='11-03-2025', to_date='16-03-2025', fo_sec=True,
    #                                     fin_period='Quarterly')
    # data = corporate_actions_for_equity(period='6M', fno_only=False)
    # data = event_calendar_for_equity(period='1M', fno_only=False)
    # data = sme_band_complete(trade_date='11-03-2025')
    # data = top_gainers_or_losers('loosers')   # gainers/losers
    # data = most_active_equities(fetch_by='volume')  # value/volume
    # data = total_traded_stocks()
    # df = index_data("NIFTY 50", from_date="01-11-2024", to_date="27-12-2024")
    # print(f"Success! Got {df} rows")
    # data.to_csv(fr'C:\Ruchi Tanmay\Stock Market\Data Analysis\Final Data\data.csv')

    # data = niftymidcap150_equity_list()
    # print(data)
    # print(data.info())
    # -----------------------------------------------------

