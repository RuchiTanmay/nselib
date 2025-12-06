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


def get_index_list(index_category: str = 'BroadMarketIndices'):
    """
     to get the available NSE indices for each category of indices. there ar 4 category defined by NSE link as below
     https://www.nseindia.com/static/products-services/about-indices..
    :param index_category: SectoralIndices/ BroadMarketIndices/ ThematicIndices/ StrategyIndices
    :return: list
    """
    return get_class(index_category).indices_list


def get_constituent_stock_list(index_category: str = 'BroadMarketIndices', index_name: str = 'Nifty 50'):
    """
    to get list of all that stocks constituent with the given index and index_category.
    :param index_category: SectoralIndices/ BroadMarketIndices/ ThematicIndices/ StrategyIndices
    :param index_name: select name of index from the index list provided by get_index_list
    :return: pandas.DataFrame
    """
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


# if __name__ == '__main__':
#
#     data = get_constituent_stock_list(index_category='BroadMarketIndices', index_name='Nifty 50')
#     print(data)
