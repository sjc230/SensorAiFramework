import tkinter
import customtkinter
import yaml
import threading
from pathlib import Path
from utils import run_script
from classification_gui import open_decision_tree_window

current_dir = Path.cwd() # assumes your working directory is in "SensorwebAiFramework"

ftype_npy = [("npy files","*.npy")]
ftype_yaml = [("yaml files","*.yaml")]

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

device =None
model = None
# Open File Dialog
def select_yaml_file(button_name = None, tab = None):
    global device
    global model
    global active_tab
    filename = customtkinter.filedialog.askopenfilename(filetypes=ftype_yaml)
    if button_name == "select_device":
        if tab == 'tab_6':
            select_device.configure(text = filename)                       
        elif tab == 'tab_7':
            select_historical.configure(text = filename)
        device = filename
        active_tab = tab 
    elif button_name == "select_model":
        if tab == 'tab_6':
            select_model.configure(text = filename)
        elif tab == 'tab_7':
            select_model7.configure(text = filename)
        model = filename
        active_tab = tab 
    
    if (device != None) and (model != None) and (".yaml" in device) and (".yaml" in model):
        if active_tab == 'tab_6':
            start_connection.configure(state="normal")
        elif active_tab == "tab_7":
            start_historical.configure(state="normal")

    return filename

# Method to connect model to smart device
def connect_model_to_device(device_name,model_name):
    global conn_script
    global stop_event
    print("Connecting - model: ",model_name,"To device: ",device_name)

    stop_event = threading.Event()
    script_path = current_dir / "mqtt/main_ai_mqtt.py"
    arguments = [device_name, model_name]

    conn_script = threading.Thread(target=run_script, args=(script_path, arguments, stop_event))
    conn_script.start()

    start_connection.configure(state="disabled")
    stop_connection.configure(state="normal")


# Method to disconnect model from device
def disconnect_model_from_device(device_name,model_name):
    global conn_script
    global device
    global model
    global stop_event
    global active_tab
    #conn_script.stop()
    stop_event.set()
    conn_script.join()
    print("Thread terminated.")
    select_device.configure(text = "select device yaml")
    select_model.configure(text = "select model yaml")
    device = None
    model = None
    start_connection.configure(state="disabled")
    stop_connection.configure(state = "disabled")
    active_tab = None

# Method to connect to db
def connect_model_to_db(device_name,model_name):
    global conn_script
    global stop_event
    print("Connecting - model: ",model_name,"To device: ",device_name)

    stop_event = threading.Event()
    script_path = current_dir / "mqtt/main_ai_influx.py"
    arguments = [device_name, model_name]

    conn_script = threading.Thread(target=run_script, args=(script_path, arguments, stop_event))
    conn_script.start()

    start_historical.configure(state="disabled")

    stop_historical.configure(state="normal")

# Method to disconnect from db
def disconnect_model_from_db(device_name,model_name):
    global conn_script
    global device
    global model
    global stop_event
    global active_tab
    #conn_script.stop()
    stop_event.set()
    conn_script.join()
    print("Thread terminated.")
    select_historical.configure(text = "select device yaml")
    select_model7.configure(text = "select model yaml")
    device = None
    model = None
    start_historical.configure(state="disabled")
    stop_historical.configure(state = "disabled")
    active_tab=None

#root = Tk()
root = customtkinter.CTk()

root.title("Sensor AI")
#root.inconbitmap("images/codemy.ico")
root.geometry("700x300")

# create Tabview
my_tab = customtkinter.CTkTabview(root,
                                  width=600,
                                  height=250,
                                  corner_radius=10,
                                  fg_color="silver",
                                  segmented_button_fg_color="black",
                                  segmented_button_selected_color="red",
                                  segmented_button_selected_hover_color="pink",
                                  segmented_button_unselected_color="grey",
                                  segmented_button_unselected_hover_color="blue",
                                  text_color="black") #command=used to inserta a command)
my_tab.pack(pady=10)

# Create tabs
tab_0 = my_tab.add("Data")
tab_1 = my_tab.add("DSP")
tab_2 = my_tab.add("Classification")
tab_3 = my_tab.add("Clustering")
tab_4 = my_tab.add("Detection")
tab_5 = my_tab.add("Regression")
tab_6 = my_tab.add("Device Connector")
tab_7 = my_tab.add("Historical Download")

# Put stuff in tab 1 - DSP

# Put stuff in tab 2 - Classification
decision_tree_button = customtkinter.CTkButton(tab_2, text="Open Decision Tree", command=open_decision_tree_window)
decision_tree_button.pack(padx=20, pady=20)

# Put stuff in tab 3 - Clustering

# Put stuff in tab 4 - Detection

# Put stuff in tab 5 - Regression

# Put stuff in tab 6 - Device Connector
select_device = customtkinter.CTkButton(tab_6,text="select device yaml",fg_color="black",command=lambda: select_yaml_file("select_device","tab_6"))
select_device.pack(pady=10)

select_model = customtkinter.CTkButton(tab_6,text="select model yaml",fg_color="black",command=lambda: select_yaml_file("select_model","tab_6"))
select_model.pack(pady=10)

start_connection = customtkinter.CTkButton(tab_6,text="start the connection",fg_color="black",state="disabled" ,command=lambda: connect_model_to_device(device_name=device,model_name=model))
start_connection.pack(pady=10)

stop_connection = customtkinter.CTkButton(tab_6,text="stop the connection",fg_color="black",state="disabled" ,command=lambda: disconnect_model_from_device(device_name=device,model_name=model))
stop_connection.pack(pady=10)

# Put stuff in tab 7 - Historical Data
select_historical = customtkinter.CTkButton(tab_7,text="select device yaml",fg_color="black",command=lambda: select_yaml_file("select_device","tab_7"))
select_historical.pack(pady=10)

select_model7 = customtkinter.CTkButton(tab_7,text="select model yaml",fg_color="black",command=lambda: select_yaml_file("select_model","tab_7"))
select_model7.pack(pady=10)

start_historical = customtkinter.CTkButton(tab_7,text="start db download",fg_color="black",state="disabled" ,command=lambda: connect_model_to_db(device_name=device,model_name=model))
start_historical.pack(pady=10)

stop_historical = customtkinter.CTkButton(tab_7,text="end db connection",fg_color="black",state="disabled" ,command=lambda: disconnect_model_from_db(device_name=device,model_name=model))
stop_historical.pack(pady=10)

# Run app
root.mainloop()