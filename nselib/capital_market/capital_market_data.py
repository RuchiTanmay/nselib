import pandas as pd
import datetime as dt
import zipfile
from io import BytesIO, StringIO
from nselib.libutil import *
from nselib.constants import *


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
        nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def get_price_volume_and_deliverable_position_data(symbol: str, from_date: str, to_date: str):
    url = "https://www.nseindia.com/api/historical/securityArchives?"
    payload = f"from={from_date}&to={to_date}&symbol={symbol}&dataType=priceVolumeDeliverable&series=ALL&csv=true"
    try:
        data_text = nse_urlfetch(url + payload).text
        data_text = data_text.replace('\x82', '').replace('â¹', 'In Rs')
        with open('file.csv', 'w') as f:
            f.write(data_text)
        f.close()
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    data_df = pd.read_csv('file.csv')
    data_df.columns = [name.replace(' ', '') for name in data_df.columns]
    return data_df


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
        nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def get_price_volume_data(symbol: str, from_date: str, to_date: str):
    url = "https://www.nseindia.com/api/historical/securityArchives?"
    payload = f"from={from_date}&to={to_date}&symbol={symbol}&dataType=priceVolume&series=ALL&csv=true"
    try:
        data_text = nse_urlfetch(url + payload).text
        with open('file.csv', 'w') as f:
            f.write(data_text)
        f.close()
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    data_df = pd.read_csv('file.csv')
    data_df.columns = [name.replace(' ', '') for name in data_df.columns]
    return data_df


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
        data_df = get_price_volume_data(symbol=symbol, from_date=start_date, to_date=end_date)
        from_date = from_date + dt.timedelta(365)
        load_days = (to_date - from_date).days
        nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def get_deliverable_position_data(symbol: str, from_date: str, to_date: str):
    url = "https://www.nseindia.com/api/historical/securityArchives?"
    payload = f"from={from_date}&to={to_date}&symbol={symbol}&dataType=deliverable&series=ALL&csv=true"
    try:
        data_text = nse_urlfetch(url + payload).text
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    # data_text = data_text.replace('\x82','').replace('â¹', 'In Rs')
    with open('file.csv', 'w') as f:
        f.write(data_text)
    f.close()
    data_df = pd.read_csv('file.csv')
    data_df.columns = [name.replace(' ', '') for name in data_df.columns]
    return data_df


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
        nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def get_india_vix_data(from_date: str, to_date: str):
    url = f"https://www.nseindia.com/api/historical/vixhistory?from={from_date}&to={to_date}&csv=true"
    try:
        data_json = nse_urlfetch(url).json()
        data_df = pd.DataFrame(data_json['data'])
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    data_df.drop(columns='TIMESTAMP', inplace=True)
    data_df.columns = cleaning_column_name(data_df.columns)
    return data_df[india_vix_data_column]


