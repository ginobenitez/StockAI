import customtkinter as ctk
import tempai as ai
def search():
    stock = entry.get()
    stock = stock.upper()
    stock = ai.get_company_data(stock)
    
    predictions, precision = ai.stock_price_prediction(stock)
    
    label = ctk.CTkLabel(scrollable, text = stock)
    
    label.pack()


root = ctk.CTk()
root.geometry("750x450")

root.title("StockAI")

ctk.set_default_color_theme("blue")
scrollable = ctk.CTkScrollableFrame(root,
                                    width = 250,
                                    height = 100)

label_title = ctk.CTkLabel(root, text = "StockAI", 
                           font = ctk.CTkFont(size = 30, weight= "bold"))

button_search = ctk.CTkButton(root, text="Search Stock", width=200,
                              text_color= "black", 
                              hover_color= "#A2D6F9",
                              fg_color= "#2E5EAA", 
                              command=search)


label_title.pack(padx = 10, pady =(40, 20))

entry = ctk.CTkEntry(root, placeholder_text= "Find Stock")
entry.pack()

scrollable.pack()

button_search.pack()


root.mainloop()