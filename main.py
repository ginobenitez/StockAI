import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ai
import yfinance as yf
import pandas as pd
from tkinter import scrolledtext

pd.set_option('display.max_rows', None)

def predict_stock():
    ticker = entry.get()
    if not ticker:
        messagebox.showerror("Error", "Please enter a ticker symbol")
        return
    
    try:
        predictions, precision = ai.stock_price_prediction(ticker)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Predictions for {ticker}:\n{predictions}\n\nEstimated Precision Score (Not Actual): {precision}")
        ai.plot_historical_data(ticker)
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {str(e)}")

root = tk.Tk()
root.title("StockAI")
root.geometry("600x400")

# Configure a light theme
root.tk_setPalette(background="white", foreground="black")
style = ttk.Style()
style.configure("TButton", foreground="black", borderwidth=0, relief="flat", background="white")
style.configure("TLabel", foreground="black", background="white")
style.map("TButton", background=[("active", "lightblue")])

frame = ttk.Frame(root)
frame.pack(padx=20, pady=20)

title_label = ttk.Label(frame, text="StockAI", font=("Helvetica", 36))
title_label.pack()

label = ttk.Label(frame, text="Enter Company Ticker:")
label.pack()

entry = ttk.Entry(frame)
entry.pack()

predict_button = ttk.Button(frame, text="Predict", command=predict_stock)
predict_button.pack()

result_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=60, height=20)
result_text.pack()

root.mainloop()
