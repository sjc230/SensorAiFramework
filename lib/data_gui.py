#from tkinter import Toplevel, Label, Entry, Button
import customtkinter
import shutil
from pathlib import Path
import yaml
from utils import open_file, update_yaml_variable, data_loader_confg, parse_text_entry
from dsp import scg_simulate

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
            split_checkbox.configure(state="normal")
        else:
            update_yaml_variable(config_path, "labeled_data", False)
            checkbox.configure(state="disabled")
            split_checkbox.configure(state="disabled")

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

    # Checkbox state
    split_check_var = customtkinter.StringVar(value="off")
    # Checkbox Text
    split_text_var = customtkinter.StringVar(value="Check if you require a train / test split on data")

    def split_check_action():
        if split_checkbox.get() == "on":
            update_yaml_variable(config_path, "test_train_split", True)
            split_entry.configure(state="normal")
        else:
           update_yaml_variable(config_path, "test_train_split", False)
           split_entry.configure(state="disabled")

    split_checkbox = customtkinter.CTkCheckBox(
        master=data_loader_window,
        textvariable=split_text_var,
        command=split_check_action,
        variable=split_check_var,
        onvalue="on",
        offvalue="off",
        state="disabled"
    )
    split_checkbox.pack(pady=10)

    split_label = customtkinter.CTkLabel(data_loader_window, text="Enter Split Value Here:")
    split_label.pack()

    split_entry = customtkinter.CTkEntry(data_loader_window,state='disabled')
    split_entry.pack(pady=10) 
       
    

    def load_files():
        split_val = split_entry.get()
        update_yaml_variable(config_path, "split_value", split_val)
        labels_checkbox.configure(state='disabled')
        checkbox.configure(state='disabled')
        split_checkbox.configure(state='disabled')
        split_entry.configure(state='disabled')
        select_data_button.configure(state='disabled')
        select_labels_button.configure(state='disabled')
        load_files_button.configure(state='disabled')

        

    def clear_data():
        data_loader_confg()
        labels_check_var.set('off') #.configure(variable='off')
        labels_checkbox.configure(state='normal')
        check_var.set('off') #.configure(variable='off')
        split_check_var.set('off')
        update_yaml_variable(config_path, "current_data_file", '')
        select_data_button.configure(text="select data npy",state='normal')
        update_yaml_variable(config_path, "current_label_file", '')
        select_labels_button.configure(text="select data npy",state='disabled')
        split_entry.insert(0, '')
        split_entry.pack(pady=10)
        split_entry.configure(state='disabled')
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
        if label_bool == 'true':
            label_bool = True            
        elif label_bool == 'false':
            label_bool = False            
        seperate_labels = yaml_data['seperate_labels']
        if seperate_labels == 'true':
            seperate_labels = True            
        elif seperate_labels == 'false':
            seperate_labels = False            
        data = yaml_data['current_data_file']
        labels = yaml_data['current_label_file']
        
        #if (device != None) and (model != None) and (".yaml" in device) and (".yaml" in model):
        if (label_bool == True) and (seperate_labels ==  True) and (data != '') and ('.npy' in data) and (labels != '') and ('.npy' in labels):
            load_files_button.configure(state='normal')
        elif (label_bool == True) and (seperate_labels ==  False) and (data != '') and ('.npy' in data) and (labels == ''):
            load_files_button.configure(state='normal')
        elif (label_bool == False) and (seperate_labels ==  False) and (data != '') and ('.npy' in data) and (labels == ''):
            load_files_button.configure(state='normal')
        else:
            load_files_button.configure(state='disabled')
    
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
    num_rows = 1
    duration = 10
    sampling_rate = 100
    add_respritory = 'True'
    respiratory_rate = '10,30'
    systolic = '90,140'
    diastolic = '80,100'
    pulse_type = 'db'
    noise_type = 'basic'
    noise_shape = 'laplace'
    noise_amplitude = 0.1
    noise_frequency = '5,10,100'
    power_line_amplitude = 0
    power_line_frequency = 50
    artifacts_amplitude = 0
    artifacts_frequency = 100
    artifacts_number = 5
    artifacts_shape = 'laplace'
    n_echo = 3
    attenuation_factor = '0.1,0.05,0.02'
    delay_factor = 15
    random_state = 'None'
    silent = 'False'

    def retrieve_data():
        n_rows = num_rows_entry.get()
        n_rows = int(n_rows)

        dur = duration_entry.get()
        dur = int(dur)

        s_rate = sampling_rate_entry.get()
        s_rate = int(s_rate)

        add_rep = add_repository_entry.get()
        add_rep = bool(add_rep)

        resp_rate = respiratory_rate_entry.get()
        resp_rate = parse_text_entry(resp_rate,'int')
        resp_rate = tuple(resp_rate)

        syst = respiratory_rate_entry.get()
        syst = parse_text_entry(syst,'int')
        syst = tuple(syst)

        dias = respiratory_rate_entry.get()
        dias = parse_text_entry(dias,'int')
        dias = tuple(dias)

        pulse_t = pulse_type_entry.get()

        noise_t = noise_type_entry.get()
        noise_t = parse_text_entry(noise_t,'string')

        noise_s = noise_shape_entry.get()

        noise_a = noise_amplitude_entry.get()
        noise_a = float(noise_a)

        noise_f = noise_frequency_entry.get()
        noise_f = parse_text_entry(noise_f,'float')

        pl_a = power_line_amplitude_entry.get()
        pl_a = float(pl_a)

        pl_f = power_line_frequency_entry.get()
        pl_f = float(pl_f)

        art_a = artifacts_amplitude_entry.get()
        art_a = float(art_a)

        art_f = artifacts_frequency_entry.get()
        art_f = float(art_f)

        art_n = artifacts_number_entry.get()
        art_n = int(art_n)

        art_s = artifacts_shape_entry.get()

        n_e = n_echo_entry.get(n_e)
        n_e = int(n_e)

        att_f = attenuation_factor_entry.get()
        att_f = parse_text_entry(att_f,'float')
        
        del_f = delay_factor_entry.get()
        del_f = int(del_f)

        rs = random_state_entry.get()
        rs = int(rs)

        sil = silent_entry.get()
        sil = bool(sil)

                
        #name = "K Means"
        scg_data = scg_simulate()
        #add_to_clust_queue(name,kmeans)
        print("K Means Model Created")

    generate_scg_window = customtkinter.CTkToplevel()
    generate_scg_window.title("Generate SCG Data")
    generate_scg_window.grab_set() # Keep focus
    generate_scg_window.lift() # Bring to front

    random_label = customtkinter.CTkLabel(generate_scg_window, text="Random State: None or a single integer")
    random_label.pack(pady=5)

    random_state_entry = customtkinter.CTkEntry(generate_scg_window)
    random_state_entry.pack(pady=5)
    #random_state_entry.insert(0, random_state)

    add_to_queue_button = customtkinter.CTkButton(generate_scg_window, text="Get Text", command=retrieve_data)
    add_to_queue_button.grid(row=9,column=4,padx=5, pady=5)