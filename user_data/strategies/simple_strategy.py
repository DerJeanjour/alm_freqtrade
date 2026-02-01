# Import necessary libraries
from freqtrade.strategy import IStrategy
import talib.abstract as ta
from pandas import DataFrame

class SimpleStrategy(IStrategy):

    can_short: bool = False

    # --- SAFETY SETTINGS ---
    # 1. ROI (Return on Investment): If we make 10% profit, sell immediately.
    minimal_roi = {
        "0": 0.10
    }

    # 2. STOPLOSS: If we lose 5%, sell immediately to prevent losing more.
    stoploss = -0.05

    # 3. TIMEFRAME: Look at the chart candles every 1 hour.
    timeframe = '1h'

    # --- LOGIC STEP 1: Get the Data ---
    def populate_indicators(self, dataframe, metadata):
        # Calculate the RSI (The Rubber Band Meter) for the price data
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        return dataframe

    # --- LOGIC STEP 2: When to Buy? ---
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # "enter_long" means BUY.
        # We buy if RSI is LESS than 30 (Rubber band stretched down)
        dataframe.loc[
            (dataframe['rsi'] < 30),
            'enter_long'] = 1
        return dataframe

    # --- LOGIC STEP 3: When to Sell? ---
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # "exit_long" means SELL.
        # We sell if RSI is GREATER than 70 (Rubber band stretched up)
        dataframe.loc[
            (dataframe['rsi'] > 70),
            'exit_long'] = 1
        return dataframe