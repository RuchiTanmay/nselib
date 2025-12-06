# NSElib 2.1

Python Library to get publicly available data on new NSE india website.

Release Notes
* Compatible and Tested with Python 3.8 and above 
* Future release will be done on requirement basic

## Libraries Required
- requests
- beautifulsoup
- numpy 
- scipy
- pandas
- lxml
- pandas_market_calendars

For Windows systems you can install Anaconda, this will cover many dependencies (You'll have to install requests and beautifulsoup additionally though)

## Installation
Fresh installation 

```$pip install nselib```

Upgrade

```$pip install nselib --upgrade```

## Function list

### nselib
* trading_holiday_calendar

Example :

import nselib

data = nselib.trading_holiday_calendar()

### Capital Market
* price_volume_and_deliverable_position_data 
* price_volume_data
* deliverable_position_data
* bulk_deal_data
* block_deals_data
* short_selling_data
* bhav_copy_with_delivery
* bhav_copy_equities
* equity_list
* fno_equity_list
* fno_index_list
* nifty50_equity_list
* niftynext50_equity_list
* niftymidcap150_equity_list
* niftysmallcap250_equity_list
* india_vix_data
* index_data
* market_watch_all_indices
* fii_dii_trading_activity
* var_begin_day
* var_1st_intra_day
* var_2nd_intra_day
* var_3rd_intra_day
* var_4th_intra_day
* var_end_of_day
* sme_bhav_copy
* sme_band_complete
* week_52_high_low_report
* financial_results_for_equity
* corporate_bond_trade_report
* bhav_copy_sme
* pe_ratio
* corporate_actions_for_equity
* event_calendar_for_equity

Example : 

from nselib import capital_market 

data = capital_market.price_volume_and_deliverable_position_data(symbol='SBIN', from_date='20-06-2023', to_date='20-07-2023')
                                            
OR

data = capital_market.price_volume_and_deliverable_position_data(symbol='SBIN', period='1M')

data = capital_market.bhav_copy_with_delivery(trade_date='20-06-2024')

More functions will be available in future releases...

### Derivative
* future_price_volume_data
* option_price_volume_data
* fno_bhav_copy
* participant_wise_open_interest
* participant_wise_trading_volume
* expiry_dates_future
* expiry_dates_option_index
* nse_live_option_chain
* fii_derivatives_statistics
* fno_security_in_ban_period

Example : 

from nselib import derivatives

data = derivatives.future_price_volume_data(symbol='SBIN', instrument='FUTSTK', from_date='20-06-2023', to_date='20-07-2023')

OR

data = derivatives.price_volume_and_deliverable_position_data(symbol='BANKNIFTY', instrument='FUTIDX', period='1M')

Note: instrument type ( future index = FUTIDX, future stocks = FUTSTK, option index = OPTIDX, option stocks = OPTSTK)

More functions will be available in future releases...

### Indices
* get_index_list
* get_constituent_stock_list

Example :

from nselib import indices

data = indices.get_constituent_stock_list(index_category='BroadMarketIndices', index_name='Nifty 50')

More functions will be available in future releases...

### Debt

More functions will be available in future releases...


## How can I contribute?
There are multiple ways in which you can contribute-

### Write about your project

There are working on to add many function to this library. NSElib at the moment is short of good documentation. There are a lot of features in NSElib yet to come :( , so till we complete the documentation, I'll need support from the community.

Please write about your projects in blogs, quora answers and other forums, so that people find working examples to get started.

### Raising issues, bugs, enhancement requests

For quick resolution please raise issues both [here on issue page](https://github.com/RuchiTanmay/nselib/issues). I'll try my best to address the issues quickly on github as and when I get notified, but raising it on stackoverflow will provide you access to a larger group and someone else might solve your problem before I do.

### Contact author on [LinkedIn](https://www.linkedin.com/in/ruchi-tanmay-61848219)

### Submit patches

If you have fixed an issue or added a new feature, please fork this repository, make your changes and submit a pull request. [Here's good article on how to do this.](https://code.tutsplus.com/tutorials/how-to-collaborate-on-github--net-34267) 

Looking forward for healthy participation from community.
