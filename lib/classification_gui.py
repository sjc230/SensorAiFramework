import customtkinter
from tkinter import Toplevel, Label, Entry, Button
from utils import parse_text_entry


def open_new_window(self):
    new_window = Toplevel(self)
    new_window.title("New Window")
    new_window.geometry("600x500")

    # Text boxes for data entry
    Label(new_window, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
    name_entry = Entry(new_window)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(new_window, text="Email:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
    email_entry = Entry(new_window)
    email_entry.grid(row=1, column=1, padx=10, pady=10)

    # Button to process the data
    submit_button = Button(new_window, text="Submit", command=lambda: self.process_data(name_entry.get(), email_entry.get()))
    submit_button.grid(row=2, column=0, columnspan=2, pady=20)

def process_data(self, name, email):
    print(f"Name: {name}, Email: {email}")


button = ctk.CTkButton(master=app, text="Click Me")