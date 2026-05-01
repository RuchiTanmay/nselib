import json
import logging
from io import BytesIO, StringIO

import pandas as pd
import requests

from nselib.constants import india_vix_data_column, index_data_columns
from nselib.errors import NSEdataNotFound
from nselib.libutil import (
    cleaning_column_name,
    default_header,
    derive_from_and_to_date,
    header,
    nse_urlfetch,
    validate_date_param,
)

logger = logging.getLogger(__name__)


def get_price_volume_and_deliverable_position_data(
    symbol: str, from_date: str, to_date: str
) -> pd.DataFrame:
    """
    Fetch price, volume, and deliverable position data for a given symbol and date range.

    Args:
        symbol (str): The NSE symbol (e.g., 'SBIN').
        from_date (str): Start date in 'dd-mm-YYYY' format.
        to_date (str): End date in 'dd-mm-YYYY' format.

    Returns:
        pandas.DataFrame: A DataFrame containing the price, volume, and deliverable data.

    Example:
        >>> from nselib import capital_market
        >>> df = capital_market.get_func.get_price_volume_and_deliverable_position_data('SBIN', '17-03-2022', '17-06-2023')
    """
    logger.debug(
        f"Fetching price, volume and deliverable data for {symbol} from {from_date} to {to_date}"
    )
    origin_url = "https://nsewebsite-staging.nseindia.com/report-detail/eq_security"
    url = (
        "https://www.nseindia.com/api/historicalOR/generateSecurityWiseHistoricalData?"
    )
    payload = f"from={from_date}&to={to_date}&symbol={symbol}&type=priceVolumeDeliverable&series=ALL&csv=true"
    try:
        data_text = nse_urlfetch(url + payload, origin_url=origin_url).text
        data_text = data_text.replace("\x82", "").replace("â¹", "In Rs")
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}", exc_info=e)
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    data_df = pd.read_csv(StringIO(data_text))
    data_df.columns = [name.replace(" ", "") for name in data_df.columns]
    return data_df


def get_price_volume_data(symbol: str, from_date: str, to_date: str) -> pd.DataFrame:
    """
    Fetch price and volume data for a given symbol and date range.

    Args:
        symbol (str): The NSE symbol (e.g., 'SBIN').
        from_date (str): Start date in 'dd-mm-YYYY' format.
        to_date (str): End date in 'dd-mm-YYYY' format.

    Returns:
        pandas.DataFrame: A DataFrame containing the price and volume data.

    Example:
        >>> from nselib import capital_market
        >>> df = capital_market.get_func.get_price_volume_data('SBIN', '17-03-2022', '17-06-2023')
    """
    logger.debug(
        f"Fetching price and volume data for {symbol} from {from_date} to {to_date}"
    )
    origin_url = "https://nsewebsite-staging.nseindia.com/report-detail/eq_security"
    url = (
        "https://www.nseindia.com/api/historicalOR/generateSecurityWiseHistoricalData?"
    )
    payload = f"from={from_date}&to={to_date}&symbol={symbol}&type=priceVolume&series=ALL&csv=true"
    try:
        data_text = nse_urlfetch(url + payload, origin_url=origin_url)
        if data_text.status_code != 200:
            raise NSEdataNotFound(f" Resource not available for Price Volume Data")
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}", exc_info=e)
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    data_df = pd.read_csv(BytesIO(data_text.content), index_col=False)
    data_df.columns = [name.replace(" ", "") for name in data_df.columns]
    return data_df


