# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 13:47:15 2023

@author: Noah
"""

#Price Action Analysis using upper and lower bounds and the median and plotting with Streamlit

from binance.client import Client
import pandas as pd
import numpy as np
import streamlit as st
from bokeh.plotting import figure

def set_pandas_display_options() -> None:
    """Set pandas display options."""
    # Ref: https://stackoverflow.com/a/52432757/
    display = pd.options.display

    display.max_columns = 10
    display.max_colwidth = 100
    display.width = 200
    display.precision = 6  # set as needed

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


# Create the plot elements using Bokeh

timeframe_seconds = (df["Start Date"].iat[1] - df["Start Date"].iat[0]).total_seconds()
inc = df["Close Price"] > df["Open Price"]
dec = df["Open Price"] > df["Close Price"]
timeframe_to_miliseconds = timeframe_seconds*1000/2 #half the timeframe in milliseconds

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

# Plot elements of the regular entries
p = figure(x_axis_type="datetime", tools=TOOLS, width=720, height=720,
           title=f"{symbol} - {timeframe}", background_fill_color="#efefef")
p.xaxis.major_label_orientation = 0.8 # radians

p.segment(df["Start Date"], df["High Price"], df["Start Date"], df["Low Price"], color="black")

p.vbar(df["Start Date"][dec], timeframe_to_miliseconds, df["Open Price"][dec], df["Close Price"][dec], color="#eb3c40")
p.vbar(df["Start Date"][inc], timeframe_to_miliseconds, df["Open Price"][inc], df["Close Price"][inc], color="#49a3a3", line_width=2)
p.line(df["Start Date"], pd.DataFrame(upper_bound)["Close Price"], line_width=1.5, color='#F93BFF', legend_label='Upper Bound')
p.line(df["Start Date"], pd.DataFrame(lower_bound)["Close Price"], line_width=1.5, color='black', legend_label='Lower Bound')
p.triangle(df["Start Date"], df_mark_entry_points['Bullish Entries'], size=10, color="#0AE318", alpha=1, legend_label = 'Regular Long Entry Points') # Mark Regular Long Entry Points
p.inverted_triangle(df["Start Date"], df_mark_tp_points['Bullish Entries'], size=10, color="#F43E3E", alpha=1, legend_label = 'Regular Take Profit Points') # Mark Regular Take Profit Points

p.legend.location = "top_left"

# Plot elements of the recommended entries
p_2 = figure(x_axis_type="datetime", tools=TOOLS, width=720, height=720,
           title=f"{symbol} - {timeframe}", background_fill_color="#efefef")
p_2.xaxis.major_label_orientation = 0.8 # radians

p_2.segment(df["Start Date"], df["High Price"], df["Start Date"], df["Low Price"], color="black")

p_2.vbar(df["Start Date"][dec], timeframe_to_miliseconds, df["Open Price"][dec], df["Close Price"][dec], color="#eb3c40")
p_2.vbar(df["Start Date"][inc], timeframe_to_miliseconds, df["Open Price"][inc], df["Close Price"][inc], color="#49a3a3", line_width=2)
p_2.line(df["Start Date"], pd.DataFrame(upper_bound)["Close Price"], line_width=1.5, color='#F93BFF', legend_label='Upper Bound')
p_2.line(df["Start Date"], pd.DataFrame(lower_bound)["Close Price"], line_width=1.5, color='black', legend_label='Lower Bound')
p_2.triangle(df["Start Date"], df_mark_real_entry_points['Bullish Entries'], size=10, color="#1266E6", alpha=1, legend_label = 'Recommended Long Entry Points') # Mark Recommended Long Entry Points
p_2.inverted_triangle(df["Start Date"], df_mark_real_tp_points['Bullish Entries'], size=10, color="#6A0B02", alpha=1, legend_label = 'Recommended Take Profit Points') # Mark Recommended Take Profit Points

p_2.legend.location = "top_left"

# Create a financial report with Streamlit framework

# Write the tittle
st.markdown(f"<h1 style='color: black; font-size:34px'>Price action analysis report for {symbol}</h1>", unsafe_allow_html=True)

# Write the headers for input parameters
st.markdown(f"<h1 style='color: black; font-size:20px'>Timeframe: {timeframe}</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style='color: black; font-size:20px'>Start Date: {start_date}</h1>", unsafe_allow_html=True)

# Write the headers for statistical insights
if (abs(skewness_value) > 0.5):    
    st.markdown(f"<h2 style='color: gray; font-size:20px'>Skewness Value: {round(skewness_value,4)}</h2>", unsafe_allow_html=True)
    if kurtosis_value > 3:
        st.markdown(f"<h2 style='color: gray; font-size:20px'>Kurtosis Value: {round(kurtosis_value,4)}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='color: black; font-size:20px'>The percentage increase between bounds follows a Leptokurtic distribution, and the median (suggested ROI per trade) is: {expected_roi}%</h1>", unsafe_allow_html=True)
    elif kurtosis_value < 3:
        st.markdown(f"<h2 style='color: gray; font-size:20px'>Kurtosis Value: {round(kurtosis_value,4)}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='color: black; font-size:20px'>The percentage increase change between bounds follows a Platikurtic distribution, and the median (suggested ROI per trade) is: {expected_roi}%", unsafe_allow_html=True)
elif (abs(skewness_value) <= 0.5):    
    st.markdown(f"<h2 style='color: gray; font-size:20px'>Skewness Value: {round(skewness_value,4)}</h2>", unsafe_allow_html=True)
    if kurtosis_value > 3:
        st.markdown(f"<h2 style='color: gray; font-size:20px'>Kurtosis Value: {round(kurtosis_value,4)}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='color: black; font-size:20px'>The percentage increase between bounds follows a Leptokurtic distribution, and the mean (suggested ROI per trade) is: {expected_roi}%'", unsafe_allow_html=True)
    elif kurtosis_value < 3:
        st.markdown(f"<h2 style='color: gray; font-size:20px'>Kurtosis Value: {round(kurtosis_value,4)}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='color: black; font-size:20px'>The percentage increase between bounds follows a Platikurtic distribution, and the mean (suggested ROI per trade) is: {expected_roi}%'", unsafe_allow_html=True)

# Write the header for possible_long_entries
st.markdown("<h2 style='color: gray; font-size:20px'>Table of regular long entries made using only the upper and lower bounds:</h2>", unsafe_allow_html=True)

# Display the possible_long_entries DataFrame
st.dataframe(possible_long_entries)

# Write the subheader for sum of potential roi per trades of possible_long_entries
st.markdown(f"<h3 style='color: gray; font-size:20px'>Total sum of potential roi per trades is: {round(possible_long_entries['Bullish Percentage Change'].sum(),2)}%</h3>", unsafe_allow_html=True)

# Write the subheader for average time spent per trade of possible_long_entries
st.markdown(f"<h3 style='color: gray; font-size:20px'>The average time spent per trade was: {round(possible_long_entries['Hours Spent'].mean(),2)} hours</h3>", unsafe_allow_html=True)

# Write the header for actual_long_entries
st.markdown("<h2 style='color: gray; font-size:20px'>Table of recommended long entries made using only the lower bound and the median:</h2>", unsafe_allow_html=True)

# Display the actual_long_entries DataFrame
st.dataframe(actual_long_entries)

# Write the subheader for sum of potential roi per trades of actual_long_entries
st.markdown(f"<h3 style='color: gray; font-size:20px'>Total sum of potential roi per trades is: {round(actual_long_entries['Bullish Percentage Change'].sum(),2)}%</h3>", unsafe_allow_html=True)

# Write the subheader for average time spent per trade of actual_long_entries
st.markdown(f"<h3 style='color: gray; font-size:20px'>The average time spent per trade was: {round(actual_long_entries['Hours Spent'].mean(),2)} hours</h3>", unsafe_allow_html=True)

# Plot the Bokeh candlestick chart with the regular entries
st.markdown("<h2 style='color: black; font-size:20px'>Plot of Regular Long Entries</h2>", unsafe_allow_html=True)
st.bokeh_chart(p)

st.markdown("<h2 style='color: black; font-size:20px'>Plot of Recommended Long Entries</h2>", unsafe_allow_html=True)
st.bokeh_chart(p_2)

if df['Close Price'].iat[-1] <= lower_bound.iat[-1]:
    st.markdown(f"<h2 style='color: black; font-size:20px'>Currently, as the close price of {symbol} is greater than the estimated upper boud value, the future price is likely to go up.</h2>", unsafe_allow_html=True)
elif df['Close Price'].iat[-1] >= upper_bound.iat[-1]:
    st.markdown(f"<h2 style='color: black; font-size:20px'>Currently, as the close price of {symbol} is less than the estimated upper boud value, the future price is likely to go down.</h2>", unsafe_allow_html=True)
else:
    st.markdown(f"<h2 style='color: black; font-size:20px'>Currently, the close price of {symbol} is likely to remain stable.</h2>", unsafe_allow_html=True)
