<p align="center">
  <h1 align="center">nselib</h1>
  <p align="center">
    A Python library to fetch publicly available data from <a href="https://www.nseindia.com">NSE India</a>.
  </p>
</p>

<p align="center">
  <a href="https://pypi.org/project/nselib/"><img src="https://img.shields.io/pypi/v/nselib?color=blue" alt="PyPI Version"></a>
  <a href="https://pypi.org/project/nselib/"><img src="https://img.shields.io/pypi/pyversions/nselib" alt="Python Versions"></a>
  <a href="https://github.com/RuchiTanmay/nselib/blob/main/LICENSE"><img src="https://img.shields.io/github/license/RuchiTanmay/nselib" alt="License"></a>
  <a href="https://pypi.org/project/nselib/"><img src="https://img.shields.io/pypi/dm/nselib?color=green" alt="Downloads"></a>
</p>

---

## ✨ Features

- **Capital Market** — Price volume data, deliverable positions, bhav copies, bulk/block deals, short selling, VaR margins, PE ratios, 52-week highs/lows, and more
- **Cash Market** — NSDL FPI investment and derivative activity plus AMFI monthly archive reports
- **Derivatives** — Futures & options price volume data, bhav copies, participant-wise OI & volume, live option chains, FII statistics, ban period securities
- **Indices** — Index constituent lists, live index performances across Broad Market, Sectoral, Thematic, and Strategy categories
- **Debt** — Securities available for trading
- **Corporate Filings** — Financial results, corporate actions, event calendars
- **Market Activity** — Top gainers/losers, most active equities, total traded stocks, FII/DII activity
- **Utilities** — Trading holiday calendar, India VIX historical data

## 📦 Installation

**Fresh install:**

```bash
pip install nselib
```

**Upgrade to latest:**

```bash
pip install nselib --upgrade
```

> **Note:** Compatible and tested with Python 3.8 and above.

## 🚀 Quick Start

```python
from nselib import capital_market

# Get price volume data for a stock (last 1 month)
df = capital_market.price_volume_data(symbol='SBIN', period='1M')
print(df.head())

# Or specify a custom date range
df = capital_market.price_volume_and_deliverable_position_data(
    symbol='SBIN',
    from_date='01-01-2024',
    to_date='31-01-2024'
)
print(df)
```

## 📖 API Reference

### Date Parameters

Most functions accept dates in two ways:

| Parameter | Format | Example |
|---|---|---|
| `from_date` / `to_date` | `dd-mm-YYYY` | `'01-06-2024'` |
| `period` | Shorthand code | `'1D'`, `'1W'`, `'1M'`, `'6M'`, `'1Y'` |

> You must provide **either** `from_date` + `to_date` **or** `period`, not both.

---

### Capital Market

```python
from nselib import capital_market
```

