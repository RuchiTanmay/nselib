# mcxlib 0.1

Python Library to get publicly available data on new MCX website.

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

```$pip install mcxlib```

Upgrade

```$pip install mcxlib --upgrade```

## Function list

* get_live_market_watch
* get_live_top_gainers
* get_live_heat_map
* get_live_top_gainers
* get_live_top_losers
* get_live_most_active_contracts
* get_live_most_active_puts_calls
* get_bhav_copy
* get_historical_data
* get_pro_cli_details
* get_option_chain
* get_put_call_ratio
* get_category_wise_oi
* get_category_wise_turnover

Example : 

import mcxlib

data = get_live_market_watch()
                                            
More functions will be available in future releases...


## How can I contribute?
There are multiple ways in which you can contribute-

### Write about your project

There are working on to add many function to this library. mcxlib at the moment is short of good documentation. There are lot of features in mcxlib yet to come :( , so till we complete the documentation, I'll need support from the community.

Please write about your projects in blogs, quora answers and other forums, so that people find working examples to get started.

### Raising issues, bugs, enhancement requests

For quick resolution please raise issues both [here on issue page](https://github.com/RuchiTanmay/mcxlib/issues). I'll try my best to address the issues quickly on github as and when I get notified, but raising it on stackoverflow will provide you access to a larger group and someone else might solve your problem before I do.

### Submit patches

If you have fixed an issue or added a new feature, please fork this repository, make your changes and submit a pull request. [Here's good article on how to do this.](https://code.tutsplus.com/tutorials/how-to-collaborate-on-github--net-34267) 

Looking forward for healthy participation from community.
