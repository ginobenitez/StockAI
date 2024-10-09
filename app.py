from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from lstm_model import load_model
from utils import download_data, Normalizer, prepare_data_x
from config import config
from datetime import datetime, timedelta
import numpy as np
from mangum import Mangum

app = FastAPI()

handler = Mangum(app)
# Define the request model using Pydantic
class StockRequest(BaseModel):
    symbol: str

# Load model and normalizer globally
model = load_model(config)
scaler = Normalizer()

# Helper function to calculate the next trading day (skipping weekends)
def get_next_trading_day(last_date_str):
    # Convert string date to datetime
    last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
    next_day = last_date + timedelta(days=1)

    # If the next day is Saturday (5) or Sunday (6), move to Monday
    if next_day.weekday() == 5:  # Saturday
        next_day += timedelta(days=2)
    elif next_day.weekday() == 6:  # Sunday
        next_day += timedelta(days=1)

    return next_day.strftime("%Y-%m-%d")

@app.post("/predict/")
def predict_stock(request: StockRequest):
    try:
        # Step 1: Download the stock data
        data_close_price = download_data(request.symbol)
        
        if len(data_close_price) == 0:
            raise ValueError("No data found for the provided stock symbol")

        # Step 2: Get the last available date from the data
        last_data_date = np.datetime_as_string(np.datetime64('today'))  # Assuming today

        # Step 3: Calculate the next trading day
        predicted_date = get_next_trading_day(last_data_date)

        # Step 4: Normalize the data
        normalized_data_close_price = scaler.fit_transform(data_close_price)

        # Step 5: Prepare the data for the LSTM model
        data_x, data_x_unseen = prepare_data_x(normalized_data_close_price, window_size=config["data"]["window_size"])

        # Step 6: Convert the unseen data to tensor for model prediction
        x = torch.tensor(data_x_unseen).float().unsqueeze(0).unsqueeze(2)

        # Step 7: Make the prediction
        with torch.no_grad():
            prediction = model(x).cpu().detach().numpy()

        # Step 8: Inverse transform the prediction to original scale
        predicted_price = scaler.inverse_transform(prediction)

        # Step 9: Return the predicted stock price and the next trading day
        return {
            "symbol": request.symbol,
            "predicted_close_price": round(predicted_price[0], 2),
            "predicted_date": predicted_date
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Out of requests for the day. Try again later!")

    except Exception as e:
        # Log the exception details (you can add proper logging here)
        print(f"Error occurred: {e}")

        # Raise an HTTPException with status code 500 and the error message
        raise HTTPException(status_code=500, detail="Out of requests for the day. Try again later!")