def get_deliverable_position_data(
    symbol: str, from_date: str, to_date: str
) -> pd.DataFrame:
    """
    Fetch deliverable position data for a given symbol and date range.

    Args:
        symbol (str): The NSE symbol (e.g., 'SBIN').
        from_date (str): Start date in 'dd-mm-YYYY' format.
        to_date (str): End date in 'dd-mm-YYYY' format.

    Returns:
        pandas.DataFrame: A DataFrame containing the deliverable position data.

    Example:
        >>> from nselib import capital_market
        >>> df = capital_market.get_func.get_deliverable_position_data('SBIN', '17-03-2022', '17-06-2023')
    """
    logger.debug(
        f"Fetching deliverable position data for {symbol} from {from_date} to {to_date}"
    )
    origin_url = "https://nsewebsite-staging.nseindia.com/report-detail/eq_security"
    url = (
        "https://www.nseindia.com/api/historicalOR/generateSecurityWiseHistoricalData?"
    )
    payload = f"from={from_date}&to={to_date}&symbol={symbol}&type=deliverable&series=ALL&csv=true"
    try:
        data_text = nse_urlfetch(url + payload, origin_url=origin_url)
        if data_text.status_code != 200:
            raise NSEdataNotFound(
                "Resource not available for deliverable_position_data"
            )
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}", exc_info=e)
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    data_df = pd.read_csv(BytesIO(data_text.content), index_col=False)
    data_df.columns = [name.replace(" ", "") for name in data_df.columns]
    return data_df


def get_india_vix_data(from_date: str, to_date: str) -> pd.DataFrame:
    """
    Fetch India VIX data for a given date range.

    Args:
        from_date (str): Start date in 'dd-mm-YYYY' format.
        to_date (str): End date in 'dd-mm-YYYY' format.

    Returns:
        pandas.DataFrame: A DataFrame containing the India VIX data.

    Example:
        >>> from nselib import capital_market
        >>> df = capital_market.get_func.get_india_vix_data('17-03-2022', '17-06-2023')
    """
    logger.debug(f"Fetching India VIX data from {from_date} to {to_date}")
    origin_url = "https://nsewebsite-staging.nseindia.com/report-detail/eq_security"
    url = f"https://www.nseindia.com/api/historicalOR/vixhistory?from={from_date}&to={to_date}&csv=true"
    try:
        data_json = nse_urlfetch(url, origin_url=origin_url).json()
        data_df = pd.DataFrame(data_json["data"])
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}", exc_info=e)
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    # data_df.drop(columns='TIMESTAMP', inplace=True)
    if not data_df.empty:
        data_df.columns = cleaning_column_name(data_df.columns)
        return data_df[india_vix_data_column]
    return data_df


def get_index_data(index: str, from_date: str, to_date: str) -> pd.DataFrame:
    """
    Fetch index data for a given index and date range.

    Args:
        index (str): The index name (e.g., 'NIFTY 50').
        from_date (str): Start date in 'dd-mm-YYYY' format.
        to_date (str): End date in 'dd-mm-YYYY' format.

    Returns:
        pandas.DataFrame: A DataFrame containing the historical index data.

    Example:
        >>> from nselib import capital_market
        >>> df = capital_market.get_func.get_index_data('NIFTY 50', '17-03-2022', '17-06-2023')
    """
    logger.debug(f"Fetching index data for {index} from {from_date} to {to_date}")
    index = index.replace(" ", "%20").upper()
    origin_url = "https://www.nseindia.com/reports-indices-historical-index-data"
    url = f"https://www.nseindia.com/api/historicalOR/indicesHistory?indexType={index}&from={from_date}&to={to_date}"
    try:
        data_json = nse_urlfetch(url, origin_url=origin_url).json()
        data_df = pd.DataFrame(data_json["data"])
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}", exc_info=e)
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    if not data_df.empty:
        data_df.drop(columns="HI_TIMESTAMP", inplace=True)
        data_df.columns = index_data_columns
    return data_df


def get_bulk_deal_data(from_date: str, to_date: str) -> pd.DataFrame:
    """
    Fetch bulk deal data for a given date range.

    Args:
        from_date (str): Start date in 'dd-mm-YYYY' format.
        to_date (str): End date in 'dd-mm-YYYY' format.

    Returns:
        pandas.DataFrame: A DataFrame containing the bulk deal data.

    Example:
        >>> from nselib import capital_market
        >>> df = capital_market.get_func.get_bulk_deal_data('17-03-2022', '17-06-2023')
    """
    logger.debug(f"Fetching bulk deal data from {from_date} to {to_date}")
    origin_url = "https://nsewebsite-staging.nseindia.com"
    url = "https://www.nseindia.com/api/historicalOR/bulk-block-short-deals?optionType=bulk_deals&"
    payload = f"from={from_date}&to={to_date}&csv=true"
    data_text = nse_urlfetch(url + payload, origin_url=origin_url)
    if data_text.status_code != 200:
        raise NSEdataNotFound(f" Resource not available for bulk_deal_data")
    data_df = pd.read_csv(BytesIO(data_text.content), index_col=False)
    data_df.columns = [name.replace(" ", "") for name in data_df.columns]
    return data_df


