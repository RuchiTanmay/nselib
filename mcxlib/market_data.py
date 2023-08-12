from mcxlib.libutil import *


def get_live_market_watch():
    url="https://www.mcxindia.com/backpage.aspx/GetMarketWatch"
    try:
        data_dict = requests.post(url, headers=header).json()
    except Exception as e:
        raise ValueError(f" Invalid parameters : MCX error:{e}")
    data_df = pd.DataFrame(data_dict)
    return data_df


def get_live_heat_map():
    url="https://www.mcxindia.com/backpage.aspx/GetHeatMap"
    try:
        data_dict = requests.post(url, headers=header).json()
    except Exception as e:
        raise ValueError(f" Invalid parameters : MCX error:{e}")
    data_df = pd.DataFrame(data_dict)
    return data_df


def get_live_top_gainers():
    url = "https://www.mcxindia.com/backpage.aspx/GetGainer"
    try:
        data_dict = requests.post(url, headers=header).json()
    except Exception as e:
        raise ValueError(f" Invalid parameters : MCX error:{e}")
    data_df = pd.DataFrame(data_dict)
    return data_df


def get_live_top_losers():
    url = "https://www.mcxindia.com/backpage.aspx/GetLosers"
    try:
        data_dict = requests.post(url, headers=header).json()
    except Exception as e:
        raise ValueError(f" Invalid parameters : MCX error:{e}")
    data_df = pd.DataFrame(data_dict)
    return data_df


def get_live_most_active_contracts(instrument:str = 'ALL'):
    url = "https://www.mcxindia.com/backpage.aspx/GetMostActiveContractByValueFilter"
    payload = {
        "InstrumentType": instrument
    }
    try:
        data_dict = requests.post(url, headers=header, params=payload).json()
    except Exception as e:
        raise ValueError(f" Invalid parameters : MCX error:{e}")
    data_df = pd.DataFrame(data_dict)
    return data_df


def get_live_most_active_puts_calls(option_type:str = 'PE', product:str = 'ALL', instrument:str = 'OPTFUT'):
    url="https://www.mcxindia.com/backpage.aspx/GetMostActiveOptionsContractsByVolume"
    payload = {
        "OptionType":option_type,
        "Product":product,
        "InstrumentType":instrument
    }
    try:
        data_dict = requests.post(url, headers=header, params=payload).json()
    except Exception as e:
        raise ValueError(f" Invalid parameters : MCX error:{e}")
    data_df = pd.DataFrame(data_dict)
    return data_df


def get_bhav_copy(trade_date:str = '20230101', instrument:str = 'ALL'):
    url="https://www.mcxindia.com/backpage.aspx/GetDateWiseBhavCopy"
    payload = {
        "Date":trade_date,
        "InstrumentName":instrument
    }
    try:
        data_dict = requests.post(url, headers=header, params=payload).json()
    except Exception as e:
        raise ValueError(f" Invalid parameters : MCX error:{e}")
    data_df = pd.DataFrame(data_dict)
    return data_df


def get_historical_data(group_by:str = 'D',  instrument:str = 'ALL', segment:str = 'ALL', commodity:str = 'ALL',
                        commodity_head:str = 'ALL', start_date:str = '20230101', end_date:str = '20230103',):
    url="https://www.mcxindia.com/backpage.aspx/GetHistoricalDataDetails"
    payload = {
        "Commodity":commodity,
        "CommodityHead":commodity_head,
        "EndDate":end_date,
        "GroupBy":group_by,
        "InstrumentName":instrument,
        "Segment":segment,
        "Startdate":start_date
    }
    try:
        data_dict = requests.post(url, headers=header, params=payload).json()
    except Exception as e:
        raise ValueError(f" Invalid parameters : MCX error:{e}")
    data_df = pd.DataFrame(data_dict)
    return data_df


def get_pro_cli_details(group_by:str = 'D', segment:str = 'ALL', commodity:str = 'ALL',
                        commodity_head:str = 'ALL', trade_date:str = '20230101'):
    url="https://www.mcxindia.com/backpage.aspx/GetPROClientDetailsSegmentWise"
    payload = {
        "Commodity":commodity,
        "CommodityHead":commodity_head,
        "GroupBy":group_by,
        "Segment":segment,
        "Startdate":trade_date
    }
    try:
        data_dict = requests.post(url, headers=header, params=payload).json()
    except Exception as e:
        raise ValueError(f" Invalid parameters : MCX error:{e}")
    data_df = pd.DataFrame(data_dict)
    return data_df


def get_option_chain(commodity:str = 'CRUDEOIL', expiry:str = '17AUG2023'):
    url="https://www.mcxindia.com/backpage.aspx/GetOptionChain"
    payload = {
        "Commodity":commodity,
        "Expiry":expiry
    }
    try:
        data_dict = requests.post(url, headers=header, params=payload).json()
    except Exception as e:
        raise ValueError(f" Invalid parameters : MCX error:{e}")
    data_df = pd.DataFrame(data_dict)
    return data_df


def get_put_call_ratio():
    url="https://www.mcxindia.com/backpage.aspx/GetExpirywisePutCallRatio"
    try:
        data_dict = requests.post(url, headers=header).json()
    except Exception as e:
        raise ValueError(f" Invalid parameters : MCX error:{e}")
    data_df = pd.DataFrame(data_dict)
    return data_df


def get_category_wise_oi(year:str = '2023', month:str = 'June'):
    url="https://www.mcxindia.com/docs/default-source/market-data/historicaldata/2023/july/category-wise-oi-jul-2023.xlsx"
    data_df = pd.read_excel(url)
    return data_df


def get_category_wise_turnover(year:str = '2023', month:str = 'June'):
    url="https://www.mcxindia.com/docs/default-source/market-data/historicaldata/2023/june/" \
        "category-wise-turnover-jun-2023.xlsx"
    data_df = pd.read_excel(url)
    return data_df


if __name__ == '__main__':
    df = get_live_market_watch()
    print(df)


