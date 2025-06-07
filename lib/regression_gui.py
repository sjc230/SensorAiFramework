import customtkinter
from tkinter import Toplevel, Label, Entry, Button
import customtkinter
from utils import parse_text_entry, convert_list_to_string, load_gui_data
from regression import *


global regress_queue_names
global regress_queue_models

regress_queue_names = []
regress_queue_models = []

def add_to_regress_queue(name,model):
    global regress_queue_names
    regress_queue_names.append(name)
    regress_queue_models.append(model)
    print("Queue: ", regress_queue_names)

def show_regress_queue():
    global regress_queue_names
    regress_queue_window = customtkinter.CTkToplevel()
    regress_queue_window.title("Regressor Queue")
    regress_queue_window.geometry("200x400")
    regress_queue_window.attributes('-topmost', True)

    queue_string = convert_list_to_string(regress_queue_names)
    queue_label = customtkinter.CTkLabel(master=regress_queue_window,text=queue_string)
    queue_label.pack()

def reset_regress_queue():
    global regress_queue_names
    global regress_queue_models
    regress_queue_names = []
    regress_queue_models = []

def execute_regress_gridsearch():
    global regress_queue_names
    global regress_queue_models

    X_train, y_train, X_test, y_test = load_gui_data()

    gridsearch_regressor(names=regress_queue_names,pipes=regress_queue_models,
                              X=X_test,y=y_test,
                              plot_number=3,save_best=True)

def open_decision_tree_window():
    criterion = 'gini'
    splitter = 'best'
    max_depth = 'None'
    random_state = 'None'

    def retrieve_data():
        crit = criterion_entry.get()
        split = splitter_entry.get()
        max_d = max_depth_entry.get()
        rand_st = random_state_entry.get()

        criterion_list = parse_text_entry(crit,'string')
        splitter_list = parse_text_entry(split,'string')
        max_depth_list = parse_text_entry(max_d,'int')
        random_state_list = parse_text_entry(rand_st,'int')

        name = "Decision Tree"
        decision_tree = pipeBuild_DecisionTreeregressifier(criterion=criterion_list,splitter=splitter_list,max_depth=max_depth_list,random_state=random_state_list[0])
        add_to_regress_queue(name,decision_tree)
        print("Decision Tree Model Created")

    decision_tree_window = customtkinter.CTkToplevel()
    decision_tree_window.title("Decision Tree Pipe Builder")
    decision_tree_window.geometry("500x400")
    decision_tree_window.attributes('-topmost', True)

    criterion_entry = customtkinter.CTkEntry(decision_tree_window)
    criterion_entry.pack(pady=10)
    criterion_entry.insert(0, criterion)
    criterion_entry.pack(pady=10)

    splitter_entry = customtkinter.CTkEntry(decision_tree_window)
    splitter_entry.pack(pady=10)
    splitter_entry.insert(0, splitter)
    splitter_entry.pack(pady=10)

    max_depth_entry = customtkinter.CTkEntry(decision_tree_window)
    max_depth_entry.pack(pady=10)
    max_depth_entry.insert(0, max_depth)
    max_depth_entry.pack(pady=10)

    random_state_entry = customtkinter.CTkEntry(decision_tree_window)
    random_state_entry.pack(pady=10)
    random_state_entry.insert(0, random_state)
    random_state_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(decision_tree_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)
    

