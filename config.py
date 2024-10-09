import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

config = {
    "alpha_vantage": {
        "key": os.getenv("API_KEY"),  # API key for Alpha Vantage
        "outputsize": "compact",      # Smaller output for faster response
        "key_close": "4. close",      # Which key to use for closing price
    },
    "data": {
        "window_size": 20,            # Window size for LSTM input
    },
    "model": {
        "input_size": 1,              # Number of features (just close price)
        "num_lstm_layers": 2,         # Number of LSTM layers
        "lstm_size": 32,              # Size of LSTM hidden layer
        "dropout": 0.2,               # Dropout rate
    },
    "training": {
        "device": "cpu",              # Use CPU for inference
    }
}