def get_block_deals_data(from_date: str, to_date: str) -> pd.DataFrame:
    """
    Fetch block deals data for a given date range.

    Args:
        from_date (str): Start date in 'dd-mm-YYYY' format.
        to_date (str): End date in 'dd-mm-YYYY' format.

    Returns:
        pandas.DataFrame: A DataFrame containing the block deals data.

    Example:
        >>> from nselib import capital_market
        >>> df = capital_market.get_func.get_block_deals_data('17-03-2022', '17-06-2023')
    """
    logger.debug(f"Fetching block deals data from {from_date} to {to_date}")
    origin_url = "https://nsewebsite-staging.nseindia.com"
    url = "https://www.nseindia.com/api/historicalOR/bulk-block-short-deals?optionType=block_deals&"
    payload = f"from={from_date}&to={to_date}&csv=true"
    data_text = nse_urlfetch(url + payload, origin_url=origin_url)
    if data_text.status_code != 200:
        raise NSEdataNotFound(f" Resource not available for block_deals_data")
    data_df = pd.read_csv(BytesIO(data_text.content), index_col=False)
    data_df.columns = [name.replace(" ", "") for name in data_df.columns]
    return data_df


def get_short_selling_data(from_date: str, to_date: str) -> pd.DataFrame:
    """
    Fetch NSE short selling data in a data frame.

    Args:
        from_date (str): Start date in 'dd-mm-YYYY' format.
        to_date (str): End date in 'dd-mm-YYYY' format.

    Returns:
        pandas.DataFrame: A DataFrame containing the short selling data.

    Example:
        >>> from nselib import capital_market
        >>> df = capital_market.get_func.get_short_selling_data('17-03-2022', '17-06-2023')
    """
    logger.debug(f"Fetching short selling data from {from_date} to {to_date}")
    origin_url = "https://nsewebsite-staging.nseindia.com"
    url = "https://www.nseindia.com/api/historicalOR/bulk-block-short-deals?optionType=short_selling&"
    payload = f"from={from_date}&to={to_date}&csv=true"
    data_text = nse_urlfetch(url + payload, origin_url=origin_url)
    if data_text.status_code != 200:
        raise NSEdataNotFound(f" Resource not available for short_selling_data")
    data_df = pd.read_csv(BytesIO(data_text.content), index_col=False)
    data_df.columns = [name.replace(" ", "") for name in data_df.columns]
    return data_df


def _get_business_growth_cm_segment_data(api_path: str) -> dict:
    """
    Internal helper to fetch business growth CM segment data.

    Args:
        api_path (str): The specific API path to fetch.

    Returns:
        dict: Parsed JSON data.
    """
    logger.debug(f"Fetching business growth CM segment data from path: {api_path}")
    origin_url = "https://www.nseindia.com/market-data/business-growth-cm-segment"
    url = f"https://www.nseindia.com{api_path}"
    try:
        r_session = requests.session()
        r_session.trust_env = False
        nse_live = r_session.get(origin_url, headers=default_header)
        cookies = nse_live.cookies
        data_json = r_session.get(url, headers=header, cookies=cookies).json()
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}", exc_info=e)
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    return data_json


def get_business_growth_cm_segment_yearly() -> dict:
    """
    Fetch yearly business growth data for the CM segment.

    Returns:
        dict: Parsed JSON response.

    Example:
        >>> from nselib import capital_market
        >>> data = capital_market.get_func.get_business_growth_cm_segment_yearly()
    """
    logger.debug("Fetching yearly business growth CM segment data")
    return _get_business_growth_cm_segment_data("/api/historicalOR/cm/tbg/yearly")


