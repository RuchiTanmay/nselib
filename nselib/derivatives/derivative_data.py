import pandas as pd
import datetime as dt
import time
import zipfile
from io import BytesIO, StringIO
from nselib.libutil import *
from nselib.constants import *


def future_price_volume_data(symbol: str, instrument: str, from_date: str = None, to_date: str = None,
                             period: str = None):
    """
    get contract wise future price volume data set.
    :param instrument:  FUTIDX/FUTSTK
    :param symbol: symbol eg: 'SBIN' / 'BANKNIFTY'
    :param from_date: '17-03-2022' ('dd-mm-YYYY')
    :param to_date: '17-06-2023' ('dd-mm-YYYY')
    :param period: use one {'1D': last day data,
                            '1W': for last 7 days data,
                            '1M': from last month same date,
                            '3M': last 3 month data
                            '6M': last 6 month data}
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    validate_date_param(from_date, to_date, period)

    if instrument not in ['FUTIDX', 'FUTSTK']:
        raise ValueError(f'{instrument} is not a future instrument')

    from_date, to_date = derive_from_and_to_date(from_date=from_date, to_date=to_date, period=period)
    nse_df = pd.DataFrame(columns=future_price_volume_data_column)
    from_date = datetime.strptime(from_date, dd_mm_yyyy)
    to_date = datetime.strptime(to_date, dd_mm_yyyy)
    load_days = (to_date - from_date).days
    while load_days > 0:
        if load_days > 90:
            end_date = (from_date + dt.timedelta(90)).strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        else:
            end_date = to_date.strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        data_df = get_future_price_volume_data(symbol=symbol, instrument=instrument,
                                               from_date=start_date, to_date=end_date)
        from_date = from_date + dt.timedelta(91)
        load_days = (to_date - from_date).days
        nse_df = pd.concat([nse_df, data_df], ignore_index=True)
    return nse_df


def get_future_price_volume_data(symbol: str, instrument: str, from_date: str, to_date: str):
    # print(from_date, to_date)
    data_df = pd.DataFrame()
    url = "https://www.nseindia.com/api/historical/foCPV?"
    payload = f"from={from_date}&to={to_date}&instrumentType={instrument}&symbol={symbol}&csv=true"
    try:
        data_dict = nse_urlfetch(url + payload).json()
    except Exception as e:
        raise ValueError(" Invalid parameters ")
    data_df = pd.DataFrame(data_dict['data']).drop(columns='TIMESTAMP')
    data_df.columns = cleaning_column_name(data_df.columns)
    return data_df[future_price_volume_data_column]


def option_price_volume_data(symbol: str, instrument: str, option_type: str = None, from_date: str = None,
                             to_date: str = None, period: str = None):
    """
    get contract wise option price volume data set. more than 90 days will take more time to collect data.
    :param option_type: PE/CE
    :param instrument:  OPTIDX/OPTSTK
    :param symbol: symbol eg: 'SBIN' / 'BANKNIFTY'
    :param from_date: '17-03-2022' ('dd-mm-YYYY')
    :param to_date: '17-06-2023' ('dd-mm-YYYY')
    :param period: use one {'1D': last day data,
                            '1W': for last 7 days data,
                            '1M': from last month same date,
                            '3M': last 3 month data
                            '6M': last 6 month data}
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    validate_date_param(from_date, to_date, period)

    if instrument not in ['OPTIDX', 'OPTSTK']:
        raise ValueError(f'{instrument} is not a future instrument')

    if option_type and option_type not in ['PE', 'CE']:
        raise ValueError(f'{option_type} is not a valid option type')

    option_type = [option_type] if option_type else ['PE', 'CE']
    from_date, to_date = derive_from_and_to_date(from_date=from_date, to_date=to_date, period=period)
    nse_df = pd.DataFrame(columns=future_price_volume_data_column)
    from_date = datetime.strptime(from_date, dd_mm_yyyy)
    to_date = datetime.strptime(to_date, dd_mm_yyyy)
    load_days = (to_date - from_date).days
    while load_days > 0:
        if load_days > 90:
            end_date = (from_date + dt.timedelta(90)).strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        else:
            end_date = to_date.strftime(dd_mm_yyyy)
            start_date = from_date.strftime(dd_mm_yyyy)
        for opt_typ in option_type:
            data_df = get_option_price_volume_data(symbol=symbol, instrument=instrument, option_type=opt_typ,
                                                   from_date=start_date, to_date=end_date)
            nse_df = pd.concat([nse_df, data_df], ignore_index=True)
        from_date = from_date + dt.timedelta(91)
        load_days = (to_date - from_date).days

    return nse_df


