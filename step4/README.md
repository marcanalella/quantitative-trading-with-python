# 4 - Developing a Trading Strategy

it's time to build our moving average crossover strategy! The most common applications of moving averages are to identify trend direction and to determine support and resistance levels.

We shall be applying two strategies:

1. Price crossover, which is when the price crosses above or below a moving average to signal a potential change in trend. We will use an exponential weighted moving average for this.

2. Another strategy is to apply two moving averages to a chart, one longer and one shorter. When the shorter-term MA crosses above the longer-term MA, it's a buy signal, as it indicates that the trend is shifting up. This is known as a "golden cross." Meanwhile, when the shorter-term MA crosses below the longer-term MA, it's a sell signal, as it indicates that the trend is shifting down. This is known as a "dead/death cross."
For the first step, we will import our libraries, read our data, compute simple moving average for two windows (short term of 50 and long term of 120), and compute exponential moving average with alpha of 0.1. We will create a separate dataframe to store these values.

At the same time, for both the strategies, we will initialize a 'signals' column and a 'positions' column. We shall explain what these two columns are in subsequent steps. This should serve as a recap from the previous labs.