def index_data(index:str, from_date: str = None, to_date: str = None, period: str = None):
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
    nse_df = pd.DataFrame(columns=index_data_columns)
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
        nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def get_index_data(index:str, from_date: str, to_date: str):
    index = index.replace(' ', '%20').upper()
    url = f"https://www.nseindia.com/api/historical/indicesHistory?indexType={index}&from={from_date}&to={to_date}"
    try:
        data_json = nse_urlfetch(url).json()
        data_close_df = pd.DataFrame(data_json['data']['indexCloseOnlineRecords']).drop(columns=['_id', "EOD_TIMESTAMP"])
        data_turnover_df = pd.DataFrame(data_json['data']['indexTurnoverRecords']).drop(columns=['_id',
                                                                                                 'HIT_INDEX_NAME_UPPER'])
        data_df = pd.merge(data_close_df,data_turnover_df, on='TIMESTAMP', how='inner')
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    data_df.drop(columns='TIMESTAMP', inplace=True)
    data_df.columns = cleaning_column_name(data_df.columns)
    return data_df[index_data_columns]


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
        nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def get_bulk_deal_data(from_date: str, to_date: str):
    # print(from_date, to_date)
    url = "https://www.nseindia.com/api/historical/bulk-deals?"
    payload = f"from={from_date}&to={to_date}&csv=true"
    data_text = nse_urlfetch(url + payload).text
    # data_text = data_text.replace('\x82','').replace('â¹', 'In Rs')
    with open('file.csv', 'w') as f:
        f.write(data_text)
    f.close()
    data_df = pd.read_csv('file.csv')
    data_df.columns = [name.replace(' ', '') for name in data_df.columns]
    return data_df


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
        nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def get_block_deals_data(from_date: str, to_date: str):
    # print(from_date, to_date)
    url = "https://www.nseindia.com/api/historical/block-deals?"
    payload = f"from={from_date}&to={to_date}&csv=true"
    data_text = nse_urlfetch(url + payload).text
    # data_text = data_text.replace('\x82','').replace('â¹', 'In Rs')
    with open('file.csv', 'w') as f:
        f.write(data_text)
    f.close()
    data_df = pd.read_csv('file.csv')
    data_df.columns = [name.replace(' ', '') for name in data_df.columns]
    return data_df


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
        nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def get_short_selling_data(from_date: str, to_date: str):
    """
    NSE short selling data in data frame
    :param from_date:
    :param to_date:
    :return:
    """
    # print(from_date, to_date)
    url = "https://www.nseindia.com/api/historical/short-selling?"
    payload = f"from={from_date}&to={to_date}&csv=true"
    data_text = nse_urlfetch(url + payload).text
    # data_text = data_text.replace('\x82','').replace('â¹', 'In Rs')
    with open('file.csv', 'w') as f:
        f.write(data_text)
    f.close()
    data_df = pd.read_csv('file.csv')
    data_df.columns = [name.replace(' ', '') for name in data_df.columns]
    return data_df


def bhav_copy_with_delivery(trade_date: str):
    """
    get the NSE bhav copy with delivery data as per the traded date
    :param trade_date: eg:'01-06-2023'
    :return: pandas data frame
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    use_date = trade_date.strftime(ddmmyyyy)
    url = f'https://archives.nseindia.com/products/content/sec_bhavdata_full_{use_date}.csv'
    request_bhav = nse_urlfetch(url)
    bhav_df = pd.DataFrame()
    if request_bhav.status_code == 200:
        bhav_df = pd.read_csv(StringIO(request_bhav.text), sep=', ', engine='python')
    elif request_bhav.status_code == 403:
        raise FileNotFoundError(f' Data not found, change the date...')
    return bhav_df[['SYMBOL', 'SERIES', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE',
                    'PREV_CLOSE', 'TTL_TRD_QNTY', 'TURNOVER_LACS', 'NO_OF_TRADES', 'DELIV_QTY',
                    'DELIV_PER', 'DATE1']]


def bhav_copy_equities(trade_date: str):
    """
    get nse bhav copy as per the traded date provided
    :param trade_date:
    :return: pandas dataframe
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    url = 'https://archives.nseindia.com/content/historical/EQUITIES/'
    payload = f"{str(trade_date.strftime('%Y'))}/{str(trade_date.strftime('%b').upper())}/" \
              f"cm{str(trade_date.strftime('%d%b%Y').upper())}bhav.csv.zip"
    request_bhav = nse_urlfetch(url + payload)
    bhav_df = pd.DataFrame()
    if request_bhav.status_code == 200:
        zip_bhav = zipfile.ZipFile(BytesIO(request_bhav.content), 'r')
        for file_name in zip_bhav.filelist:
            if file_name:
                bhav_df = pd.read_csv(zip_bhav.open(file_name))
    elif request_bhav.status_code == 403:
        raise FileNotFoundError(f' Data not found, change the date...')
    bhav_df = bhav_df[['SYMBOL', 'SERIES', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST', 'PREVCLOSE', 'TOTTRDQTY',
                       'TOTTRDVAL', 'TIMESTAMP', 'TOTALTRADES']]
    return bhav_df


