"""
Module that defines methods/functions which can be used to fetch symbols
related data.
"""

from .utils import fetch_urls_json_data

import os
import sys
import asyncio
import pandas as pd


# Condition to set the policy for windows otherwise asyncio will throw
# runtime 'event loop closed error'.
if (
    sys.version_info[0] == 3 and
    sys.version_info[1] >= 8 and
    sys.platform.startswith('win')
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def fetch_symbols_based_time_series_intraday_data(symbols, interval):
    """Fetches intraday time series data for a list of symbols.

    Args:
        symbols (List[str]): List of symbols for which to fetch data.
        interval (str): Time interval for the data (e.g., '1min',
            '5min', '15min', '30min', '60min').

    Returns:
        list: List of JSON responses containing intraday time series
        data for each symbol.
    """

    api_key = 'E65YE0OJS72PFY26'
    alpha_avantage_api_url = (
        'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&' +
        'symbol={}&interval={}&apikey={}'
    )
    symbol_based_api_urls = []
    for symbol in symbols:
        symbol_based_api_urls.append(
            alpha_avantage_api_url.format(symbol, interval, api_key)
        )
    return asyncio.run(fetch_urls_json_data(symbol_based_api_urls))


def get_symbols_latest_and_graph_data(symbols, interval='5min'):
    """Retrieves the latest prices and candlestick graph data for
    a list of symbols. Also, when an api is called 6th time within
    a single minute then this function returns with 429 error, and
    when symbol data is not available then that symbol is not included
    in the response.

    Args:
        symbols (list): List of symbols for which to fetch data.
        interval optional(str): Time interval for the data (default: '5min').

    Returns:
        dict: A dictionary containing the following information:
            - symbols (list): List of symbols for which data was retrieved.
            - values (list): List of names of values for each data point (eg:
                open, close, volume and etc.).
            - latest_prices (dict): Dictionary mapping symbols to their
                latest prices.
            - candle_stick_graph_data (dict): Dictionary mapping symbols
                to their candlestick graph data.
    """

    # Removing duplicate symbols.
    symbols = list(set(symbols))

    symbols_intraday_data = fetch_symbols_based_time_series_intraday_data(
        symbols, interval
    )

    symbols_latest_prices_dict = dict()
    symbols_candle_stick_graph_dict = dict()
    fetched_symbols = []
    values = []

    for index, symbol_data in enumerate(symbols_intraday_data):

        # Whenever a note is returned with a thank you message in response
        # from api, then that means we have called apis 6 times in a row
        # within a single minute, which is not allowed with free subscription.
        if 'Note' in symbol_data and 'Thank you' in symbol_data['Note']:
            return {
                "Note": "You have reached the limit of 5 calls per minute."
            }

        # If data is not provided for a specific symbol from api then that means
        # either the symbol is invalid or the data for that symbol is not available
        # for free subscription. So, we are not including that particular symbol
        # in our response.
        if 'Error Message' in symbol_data:
            continue

        symbol_name = symbol_data['Meta Data']['2. Symbol']
        symbol_data_df = pd.DataFrame(
            symbol_data['Time Series ({})'.format(interval)]
        )
        symbol_data_df = symbol_data_df.transpose()
        symbol_data_df['6. date_time'] = symbol_data_df.index
        symbol_data_df.reset_index(inplace=True, drop=True)
        symbol_data_df.columns = symbol_data_df.columns.str[3:]

        fetched_symbols.append(symbol_name)
        symbols_latest_prices_dict[symbol_name] = symbol_data_df.iloc[-1]
        symbols_candle_stick_graph_dict[symbol_name] = (
            symbol_data_df.to_numpy().tolist()
        )

        values = symbol_data_df.columns.tolist()

    response = {
        "symbols": fetched_symbols,
        "values": values,
        "latest_prices": symbols_latest_prices_dict,
        "candle_stick_graph_data": symbols_candle_stick_graph_dict
    }

    return response
