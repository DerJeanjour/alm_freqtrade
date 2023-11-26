import numpy as np
import pandas as pd
from pandas import DataFrame

from freqtrade.strategy.interface import IStrategy

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class AlmStrategy(IStrategy):
    INTERFACE_VERSION = 3

    can_short: bool = False

    minimal_roi = {
        "40": 0.2,
        "0": 0.5
    }

    stoploss = -0.15
    trailing_stop = False
    timeframe = '5m'
    process_only_new_candles = False

    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    startup_candle_count: int = 200

    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    order_time_in_force = {
        'entry': 'GTC',
        'exit': 'GTC'
    }

    plot_config = {
        'main_plot': {
            'tema': {},
            'sar': {'color': 'white'},
        },
        'subplots': {
            "MACD": {
                'macd': {'color': 'blue'},
                'macdsignal': {'color': 'orange'},
            },
            "RSI": {
                'rsi': {'color': 'red'},
            }
        }
    }

    # get additional pairs, accessible by the DataProvider
    def informative_pairs(self):
        return []

    # will be executed first
    # add additional data to entries, used by the buy and sell functions
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe)
        return dataframe

    # will be after populate_indicators
    # funtion to mark entries to buy
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] < 30)
            ),
            'enter_long'] = 1
        return dataframe

    # will be after populate_entry_trend
    # funtion to mark entries to sell
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > 70)
            ),
            'exit_long'] = 1
        return dataframe
