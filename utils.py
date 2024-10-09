import numpy as np
from alpha_vantage.timeseries import TimeSeries
from config import config

# Class for normalization
class Normalizer():
    def __init__(self):
        self.mu = None
        self.sd = None

    def fit_transform(self, x):
        self.mu = np.mean(x, axis=(0), keepdims=True)
        self.sd = np.std(x, axis=(0), keepdims=True)
        return (x - self.mu) / self.sd

    def inverse_transform(self, x):
        return (x * self.sd) + self.mu

# Function to download data from Alpha Vantage
def download_data(symbol):
    ts = TimeSeries(config["alpha_vantage"]["key"])
    data, _ = ts.get_daily(symbol, outputsize=config["alpha_vantage"]["outputsize"])
    
    data_date = list(data.keys())
    data_date.reverse()

    data_close_price = [float(data[date][config["alpha_vantage"]["key_close"]]) for date in data.keys()]
    data_close_price.reverse()
    data_close_price = np.array(data_close_price)

    return data_close_price

# Prepare data for LSTM input
def prepare_data_x(x, window_size):
    n_row = x.shape[0] - window_size + 1
    output = np.lib.stride_tricks.as_strided(x, shape=(n_row, window_size), strides=(x.strides[0], x.strides[0]))
    return output[:-1], output[-1]
