#from tkinter import Toplevel, Label, Entry, Button
import customtkinter
import shutil
from pathlib import Path
from utils import parse_text_entry, open_file

current_dir = Path.cwd()

ftype_npy = [("npy files","*.npy")]

def open_data_loader_window():
    data_file = None
    label_file = None

    def retrieve_files(button_name):
        if button_name == 'select_data':
            data_file = open_file(title="Select you .npy data file",filetypes=ftype_npy)
        elif button_name == 'select_labels':
            label_file = open_file(title="Select you .npy label file",filetypes=ftype_npy)

    
    data_loader_window = customtkinter.CTkToplevel()
    data_loader_window.title("Load Data Files (.npy)")
    data_loader_window.geometry("400x200")
    data_loader_window.attributes('-topmost', True)

    # Checkbox state
    check_var = customtkinter.StringVar(value="off")
    # Checkbox Text
    text_var = customtkinter.StringVar(value="Check if labels are in a seperate datafile")

    def check_action():
        if checkbox.get() == "on":
            select_labels.configure(state="normal")
        else:
            select_labels.configure(state="disabled")

    checkbox = customtkinter.CTkCheckBox(
        master=data_loader_window,
        textvariable=text_var,
        command=check_action,
        variable=check_var,
        onvalue="on",
        offvalue="off"
    )
    checkbox.pack(pady=10)

    select_data = customtkinter.CTkButton(data_loader_window,text="select data npy",command=lambda: retrieve_files(button_name="select_data"))
    select_data.pack(pady=10)

    select_labels = customtkinter.CTkButton(data_loader_window,text="select labels npy",state="disabled" ,command=lambda: retrieve_files(button_name="select_labels"))
    select_labels.pack(pady=10)
    
    load_files_button = customtkinter.CTkButton(data_loader_window, text="load files", command=retrieve_files)
    load_files_button.pack(pady=10)

def generate_wavedata_window_opener():
    data_file = None
    label_file = None

    def retrieve_files():
        return data_file, label_file

    generate_wavedata_window = customtkinter.CTkToplevel()
    generate_wavedata_window.title("Generate Waveform Data")
    generate_wavedata_window.attributes('-topmost', True)

    random_state_entry = customtkinter.CTkEntry(generate_wavedata_window)
    random_state_entry.pack(pady=10)
    random_state_entry.insert(0, random_state)

    add_to_queue_button = customtkinter.CTkButton(generate_wavedata_window, text="Get Text", command=retrieve_files)
    add_to_queue_button.pack(pady=10)

def generate_scg_window_opener():
    data_file = None
    label_file = None

    def retrieve_files():
        return data_file, label_file

    generate_scg_window = customtkinter.CTkToplevel()
    generate_scg_window.title("Generate SCG Data")
    generate_scg_window.attributes('-topmost', True)

    random_state_entry = customtkinter.CTkEntry(generate_scg_window)
    random_state_entry.pack(pady=10)
    random_state_entry.insert(0, random_state)

    add_to_queue_button = customtkinter.CTkButton(generate_scg_window, text="Get Text", command=retrieve_files)
    add_to_queue_button.pack(pady=10)