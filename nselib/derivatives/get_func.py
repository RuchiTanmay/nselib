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