def bhav_copy_indices(trade_date: str):
    """
    get nse bhav copy as per the traded date provided
    :param trade_date: eg:'01-06-2023'
    :return: pandas dataframe
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    url = f"https://archives.nseindia.com/content/indices/ind_close_all_{str(trade_date.strftime('%d%m%Y').upper())}.csv"
    try:
        bhav_df = pd.read_csv(url)
    except Exception as e:
        raise FileNotFoundError(f' Bhav copy indices not found for : {trade_date} :: NSE error : {e}')
    return bhav_df


def equity_list():
    """
    get list of all equity available to trade in NSE
    :return: pandas data frame
    """
    try:
        data_df = pd.read_csv("https://archives.nseindia.com/content/equities/EQUITY_L.csv")
    except Exception as e:
        raise FileNotFoundError(f' Equity List not found :: NSE error : {e}')
    data_df = data_df[['SYMBOL', 'NAME OF COMPANY', ' SERIES', ' DATE OF LISTING', ' FACE VALUE']]
    return data_df


def fno_equity_list():
    """
    get a dataframe of all listed derivative list with the recent lot size to trade
    :return: pandas data frame
    """
    today = dt.date.today()
    MMM_YY = today.strftime(mmm_yy).upper()
    try:
        ind_data_df = pd.read_csv("https://archives.nseindia.com/content/fo/fo_mktlots.csv")
        data_df = pd.read_csv("https://archives.nseindia.com/content/fo/fo_mktlots.csv", skiprows=5)
    except Exception as e:
        raise FileNotFoundError(f' all listed derivative List not found :: NSE error : {e}')

    ind_data_df.columns = [name.replace('    ', '').replace(' ', '') for name in ind_data_df.columns]
    ind_data_df = ind_data_df[['UNDERLYING', 'SYMBOL', f'{MMM_YY}']].head(4)
    ind_data_df.columns = ['Company_Name', 'Symbol', f'{MMM_YY}']
    data_df.rename(columns={'Derivatives on Individual Securities': 'Company_Name'}, inplace=True)
    data_df.columns = [name.replace('    ', '').replace(' ', '') for name in data_df.columns]
    data_df = data_df[['Company_Name', 'Symbol', f'{MMM_YY}']]
    data_df = pd.concat([ind_data_df, data_df], ignore_index=True)
    return data_df


def nifty50_equity_list():
    """
    list of all equities under NIFTY 50 index
    :return: pandas data frame
    """
    try:
        data_df = pd.read_csv("https://archives.nseindia.com/content/indices/ind_nifty50list.csv")
    except Exception as e:
        raise FileNotFoundError(f' equities under NIFTY 50 index not found :: NSE error : {e}')
    data_df = data_df[['Company Name', 'Industry', 'Symbol']]
    return data_df


def market_watch_all_indices():
    """
    Market Watch - Indices of the day in data frame
    :return: pd.DataFrame
    """
    url = "https://www.nseindia.com/api/allIndices"
    data_json = nse_urlfetch(url).json()
    data_df = pd.DataFrame(data_json['data'])
    return data_df[['key', 'index', 'indexSymbol', 'last', 'variation', 'percentChange', 'open', 'high', 'low',
                   'previousClose', 'yearHigh', 'yearLow', 'pe', 'pb', 'dy', 'declines', 'advances', 'unchanged',
                   'perChange365d', 'perChange30d', 'previousDay', 'oneWeekAgo', 'oneMonthAgo', 'oneYearAgo']]


def fii_dii_trading_activity():
    """
    FII and DII trading activity of the day in data frame
    :return: pd.DataFrame
    """
    url = "https://www.nseindia.com/api/fiidiiTradeReact"
    data_json = nse_urlfetch(url).json()
    data_df = pd.DataFrame(data_json)
    return data_df


# if __name__ == '__main__':
    # import nselib.capital_market as cm
    # data = fii_dii_trading_activity()
    # print(data)
    # print(data.columns)
    # data = fno_equity_list()  #from_date='23-03-2022', to_date='23-06-2023'