def get_business_growth_cm_segment_monthly(from_year: str, to_year: str) -> dict:
    """
    Fetch monthly business growth data for the CM segment for a specific year range.

    Args:
        from_year (str): The starting year (e.g., '2022').
        to_year (str): The ending year (e.g., '2023').

    Returns:
        dict: Parsed JSON response.

    Example:
        >>> from nselib import capital_market
        >>> data = capital_market.get_func.get_business_growth_cm_segment_monthly('2022', '2023')
    """
    logger.debug(
        f"Fetching monthly business growth CM segment data for {from_year}-{to_year}"
    )
    return _get_business_growth_cm_segment_data(
        f"/api/historicalOR/cm/tbg/monthly?from={from_year}&to={to_year}"
    )


def get_business_growth_cm_segment_daily(month: str, year: str) -> dict:
    """
    Fetch daily business growth data for the CM segment for a specific month and year.

    Args:
        month (str): The month abbreviation (e.g., 'Mar').
        year (str): The year (e.g., '2023').

    Returns:
        dict: Parsed JSON response.

    Example:
        >>> from nselib import capital_market
        >>> data = capital_market.get_func.get_business_growth_cm_segment_daily('Mar', '2023')
    """
    logger.debug(f"Fetching daily business growth CM segment data for {month}-{year}")
    return _get_business_growth_cm_segment_data(
        f"/api/historicalOR/cm/tbg/daily?month={month}&year={year}"
    )


