# hello_psg.py

import PySimpleGUI as sg
import ai as ai

score = ai.accuracy()
layout = [[sg.Text("StockAI")],[sg.Button("OK")]]

# Create the window
window = sg.Window("StockAI", layout, background_color= "#313030", margins=(600, 300))

# Create an event loop
while True:
    event, values = window.read()
    if event == "OK":
        print("hi")
        #score = ai.accuracy()
        #sg.Text(score)
        
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break

window.close()