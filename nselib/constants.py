
dd_mm_yyyy = '%d-%m-%Y'
dd_mmm_yyyy = '%d-%b-%Y'
ddmmyyyy = '%d%m%Y'
ddmmyy = '%d%m%y'
mmm_yy = '%b-%y'

equity_periods = ['1D', '1W', '1M', '3M', '6M', '1Y']
indices_list = ['NIFTY', 'FINNIFTY', 'BANKNIFTY']


# ---------- column lists-----------------

price_volume_and_deliverable_position_data_columns = \
    ['Symbol', 'Series', 'Date', 'PrevClose', 'OpenPrice', 'HighPrice',
     'LowPrice', 'LastPrice', 'ClosePrice', 'AveragePrice', 'TotalTradedQuantity',
     'TurnoverInRs', 'No.ofTrades', 'DeliverableQty', '%DlyQttoTradedQty']

price_volume_data_columns = ['Symbol', 'Series', 'Date', 'PrevClose', 'OpenPrice', 'HighPrice',
                             'LowPrice', 'LastPrice', 'ClosePrice', 'AveragePrice',
                             'TotalTradedQuantity', 'Turnover', 'No.ofTrades']

deliverable_data_columns = ['Symbol', 'Series', 'Date', 'TradedQty', 'DeliverableQty', '%DlyQttoTradedQty']

bulk_deal_data_columns = ['Date', 'Symbol', 'SecurityName', 'ClientName', 'Buy/Sell', 'QuantityTraded',
                          'TradePrice/Wght.Avg.Price', 'Remarks']

block_deals_data_columns = ['Date', 'Symbol', 'SecurityName', 'ClientName', 'Buy/Sell', 'QuantityTraded',
                            'TradePrice/Wght.Avg.Price', 'Remarks']

short_selling_data_columns = ['Date', 'Symbol', 'SecurityName', 'Quantity']

bhavcopy_old = ['TradDt', 'ISIN', 'TckrSymb', 'SctySrs', 'OpnPric', 'HghPric', 'LwPric', 'ClsPric', 'LastPric',
                'PrvsClsgPric', 'TtlTradgVol', 'TtlTrfVal', 'TtlNbOfTxsExctd']

bhavcopy_new = ['TIMESTAMP', 'ISIN', 'SYMBOL', 'SERIES', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST', 'PREVCLOSE',
                'TOTTRDQTY', 'TOTTRDVAL', 'TOTALTRADES']

future_price_volume_data_column = ['TIMESTAMP', 'INSTRUMENT', 'SYMBOL', 'EXPIRY_DT', 'STRIKE_PRICE', 'OPTION_TYPE', 'MARKET_TYPE',
                                   'OPENING_PRICE', 'TRADE_HIGH_PRICE', 'TRADE_LOW_PRICE', 'CLOSING_PRICE',
                                   'LAST_TRADED_PRICE', 'PREV_CLS', 'SETTLE_PRICE', 'TOT_TRADED_QTY', 'TOT_TRADED_VAL',
                                   'OPEN_INT', 'CHANGE_IN_OI', 'MARKET_LOT', 'UNDERLYING_VALUE']

india_vix_data_column = ['TIMESTAMP', 'INDEX_NAME', 'OPEN_INDEX_VAL', 'CLOSE_INDEX_VAL', 'HIGH_INDEX_VAL',
                         'LOW_INDEX_VAL', 'PREV_CLOSE', 'VIX_PTS_CHG', 'VIX_PERC_CHG']

index_data_columns = ['TIMESTAMP', 'INDEX_NAME', 'OPEN_INDEX_VAL', 'HIGH_INDEX_VAL', 'CLOSE_INDEX_VAL',
                      'LOW_INDEX_VAL', 'TRADED_QTY', 'TURN_OVER']

var_columns = ['RecordType', 'Symbol', 'Series', 'Isin', 'SecurityVaR', 'IndexVaR', 'VaRMargin',
               'ExtremeLossRate', 'AdhocMargin', 'ApplicableMarginRate']
