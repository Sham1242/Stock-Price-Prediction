import customtkinter
from tkinter import *
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()


current_stock = "APPL"

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.label = customtkinter.CTkLabel(self, text="Buttons", fg_color="transparent", text_color="Red")
        self.label.grid(row=0, column=0, padx=10)

        self.button1 = customtkinter.CTkButton(master=self,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text="MSFT Button",
                                 command=lambda: button_event("MSFT"))
        self.button1.grid(row=2, column=0, padx=10, pady= 3)        


        self.button2 = customtkinter.CTkButton(master=self,
                         width=120,
                         height=32,
                         border_width=0,
                         corner_radius=8,
                         text="APPL Button",
                         command=lambda: button_event("APPL"))
        self.button2.grid(row=3, column=0, padx=10, pady= 3)


        self.button3 = customtkinter.CTkButton(master=self,
                                width=120,
                                height=32,
                                border_width=0,
                                corner_radius=8,
                                text="GOOG Button",
                                command=lambda: button_event("GOOG"))
        self.button3.grid(row=4, column=0, padx=10, pady= 3)

        self.button4 = customtkinter.CTkButton(master=self,
                                width=120,
                                height=32,
                                border_width=0,
                                corner_radius=8,
                                text="AMD Button",
                                command=lambda: button_event("AMD"))
        self.button4.grid(row=5, column=0, padx=10, pady= 3)

        self.button5 = customtkinter.CTkButton(master=self,
                                width=120,
                                height=32,
                                border_width=0,
                                corner_radius=8,
                                text="TSLA Button",
                                command=lambda: button_event("TSLA"))
        self.button5.grid(row=6, column=0, padx=10, pady= 3)

        self.button6 = customtkinter.CTkButton(master=self,
                                width=120,
                                height=32,
                                border_width=0,
                                corner_radius=8,
                                text="INTC Button",
                                command=lambda: button_event("INTC"))
        self.button6.grid(row=7, column=0, padx=10, pady= 3)

        self.button7 = customtkinter.CTkButton(master=self,
                                width=120,
                                height=32,
                                border_width=0,
                                corner_radius=8,
                                text="DIS Button",
                                command=lambda: button_event("DIS"))
        self.button7.grid(row=8, column=0, padx=10, pady= 3)      



        def button_event(stock_name):
            print("button pressed: " + str(stock_name))






class MyFrame2(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        def update():
            button['text'] = ("Succesfully updated")

        button = customtkinter.CTkButton(master=self, text="Update", command=update)
        button.grid(row=0, column=0, padx=(20), pady=(5), sticky="nsew")

        self.tabview = customtkinter.CTkTabview(self, width = 950)
        self.tabview.grid(row=1, column=0, padx=(20), pady=(10), sticky="nsew")
        self.tabview.add("Tab 1")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        



class App(customtkinter.CTk):
    def __init__(self):

        super().__init__()
        self.geometry("1200x800")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")

        self.my_frame_2 = MyFrame2(master=self)
        self.my_frame_2.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")



def button_event(stock_name):
    print("button pressed: " + str(stock_name))
    current_stock = stock_name

app = App()
app.mainloop()

