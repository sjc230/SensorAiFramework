import customtkinter
from tkinter import Toplevel, Label, Entry, Button
import customtkinter
from utils import parse_text_entry
from classification import *

class_models = ['decision tree','random forest','knn','gaussian','adaboost','gaussian nb','qda','svc','mlp','nusvc','bagging','extra trees','gradient boost','histogram gradient boost','bernoulli nb','nearest centroid','passive agressive','lda','sgd','radius nn','non-myopic early','time series knn','time series svc']

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
        decision_tree_name = "Decision Tree"
        decision_tree = pipeBuild_DecisionTreeClassifier(criterion=criterion_list,splitter=splitter_list,max_depth=max_depth_list,random_state=random_state_list[0])
        print("Decision Tree Model Created")
        return decision_tree_name, decision_tree

    decision_tree_window = customtkinter.CTkToplevel()
    decision_tree_window.title("Decision Tree Pipe Builder")

    criterion_entry = customtkinter.CTkEntry(decision_tree_window)
    criterion_entry.pack(pady=10)
    criterion_entry.insert(0, criterion)

    splitter_entry = customtkinter.CTkEntry(decision_tree_window)
    splitter_entry.pack(pady=10)
    splitter_entry.insert(0, splitter)

    max_depth_entry = customtkinter.CTkEntry(decision_tree_window)
    max_depth_entry.pack(pady=10)
    max_depth_entry.insert(0, max_depth)

    random_state_entry = customtkinter.CTkEntry(decision_tree_window)
    random_state_entry.pack(pady=10)
    random_state_entry.insert(0, random_state)

    add_to_queue_button = customtkinter.CTkButton(decision_tree_window, text="Get Text", command=retrieve_data)
    add_to_queue_button.pack(pady=10)
    

def open_random_forest_window():
    new_window = customtkinter.CTkToplevel()
    new_window.title("New Window")
    label = customtkinter.CTkLabel(new_window, text="This is a new window")
    label.pack(padx=20, pady=20)

def open_extra_trees_window():
    new_window = customtkinter.CTkToplevel()
    new_window.title("New Window")
    label = customtkinter.CTkLabel(new_window, text="This is a new window")
    label.pack(padx=20, pady=20)

def open_knn_window():
    new_window = customtkinter.CTkToplevel()
    new_window.title("New Window")
    label = customtkinter.CTkLabel(new_window, text="This is a new window")
    label.pack(padx=20, pady=20)

def open_tsknn_window():
    new_window = customtkinter.CTkToplevel()
    new_window.title("New Window")
    label = customtkinter.CTkLabel(new_window, text="This is a new window")
    label.pack(padx=20, pady=20)