def get_financial_results_master(
    from_date: str = None,
    to_date: str = None,
    period: str = None,
    fo_sec: bool = False,
    fin_period: str = "Quarterly",
) -> tuple:
    """
    Fetch corporate financial results master data.

    Args:
        from_date (str, optional): Start date in 'dd-mm-YYYY' format.
        to_date (str, optional): End date in 'dd-mm-YYYY' format.
        period (str, optional): Period like '1M', '1Y'.
        fo_sec (bool, optional): Whether to fetch for F&O securities.
        fin_period (str, optional): Financial period (e.g., 'Quarterly').

    Returns:
        tuple: (master_data_df, headers, ns, keys_to_extract)

    Example:
        >>> from nselib import capital_market
        >>> master_df, hdrs, ns, keys = capital_market.get_func.get_financial_results_master(period='1M')
    """
    logger.debug(
        f"Fetching financial results master for period={period}, from={from_date}, to={to_date}"
    )
    validate_date_param(from_date, to_date, period)
    from_date, to_date = derive_from_and_to_date(
        from_date=from_date, to_date=to_date, period=period
    )
    origin_url = (
        "https://www.nseindia.com/companies-listing/corporate-filings-financial-results"
    )
    url_ = "https://www.nseindia.com/api/corporates-financial-results?index=equities&"
    if fo_sec:
        payload = (
            f"from_date={from_date}&to_date={to_date}&fo_sec=true&period={fin_period}"
        )
    else:
        payload = f"from_date={from_date}&to_date={to_date}&period={fin_period}"
    data_text = nse_urlfetch(url_ + payload, origin_url=origin_url)
    if data_text.status_code != 200:
        raise NSEdataNotFound(
            f" Resource not available for financial data with these parameters"
        )
    json_str = data_text.content.decode("utf-8")
    data_list = json.loads(json_str)
    master_data_df = pd.DataFrame(data_list)
    master_data_df.columns = [name.replace(" ", "") for name in master_data_df.columns]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/",
    }
    ns = {
        "xbrli": "http://www.xbrl.org/2003/instance",
        "in-bse-fin": "http://www.bseindia.com/xbrl/fin/2020-03-31/in-bse-fin",
    }
    keys_to_extract = [
        "ScripCode",
        "Symbol",
        "MSEISymbol",
        "NameOfTheCompany",
        "ClassOfSecurity",
        "DateOfStartOfFinancialYear",
        "DateOfEndOfFinancialYear",
        "DateOfBoardMeetingWhenFinancialResultsWereApproved",
        "DateOnWhichPriorIntimationOfTheMeetingForConsideringFinancialResultsWasInformedToTheExchange",
        "DescriptionOfPresentationCurrency",
        "LevelOfRoundingUsedInFinancialStatements",
        "ReportingQuarter",
        "StartTimeOfBoardMeeting",
        "EndTimeOfBoardMeeting",
        "DateOfStartOfBoardMeeting",
        "DateOfEndOfBoardMeeting",
        "DeclarationOfUnmodifiedOpinionOrStatementOnImpactOfAuditQualification",
        "IsCompanyReportingMultisegmentOrSingleSegment",
        "DescriptionOfSingleSegment",
        "DateOfStartOfReportingPeriod",
        "DateOfEndOfReportingPeriod",
        "WhetherResultsAreAuditedOrUnaudited",
        "NatureOfReportStandaloneConsolidated",
        "RevenueFromOperations",
        "OtherIncome",
        "Income",
        "CostOfMaterialsConsumed",
        "PurchasesOfStockInTrade",
        "ChangesInInventoriesOfFinishedGoodsWorkInProgressAndStockInTrade",
        "EmployeeBenefitExpense",
        "FinanceCosts",
        "DepreciationDepletionAndAmortisationExpense",
        "OtherExpenses",
        "Expenses",
        "ProfitBeforeExceptionalItemsAndTax",
        "ExceptionalItemsBeforeTax",
        "ProfitBeforeTax",
        "CurrentTax",
        "DeferredTax",
        "TaxExpense",
        "NetMovementInRegulatoryDeferralAccountBalancesRelatedToProfitOrLossAndTheRelatedDeferredTaxMovement",
        "ProfitLossForPeriodFromContinuingOperations",
        "ProfitLossFromDiscontinuedOperationsBeforeTax",
        "TaxExpenseOfDiscontinuedOperations",
        "ProfitLossFromDiscontinuedOperationsAfterTax",
        "ShareOfProfitLossOfAssociatesAndJointVenturesAccountedForUsingEquityMethod",
        "ProfitLossForPeriod",
        "OtherComprehensiveIncomeNetOfTaxes",
        "ComprehensiveIncomeForThePeriod",
        "ProfitOrLossAttributableToOwnersOfParent",
        "ProfitOrLossAttributableToNonControllingInterests",
        "ComprehensiveIncomeForThePeriodAttributableToOwnersOfParent",
        "ComprehensiveIncomeForThePeriodAttributableToOwnersOfParentNonControllingInterests",
        "PaidUpValueOfEquityShareCapital",
        "FaceValueOfEquityShareCapital",
        "BasicEarningsLossPerShareFromContinuingOperations",
        "DilutedEarningsLossPerShareFromContinuingOperations",
        "BasicEarningsLossPerShareFromDiscontinuedOperations",
        "DilutedEarningsLossPerShareFromDiscontinuedOperations",
        "BasicEarningsLossPerShareFromContinuingAndDiscontinuedOperations",
        "DilutedEarningsLossPerShareFromContinuingAndDiscontinuedOperations",
        "DescriptionOfOtherExpenses",
        "OtherExpenses",
        "DescriptionOfItemThatWillNotBeReclassifiedToProfitAndLoss",
        "AmountOfItemThatWillNotBeReclassifiedToProfitAndLoss",
        "IncomeTaxRelatingToItemsThatWillNotBeReclassifiedToProfitOrLoss",
        "DescriptionOfItemThatWillBeReclassifiedToProfitAndLoss",
        "AmountOfItemThatWillBeReclassifiedToProfitAndLoss",
        "IncomeTaxRelatingToItemsThatWillBeReclassifiedToProfitOrLoss",
    ]
    return master_data_df, headers, ns, keys_to_extract


def get_top_gainers_or_losers(to_get: str) -> dict:
    """
    Fetch top gainers or losers for a given index.

    Args:
        to_get (str): Index to fetch (e.g., 'NIFTY 50').

    Returns:
        dict: Parsed JSON data.

    Example:
        >>> from nselib import capital_market
        >>> data = capital_market.get_func.get_top_gainers_or_losers('NIFTY 50')
    """
    logger.debug(f"Fetching top gainers or losers for index: {to_get}")
    origin_url = "https://www.nseindia.com/market-data/top-gainers-losers"
    url = f"https://www.nseindia.com/api/live-analysis-variations?index={to_get}"
    try:
        data_json = nse_urlfetch(url, origin_url=origin_url).json()
    except Exception as e:
        logger.error(f"Failed to fetch data: {e}", exc_info=e)
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    return data_json