def get_option_price_volume_data(symbol: str, instrument: str, option_type: str, from_date: str, to_date: str):
    data_df = pd.DataFrame()
    url = "https://www.nseindia.com/api/historical/foCPV?"
    payload = f"from={from_date}&to={to_date}&instrumentType={instrument}&symbol={symbol}" \
              f"&optionType={option_type}&csv=true"
    try:
        data_dict = nse_urlfetch(url + payload).json()
    except Exception as e:
        raise ValueError(" Invalid parameters ")
    data_df = pd.DataFrame(data_dict['data']).drop(columns='TIMESTAMP')
    data_df.columns = cleaning_column_name(data_df.columns)
    # print(data_df.columns)
    return data_df[future_price_volume_data_column]


def fno_bhav_copy(trade_date: str):
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    url = 'https://archives.nseindia.com/content/historical/DERIVATIVES/'
    payload = f"{str(trade_date.strftime('%Y'))}/{str(trade_date.strftime('%b').upper())}/" \
              f"fo{str(trade_date.strftime('%d%b%Y').upper())}bhav.csv.zip"
    request_bhav = nse_urlfetch(url + payload)
    bhav_df = pd.DataFrame()
    if request_bhav.status_code == 200:
        zip_bhav = zipfile.ZipFile(BytesIO(request_bhav.content), 'r')
        for file_name in zip_bhav.filelist:
            if file_name:
                bhav_df = pd.read_csv(zip_bhav.open(file_name))
    elif request_bhav.status_code == 403:
        raise FileNotFoundError(f' Data not found, change the date...')
    bhav_df = bhav_df[['INSTRUMENT', 'SYMBOL', 'EXPIRY_DT', 'STRIKE_PR', 'OPTION_TYP', 'OPEN', 'HIGH', 'LOW',
                       'CLOSE', 'SETTLE_PR', 'CONTRACTS', 'VAL_INLAKH', 'OPEN_INT', 'CHG_IN_OI', 'TIMESTAMP']]
    return bhav_df


def participant_wise_open_interest(trade_date: str):
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    raw_data = pd.DataFrame()
    url = f"https://archives.nseindia.com/content/nsccl/fao_participant_oi_{str(trade_date.strftime('%d%m%Y'))}.csv"
    # payload = f"{str(for_date.strftime('%d%m%Y'))}.csv"
    file_chk = requests.get(url, headers=header)
    if file_chk.status_code != 200:
        raise FileNotFoundError(f" No data available for : {trade_date}")
    try:
        data_df = pd.read_csv(url, engine='python', sep=',', quotechar='"', on_bad_lines='skip', skiprows=1,
                              skipfooter=1)
    except:
        data_df = pd.read_csv(url, engine='c', sep=',', quotechar='"', on_bad_lines='skip', skiprows=1)
        data_df.drop(data_df.tail(1).index, inplace=True)
        data_df.columns = [name.replace('\t', '') for name in data_df.columns]
    return data_df


def participant_wise_trading_volume(trade_date: str):
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    raw_data = pd.DataFrame()
    url = f"https://archives.nseindia.com/content/nsccl/fao_participant_vol_{str(trade_date.strftime('%d%m%Y'))}.csv"
    # payload = f"{str(for_date.strftime('%d%m%Y'))}.csv"
    file_chk = requests.get(url, headers=header)
    if file_chk.status_code != 200:
        raise FileNotFoundError(f" No data available for : {trade_date}")
    try:
        data_df = pd.read_csv(url, engine='python', sep=',', quotechar='"', on_bad_lines='skip', skiprows=1,
                              skipfooter=1)
    except Exception:
        data_df = pd.read_csv(url, engine='c', sep=',', quotechar='"', on_bad_lines='skip', skiprows=1)
        data_df.drop(data_df.tail(1).index, inplace=True)
        data_df.columns = [name.replace('\t', '') for name in data_df.columns]
    return data_df


# if __name__ == '__main__':
#     df = future_price_volume_data("BANKNIFTY", "FUTIDX", from_date='17-06-2023', to_date='19-06-2023', period='1D')
#     # df = participant_wise_trading_volume(trade_date='03-04-2023')
#     print(df)
#     print(df[df['EXPIRY_DT']=='27-Jul-2023'])
