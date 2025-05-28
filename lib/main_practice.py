import tkinter
import customtkinter
import yaml
import subprocess
import threading
import time
from pathlib import Path

current_dir = Path.cwd() # assumes your working directory is in "SensorwebAiFramework"


# Load the YAML file
with open(current_dir / "config/classification.yaml", "r") as file:
    classifiers = yaml.safe_load(file)

with open(current_dir / "config/clustering.yaml", "r") as file:
    clusterers = yaml.safe_load(file)

with open(current_dir / "config/dsp.yaml", "r") as file:
    dsps = yaml.safe_load(file)

with open(current_dir / "config/novelty.yaml", "r") as file:
    novelties = yaml.safe_load(file)

with open(current_dir / "config/outlier.yaml", "r") as file:
    outliers = yaml.safe_load(file)

with open(current_dir / "config/regression.yaml", "r") as file:
    regressors = yaml.safe_load(file)

ftype_yaml = [("yaml files","*.yaml")]

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Class to handle running scripts with arguments via threads
class ScriptRunner:
    def __init__(self, script_path, arguments=None):
        self.script_path = script_path
        self.arguments = arguments if arguments else []
        self.process = None
        self.stop_flag = threading.Event()

    def run_script(self):
        command = ["python", self.script_path] + self.arguments
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while not self.stop_flag.is_set():
            if self.process.poll() is not None:
                break
            time.sleep(0.1)
        if self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
        stdout, stderr = self.process.communicate()
        if stdout:
            print("stdout:\n", stdout.decode())
        if stderr:
            print("stderr:\n", stderr.decode())
        print("Script finished")
            
    def start(self):
        self.thread = threading.Thread(target=self.run_script)
        self.thread.start()

    def stop(self):
        self.stop_flag.set()
        self.thread.join()

  

device =None
model = None
# Open File Dialog
def select_yaml_file(button_name = None):
    global device
    global model
    filename = customtkinter.filedialog.askopenfilename(filetypes=ftype_yaml)
    if button_name == "select_device":
        select_device.configure(text = filename)
        device = filename
    elif button_name == "select_model":
        select_model.configure(text = filename)
        model = filename
    elif button_name == "reset":
        select_device.configure(text = "select device yaml")
        select_model.configure(text = "select model yaml")
        device = None
        model = None
        start_connection.configure(state="disabled")
    
    if (device != None) and (model != None) and (".yaml" in device) and (".yaml" in model):
        start_connection.configure(state="normal")

    return filename

def connect_model_to_device(device_name,model_name):
    global conn_script
    print("Connecting - model: ",model_name,"To device: ",device_name)

    #stop_flag = threading.Event()
    script_path = current_dir / "mqtt/mqtt_subscriber.py"
    arguments = [device_name, model_name] #, stop_flag]

    conn_script = ScriptRunner(script_path, arguments)
    conn_script.start()

    start_connection.configure(state="disabled")

    stop_connection.configure(state="normal")


# Method to disconnect devices
def disconnect_model_from_device(device_name,model_name):
    global conn_script
    conn_script.stop()
    select_yaml_file(button_name="reset")
    stop_connection.configure(state = "disabled")



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
tab_1 = my_tab.add("DSP")
tab_2 = my_tab.add("Classification")
tab_3 = my_tab.add("Clustering")
tab_4 = my_tab.add("Detection")
tab_5 = my_tab.add("Regression")
tab_6 = my_tab.add("Smart Device Connection")

# Put stuff in tab 6
select_device = customtkinter.CTkButton(tab_6,text="select device yaml",fg_color="black",command=lambda: select_yaml_file("select_device"))
select_device.pack(pady=10)

select_model = customtkinter.CTkButton(tab_6,text="select model yaml",fg_color="black",command=lambda: select_yaml_file("select_model"))
select_model.pack(pady=10)

start_connection = customtkinter.CTkButton(tab_6,text="start the connection",fg_color="black",state="disabled" ,command=lambda: connect_model_to_device(device_name=device,model_name=model))
start_connection.pack(pady=10)

stop_connection = customtkinter.CTkButton(tab_6,text="stop the connection",fg_color="black",state="disabled" ,command=lambda: disconnect_model_from_device(device_name=device,model_name=model))
stop_connection.pack(pady=10)

# Run app
root.mainloop()