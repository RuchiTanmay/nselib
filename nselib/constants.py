import os

dd_mm_yyyy = '%d-%m-%Y'
dd_mmm_yyyy = '%d-%b-%Y'
ddmmyyyy = '%d%m%Y'

equity_periods = ['1D', '1W', '1M', '6M', '1Y']

#---------- column lists-----------------

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

bhavcopy_old = ['ISIN', 'TckrSymb', 'SctySrs', 'OpnPric', 'HghPric', 'LwPric', 'ClsPric', 'LastPric',
                'PrvsClsgPric', 'TtlTradgVol', 'TtlTrfVal', 'TradDt', 'TtlNbOfTxsExctd']

bhavcopy_new = ['ISIN', 'SYMBOL', 'SERIES', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST', 'PREVCLOSE', 'TOTTRDQTY',
                'TOTTRDVAL', 'TIMESTAMP',	'TOTALTRADES']

