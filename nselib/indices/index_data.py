from io import BytesIO
from nselib.indices import nse_config as conf
from nselib.libutil import nse_urlfetch
import pandas as pd
from nselib.errors import (
    InvalidIndexCategoryError,
    InvalidIndexError,
    IndexDataNotFound,
    NSEApiError,
)
import logging

logger = logging.getLogger(__name__)


def get_class(index_category: str) -> str:
    """
    Retrieve the configuration class for a given NSE index category.

    Args:
        index_category (str): The category of the index (e.g., 'BroadMarketIndices').

    Returns:
        class: The configuration class containing indices and URLs for the specified category.

    Raises:
        InvalidIndexCategoryError: If the provided index category does not exist.

    Example:
        >>> from nselib import indices
        >>> config_class = indices.index_data.get_class('BroadMarketIndices')
    """
    category = f"Nifty{index_category}"
    category_class = getattr(conf, category, None)

    if not category_class:
        raise InvalidIndexCategoryError(f"'{category}': is an invalid Index Category")

    return category_class


def index_list(index_category: str = "BroadMarketIndices") -> list:
    """
    Fetch the list of available NSE indices for a specific index category.

    The National Stock Exchange (NSE) classifies indices into four main categories:
    - SectoralIndices
    - BroadMarketIndices
    - ThematicIndices
    - StrategyIndices

    Reference: https://www.nseindia.com/static/products-services/about-indices

    Args:
        index_category (str): The category of indices to fetch. Defaults to 'BroadMarketIndices'.

    Returns:
        list: A list of index names belonging to the specified category.

    Example:
        >>> from nselib import indices
        >>> list_of_indices = indices.index_list('BroadMarketIndices')
    """
    return get_class(index_category).indices_list


def validate_index_category(index_category: str = "BroadMarketIndices") -> bool:
    """
    Validate if a given index category is supported by the NSE.

    Args:
        index_category (str): The category string to validate.

    Raises:
        InvalidIndexCategoryError: If the category is not one of the standardized NSE categories.

    Example:
        >>> from nselib import indices
        >>> is_valid = indices.index_data.validate_index_category('SectoralIndices')
    """
    category_list = [
        "SectoralIndices",
        "BroadMarketIndices",
        "ThematicIndices",
        "StrategyIndices",
    ]
    if index_category not in category_list:
        print(f"Valid Index Categories: {category_list}")
        raise InvalidIndexCategoryError(
            f"'{index_category}': is an invalid Index Category"
        )

    return True


def validate_index_name(
    index_category: str = "BroadMarketIndices", index_name: str = "Nifty 50"
) -> bool:
    """
    Validate if a given index name exists within a specified index category.

    Args:
        index_category (str): The category of the index. Defaults to 'BroadMarketIndices'.
        index_name (str): The name of the index to validate. Defaults to 'Nifty 50'.

    Raises:
        InvalidIndexError: If the index name is not found in the given category.

    Example:
        >>> from nselib import indices
        >>> is_valid = indices.index_data.validate_index_name('BroadMarketIndices', 'NIFTY 50')
    """
    validate_index_category(index_category)
    ind_list = index_list(index_category)
    if index_name not in ind_list:
        print(f"Valid Index Names: {ind_list}")
        raise InvalidIndexError(f"'{index_name}' is invalid index_name.")

    return True


def constituent_stock_list(
    index_category: str = "BroadMarketIndices", index_name: str = "Nifty 50"
) -> pd.DataFrame:
    """
    Retrieve the list of constituent stocks for a specific NSE index.

    Fetches the current composition of the requested index as a pandas DataFrame.
    It also prints a link to the index's official fact-sheet for more details.

    Args:
        index_category (str): The category of the index. Defaults to 'BroadMarketIndices'.
        index_name (str): The specific name of the index. Defaults to 'Nifty 50'.

    Returns:
        pandas.DataFrame: A DataFrame containing the constituent stocks and their details.

    Raises:
        InvalidIndexError: If the index category or name is invalid.
        IndexDataNotFound: If the data for the index is unavailable or fails to download.

    Example:
        >>> from nselib import indices
        >>> df = indices.constituent_stock_list('BroadMarketIndices', 'NIFTY 50')
    """
    logger.debug(f"Fetching constituent stock list for index_name: {index_name} in category: {index_category}")
    validate_index_name(index_category, index_name)
    url = get_class(index_category).index_constituent_list_urls[index_name]
    if not url:
        raise IndexDataNotFound(f"'{index_name}': No Data found for index")

    response = nse_urlfetch(url)
    if response.status_code == 200:
        stocks_df = pd.read_csv(BytesIO(response.content))
    else:
        raise IndexDataNotFound(
            f"'{index_name}': No Data found for index, Kindly check the "
            "index category & name"
        )

    url_fs = get_class(index_category).index_factsheet_urls[index_name]
    print(
        f" Note: For more detail information related to {index_name}. "
        f"Please check the Fact Sheet - {url_fs}"
    )
    return stocks_df


def live_index_performances() -> pd.DataFrame:
    """
    Fetch the live or last traded performance data for all NSE indices.

    During market hours, this returns live data. After market hours, it returns
    the final index performance data for the day.

    Data Source: https://www.nseindia.com/market-data/index-performances

    Returns:
        pandas.DataFrame: A DataFrame containing performance metrics for all indices.

    Raises:
        NSEApiError: If the NSE API is unreachable or returns an error.

    Example:
        >>> from nselib import indices
        >>> df = indices.live_index_performances()
    """
    logger.debug("Fetching live index performances for all indices")
    origin_url = "https://www.nseindia.com/market-data/index-performances"
    url = f"https://www.nseindia.com/api/allIndices"
    try:
        data_json = nse_urlfetch(url, origin_url=origin_url).json()
        data_df = pd.DataFrame(data_json["data"])
    except Exception as e:
        print(f"NSE Resource not available: {e}")
        raise NSEApiError(f" Resource not available MSG: {e}")

    data_df.drop(
        columns=["chartTodayPath", "chart30dPath", "chart365dPath"], inplace=True
    )
    return data_df


# if __name__ == '__main__':

# data = constituent_stock_list(index_category='BroadMarketIndices', index_name='Nifty 50')
# data = live_index_performances()
# print(data)
