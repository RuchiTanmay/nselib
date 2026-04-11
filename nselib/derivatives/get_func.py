from io import BytesIO, StringIO
import json
from nselib.libutil import *
from nselib.constants import *


def get_future_price_volume_data(symbol: str, instrument: str, from_date: str, to_date: str):
    origin_url = "https://www.nseindia.com/report-detail/fo_eq_security"
    url = "https://www.nseindia.com/api/historicalOR/foCPV?"
    payload = f"from={from_date}&to={to_date}&instrumentType={instrument}&symbol={symbol}&csv=true"
    try:
        data_dict = nse_urlfetch(url + payload, origin_url=origin_url).json()
    except Exception as e:
        raise ValueError(f" Invalid parameters : NSE error:{e}")
    data_df = pd.DataFrame(data_dict['data'])
    data_df.columns = cleaning_column_name(data_df.columns)
    return data_df


def get_option_price_volume_data(symbol: str, instrument: str, option_type: str, from_date: str, to_date: str):
    origin_url = "https://www.nseindia.com/report-detail/fo_eq_security"
    url = "https://www.nseindia.com/api/historicalOR/foCPV?"
    payload = f"from={from_date}&to={to_date}&instrumentType={instrument}&symbol={symbol}" \
              f"&optionType={option_type}&csv=true"
    try:
        data_dict = nse_urlfetch(url + payload, origin_url=origin_url).json()
    except Exception as e:
        raise ValueError(f" Invalid parameters : NSE error : {e}")
    data_df = pd.DataFrame(data_dict['data'])
    if data_df.empty:
        raise ValueError(f"Invalid parameters, Please change the parameters")
    data_df.columns = cleaning_column_name(data_df.columns)
    return data_df[future_price_volume_data_column]


def get_nse_option_chain(symbol: str, expiry_date: str):
    """
    get NSE option chain for the symbol
    :param expiry_date: in 'DD-MMM-YYYY' format eg='25-Dec-2025'
    :param symbol: eg:'TCS'/'BANKNIFTY'
    :return: pandas dataframe
    """
    symbol = cleaning_nse_symbol(symbol)
    origin_url = "https://www.nseindia.com/option-chain"

    if any(x in symbol for x in indices_list):
        url = f'https://www.nseindia.com/api/option-chain-v3?type=Indices&symbol={symbol}&expiry={expiry_date}'
    else:
        url = f'https://www.nseindia.com/api/option-chain-v3?type=Equity&symbol={symbol}&expiry={expiry_date}'
    payload = nse_urlfetch(url, origin_url=origin_url)
    return payload


def _get_business_growth_fo_segment_data(api_path: str):
    origin_url = "https://www.nseindia.com/market-data/business-growth-fo-segment"
    url = f"https://www.nseindia.com{api_path}"
    try:
        r_session = requests.session()
        r_session.trust_env = False
        nse_live = r_session.get(origin_url, headers=default_header)
        cookies = nse_live.cookies
        data_json = r_session.get(url, headers=header, cookies=cookies).json()
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    return data_json


def get_business_growth_fo_segment_yearly():
    return _get_business_growth_fo_segment_data("/api/historicalOR/fo/tbg/yearly")


def get_business_growth_fo_segment_monthly(from_year: str, to_year: str):
    return _get_business_growth_fo_segment_data(
        f"/api/historicalOR/fo/tbg/monthly?from={from_year}&to={to_year}"
    )


def get_business_growth_fo_segment_daily(month: str, year: str):
    return _get_business_growth_fo_segment_data(
        f"/api/historicalOR/fo/tbg/daily?month={month}&year={year}"
    )



