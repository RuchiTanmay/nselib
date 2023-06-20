import pandas as pd
import datetime as dt
import time
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
    # print(from_date, to_date)
    data_df = pd.DataFrame()
    url = "https://www.nseindia.com/api/historical/securityArchives?"
    payload = f"from={from_date}&to={to_date}&symbol={symbol}&dataType=priceVolumeDeliverable&series=ALL&csv=true"
    data_text = nse_urlfetch(url + payload).text
    data_text = data_text.replace('\x82', '').replace('â¹', 'In Rs')
    with open('file.csv', 'w') as f:
        f.write(data_text)
    f.close()
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
    # print(from_date, to_date)
    url = "https://www.nseindia.com/api/historical/securityArchives?"
    payload = f"from={from_date}&to={to_date}&symbol={symbol}&dataType=priceVolume&series=ALL&csv=true"
    data_text = nse_urlfetch(url + payload).text
    with open('file.csv', 'w') as f:
        f.write(data_text)
    f.close()
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
    # print(from_date, to_date)
    url = "https://www.nseindia.com/api/historical/securityArchives?"
    payload = f"from={from_date}&to={to_date}&symbol={symbol}&dataType=deliverable&series=ALL&csv=true"
    data_text = nse_urlfetch(url + payload).text
    # data_text = data_text.replace('\x82','').replace('â¹', 'In Rs')
    with open('file.csv', 'w') as f:
        f.write(data_text)
    f.close()
    data_df = pd.read_csv('file.csv')
    data_df.columns = [name.replace(' ', '') for name in data_df.columns]
    return data_df


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


def bhav_copy(trade_date: str):
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


def equity_list():
    data_df = pd.read_csv("https://archives.nseindia.com/content/equities/EQUITY_L.csv")
    data_df = data_df[['SYMBOL', 'NAME OF COMPANY', ' SERIES', ' DATE OF LISTING', ' FACE VALUE']]
    return data_df


def fno_equity_list():
    data_df = pd.read_csv("https://archives.nseindia.com/content/fo/fo_mktlots.csv", skiprows=5)
    today = dt.date.today()
    MMM_YY = today.strftime(mmm_yy).upper()
    data_df.rename(columns={'Derivatives on Individual Securities': 'Company_Name'}, inplace=True)
    data_df.columns = [name.replace('    ', '').replace(' ', '') for name in data_df.columns]
    data_df = data_df[['Company_Name', 'Symbol', f'{MMM_YY}']]
    return data_df


def nifty50_equity_list():
    data_df = pd.read_csv("https://archives.nseindia.com/content/indices/ind_nifty50list.csv")
    data_df = data_df[['Company Name', 'Industry', 'Symbol']]
    return data_df


# if __name__ == '__main__':
#     import nselib
#     data = nselib.trading_holiday_calendar()
#     print(data)
