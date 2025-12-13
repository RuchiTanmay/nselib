from io import BytesIO
from nselib.libutil import *
import config as conf
import pandas as pd


def get_class(index_category: str):
    category = f"Nifty{index_category}"
    category_class = getattr(conf, category, None)

    if category_class is None:
        raise ValueError(f"No such category in config: {category}")
    return category_class


def index_list(index_category: str = 'BroadMarketIndices'):
    """
     to get the available NSE indices for each category of indices. there ar 4 category defined by NSE link as below
     https://www.nseindia.com/static/products-services/about-indices..
    :param index_category: SectoralIndices/ BroadMarketIndices/ ThematicIndices/ StrategyIndices
    :return: list
    """
    return get_class(index_category).indices_list


def validate_index_category(index_category: str = 'BroadMarketIndices'):
    category_list = ['SectoralIndices', 'BroadMarketIndices', 'ThematicIndices', 'StrategyIndices']
    if index_category in category_list:
        pass
    else:
        raise ValueError(f'{index_category} is not a valid index_category:: please select category_list from list :  {category_list}')


def validate_index_name(index_category: str = 'BroadMarketIndices', index_name: str = 'Nifty 50'):
    validate_index_category(index_category)
    ind_list = index_list(index_category)
    if index_name in ind_list:
        pass
    else:
        raise ValueError(f'{index_name} is not a valid index_name:: please select index name from list :  {ind_list}')


def constituent_stock_list(index_category: str = 'BroadMarketIndices', index_name: str = 'Nifty 50'):
    """
    to get list of all that stocks constituent with the given index and index_category.
    :param index_category: SectoralIndices/ BroadMarketIndices/ ThematicIndices/ StrategyIndices
    :param index_name: select name of index from the index list provided by get_index_list
    :return: pandas.DataFrame
    :raise ValueError if the parameter input is not proper
    """
    validate_index_name(index_category, index_name)
    url = get_class(index_category).index_constituent_list_urls[index_name]
    if not url:
        raise FileNotFoundError(f' Data not found for index {index_name}')
    response = nse_urlfetch(url)
    if response.status_code == 200:
        stocks_df = pd.read_csv(BytesIO(response.content))
    else:
        raise FileNotFoundError(f' Data not found, check index_name or index_category ...')
    url_fs = get_class(index_category).index_factsheet_urls[index_name]
    print(f" Note: For more detail information related to {index_name} Please check the Fact Sheet - {url_fs}")
    return stocks_df


def live_index_performances():
    """
    to get index performances in live market, after market hour it will get as per last traded value
    link : https://www.nseindia.com/market-data/index-performances
    :return:
    """
    origin_url = "https://www.nseindia.com/market-data/index-performances"
    url = f"https://www.nseindia.com/api/allIndices"
    try:
        data_json = nse_urlfetch(url, origin_url=origin_url).json()
        data_df = pd.DataFrame(data_json['data'])
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    data_df.drop(columns=['chartTodayPath', 'chart30dPath', 'chart365dPath'], inplace=True)
    return data_df


# if __name__ == '__main__':

    # data = constituent_stock_list(index_category='BroadMarketIndices', index_name='Nifty  50')
    # data = live_index_performances()
    # print(data)
