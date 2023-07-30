# NSElib 0.6

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
* nifty50_equity_list
* india_vix_data
* index_data
* market_watch_all_indices
* fii_dii_trading_activity

Example : 

from nselib import capital_market 

data = capital_market.price_volume_and_deliverable_position_data(symbol='SBIN', from_date='01-06-2023', to_date='10-06-2023')
                                            
OR

data = capital_market.price_volume_and_deliverable_position_data(symbol='SBIN', period='1M')

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

Example : 

from nselib import derivatives

data = derivatives.future_price_volume_data(symbol='SBIN', instrument='FUTSTK', from_date='01-06-2023', to_date='10-06-2023')

OR

data = derivatives.price_volume_and_deliverable_position_data(symbol='BANKNIFTY', instrument='FUTIDX', period='1M')

Note: instrument type ( future index = FUTIDX, future stocks = FUTSTK, option index = OPTIDX, option stocks = OPTSTK)

More functions will be available in future releases...

### Debt

More functions will be available in future releases...


## How can I contribute?
There are multiple ways in which you can contribute-

### Write about your project

There are working on to add many function to this library. NSElib at the moment is short of good documentation. There are lot of features in NSElib yet to come :( , so till we complete the documentation, I'll need support from the community.

Please write about your projects in blogs, quora answers and other forums, so that people find working examples to get started.

### Raising issues, bugs, enhancement requests

For quick resolution please raise issues both [here on issue page](https://github.com/RuchiTanmay/nselib/issues). I'll try my best to address the issues quickly on github as and when I get notified, but raising it on stackoverflow will provide you access to a larger group and someone else might solve your problem before I do.

### Submit patches

If you have fixed an issue or added a new feature, please fork this repository, make your changes and submit a pull request. [Here's good article on how to do this.](https://code.tutsplus.com/tutorials/how-to-collaborate-on-github--net-34267) 

Looking forward for healthy participation from community.
