import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df =  pd.read_csv("https://raw.githubusercontent.com/dswh/python_fundamentals/master/images/apple_stock_eod_prices.csv",
                parse_dates=True, header=0, index_col=0)

# Initialize the short and long windows
short_window = 50
long_window = 120

# Initialize alpha
alpha = 0.1

# Create a new dataframe called signals with indices taken from our original dataframe.
signals = pd.DataFrame(index=df.index)

print(signals)

# Initialize to zeros
signals['ema_signal'] = 0.0

# Create exponential moving average values for an alpha value
signals['ema'] =  df['Close'].ewm(alpha=alpha, adjust=False).mean()

# Initialize to zeros
signals['ema_positions'] = 0.0

# Initialize to zeros
signals['sma_signal'] = 0.0

# Create short simple moving average over the short window. We use the following arguments for the 'rolling' method

# min_periods = 1 - Minimum number of observations in window required to have a value (otherwise result is NA).  

# center = False, so that the labels are not set at the center of the window (default value is actually False,
# so even if we did not use this argument, that would be alright).   
signals['short_mavg'] =  df['Close'].rolling(window=short_window, min_periods=1, center=False).mean()

# Create long simple moving average over the long window. We use the following arguments for the 'rolling' method

# min_periods = 1 - Minimum number of observations in window required to have a value (otherwise result is NA).  

# center = False, so that the labels are not set at the center of the window (default value is actually False,
# so even if we did not use this argument, that would be alright).  
signals['long_mavg'] = df['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

# Initialize to zero
signals['sma_positions'] = 0.0

print(signals)

# Change signal values to 1 whenever it is above the price
signals['ema_signal'] = np.where(signals['ema'] > df['Close'], 1.0, 0.0)

# Calculate the position values. Whenever the signal changes from 0 to 1, we will obtain a value of +1
# Whenever the signal changes from 1 to 0, we will obtain a value of -1
signals['ema_positions'] = signals['ema_signal'].diff()

print(signals)

# Initialize the plot figure
fig = plt.figure(figsize=(12,10))

# Add a subplot and label for y-axis
ax1 = fig.add_subplot(111,  ylabel='Price in $')

# Make a subset of signals from January 2018 for clearer visualization
signals2 = signals.loc['2018-01-01':,:]

# Plot the closing price
df.loc['2018-01-01':,'Close'].plot(ax=ax1, color='r', lw=2.,label='Close Price')

# Plot the short and long moving averages
signals2.loc[:,'ema'].plot(ax=ax1, lw=2.)

# Plot the buy signals
ax1.plot(signals2.loc[signals2.ema_positions == 1.0].index,
         signals2.ema[signals2.ema_positions == 1.0],
         'o', markersize=10, color='r')

# Plot the sell signals
ax1.plot(signals2.loc[signals2.ema_positions == -1.0].index,
         signals2.ema[signals2.ema_positions == -1.0],
         '^', markersize=10, color='g')

plt.legend()

fig.savefig('strategy_1_signals.png')

# Create signals in the same way we did so in step 3, but this time we assign 1 as a signal whenever the short
# MA is above the long MA

# Since we are using iloc, we need to specify the integer values of the columns. 3, 4 and 5 correspond to the
# 'sma_signal', 'short_mavg' and 'long_mavg' respectively
signals.iloc[short_window:,3] = np.where(signals.iloc[short_window:,4]
                                            > signals.iloc[short_window:,5], 1.0, 0.0)

# Create trading orders similarly to how we did in step 3
signals['sma_positions'] = signals['sma_signal'].diff()
print(signals)

# Initialize the plot figure
fig = plt.figure(figsize=(12,10))

# Add a subplot and label for y-axis
ax1 = fig.add_subplot(111,  ylabel='Price in $')

# Plot the closing price
df['Close'].plot(ax=ax1, color='r', lw=2.,label='Close Price')

# Plot the short and long moving averages
signals[['short_mavg', 'long_mavg',]].plot(ax=ax1, lw=2.)

# Plot the buy signals
ax1.plot(signals.loc[signals.sma_positions == 1.0].index,
         signals.short_mavg[signals.sma_positions == 1.0],
         '^', markersize=10, color='g')

# Plot the sell signals
ax1.plot(signals.loc[signals.sma_positions == -1.0].index,
         signals.short_mavg[signals.sma_positions == -1.0],
         'o', markersize=10, color='r')

plt.legend()

fig.savefig('strategy_2_signals.png')
