import customtkinter
import tkinter as tk
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import sys
from SVR import generate_predicted_data
from KNN import generate_predicted_data as knn_predict
from RF import random_forest_predict

current_stock = "AAPL"

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, my_frame_2, **kwargs):
        super().__init__(master, **kwargs)
        self.my_frame_2 = my_frame_2  # Reference to MyFrame2

        # add widgets onto the frame, for example:
        self.label = customtkinter.CTkLabel(self, text="Buttons", fg_color="transparent", text_color="Red")
        self.label.grid(row=0, column=0, padx=10)

        self.button1 = customtkinter.CTkButton(master=self, text="MSFT Button", command=lambda: button_event("MSFT"))
        self.button1.grid(row=2, column=0, padx=10, pady=3)

        self.button2 = customtkinter.CTkButton(master=self, text="AAPL Button", command=lambda: button_event("AAPL"))
        self.button2.grid(row=3, column=0, padx=10, pady=3)

        self.button3 = customtkinter.CTkButton(master=self, text="NOW Button", command=lambda: button_event("NOW"))
        self.button3.grid(row=4, column=0, padx=10, pady=3)

        self.button4 = customtkinter.CTkButton(master=self, text="GOOG Button", command=lambda: button_event("GOOG"))
        self.button4.grid(row=5, column=0, padx=10, pady=3)

        self.button5 = customtkinter.CTkButton(master=self, text="AMZN Button", command=lambda: button_event("AMZN"))
        self.button5.grid(row=6, column=0, padx=10, pady=3)

        self.button6 = customtkinter.CTkButton(master=self, text="DIS Button", command=lambda: button_event("DIS"))
        self.button6.grid(row=7, column=0, padx=10, pady=3)

        self.button7 = customtkinter.CTkButton(master=self, text="PANW Button", command=lambda: button_event("PANW"))
        self.button7.grid(row=8, column=0, padx=10, pady=3)

        self.button8 = customtkinter.CTkButton(master=self, text="BA Button", command=lambda: button_event("BA"))
        self.button8.grid(row=9, column=0, padx=10, pady=3)

        self.button9 = customtkinter.CTkButton(master=self, text="PLD Button", command=lambda: button_event("PLD"))
        self.button9.grid(row=10, column=0, padx=10, pady=3)

        self.button10 = customtkinter.CTkButton(master=self, text="JNJ Button", command=lambda: button_event("JNJ"))
        self.button10.grid(row=11, column=0, padx=10, pady=3)


        self.entry = customtkinter.CTkEntry(master=self, width=100)
        self.entry.grid(row=12, column=0, padx=10, pady=3)

        self.enter_button = customtkinter.CTkButton(master=self, text="Enter", command=self.enter_stock)
        self.enter_button.grid(row=13, column=0, padx=10, pady=3)

        # Add more buttons as needed

        def button_event(stock_name):
            print("button pressed: " + str(stock_name))
            self.my_frame_2.update_chart(stock_name)  # Call update_chart in MyFrame2

        self.terminate_button = customtkinter.CTkButton(master=self, text="Terminate", fg_color="red",
                                                        command=self.terminate_program)
        self.terminate_button.grid(row=16, column=0, padx=10, pady=10)


    def terminate_program(self):
        self.master.destroy()  # Destroy the main Tkinter window
        sys.exit(0)  # Exit the program

    def enter_stock(self):
        stock_name = self.entry.get()
        if stock_name:
            print("User entered stock symbol: " + stock_name)
            self.my_frame_2.update_chart(stock_name)

        


class MyFrame2(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.figure, self.ax = plt.subplots(figsize=(25, 20))   
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # Adjusted grid configuration

    def update_chart(self, stock_name):
        data = yf.download(stock_name, period="1mo", interval="1d")
        data = data.dropna()

        self.ax.clear()
        self.ax.xaxis_date()  # Set x-axis to display dates properly
        self.ax.set_title(stock_name + " Line Chart")

        # Plotting the line chart
        self.ax.plot(data.index, data["Close"], marker='o', markersize=3, linestyle='-')

        # Format x-axis labels as dates
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())

        self.figure.autofmt_xdate()  # Auto-rotate and align x-axis labels

        svr_predicted_data = generate_predicted_data(stock_name)
        self.ax.plot(data.index[-len(svr_predicted_data):], svr_predicted_data, color='red', linestyle='--')


        # Call File3 (KNN) to generate predicted data
        knn_predicted_data = knn_predict(stock_name)
        self.ax.plot(data.index[-len(knn_predicted_data):], knn_predicted_data, color='green', linestyle='--')


        # Call File4 (RF) to generate predicted data
        rf_predicted_data = random_forest_predict(stock_name)
        self.ax.plot(data.index[-len(rf_predicted_data):], rf_predicted_data, color='purple', linestyle='--')

        self.ax.legend(['Actual Stock Price', 'SVR', 'KNN', "RF"])

        self.canvas.draw()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.my_frame_2 = MyFrame2(master=self)
        self.my_frame_2.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        self.my_frame = MyFrame(master=self, my_frame_2=self.my_frame_2)
        self.my_frame.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
