from io import BytesIO, StringIO
import json
from nselib.libutil import *
from nselib.constants import *


def get_price_volume_and_deliverable_position_data(symbol: str, from_date: str, to_date: str):
    origin_url = "https://nsewebsite-staging.nseindia.com/report-detail/eq_security"
    url = "https://www.nseindia.com/api/historicalOR/generateSecurityWiseHistoricalData?"
    payload = f"from={from_date}&to={to_date}&symbol={symbol}&type=priceVolumeDeliverable&series=ALL&csv=true"
    try:
        data_text = nse_urlfetch(url + payload, origin_url=origin_url).text
        data_text = data_text.replace('\x82', '').replace('â¹', 'In Rs')
        with open('file.csv', 'w') as f:
            f.write(data_text)
        f.close()
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    data_df = pd.read_csv('file.csv')
    data_df.columns = [name.replace(' ', '') for name in data_df.columns]
    return data_df


def get_price_volume_data(symbol: str, from_date: str, to_date: str):
    origin_url = "https://nsewebsite-staging.nseindia.com/report-detail/eq_security"
    url = "https://www.nseindia.com/api/historicalOR/generateSecurityWiseHistoricalData?"
    payload = f"from={from_date}&to={to_date}&symbol={symbol}&type=priceVolume&series=ALL&csv=true"
    try:
        data_text = nse_urlfetch(url + payload, origin_url=origin_url)
        if data_text.status_code != 200:
            raise NSEdataNotFound(f" Resource not available for Price Volume Data")
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    data_df = pd.read_csv(BytesIO(data_text.content), index_col=False)
    data_df.columns = [name.replace(' ', '') for name in data_df.columns]
    return data_df


def get_deliverable_position_data(symbol: str, from_date: str, to_date: str):
    origin_url = "https://nsewebsite-staging.nseindia.com/report-detail/eq_security"
    url = "https://www.nseindia.com/api/historicalOR/generateSecurityWiseHistoricalData?"
    payload = f"from={from_date}&to={to_date}&symbol={symbol}&type=deliverable&series=ALL&csv=true"
    try:
        data_text = nse_urlfetch(url + payload, origin_url=origin_url)
        if data_text.status_code != 200:
            raise NSEdataNotFound(f" Resource not available for deliverable_position_data")
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    data_df = pd.read_csv(BytesIO(data_text.content), index_col=False)
    data_df.columns = [name.replace(' ', '') for name in data_df.columns]
    return data_df


def get_india_vix_data(from_date: str, to_date: str):
    origin_url = "https://nsewebsite-staging.nseindia.com/report-detail/eq_security"
    url = f"https://www.nseindia.com/api/historicalOR/vixhistory?from={from_date}&to={to_date}&csv=true"
    try:
        data_json = nse_urlfetch(url, origin_url=origin_url).json()
        data_df = pd.DataFrame(data_json['data'])
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    # data_df.drop(columns='TIMESTAMP', inplace=True)
    data_df.columns = cleaning_column_name(data_df.columns)
    return data_df[india_vix_data_column]


def get_index_data(index: str, from_date: str, to_date: str):
    index = index.replace(' ', '%20').upper()
    origin_url = "https://www.nseindia.com/reports-indices-historical-index-data"
    url = f"https://www.nseindia.com/api/historicalOR/indicesHistory?indexType={index}&from={from_date}&to={to_date}"
    try:
        data_json = nse_urlfetch(url, origin_url=origin_url).json()
        data_df = pd.DataFrame(data_json['data'])
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    data_df.drop(columns='HI_TIMESTAMP', inplace=True)
    data_df.columns = index_data_columns
    return data_df


