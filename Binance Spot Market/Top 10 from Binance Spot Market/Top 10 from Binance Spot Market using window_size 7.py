# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 05:03:09 2023

@author: Noah
"""

from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd
import numpy as np
from requests.exceptions import Timeout
import time
import random

def set_pandas_display_options() -> None:
    """Set pandas display options."""
    # Ref: https://stackoverflow.com/a/52432757/
    display = pd.options.display

    display.max_columns = 10
    display.max_colwidth = 100
    display.width = 200
    display.precision = 6  # set as needed
    display.max_rows = 10

set_pandas_display_options()

def klines_to_df(df_trading_pair):
    
    #drop unnecesary columns
    df_trading_pair.drop(7, inplace = True, axis=1)
    df_trading_pair.drop(8, inplace = True, axis=1)
    df_trading_pair.drop(9, inplace = True, axis=1)
    df_trading_pair.drop(10, inplace = True, axis=1)
    df_trading_pair.drop(11, inplace = True, axis=1)
    
    # Rename the column names for best practices
    df_trading_pair.rename(columns = { 0 : 'Start Date', 
                              1 : 'Open Price',
                              2 : 'High Price',
                              3 : 'Low Price',
                              4 :'Close Price',
                              5 : 'Volume',
                              6 :'End Date',
                              }, inplace = True)
    
    # Convert Unix Time values to actual dates
    df_trading_pair['Start Date'] = pd.to_datetime(df_trading_pair['Start Date'], unit='ms')
    df_trading_pair['End Date'] = pd.to_datetime(df_trading_pair['End Date'], unit='ms')
    df_trading_pair = df_trading_pair.astype({'Open Price': 'float'})
    df_trading_pair = df_trading_pair.astype({'High Price': 'float'})
    df_trading_pair = df_trading_pair.astype({'Low Price': 'float'})
    df_trading_pair = df_trading_pair.astype({'Close Price': 'float'})
    df_trading_pair = df_trading_pair.astype({'Volume': 'float'})
    
    return df_trading_pair

def set_DateTimeIndex(df_trading_pair):
    df_trading_pair = df_trading_pair.set_index('Start Date', inplace=False)
    # Rename the column names for best practices
    df_trading_pair.rename(columns = { "Open Price" : 'Open',
                                       "High Price" : 'High',
                                       "Low Price" : 'Low',
                                       "Close Price" :'Close',
                              }, inplace = True)
    return df_trading_pair

api_key = ""

secret_key = ""

client = Client(api_key=api_key, api_secret= secret_key, tld= "com")

start = time.perf_counter()
tickers = [dictionary for dictionary in client.get_ticker() if dictionary["symbol"].endswith("USDT")]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('BUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').endswith('BEARUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').endswith('BULLUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').endswith('UPUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').endswith('DOWNUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('BCC')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('FTT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('SXP')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('UNFI')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('STORJ')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('REEF')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('ALICE')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('PAX')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('USD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('TUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('COCOS')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('KEEP')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('LUN')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('ERD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('AUDUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('BIDRUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('BLRUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('EURUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('GBPUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('RUBUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('TRYUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('DAIUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('UAHUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('ZARUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('VAIUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('IDRTUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('NGNUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('PLNUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('RONUSD')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('VENUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('BCHABCUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('BCHSVUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('BTTUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('NANOUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('MITHUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('GTOUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('NPXSUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('MFTUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('STORMUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('CVCUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('BEAMUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('HCUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('MCOUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('TCTUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('STRATUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('XZCUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('GXSUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('LENDUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('REPUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('BKRWUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('SRMUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('BZRXUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('NBSUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('HNTUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('DNTUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('SUSDUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('BTCSTUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('RAMPUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('EPSUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('BTGUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('MIRUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('NUUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('TORNUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('TRIBEUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('POLYUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('RGTUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('ANYUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('USTUSDT')]
tickers[:] = [x for x in tickers if not x.get('symbol').startswith('ANCUSDT')]
tickers[:] = [x.get('symbol') for x in tickers]

timeframe = "" # For instance: 3m, 15m, 1h, 2h...
start_date = "" # For instance: 400 hours ago UTC, 1 week UTC, 5 days ago UTC...
window_size = 7 # The exclusive parameter that rules this test
final_df_ws_7 = pd.DataFrame(columns=["Symbol", "Avg Time Spent (hours)", "Expected ROI per trade", "Total Number of Trades", "Total Potential ROI"])

for trading_pair in tickers:
        try:
            klines = client.get_historical_klines(symbol=trading_pair, interval=timeframe, start_str = start_date)
            if len(klines) > 0:
                symbol = trading_pair.replace("USDT", "")+"/"+"USDT"
                
                # Customize the df_trading_pair that stored klines
                df = klines_to_df(pd.DataFrame(klines))

                df_trading_pair_date_time_index = set_DateTimeIndex(df)

                # Calculate moving average and std deviation of the close price
                rolling_mean = df['Close Price'].rolling(window=window_size).mean()
                rolling_std = df['Close Price'].rolling(window=window_size).std()

                print(f"Currently Analyzing {symbol} using a window size of {window_size}, this is the element number {tickers.index(trading_pair)} out of {len(tickers)} in the tickers list")
                # Calculate the upper and lower bounds of the close price based on the moving average and std deviation

                upper_bound = rolling_mean + 2 * rolling_std
                lower_bound = rolling_mean - 2 * rolling_std

                # Create masks to know at which indices the df["Low Price"] was equal or lower than the lower bound
                # as well as which indices the df["High Price"] was equal or greater than the upper bound

                mask_low = df["Low Price"] <= lower_bound
                mask_high = df["High Price"] >= upper_bound

                upper_indices = list(mask_high[mask_high].index)
                lower_indices = list(mask_low[mask_low].index)

                # Now figure out which had been the possible long entries that had been made using the information above
                # Keep in mind that this assumes the long entries made reached exactly the corresponding values of the `upper_bound`

                data = {"Start Index": [], "End Index": []}

                entry = lower_indices[0]
                for i in range(len(upper_indices)):
                    exit = upper_indices[i]
                    if exit > entry:
                        data["Start Index"].append(entry)
                        data["End Index"].append(exit)
                        next_entries = [x for x in lower_indices if x > entry and x > exit]
                        if len(next_entries) > 0:
                            entry = next_entries[0]
                        else:
                            break
                    
                possible_long_entries= pd.DataFrame(data)
                possible_long_entries['Bullish Percentage Change'] = (upper_bound[possible_long_entries['End Index']].values - lower_bound[possible_long_entries['Start Index']].values)/(lower_bound[possible_long_entries['Start Index']].values)*100
                possible_long_entries['Hours Spent'] =(possible_long_entries['End Index'] - possible_long_entries['Start Index'])*(df['Start Date'].iat[1]-df['Start Date'].iat[0]).total_seconds()/3600

                # Mark the possible long entries, in order to do this first create an NaN df that contains the same indices as the original df
                # Then assign to each index of the possible_long_entries its corresponding price from the lower_bound
                df_mark_entry_points = pd.DataFrame([float('nan')]*len(df),index=df.index,columns=['Bullish Entries'])
                for ix,val in zip(possible_long_entries['Start Index'].values,lower_bound[possible_long_entries['Start Index']].values):
                    df_mark_entry_points.loc[ix] = val

                # Mark the possible take-profits assuming the highest price would have reached the upper_bound, in order to do this first create an NaN df that contains the same indices as the original df
                # Then assign to each index of the possible_long_entries its corresponding price from the upper_bound
                df_mark_tp_points = pd.DataFrame([float('nan')]*len(df),index=df.index,columns=['Bullish Entries'])
                for ix,val in zip(possible_long_entries['End Index'].values,upper_bound[possible_long_entries['End Index']].values):
                    df_mark_tp_points.loc[ix] = val

                # Estimate the percentage change from the lower bound to the upper bound
                bullish_percentage_change_between_bounds = round((upper_bound-lower_bound)/lower_bound*100,2)
                bullish_percentage_change_between_bounds.rename('Bullish Pct Chg', inplace = True)

                #If the skewness is between -0.5 and 0.5, the data are fairly symmetrical
                #If the skewness is between -1 and — 0.5 or between 0.5 and 1, the data are moderately skewed
                #If the skewness is less than -1 or greater than 1, the data are highly skewed

                #Kurtosis applied to Financial Markets: https://www.investopedia.com/terms/k/kurtosis.asp

                skewness_value = bullish_percentage_change_between_bounds.skew()
                kurtosis_value = bullish_percentage_change_between_bounds.kurt()
                print()

                if (abs(skewness_value) > 0.5):
                    
                    # Use the median to properly estimate the return on investment per trade
                    expected_roi = bullish_percentage_change_between_bounds.median()

                elif (abs(skewness_value) <= 0.5):
                    
                    # Use the mean to properly estimate the return on investment per trade
                    expected_roi = bullish_percentage_change_between_bounds.mean()

                # Create another mask to know at which indices the expected_roi was reached by the df["High Price"]
                x = lower_bound.iloc[list(lower_bound[lower_bound.notnull()].index.values)]
                x = x + (x * expected_roi / 100)
                actual_upper_bound = x.reindex(df.index, fill_value=np.nan)

                roi_mask_high = df["High Price"] >= actual_upper_bound
                roi_indices = list(roi_mask_high[roi_mask_high].index)

                # Now figure out which long entries would have been actually made using the expected_roi
                data = {"Start Index": [], "End Index": []}

                entry = lower_indices[0]
                for i in range(len(roi_indices)):
                    exit = roi_indices[i]
                    if exit > entry:
                        if (df["High Price"].iat[exit] - lower_bound[entry])/(lower_bound[entry])*100 >=expected_roi:
                            data["Start Index"].append(entry)
                            data["End Index"].append(exit)
                            next_entries = [x for x in lower_indices if x > entry and x > exit]
                            if len(next_entries) > 0:
                                entry = next_entries[0]
                            else:
                                break

                actual_long_entries= pd.DataFrame(data)
                actual_long_entries['Bullish Percentage Change'] = (df["High Price"][actual_long_entries['End Index']].values - lower_bound[actual_long_entries['Start Index']].values)/(lower_bound[actual_long_entries['Start Index']].values)*100
                actual_long_entries['Hours Spent'] =(actual_long_entries['End Index'] - actual_long_entries['Start Index'])*(df['Start Date'].iat[1]-df['Start Date'].iat[0]).total_seconds()/3600
                
                if actual_long_entries.empty == False:
                    
                    # Mark the actual long entries, in order to do this first create an NaN df that contains the same indices as the original df
                    # Then assign to each index of the actual_long_entries its corresponding price from the lower_bound
                    df_mark_real_entry_points = pd.DataFrame([float('nan')]*len(df),index=df.index,columns=['Bullish Entries'])
                    for ix,val in zip(actual_long_entries['Start Index'].values,lower_bound[actual_long_entries['Start Index']].values):
                        df_mark_real_entry_points.loc[ix] = val
    
                    # Mark the actual take-profits that would have been actually made, in order to do this first create an NaN df that contains the same indices as the original df
                    # Then assign to each index of the actual_long_entries its corresponding price from the "High Price" column of the df
                    df_mark_real_tp_points = pd.DataFrame([float('nan')]*len(df),index=df.index,columns=['Bullish Entries'])
                    for ix,val in zip(actual_long_entries['End Index'].values,df["High Price"][actual_long_entries['End Index']].values):
                        df_mark_real_tp_points.loc[ix, 'Bullish Entries'] = val
                    
                    # Update the final df with parameter window size value 14
                    final_df_ws_7 = final_df_ws_7.append({"Symbol": symbol, "Avg Time Spent (hours)":round(possible_long_entries['Hours Spent'].mean(),2),
                                                            "Expected ROI per trade":expected_roi, "Total Number of Trades":(actual_long_entries.index.values[-1]+1),
                                                            "Total Potential ROI":round(possible_long_entries['Bullish Percentage Change'].sum(),2)}, ignore_index=True)
        except BinanceAPIException:
            continue        
        except Timeout:
            print("")
            print("The request that was sent to the Binance Server has surpassed the queue time set.")
            print("The reason for this error may have to do with a problem with your Internet Connection, or the Binance Server is too busy at the moment.")
            print("But rest assured, I'm going to send the request again to continue with my process.")
            time.sleep(4)
            while True: 
                try:
                    client = Client(api_key= api_key, api_secret= secret_key, tld= "com")
                    break
                except Exception:
                    print("")
                    print("Hmph it seems that you are not connected to the internet, first make sure to be connected before executing this program")
                    input("Once done, press 'Enter' key:")
                    
# Last magic trick
final_df_ws_7 = final_df_ws_7.astype({"Total Number of Trades": int})
final_df_ws_7 = final_df_ws_7.sort_values(by=["Total Number of Trades", "Expected ROI per trade", "Avg Time Spent (hours)", "Total Potential ROI"], 
                                            ascending=[False, False, True, False])
end = time.perf_counter()
print(final_df_ws_7.iloc[0:10]) #Print the top 10 trading pairs that worked well with this strategy and parameter
print(final_df_ws_7.iloc[0:10, [1,2,3,4]].sum()) #Print the sum of the last 4 columns to have an idea about how well this performed
print(f"Time elapsed: {end - start:0.6f} seconds")
print()

# Do a simulation based on the top 10 trading pairs

# Substract to 0.20% trading fees to every Expected Roi Per Trade and them to 2 decimal places
percentage_increase = [round(x-0.20, 2) for x in list((final_df_ws_7["Expected ROI per trade"].iloc[0:10]).values)]

# Round the hours spent to 2 decimal places
hours_spent = [round(x, 2) for x in list((final_df_ws_7["Avg Time Spent (hours)"].iloc[0:10]).values)]

# Set an initial investment ($)
initial_investment = 50

# Initialize the df
df_simulation = pd.DataFrame(columns=["Current Funds", "Hours Spent"])
df_simulation = df_simulation.append({"Current Funds": initial_investment, "Hours Spent": 0}, ignore_index=True)

# Run it until you have made 100x your initial investment
while df_simulation["Current Funds"].iloc[-1] < initial_investment*100:
    index = random.choice(range(len(percentage_increase)))
    current_funds = df_simulation["Current Funds"].iloc[-1]
    df_simulation = df_simulation.append({"Current Funds": (current_funds + (current_funds * percentage_increase[index] / 100)),
                                          "Hours Spent": df_simulation["Hours Spent"].iloc[-1] + hours_spent[index]}, ignore_index=True)
# Print results
print(df_simulation.iloc[-10:])
print(f'Total amount of trades simulated: {len(df_simulation)}')
print(f"Hours spent: {round(df_simulation['Hours Spent'].iat[-1],2)}")
