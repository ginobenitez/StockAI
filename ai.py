import yfinance as yf
import pandas as pd
from sklearn.metrics import precision_score
from sklearn.ensemble import RandomForestClassifier as RFC

def predict(train, test, predictors, model):
    model.fit(train[predictors], train["Target"])
    preds = model.predict(test[predictors])
    preds = pd.Series(preds, index=test.index, name="Predictions")
    combined = pd.concat([test["Target"], preds], axis=1)
    return combined

def backtest(data, model, predictors, start=2500, step=250):
    all_predictions = []

    for i in range(start, data.shape[0], step):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:(i+step)].copy()
        predictions = predict(train, test, predictors, model)
        all_predictions.append(predictions)

    return pd.concat(all_predictions)

def predict(train, test, predictors, model):
    model.fit(train[predictors], train["Target"])
    preds = model.predict_proba(test[predictors])[:,1]# This line is different
    preds[preds >= .6] = 1
    preds[preds < .6] = 0
    preds = pd.Series(preds, index=test.index, name="Predictions")
    combined = pd.concat([test["Target"], preds], axis=1)
    return combined

def accuracy():
    # Get data from the company based on the short
    currCompany = yf.Ticker("^GSPC")
    currCompany = currCompany.history(period = "max")

    # All time historical data
    currCompany.plot.line(y = "Close", use_index = True)

    # Remove unnecessary data
    del currCompany["Dividends"]
    del currCompany["Stock Splits"]

    # Create a new Column that will store the data for the predicted day
    # and shift it to the last position
    currCompany["Tomorrow"] = currCompany["Close"].shift(-1)

    # Set a target if tomorrow's price is greater than today
    currCompany["Target"] = (currCompany["Tomorrow"] > currCompany["Close"]).astype(int)

    # Remove data before 1990
    currCompany = currCompany.loc["1995-01-01":].copy()

    # increase estimator value later
    model = RFC(n_estimators = 100, min_samples_split = 100, random_state = 1)

    # Add first columns from data to the training stage,
    # test with the last 100 columns
    training = currCompany.iloc[:-100]
    testing = currCompany.iloc[-100:]

    # These are the parameters the model with consider to make
    # predictions
    predictor_list = ["Close", "Volume", "Open", "High", "Low"]
    model.fit(training[predictor_list], training["Target"])

    RFC(min_samples_split = 100, random_state = 1)

    preds = model.predict(testing[predictor_list])
    preds = pd.Series(preds, index = testing.index)

    precision_score(testing["Target"], preds)

    combined = pd.concat([testing["Target"], preds], axis = 1)

    combined.plot()


    predictions = backtest(currCompany, model, predictor_list)
    predictions["Predictions"].value_counts()

    precision_score(predictions["Target"], predictions["Predictions"])

    predictions["Target"].value_counts() / predictions.shape[0]

    horizons = [2, 5, 60, 250, 1000]

    new_predictors = []
    for horizon in horizons:
        rolling_averages = currCompany.rolling(horizon).mean()

        ratio_column = f"Close_Ratio_{horizon}"
        currCompany[ratio_column] = currCompany["Close"] / rolling_averages["Close"]

        trend_column = f"Trend_{horizon}"
        currCompany[trend_column] = currCompany.shift(1).rolling(horizon).sum()["Target"]

        new_predictors += [ratio_column, trend_column]

        currCompany = currCompany.dropna()

    model = RFC(n_estimators = 200, min_samples_split = 50, random_state = 1)

    predictions = backtest(currCompany, model, new_predictors)

    predictions["Predictions"].value_counts()

    ps = precision_score(predictions["Target"], predictions["Predictions"])
    
    return ps    