def get_bulk_deal_data(from_date: str, to_date: str):
    # print(from_date, to_date)
    origin_url = "https://nsewebsite-staging.nseindia.com"
    url = "https://www.nseindia.com/api/historicalOR/bulk-block-short-deals?optionType=bulk_deals&"
    payload = f"from={from_date}&to={to_date}&csv=true"
    # print(url + payload)
    data_text = nse_urlfetch(url + payload, origin_url=origin_url)
    if data_text.status_code != 200:
        raise NSEdataNotFound(f" Resource not available for bulk_deal_data")
    data_df = pd.read_csv(BytesIO(data_text.content), index_col=False)
    data_df.columns = [name.replace(' ', '') for name in data_df.columns]
    return data_df


def get_block_deals_data(from_date: str, to_date: str):
    # print(from_date, to_date)
    origin_url = "https://nsewebsite-staging.nseindia.com"
    url = "https://www.nseindia.com/api/historicalOR/bulk-block-short-deals?optionType=block_deals&"
    payload = f"from={from_date}&to={to_date}&csv=true"
    data_text = nse_urlfetch(url + payload, origin_url=origin_url)
    if data_text.status_code != 200:
        raise NSEdataNotFound(f" Resource not available for block_deals_data")
    data_df = pd.read_csv(BytesIO(data_text.content), index_col=False)
    data_df.columns = [name.replace(' ', '') for name in data_df.columns]
    return data_df


def get_short_selling_data(from_date: str, to_date: str):
    """
    NSE short selling data in data frame
    :param from_date:
    :param to_date:
    :return:
    """
    # print(from_date, to_date)
    origin_url = "https://nsewebsite-staging.nseindia.com"
    url = "https://www.nseindia.com/api/historicalOR/bulk-block-short-deals?optionType=short_selling&"
    payload = f"from={from_date}&to={to_date}&csv=true"
    data_text = nse_urlfetch(url + payload,origin_url=origin_url)
    if data_text.status_code != 200:
        raise NSEdataNotFound(f" Resource not available for short_selling_data")
    data_df = pd.read_csv(BytesIO(data_text.content), index_col=False)
    data_df.columns = [name.replace(' ', '') for name in data_df.columns]
    return data_df