| Function | Description | Key Parameters                                            |
|---|---|-----------------------------------------------------------|
| `price_volume_and_deliverable_position_data()` | OHLCV + delivery data | `symbol`, `from_date`/`to_date` or `period`               |
| `price_volume_data()` | OHLCV price volume data | `symbol`, `from_date`/`to_date` or `period`               |
| `deliverable_position_data()` | Delivery position data | `symbol`, `from_date`/`to_date` or `period`               |
| `bulk_deal_data()` | Bulk deal transactions | `from_date`/`to_date` or `period`                         |
| `block_deals_data()` | Block deal transactions | `from_date`/`to_date` or `period`                         |
| `short_selling_data()` | Short selling reports | `from_date`/`to_date` or `period`                         |
| `bhav_copy_with_delivery()` | Daily bhav copy with delivery | `trade_date`                                              |
| `bhav_copy_equities()` | CM-UDiFF bhav copy | `trade_date`                                              |
| `bhav_copy_sme()` | SME bhav copy | `trade_date`                                              |
| `equity_list()` | All listed equities | —                                                         |
| `fno_equity_list()` | F&O equity list with lot sizes | —                                                         |
| `fno_index_list()` | F&O index list with lot sizes | —                                                         |
| `nifty50_equity_list()` | Nifty 50 constituents | —                                                         |
| `niftynext50_equity_list()` | Nifty Next 50 constituents | —                                                         |
| `niftymidcap150_equity_list()` | Nifty Midcap 150 constituents | —                                                         |
| `niftysmallcap250_equity_list()` | Nifty Smallcap 250 constituents | —                                                         |
| `india_vix_data()` | India VIX historical data | `from_date`/`to_date` or `period`                         |
| `index_data()` | Historical index OHLC data | `index`, `from_date`/`to_date` or `period`                |
| `market_watch_all_indices()` | Live snapshot of all indices | —                                                         |
| `daily_volatility()` | CM daily volatility report | `trade_date`                                              |
| `fii_dii_trading_activity()` | FII/DII buy-sell activity | —                                                         |
| `var_begin_day()` | VaR — begin of day | `trade_date`                                              |
| `var_1st_intra_day()` | VaR — 1st intraday | `trade_date`                                              |
| `var_2nd_intra_day()` | VaR — 2nd intraday | `trade_date`                                              |
| `var_3rd_intra_day()` | VaR — 3rd intraday | `trade_date`                                              |
| `var_4th_intra_day()` | VaR — 4th intraday | `trade_date`                                              |
| `var_end_of_day()` | VaR — end of day | `trade_date`                                              |
| `sme_bhav_copy()` | SME bhav copy | `trade_date`                                              |
| `sme_band_complete()` | SME band complete data | `trade_date`                                              |
| `week_52_high_low_report()` | 52-week high/low report | `trade_date`                                              |
| `financial_results_for_equity()` | Quarterly/annual financials | `from_date`/`to_date` or `period`, `fin_period`, `fo_sec` |
| `corporate_bond_trade_report()` | Corporate bond trades | `trade_date`                                              |
| `pe_ratio()` | PE ratio for all equities | `trade_date`                                              |
| `corporate_actions_for_equity()` | Corporate actions | `from_date`/`to_date` or `period`, `fno_only`             |
| `event_calendar_for_equity()` | Event calendar | `from_date`/`to_date` or `period`, `fno_only`             |
| `top_gainers_or_losers()` | Top gainers or losers | `to_get` (`'gainers'` / `'loosers'`)                      |
| `most_active_equities()` | Most active by value/volume | `fetch_by` (`'value'` / `'volume'`)                       |
| `total_traded_stocks()` | All traded stocks summary | —                                                         |
| `category_turnover_cash()` | category-wise turnover data | `trade_date`                                              |
| `business_growth_cm_segment()` | business growth data for the NSE capital market | `data_type`, `from_year` , `to_year` |


**Examples:**

```python
# Bhav copy for a specific date
df = capital_market.bhav_copy_with_delivery(trade_date='20-06-2024')

# India VIX for last 1 week
df = capital_market.india_vix_data(period='1W')

# CM daily volatility report
df = capital_market.daily_volatility(trade_date='17-04-2026')

# Historical index data
df = capital_market.index_data(index='NIFTY 50', from_date='01-01-2024', to_date='31-03-2024')

# Financial results (quarterly, F&O securities only)
df = capital_market.financial_results_for_equity(period='6M', fo_sec=True, fin_period='Quarterly')

# Top gainers in live market
df = capital_market.top_gainers_or_losers('gainers')
```

---

### Derivatives

```python
from nselib import derivatives
```

| Function                            | Description | Key Parameters |
|-------------------------------------|---|---|
| `future_price_volume_data()`        | Futures price & volume | `symbol`, `instrument` (`FUTIDX`/`FUTSTK`), dates |
| `option_price_volume_data()`        | Options price & volume | `symbol`, `instrument` (`OPTIDX`/`OPTSTK`), `option_type` (`PE`/`CE`), dates |
| `fno_bhav_copy()`                   | F&O daily bhav copy | `trade_date` |
| `participant_wise_open_interest()`  | OI by participant category | `trade_date` |
| `participant_wise_trading_volume()` | Volume by participant category | `trade_date` |
| `daily_volatility()`                | F&O daily volatility report | `trade_date` |
| `expiry_dates_future()`             | Upcoming futures expiry dates | — |
| `expiry_dates_option_index()`       | Upcoming options expiry dates | — |
| `nse_live_option_chain()`           | Live option chain | `symbol`, `expiry_date` (optional), `oi_mode` |
| `fii_derivatives_statistics()`      | FII derivatives stats | `trade_date` |
| `fno_security_in_ban_period()`      | Securities in F&O ban | `trade_date` |
| `live_most_active_underlying()`     | Most active underlyings | — |
| `category_turnover_fo()`            | derivatives category-wise turnover data | `trade_date` |
| `business_growth_fo_segment()`      | business growth data for the NSE F&O segment | `data_type`, `from_year` , `to_year` |

**Instrument Types:**

| Code | Description |
|---|---|
| `FUTIDX` | Future Index |
| `FUTSTK` | Future Stock |
| `OPTIDX` | Option Index |
| `OPTSTK` | Option Stock |

