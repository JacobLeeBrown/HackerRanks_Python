"""Modified from https://www.cryptodatadownload.com/blog/how-to-download-coinbase-price-data.html
"""
import math
import pandas as pd
import requests
import json
from datetime import date
import time
import hackerranks.time_util as t
import urllib.parse as urlp

START_OF_2016 = 1451606400  # Jan. 1st, 2016 @ 00:00:00 GMT
# The granularity field must be one of the following values: {60, 300, 900, 3600, 21600, 86400}
MINUTE, FIVE_MINUTES, FIFTEEN_MINUTES, HOURLY, SIX_HOURS, DAILY = 60, 300, 900, 3600, 21600, 86400
SECONDS_TO_GRANULARITY = {60: 'MINUTE', 300: 'FIVE_MINUTES', 900: 'FIFTEEN_MINUTES', 3600: 'HOURLY', 21600: 'SIX_HOURS', 86400: 'DAILY'}
MAX_RECORDS = 300


def fetch_data(symbol, rate_s):
    # Will fetch the last MAX_RECORDS entries at the given rate, using the current timestamp as the end of the range
    url = f'https://api.pro.coinbase.com/products/{symbol}/candles?granularity={rate_s}'
    response = requests.get(url)

    if response.status_code == 200:  # check to make sure the response from server is good
        data = pd.DataFrame(json.loads(response.text), columns=['unix', 'low', 'high', 'open', 'close', 'volume'])
        data['date'] = pd.to_datetime(data['unix'], unit='s')  # convert to a readable date
        data['vol_fiat'] = data['volume'] * data['close']      # approximate fiat volume

        # if we failed to get any data, print an error...otherwise write the file
        if data is None:
            print("Did not return any data from Coinbase for this symbol")
        else:
            today = date.today().strftime("%Y-%m-%d")
            data.to_csv(f'CoinbaseData_{symbol}_{today}.csv', index=False)

    else:
        print("Did not receive OK response from Coinbase API")


def fetch_data_since(symbol, rate_s, start):
    # Will fetch all Coinbase data for the symbol, with granularity of `rate_s`, starting at timestamp `start` (in epoch
    # seconds). Determines how many requests to make and will set query params accordingly for each request.
    total_records = math.ceil((t.current_s_time() - start) / rate_s)
    total_requests = math.ceil(total_records / MAX_RECORDS)
    coinbase_cols = ['unix', 'low', 'high', 'open', 'close', 'volume']
    data = pd.DataFrame(columns=coinbase_cols)

    print(f"INFO  - Total expected record count = {total_records}")
    print(f"INFO  - Total requests to make      = {total_requests}")

    successful = True
    base_url = f'https://api.pro.coinbase.com/products/{symbol}/candles?granularity={rate_s}'
    for i in range(total_requests):
        end = start + ((MAX_RECORDS - 1) * rate_s)
        request_url = base_url + get_and_encode_time_range(start, end)
        print(f"INFO  - Making request #{i+1} to Coinbase: {request_url}")
        response = requests.get(request_url)
        if response.status_code == 200:
            # Add response data to result
            data = pd.concat([data, pd.DataFrame(json.loads(response.text), columns=coinbase_cols)], ignore_index=True)
            print("INFO  - Got 200 Response from Coinbase. Data size = " + str(data.shape))
        else:
            print("ERROR - Did not receive OK response from Coinbase API:\n" + response.text)
            successful = False
            break
        start += MAX_RECORDS * rate_s
        time.sleep(0.2)  # Delay between requests to not surpass Coinbase limit

    if successful:
        # Post-processing
        data['date'] = pd.to_datetime(data['unix'], unit='s')  # convert timestamp to a readable date
        data['vol_fiat'] = data['volume'] * data['close']      # approximate fiat volume

        data.sort_values(by=['unix'], inplace=True)

        start_date = date.fromtimestamp(start).strftime("%Y%m%d")
        today = date.today().strftime("%Y%m%d")
        data.to_csv(f'CoinbaseData_{symbol}_{start_date}-{today}_{rate_s_to_string(rate_s)}.csv', index=False)


def rate_s_to_string(rate_s):
    if SECONDS_TO_GRANULARITY[rate_s] is not None:
        return SECONDS_TO_GRANULARITY[rate_s]
    else:
        return 'UNKNOWN_RATE'


def get_and_encode_time_range(start, end):
    date_format = '%Y-%m-%dT%XZ'
    start_datetime = date.fromtimestamp(start).strftime(date_format)
    end_datetime = date.fromtimestamp(end).strftime(date_format)
    return f'&start={urlp.quote(start_datetime)}&end={urlp.quote(end_datetime)}'


if __name__ == "__main__":
    # we set which pair we want to retrieve data for
    # Format must be {crypto}-{currency}
    pair = "BTC-USD"
    fetch_data_since(symbol=pair, rate_s=DAILY, start=START_OF_2016)