def get_financial_results_master(from_date: str = None,
                                 to_date: str = None,
                                 period: str = None,
                                 fo_sec: bool = False,
                                 fin_period: str = 'Quarterly'):
    validate_date_param(from_date, to_date, period)
    from_date, to_date = derive_from_and_to_date(from_date=from_date, to_date=to_date, period=period)
    origin_url = "https://www.nseindia.com/companies-listing/corporate-filings-financial-results"
    url_ = "https://www.nseindia.com/api/corporates-financial-results?index=equities&"
    if fo_sec:
        payload = f'from_date={from_date}&to_date={to_date}&fo_sec=true&period={fin_period}'
    else:
        payload = f'from_date={from_date}&to_date={to_date}&period={fin_period}'
    data_text = nse_urlfetch(url_ + payload, origin_url=origin_url)
    if data_text.status_code != 200:
        raise NSEdataNotFound(f" Resource not available for financial data with these parameters")
    json_str = data_text.content.decode("utf-8")
    data_list = json.loads(json_str)
    master_data_df = pd.DataFrame(data_list)
    master_data_df.columns = [name.replace(' ', '') for name in master_data_df.columns]
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.nseindia.com/'
        }
    ns = {
            "xbrli": "http://www.xbrl.org/2003/instance",
            "in-bse-fin": "http://www.bseindia.com/xbrl/fin/2020-03-31/in-bse-fin"
        }
    keys_to_extract = [
        "ScripCode", "Symbol", "MSEISymbol", "NameOfTheCompany", "ClassOfSecurity",
        "DateOfStartOfFinancialYear", "DateOfEndOfFinancialYear",
        "DateOfBoardMeetingWhenFinancialResultsWereApproved",
        "DateOnWhichPriorIntimationOfTheMeetingForConsideringFinancialResultsWasInformedToTheExchange",
        "DescriptionOfPresentationCurrency", "LevelOfRoundingUsedInFinancialStatements",
        "ReportingQuarter", "StartTimeOfBoardMeeting", "EndTimeOfBoardMeeting",
        "DateOfStartOfBoardMeeting", "DateOfEndOfBoardMeeting",
        "DeclarationOfUnmodifiedOpinionOrStatementOnImpactOfAuditQualification",
        "IsCompanyReportingMultisegmentOrSingleSegment", "DescriptionOfSingleSegment",
        "DateOfStartOfReportingPeriod", "DateOfEndOfReportingPeriod",
        "WhetherResultsAreAuditedOrUnaudited", "NatureOfReportStandaloneConsolidated",
        "RevenueFromOperations", "OtherIncome", "Income", "CostOfMaterialsConsumed",
        "PurchasesOfStockInTrade", "ChangesInInventoriesOfFinishedGoodsWorkInProgressAndStockInTrade",
        "EmployeeBenefitExpense", "FinanceCosts", "DepreciationDepletionAndAmortisationExpense",
        "OtherExpenses", "Expenses", "ProfitBeforeExceptionalItemsAndTax", "ExceptionalItemsBeforeTax",
        "ProfitBeforeTax", "CurrentTax", "DeferredTax", "TaxExpense",
        "NetMovementInRegulatoryDeferralAccountBalancesRelatedToProfitOrLossAndTheRelatedDeferredTaxMovement",
        "ProfitLossForPeriodFromContinuingOperations", "ProfitLossFromDiscontinuedOperationsBeforeTax",
        "TaxExpenseOfDiscontinuedOperations", "ProfitLossFromDiscontinuedOperationsAfterTax",
        "ShareOfProfitLossOfAssociatesAndJointVenturesAccountedForUsingEquityMethod",
        "ProfitLossForPeriod", "OtherComprehensiveIncomeNetOfTaxes",
        "ComprehensiveIncomeForThePeriod", "ProfitOrLossAttributableToOwnersOfParent",
        "ProfitOrLossAttributableToNonControllingInterests",
        "ComprehensiveIncomeForThePeriodAttributableToOwnersOfParent",
        "ComprehensiveIncomeForThePeriodAttributableToOwnersOfParentNonControllingInterests",
        "PaidUpValueOfEquityShareCapital", "FaceValueOfEquityShareCapital",
        "BasicEarningsLossPerShareFromContinuingOperations",
        "DilutedEarningsLossPerShareFromContinuingOperations",
        "BasicEarningsLossPerShareFromDiscontinuedOperations",
        "DilutedEarningsLossPerShareFromDiscontinuedOperations",
        "BasicEarningsLossPerShareFromContinuingAndDiscontinuedOperations",
        "DilutedEarningsLossPerShareFromContinuingAndDiscontinuedOperations",
        "DescriptionOfOtherExpenses", "OtherExpenses",
        "DescriptionOfItemThatWillNotBeReclassifiedToProfitAndLoss",
        "AmountOfItemThatWillNotBeReclassifiedToProfitAndLoss",
        "IncomeTaxRelatingToItemsThatWillNotBeReclassifiedToProfitOrLoss",
        "DescriptionOfItemThatWillBeReclassifiedToProfitAndLoss",
        "AmountOfItemThatWillBeReclassifiedToProfitAndLoss",
        "IncomeTaxRelatingToItemsThatWillBeReclassifiedToProfitOrLoss"
    ]
    return master_data_df, headers, ns, keys_to_extract


def get_top_gainers_or_losers(to_get: str):
    origin_url = "https://www.nseindia.com/market-data/top-gainers-losers"
    url = f"https://www.nseindia.com/api/live-analysis-variations?index={to_get}"
    try:
        data_json = nse_urlfetch(url, origin_url=origin_url).json()
    except Exception as e:
        raise NSEdataNotFound(f" Resource not available MSG: {e}")
    return data_json
