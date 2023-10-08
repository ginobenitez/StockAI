import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ai
import yfinance as yf

def predict_stock():
    ticker = entry.get()
    if not ticker:
        messagebox.showerroe("Error", "Please enter a ticker symbol")
        return
    
    try:
        predictions, precision = ai.stock_price_prediction(ticker)
        result_label.config(text=f"Predictions for {ticker}:\n{predictions}\n\nEstimated Precision Score (Not Actual): {precision}")
        ai.plot_historical_data(ticker)
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Stock Price Prediction App")

# The following are GUI elements

# Create frame
frame = ttk.Frame(root)
frame.pack(padx=20, pady=20)

# Get the label from the user
label = ttk.Label(frame, text="Enter Company Ticker:")
label.pack()

# Entry field from user input
entry = ttk.Entry(frame)
entry.pack()

# Button to start prediction
predict_button = ttk.Button(frame, text="Predict", command=predict_stock)
predict_button.pack()

# Label to display prediction results
result_label = ttk.Label(frame, text="")
result_label.pack()

# Start the Tkinter main loop
root.mainloop()
