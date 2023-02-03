# CryptoRadar
A Python repository focused on applying Data Science to trade cryptocurrencies on Binance Exchange

## Introduction

A friend of a friend I met not so much ago told me that he had decided to trade a small sample of cryptocurrencies on Binance Spot Market, he shared with me the fact that he, even though had never purchased any trading course (*and seemed not interested in doing so in the short term*), was making some small yet consistent profits on a daily basis. He even went further and showed me his net worth graph over the last 2 weeks, it was clear that he wasn't lying, and he also told me that he didn't even use any type of indicator to make his trading decisions.

He told me that the only thing he did was to eyeball at which range of prices his sample of cryptocurrencies were fluctuating, for then setting buy signals with the Binance Mobile App, the first one to activate its corresponding signal would be the first to be traded (*that was his rule*) and then he just proceded to market buy that one for then inmmediately placing the sell order 2% (*never more never less*) above the price he purchased at, he never used leverage nor marging, and just stayed patient until his sell order got filled (*usually between 1 and 48 hours depending on the trading pair and market conditions*).

This project was created with the aim of making a good, yet simple, statistical analyzis on the Binance Spot Market based on the "way" this guy was trading, to finally understand why he was indeed making small profits consistently.

## Disclaimer

This project ***should not be*** taken as a financial advice for several different reasons: 

* *It hasn't been tested in a production environment.*
* *It is a bit **biased**, as it was stated that it focused on analyzing a particular "way" of making trading decisions and it didn't consider other major factors such as the liquidity of the trading pair.*
* *The output thrown as well as the assumptions made were done to please my interpretation of the "way" my friend was making profits, meaning that my minimalistic approach to analyze his case may not suit your interpretation of his case.*

Having said that, I also have to state that I'm not responsible for whatever results you get from using this information and software later, it is up to you to decide if your financial decisions will be made just as my friend was making them.

## Requirements

* **[Python Binance package](https://python-binance.readthedocs.io/en/latest/)** (unofficial Python wrapper for the [Binance exchange REST API v3](https://binance-docs.github.io/apidocs/spot/en/#change-log))
* **[Pandas](https://pandas.pydata.org/)**
* **[MatPlotLibFinance (a.k.a. "mplfinance")](https://github.com/matplotlib/mplfinance)**
* **[NumPy](https://numpy.org/)**
* **[Spyder](https://www.spyder-ide.org/)** (Or your preferred Python3 environment)

## Installation

Once you have installed Spyder (Or your preferred Python3 environment), open `cmd` on Windows, then:

- To install the **Python Binance package** run: `pip install python-binance`
- To install **Pandas** run: `pip install pandas`
- To install **MatPlotLibFinance** run: `pip install --upgrade mplfinance`
- To install **NumPy** run: `pip install numpy`

## Usage

Now before running [Price Action Analysis using upper and lower bounds and the median.py](https://github.com/noahverner1995/Cryptoradar/blob/main/Binance%20Spot%20Market/Price%20Action%20Analysis%20using%20upper%20and%20lower%20bounds%20and%20the%20median.py), you have to set the following input:

- **To set your trading pair**, go where the `trading_pair` variable is initialized and change `""` for a value like `MATICUSDT` or `BTCUSDT` (these values are strictly tied to what cryptocurrencies Binance currently has listed).
- **To set your timeframe**, go where the `klines` variable is initialized and change the current value of the parameter `interval` for your desired one, for instance: `1m` or `5m` or `1h` or `1d` (just like those values that are shown when a trading chart is displayed)
- **To set your start date**, go where the `klines` variable is initialized and change the current value of the parameter `start_str` for your desired one, for instance: `24 hours ago UTC` or `2 weeks ago UTC` or `800 minutes ago UTC` (it is recommended that you get enough data for the program to analyze, **5 days of data with a 15m timeframe is enough** imo)

`api_key` AND `secret_key` are variables that are initialized because the Binance exchange REST API V3 demands it, but as you are not actually going to trade anything they can be left initialized as `""`

## Input Data

The program already handles all of the *ETL process* completely, you don't need to input anything else than the values for `trading_pair`, `interval`, and `start_str` variables.

## Output Data

Say you set the following input values:

`trading_pair = "C98USDT"`

`interval = "15m"`

`start_str = "5 days ago UTC"`

You will get an output like this:

> The bullish percentage change between bounds follows a Leptokurtic distribution, and the median (suggested ROI per trade) is 3.25%

> The trading pair analyzed was C98/USDT

> The simulated long entries made using only the upper and lower bounds were the following:`

|    |   Start Index |   End Index |   Bullish Percentage Change |   Hours Spent |
|---:|--------------:|------------:|----------------------------:|--------------:|
|  0 |            14 |          26 |                    1.21382  |          3    |
|  1 |            38 |          58 |                    1.33546  |          5    |
|  2 |            59 |          62 |                    1.40398  |          0.75 |
|  3 |            63 |          64 |                    2.24854  |          0.25 |
|  4 |            66 |          89 |                   -2.00651  |          5.75 |
|  5 |           106 |         133 |                    2.25996  |          6.75 |
|  6 |           150 |         161 |                    2.373    |          2.75 |
|  7 |           165 |         185 |                    0.180333 |          5    |
|  8 |           211 |         214 |                    2.31662  |          0.75 |
|  9 |           215 |         224 |                    4.90001  |          2.25 |
| 10 |           247 |         281 |                   -2.80273  |          8.5  |
| 11 |           283 |         298 |                    0.273368 |          3.75 |
| 12 |           349 |         351 |                    2.08824  |          0.5  |
| 13 |           372 |         386 |                    3.18803  |          3.5  |
| 14 |           396 |         418 |                   -1.63708  |          5.5  |
| 15 |           427 |         435 |                    2.27166  |          2    |
| 16 |           444 |         456 |                    1.20849  |          3    |
| 17 |           468 |         475 |                    2.43259  |          1.75 |

> The total sum of potential roi per trades was: 23.25%

> The average time spent per trade was: 3.38 hours

> In contrast, the simulated long entries made using only the lower bound and the median were the following:

|    |   Start Index |   End Index |   Bullish Percentage Change |   Hours Spent |
|---:|--------------:|------------:|----------------------------:|--------------:|
|  0 |            14 |          65 |                     3.4554  |         12.75 |
|  1 |            66 |          94 |                     3.55851 |          7    |
|  2 |           106 |         134 |                     3.82163 |          7    |
|  3 |           150 |         161 |                     3.53776 |          2.75 |
|  4 |           165 |         187 |                     9.406   |          5.5  |
|  5 |           211 |         224 |                     7.47438 |          3.25 |
|  6 |           247 |         355 |                     3.84735 |         27    |
|  7 |           372 |         386 |                     4.37458 |          3.5  |

> The total sum of potential roi per trades was: 39.48%

> The average time spent per trade was: 8.59 hours

> Currently, the close price of C98/USDT is likely to remain stable.

![C98USDT-15m-5DAYSAGOUTC](https://user-images.githubusercontent.com/83596569/216649765-89867426-c88b-4ea0-b54a-20a647f0a36c.png)

## Contributors

[Noah Verner - Software Engineer & Data Analyst](https://www.linkedin.com/in/noahverner/)

## License

This project was released with the [MIT License](https://github.com/noahverner1995/Cryptoradar/blob/main/LICENSE)
