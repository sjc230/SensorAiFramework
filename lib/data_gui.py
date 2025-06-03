#from tkinter import Toplevel, Label, Entry, Button
import customtkinter
import shutil
from pathlib import Path
import yaml
from utils import open_file, update_yaml_variable, data_loader_confg

current_dir = Path.cwd()
config_path = current_dir / "config/current_data.yaml"


ftype_npy = [("npy files","*.npy")]

def open_data_loader_window():         
    data_loader_window = customtkinter.CTkToplevel()
    data_loader_window.title("Load Data Files (.npy)")
    data_loader_window.geometry("400x400")
    data_loader_window.grab_set() # Keep focus
    data_loader_window.lift() # Bring to front

    
    # Checkbox state
    labels_check_var = customtkinter.StringVar(value="off")
    # Checkbox Text
    labels_text_var = customtkinter.StringVar(value="Check if your data has labels")

    def labels_check_action():
        if labels_checkbox.get() == "on":
            update_yaml_variable(config_path, "labeled_data", True)
            checkbox.configure(state="normal")
        else:
            update_yaml_variable(config_path, "labeled_data", False)
            checkbox.configure(state="disabled")

    labels_checkbox = customtkinter.CTkCheckBox(
        master=data_loader_window,
        textvariable= labels_text_var,
        command=labels_check_action,
        variable=labels_check_var,
        onvalue="on",
        offvalue="off"
    )
    labels_checkbox.pack(pady=10)

    # Checkbox state
    check_var = customtkinter.StringVar(value="off")
    # Checkbox Text
    text_var = customtkinter.StringVar(value="Check if labels are in a seperate datafile")

    def check_action():
        if checkbox.get() == "on":
            update_yaml_variable(config_path, "seperate_labels", True)
            select_labels_button.configure(state="normal")
        else:
            update_yaml_variable(config_path, "seperate_labels", False)
            select_labels_button.configure(state="disabled")

    checkbox = customtkinter.CTkCheckBox(
        master=data_loader_window,
        textvariable=text_var,
        command=check_action,
        variable=check_var,
        onvalue="on",
        offvalue="off",
        state="disabled"
    )
    checkbox.pack(pady=10)

    def load_files():
        labels_checkbox.configure(state='disabled')
        checkbox.configure(state='disabled')
        select_data_button.configure(state='disabled')
        select_labels_button.configure(state='disabled')

    def clear_data():
        data_loader_confg()
        labels_check_var.set('off') #.configure(variable='off')
        check_var.set('off') #.configure(variable='off')
        update_yaml_variable(config_path, "current_data_file", '')
        select_data_button.configure(text="select data npy")
        update_yaml_variable(config_path, "current_label_file", '')
        select_labels_button.configure(text="select data npy",state='disabled')
        load_files_button.configure(state='disabled')


    select_data_button = customtkinter.CTkButton(data_loader_window,text="select data npy",command=lambda: retrieve_files(button_name="select_data"))
    select_data_button.pack(pady=10)

    select_labels_button = customtkinter.CTkButton(data_loader_window,text="select labels npy",state="disabled" ,command=lambda: retrieve_files(button_name="select_labels"))
    select_labels_button.pack(pady=10)
    
    load_files_button = customtkinter.CTkButton(data_loader_window, text="load files",state="disabled", command=load_files)
    load_files_button.pack(pady=10)

    clear_filedata_button = customtkinter.CTkButton(data_loader_window, text="clear all file data",command=clear_data)
    clear_filedata_button.pack(pady=10)

    def retrieve_files(button_name):
        if button_name == 'select_data':
            data_file = open_file(title="Select your .npy data file",filetypes=ftype_npy)
            update_yaml_variable(config_path, "current_data_file", data_file)
            select_data_button.configure(text = data_file)
        elif button_name == 'select_labels':
            label_file = open_file(title="Select your .npy label file",filetypes=ftype_npy)
            update_yaml_variable(config_path, "current_label_file", label_file)
            select_labels_button.configure(text = label_file)
        
        with open(config_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
        
        label_bool = yaml_data['labeled_data']
        print(label_bool,": label")
        print(type(label_bool),": label type")
        if label_bool == 'true':
            label_bool = True            
        elif label_bool == 'false':
            label_bool = False            
        seperate_labels = yaml_data['seperate_labels']
        print(seperate_labels,": label")
        print(type(seperate_labels),": label type")
        if seperate_labels == 'true':
            seperate_labels = True            
        elif seperate_labels == 'false':
            seperate_labels = False            
        data = yaml_data['current_data_file']
        print(data,": data")
        print(type(data),": data type")
        labels = yaml_data['current_label_file']
        print(labels,": labels")
        print(type(labels),": labels type")
        
        #if (device != None) and (model != None) and (".yaml" in device) and (".yaml" in model):
        if (label_bool == True) and (seperate_labels ==  True) and (data != '') and ('.npy' in data) and (labels != '') and ('.npy' in labels):
            load_files_button.configure(state='normal')
            print("if")
        elif (label_bool == True) and (seperate_labels ==  False) and (data != '') and ('.npy' in data) and (labels == ''):
            load_files_button.configure(state='normal')
            print("elif 1")
        elif (label_bool == False) and (seperate_labels ==  False) and (data != '') and ('.npy' in data) and (labels == ''):
            load_files_button.configure(state='normal')
            print("elif 2")
        else:
            load_files_button.configure(state='disabled')
            print("else")

def generate_wavedata_window_opener():
    generate_wavedata_window = customtkinter.CTkToplevel()
    generate_wavedata_window.title("Generate Waveform Data")
    generate_wavedata_window.grab_set() # Keep focus
    generate_wavedata_window.lift() # Bring to front

    random_state_entry = customtkinter.CTkEntry(generate_wavedata_window)
    random_state_entry.pack(pady=10)
    #random_state_entry.insert(0, random_state)

    add_to_queue_button = customtkinter.CTkButton(generate_wavedata_window, text="Get Text", command=retrieve_files)
    add_to_queue_button.pack(pady=10)

def generate_scg_window_opener():
    generate_scg_window = customtkinter.CTkToplevel()
    generate_scg_window.title("Generate SCG Data")
    generate_scg_window.grab_set() # Keep focus
    generate_scg_window.lift() # Bring to front

    random_state_entry = customtkinter.CTkEntry(generate_scg_window)
    random_state_entry.pack(pady=10)
    #random_state_entry.insert(0, random_state)

    add_to_queue_button = customtkinter.CTkButton(generate_scg_window, text="Get Text", command=retrieve_files)
    add_to_queue_button.pack(pady=10)