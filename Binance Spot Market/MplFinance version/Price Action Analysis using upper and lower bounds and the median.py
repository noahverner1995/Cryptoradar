# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 01:32:57 2023

@author: Noah
"""

from binance.client import Client
import pandas as pd
import mplfinance as mpf
import numpy as np

def set_pandas_display_options() -> None:
    """Set pandas display options."""
    # Ref: https://stackoverflow.com/a/52432757/
    display = pd.options.display

    display.max_columns = 10
    display.max_colwidth = 100
    display.width = 200
    display.precision = 6  # set as needed

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

trading_pair = ""
symbol = trading_pair.replace("USDT", "")+"/"+"USDT"
timeframe = "" # For instance: 3m, 15m, 1h, 2h...
start_date = "" # For instance: 400 hours ago UTC, 1 week UTC, 5 days ago UTC...

klines = client.get_historical_klines(symbol=trading_pair, interval=timeframe, start_str = start_date)

# Customize the df_trading_pair that stored klines
df = klines_to_df(pd.DataFrame(klines))

df_trading_pair_date_time_index = set_DateTimeIndex(df)

# Calculate moving average and std deviation of the close price

window_size = 14
rolling_mean = df['Close Price'].rolling(window=window_size).mean()
rolling_std = df['Close Price'].rolling(window=window_size).std()

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
    if kurtosis_value > 3:
        print(f'The bullish percentage change between bounds follows a Leptokurtic distribution, and the median (suggested ROI per trade) is {expected_roi}%')
    elif kurtosis_value < 3:
        print(f'The bullish percentage change between bounds follows a Platikurtic distribution, and the median (suggested ROI per trade) is {expected_roi}%')

elif (abs(skewness_value) <= 0.5):
    
    # Use the mean to properly estimate the return on investment per trade
    expected_roi = bullish_percentage_change_between_bounds.mean()
    if kurtosis_value > 3:
        print(f'The bullish percentage change between bounds follows a Leptokurtic distribution, and the mean (suggested ROI per trade) is {expected_roi}%')
    elif kurtosis_value < 3:
        print(f'The bullish percentage change between bounds follows a Platikurtic distribution, and the mean (suggested ROI per trade) is {expected_roi}%')

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

# Store the plots of upper and lower bounds as well as the possible for later use
plots_to_add = {"Upper Bound":mpf.make_addplot(upper_bound,color='#F93BFF'), "Lower Bound":mpf.make_addplot(lower_bound,color='white'),
                "Regular Long Entry Points":mpf.make_addplot(df_mark_entry_points,type='scatter',markersize=50,marker='^', color='#00FFE0'),
                "Regular Take Profit Points":mpf.make_addplot(df_mark_tp_points,type='scatter',markersize=50,marker='v', color='#FFF000')
                }

print()
# Plot the Close Price, Moving average, upper and lower bounds using a line chart.

# Plotting
# Create my own `marketcolors` style:
mc = mpf.make_marketcolors(up='#2fc71e',down='#ed2f1a',inherit=True)
# Create my own `MatPlotFinance` style:
s  = mpf.make_mpf_style(base_mpl_style=['bmh', 'dark_background'],marketcolors=mc, y_on_right=True)    

# Plot it
candlestick_plot, axlist = mpf.plot(df_trading_pair_date_time_index,
                    figsize=(40,20),
                    figratio=(10, 6),
                    type="candle",
                    style=s,
                    tight_layout=True,
                    datetime_format = '%b %d, %H:%M:%S',
                    ylabel = "Price ($)",
                    returnfig=True,
                    show_nontrading=True,
                    warn_too_much_data=870, # Silence the Too Much Data Plot Warning by setting a value greater than the amount of rows you want to be plotted
                    addplot = list(plots_to_add.values()) # Add the upper and lower bounds plots as well as the bullish entries to the main plot
                    )
# Add Title
symbol = trading_pair.replace("USDT", "")+"/"+"USDT"
axlist[0].set_title(f"{symbol} - {timeframe}", fontsize=45, style='italic', fontfamily='fantasy')

# Set the legends
# First set the amount of legends to add to the legend box
axlist[0].legend([None]*(len(plots_to_add)+2))
# Then Store the legend objects in a variable called "handles", based on this script, your objects to legend will appear from the third element in this list
handles = axlist[0].get_legend().legendHandles
# Finally set the corresponding names for the plotted SMA trends and place the legend box to the lower right corner in the bigger plot
axlist[0].legend(handles=handles[2:],labels=list(plots_to_add.keys()), loc = 'lower left', fontsize = 30)

del candlestick_plot, axlist, plots_to_add

# Store the plots of upper and lower bounds as well as the actual long entries 
plots_to_add = {"Upper Bound":mpf.make_addplot(upper_bound,color='#F93BFF'), "Lower Bound":mpf.make_addplot(lower_bound,color='white'),
                "Recommended Long Entry Points":mpf.make_addplot(df_mark_real_entry_points,type='scatter',markersize=50,marker='^', color='#0042FF'),
                "Recommended Take Profit Points":mpf.make_addplot(df_mark_real_tp_points,type='scatter',markersize=50,marker='v', color='white')
                }

# Plot the Candlesticks, upper and lower bounds, and recommended long entry points and take profit points.

# Plotting
# Create my own `marketcolors` style:
mc = mpf.make_marketcolors(up='#2fc71e',down='#ed2f1a',inherit=True)
# Create my own `MatPlotFinance` style:
s  = mpf.make_mpf_style(base_mpl_style=['bmh', 'dark_background'],marketcolors=mc, y_on_right=True)    

# Plot it
candlestick_plot, axlist = mpf.plot(df_trading_pair_date_time_index,
                    figsize=(40,20),
                    figratio=(10, 6),
                    type="candle",
                    style=s,
                    tight_layout=True,
                    datetime_format = '%b %d, %H:%M:%S',
                    ylabel = "Price ($)",
                    returnfig=True,
                    show_nontrading=True,
                    warn_too_much_data=870, # Silence the Too Much Data Plot Warning by setting a value greater than the amount of rows you want to be plotted
                    addplot = list(plots_to_add.values()) # Add the upper and lower bounds plots as well as the bullish entries to the main plot
                    )
# Add Title
symbol = trading_pair.replace("USDT", "")+"/"+"USDT"
axlist[0].set_title(f"{symbol} - {timeframe}", fontsize=45, style='italic', fontfamily='fantasy')

# Set the legends
# First set the amount of legends to add to the legend box
axlist[0].legend([None]*(len(plots_to_add)+2))
# Then Store the legend objects in a variable called "handles", based on this script, your objects to legend will appear from the third element in this list
handles = axlist[0].get_legend().legendHandles
# Finally set the corresponding names for the plotted SMA trends and place the legend box to the lower right corner in the bigger plot
axlist[0].legend(handles=handles[2:],labels=list(plots_to_add.keys()), loc = 'lower left', fontsize = 30)

# Create a financial report
print(f"The trading pair analyzed was {symbol}")
print("The simulated long entries made using only the upper and lower bounds were the following:")
print(possible_long_entries)
print(f"The total sum of potential roi per trades was: {round(possible_long_entries['Bullish Percentage Change'].sum(),2)}%")
print(f"The average time spent per trade was: {round(possible_long_entries['Hours Spent'].mean(),2)} hours")

print()
print("In contrast, the simulated long entries made using only the lower bound and the median were the following:")
print(actual_long_entries)
print(f"The total sum of potential roi per trades was: {round(actual_long_entries['Bullish Percentage Change'].sum(),2)}%")
print(f"The average time spent per trade was: {round(actual_long_entries['Hours Spent'].mean(),2)} hours")

print()

if df['Close Price'].iloc[-1] > upper_bound.iloc[-1]:
    print(f"Currently, the close price of {symbol} is likely to go up.")
elif df['Close Price'].iloc[-1] < lower_bound.iloc[-1]:
    print(f"Currently, the close price of {symbol} is likely to go down.")
else:
    print(f"Currently, the close price of {symbol} is likely to remain stable.")
