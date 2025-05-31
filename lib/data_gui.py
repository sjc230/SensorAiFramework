#from tkinter import Toplevel, Label, Entry, Button
import customtkinter
from utils import parse_text_entry


def open_data_loader_window():
    data_file = None
    label_file = None

    def retrieve_files():
        print("testing")
        return 
    
    data_loader_window = customtkinter.CTkToplevel()
    data_loader_window.title("Load Data Files (.npy)")
    data_loader_window.geometry("400x200")

    # Checkbox state
    check_var = customtkinter.StringVar(value="off")
    # Checkbox Text
    text_var = customtkinter.StringVar(value="Check if labels are in a seperate datafile")

    checkbox = customtkinter.CTkCheckBox(
        master=data_loader_window,
        textvariable=text_var,
        command=retrieve_files(),
        variable=check_var,
        onvalue="on",
        offvalue="off"
    )
    checkbox.pack(pady=10)

    select_model = customtkinter.CTkButton(data_loader_window,text="select data npy",command=lambda: select_yaml_file("select_model","tab_6"))
    select_model.pack(pady=10)

    start_connection = customtkinter.CTkButton(data_loader_window,text="select labels npy",state="disabled" ,command=lambda: connect_model_to_device(device_name=device,model_name=model))
    start_connection.pack(pady=10)
    
    load_files_button = customtkinter.CTkButton(data_loader_window, text="load files", command=retrieve_files)
    load_files_button.pack(pady=10)

def generate_wavedata_window_opener():
    data_file = None
    label_file = None

    def retrieve_files():
        return data_file, label_file

    generate_wavedata_window = customtkinter.CTkToplevel()
    generate_wavedata_window.title("Generate Waveform Data")

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

    random_state_entry = customtkinter.CTkEntry(generate_scg_window)
    random_state_entry.pack(pady=10)
    random_state_entry.insert(0, random_state)

    add_to_queue_button = customtkinter.CTkButton(generate_scg_window, text="Get Text", command=retrieve_files)
    add_to_queue_button.pack(pady=10)