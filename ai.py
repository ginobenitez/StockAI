import yfinance as yf
import pandas as pd
from pandas.io.formats.style import Styler
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.metrics import precision_score
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

def get_company_data(ticker):
    try:
        company = yf.Ticker(ticker)
        company_data = company.history(period = "max")
        return company_data
    except Exception as e:
        print("Error fetching data for company, please check again")
        print(e)
        return None

def stock_price_prediction(ticker):
    # Fetch historical stock data
    currCompany = get_company_data(ticker)

    # Define features and target variable
    predictor_list = ["Close", "Volume", "Open", "High", "Low"]
    currCompany["Tomorrow"] = currCompany["Close"].shift(-1)
    currCompany["Target"] = (currCompany["Tomorrow"] > currCompany["Close"]).astype(int)
    currCompany = currCompany.loc["1995-01-01":].copy()

    # Split the data into training and testing sets
    training = currCompany.iloc[:-110]
    testing = currCompany.iloc[-110:]

    # Hyperparameter tuning with GridSearchCV
    '''param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }'''
    param_grid = {
        'n_estimators': [100],# Change this to 100 later
        'max_depth': [None, 10],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }

    model = RFC(random_state=1)
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='precision')
    grid_search.fit(training[predictor_list], training["Target"])

    # Get the best model from the grid search
    best_model = grid_search.best_estimator_

    # Make predictions on the testing set
    preds = best_model.predict(testing[predictor_list])
    precision = precision_score(testing["Target"], preds)

    # Map binary values to user-friendly labels using a list comprehension
    label_mapping = {0: "Sell", 1: "Buy"}
    actual_labels = [label_mapping[val] for val in testing["Target"]]
    predicted_labels = [label_mapping[val] for val in preds]

    # Create a DataFrame with predictions
    predictions = pd.DataFrame({
        "Date": testing.index.date,
        "Actual": actual_labels,
        "Predicted": predicted_labels
    })
    return predictions, precision

def plot_historical_data(ticker):
    try:
        company = yf.Ticker(ticker)
        
        # Fetch historical data for the last 15 years
        end_date = pd.Timestamp.now()
        start_date = end_date - pd.DateOffset(years=1)
        company_data = company.history(start=start_date, end=end_date)

        # Plot historical Close prices
        plt.figure(figsize=(12, 6))
        plt.plot(company_data.index, company_data['Close'], label=f'{ticker} Close Price', color='b')
        plt.title(f'Historical Close Prices for {ticker} (Last 1 Year)')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()
        plt.grid()
        plt.show()

    except Exception as e:
        print("Error fetching data for company, please check again")
        
