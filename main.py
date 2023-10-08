import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import tempai as ai
import yfinance as yf

def predict_stock():
    ticker = entry.get()
    if not ticker:
        messagebox.showerroe("Error", "Please enter a ticker symbol")
        return
    
    try:
        predictions, precision = ai.stock_price_prediction(ticker)
        result_label.config(text=f"Predictions for {ticker}:\n{predictions}\n\nEstimated Precision Score (Not Actual): {precision}")
        figure  = ai.plot_historical_data(ticker)
        
        #canvas = FigureCanvasTkAgg(figure, graph_frame)
        #canvas.draw()
        #canvas.get_tk_widget.pack()
        #figure.draw() 
  
        # placing the canvas on the Tkinter window 
    
        
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Stock Price Prediction App")
root.geometry("750x450")

# Create and pack widgets
frame = ttk.Frame(root)

frame.pack(padx=20, pady=20)
#graph_frame = ttk.Frame(root)

label = ttk.Label(frame, text="Enter Company Ticker:")
label.pack()

entry = ttk.Entry(frame)
entry.pack()

predict_button = ttk.Button(frame, text="Predict", command=predict_stock)
predict_button.pack()

result_label = ttk.Label(frame, text="")

result_label.pack()

#graph_frame.pack()

# Start the Tkinter main loop
root.mainloop()
