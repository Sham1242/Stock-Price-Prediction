import customtkinter
import tkinter as tk
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import quandl
import numpy as np
from mpl_finance import candlestick_ohlc
import sys

current_stock = "AAPL"

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, my_frame_2, **kwargs):
        super().__init__(master, **kwargs)
        self.my_frame_2 = my_frame_2  # Reference to MyFrame2

        self.label = customtkinter.CTkLabel(self, text="Buttons", fg_color="transparent", text_color="Red")
        self.label.grid(row=0, column=0, padx=10)

        self.button1 = customtkinter.CTkButton(master=self, text="MSFT Button", command=lambda: button_event("MSFT"))
        self.button1.grid(row=2, column=0, padx=10, pady=3)

        self.button2 = customtkinter.CTkButton(master=self, text="AAPL Button", command=lambda: button_event("AAPL"))
        self.button2.grid(row=3, column=0, padx=10, pady=3)

        self.entry = customtkinter.CTkEntry(master=self, width=20)  # Adjust the width here
        self.entry.grid(row=4, column=0, padx=10, pady=3)

        self.enter_button = customtkinter.CTkButton(master=self, text="Enter", command=self.enter_stock)
        self.enter_button.grid(row=5, column=0, padx=10, pady=3)

        self.terminate_button = customtkinter.CTkButton(master=self, text="Terminate", fg_color="red",
                                                        command=self.terminate_program)
        self.terminate_button.grid(row=6, column=0, padx=10, pady=10)

        def button_event(stock_name):
            print("button pressed: " + str(stock_name))
            self.my_frame_2.update_chart(stock_name)  # Call update_chart in MyFrame2

    def enter_stock(self):
        stock_name = self.entry.get()
        if stock_name:
            print("User entered stock symbol: " + stock_name)
            self.my_frame_2.update_chart(stock_name)

    def terminate_program(self):
        self.master.destroy()  # Destroy the main Tkinter window
        sys.exit(0)  # Exit the program


class MyFrame2(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.figure, self.ax = plt.subplots(figsize=(20, 20))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # Adjusted grid configuration

    def update_chart(self, stock_name):
        data = yf.download(stock_name, period="1mo", interval="1d")
        data = data.dropna()

        self.ax.clear()
        self.ax.set_title(stock_name + " Candlestick Chart")

        # getting data and modifying it to remove gaps at weekends
        r = quandl.get('WIKI/' + stock_name, start_date='2016-01-01', end_date='2017-11-10')
        date_list = np.array(r.index.to_pydatetime())
        plot_array = np.zeros([len(r), 5])
        plot_array[:, 0] = np.arange(plot_array.shape[0])
        plot_array[:, 1:] = r.iloc[:, :4]

        # plotting candlestick chart
        num_of_bars = 100  # the number of candlesticks to be plotted
        candlestick_ohlc(self.ax, plot_array[-num_of_bars:], colorup='g', colordown='r')
        self.ax.margins(x=0.0, y=0.1)
        self.ax.yaxis.tick_right()
        x_tick_labels = []
        self.ax.set_xlim(right=plot_array[-1, 0]+10)
        self.ax.grid(True, color='k', ls='--', alpha=0.2)
        # setting xticklabels actual dates instead of numbers
        indices = np.linspace(plot_array[-num_of_bars, 0], plot_array[-1, 0], 8, dtype=int)
        for i in indices:
            date_dt = date_list[i]
            date_str = date_dt.strftime('%b-%d')
            x_tick_labels.append(date_str)
        self.ax.set(xticks=indices, xticklabels=x_tick_labels)

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
