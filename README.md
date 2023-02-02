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

The program already handles all of the *ETL process* completely, you don't need to input anything else than the values for `trading_pair, `interval`, and `start_str` variables.