**Examples:**

```python
# Futures price data
df = derivatives.future_price_volume_data(
    symbol='SBIN', instrument='FUTSTK', period='1M'
)

# Live option chain
df = derivatives.nse_live_option_chain(symbol='BANKNIFTY', expiry_date='27-03-2025')

# Compact option chain (fewer columns)
df = derivatives.nse_live_option_chain(symbol='NIFTY', oi_mode='compact')

# FII derivatives statistics
df = derivatives.fii_derivatives_statistics(trade_date='20-12-2025')

# F&O daily volatility report
df = derivatives.daily_volatility(trade_date='17-04-2026')
```

---

### Cash Market

```python
from nselib import cash_market
```

| Function | Description | Key Parameters |
|---|---|---|
| `nsdl_fpi_investment_activity()` | NSDL FPI investment activity for a reporting date | `trade_date` |
| `nsdl_fpi_latest_investment_activity()` | Latest NSDL FPI investment activity | — |
| `nsdl_fpi_derivative_activity()` | NSDL FPI derivative activity for a reporting date | `trade_date` |
| `nsdl_fpi_latest_derivative_activity()` | Latest NSDL FPI derivative activity | — |
| `amfi_monthly_report_links()` | List AMFI monthly archive links | — |
| `amfi_monthly_data()` | Parse one AMFI monthly report | `report_month`, `file_type_priority` |
| `amfi_monthly_historical_data()` | Parse AMFI monthly reports across a range | `from_month`, `to_month`, `file_type_priority` |

**Examples:**

```python
# NSDL FPI investment activity for a specific reporting date
df = cash_market.nsdl_fpi_investment_activity(trade_date='30-10-2025')

# Latest NSDL FPI derivative activity
df = cash_market.nsdl_fpi_latest_derivative_activity()

# List available AMFI archive reports
links = cash_market.amfi_monthly_report_links()

# Parse a single AMFI monthly report
df = cash_market.amfi_monthly_data(report_month='01-03-2026')

# Parse AMFI history for a month range
history = cash_market.amfi_monthly_historical_data(from_month='01-01-2024', to_month='01-03-2026')
```

---

### Indices

```python
from nselib import indices
```

| Function | Description | Key Parameters |
|---|---|---|
| `index_list()` | Available indices by category | `index_category` |
| `constituent_stock_list()` | Stocks in a given index | `index_category`, `index_name` |
| `live_index_performances()` | Live performance of all indices | — |

**Index Categories:** `BroadMarketIndices`, `SectoralIndices`, `ThematicIndices`, `StrategyIndices`

**Examples:**

```python
# List all broad market indices
index_names = indices.index_list(index_category='BroadMarketIndices')

# Get Nifty 50 constituents
df = indices.constituent_stock_list(index_category='BroadMarketIndices', index_name='Nifty 50')

# Live index performances
df = indices.live_index_performances()
```

---

### Debt

```python
from nselib import debt
```

| Function | Description | Key Parameters |
|---|---|---|
| `securities_available_for_trading()` | Debt securities available | `trade_date` |

**Example:**

```python
df = debt.securities_available_for_trading(trade_date='20-12-2025')
```

---

### Utilities

```python
import nselib
```

| Function | Description |
|---|---|
| `trading_holiday_calendar()` | NSE trading holidays for all segments |

**Example:**

```python
df = nselib.trading_holiday_calendar()
```

---

## 🐞 Logging & Debugging

`nselib` comes with a built-in logger that is silent by default so it doesn't pollute your application's logs. If you want to see detailed network requests, API responses, or debug errors while working with the library, you can easily enable it.

```python
import nselib
import logging

# Enable the logger to output to the console
nselib.enable_logging(level=logging.DEBUG)

# Now, function calls will emit helpful trace logs
df = nselib.capital_market.price_volume_data('SBIN', period='1W')
```

---

## 🤝 How to Contribute

There are multiple ways to contribute to nselib:

### Report Issues & Suggest Features

Found a bug or have a feature request? Please open an issue on the [GitHub Issues page](https://github.com/RuchiTanmay/nselib/issues).

### Submit Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

### Write About nselib

Help the community by writing tutorials, blog posts, or example projects using nselib.

### Contact

- **Original Author:** [Ruchi Tanmay](https://www.linkedin.com/in/ruchi-tanmay-61848219)
- **GitHub:** [RuchiTanmay/nselib](https://github.com/RuchiTanmay/nselib)

## 📄 License

This project is licensed under the Apache License 2.0 — see the [LICENSE](LICENSE) file for details.
