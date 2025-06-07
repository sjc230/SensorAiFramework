import customtkinter
from tkinter import Toplevel, Label, Entry, Button
import customtkinter
from utils import parse_text_entry, convert_list_to_string, load_gui_data
from classification import *

class_models = ['decision tree','random forest','knn','gaussian','adaboost','gaussian nb','qda','svc','mlp','nusvc','bagging','extra trees','gradient boost','histogram gradient boost','bernoulli nb','nearest centroid','passive agressive','lda','sgd','radius nn','non-myopic early','time series knn','time series svc']

global class_queue_names
global class_queue_models

class_queue_names = []
class_queue_models = []

def add_to_queue(name,model):
    global class_queue_names
    class_queue_names.append(name)
    class_queue_models.append(model)
    print("Queue: ", class_queue_names)

def show_class_queue():
    global class_queue_names
    class_queue_window = customtkinter.CTkToplevel()
    class_queue_window.title("Classifier Queue")
    class_queue_window.geometry("200x400")
    class_queue_window.attributes('-topmost', True)

    queue_string = convert_list_to_string(class_queue_names)
    queue_label = customtkinter.CTkLabel(master=class_queue_window,text=queue_string)
    queue_label.pack()

def execute_class_gridsearch():
    global class_queue_names
    global class_queue_models

    X_train, y_train, X_test, y_test = load_gui_data()

    gridsearch_classifier(names=class_queue_names,pipes=class_queue_models,
                              X_train=X_train,X_test=X_test,y_train=y_train,y_test=y_test,
                              plot_number=1,scoring="neg_mean_squared_error",save_best=False)

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
        decision_tree = pipeBuild_DecisionTreeClassifier(criterion=criterion_list,splitter=splitter_list,max_depth=max_depth_list,random_state=random_state_list[0])
        add_to_queue(name,decision_tree)
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
    

def open_random_forest_window():
    n_estimators = 100
    criterion = 'gini'    
    max_depth = 'None'
    random_state = 'None'

    def retrieve_data():
        crit = criterion_entry.get()
        n_estimators = n_estimators_entry.get()
        max_d = max_depth_entry.get()
        rand_st = random_state_entry.get()

        criterion_list = parse_text_entry(crit,'string')
        n_estimators_list = parse_text_entry(n_estimators,'int')
        max_depth_list = parse_text_entry(max_d,'int')
        random_state_list = parse_text_entry(rand_st,'int')

        name = "Random Forest"
        random_forest = pipeBuild_RandomForestClassifier(n_estimators=n_estimators_list,criterion=criterion_list,max_depth=max_depth_list,random_state=random_state_list[0])
        add_to_queue(name,random_forest)
        print("Random Forest Model Created")

    
    random_forest_window = customtkinter.CTkToplevel()
    random_forest_window.title("Raondom Forest Pipe Builder")
    random_forest_window.geometry("500x400")
    random_forest_window.attributes('-topmost', True)

    n_estimators_entry = customtkinter.CTkEntry(random_forest_window)
    n_estimators_entry.pack(pady=10)
    n_estimators_entry.insert(0, n_estimators)
    n_estimators_entry.pack(pady=10)

    criterion_entry = customtkinter.CTkEntry(random_forest_window)
    criterion_entry.pack(pady=10)
    criterion_entry.insert(0, criterion)
    criterion_entry.pack(pady=10)

    max_depth_entry = customtkinter.CTkEntry(random_forest_window)
    max_depth_entry.pack(pady=10)
    max_depth_entry.insert(0, max_depth)
    max_depth_entry.pack(pady=10)

    random_state_entry = customtkinter.CTkEntry(random_forest_window)
    random_state_entry.pack(pady=10)
    random_state_entry.insert(0, random_state)
    random_state_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(random_forest_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)

def open_extra_trees_window():
    n_estimators = 100
    criterion = 'gini'    
    max_depth = 'None'
    random_state = 'None'
    min_samples_split = 2
    min_samples_leaf =  1

    def retrieve_data():
        crit = criterion_entry.get()
        n_estimators = n_estimators_entry.get()
        max_d = max_depth_entry.get()
        rand_st = random_state_entry.get()
        min_samp = min_split_entry.get()
        min_leaf = min_leaf_entry.get()

        criterion_list = parse_text_entry(crit,'string')
        n_estimators_list = parse_text_entry(n_estimators,'int')
        max_depth_list = parse_text_entry(max_d,'int')
        min_split_list = parse_text_entry(min_samp,'int')
        min_leaf_list = parse_text_entry(min_leaf,'int')
        random_state_list = parse_text_entry(rand_st,'int')

        name = "Extra Trees"
        extra_trees = pipeBuild_ExtraTreesClassifier(n_estimators=n_estimators_list,criterion=criterion_list,max_depth=max_depth_list,min_samples_split=min_split_list,min_samples_leaf=min_leaf_list,random_state=random_state_list[0])
        add_to_queue(name,extra_trees)
        print("Extra Trees Model Created")

    
    extra_trees_window = customtkinter.CTkToplevel()
    extra_trees_window.title("Extra Trees Pipe Builder")
    extra_trees_window.geometry("500x400")
    extra_trees_window.attributes('-topmost', True)

    n_estimators_entry = customtkinter.CTkEntry(extra_trees_window)
    n_estimators_entry.pack(pady=10)
    n_estimators_entry.insert(0, n_estimators)
    n_estimators_entry.pack(pady=10)

    criterion_entry = customtkinter.CTkEntry(extra_trees_window)
    criterion_entry.pack(pady=10)
    criterion_entry.insert(0, criterion)
    criterion_entry.pack(pady=10)

    max_depth_entry = customtkinter.CTkEntry(extra_trees_window)
    max_depth_entry.pack(pady=10)
    max_depth_entry.insert(0, max_depth)
    max_depth_entry.pack(pady=10)

    min_split_entry = customtkinter.CTkEntry(extra_trees_window)
    min_split_entry.pack(pady=10)
    min_split_entry.insert(0, min_samples_split)
    min_split_entry.pack(pady=10)

    min_leaf_entry = customtkinter.CTkEntry(extra_trees_window)
    min_leaf_entry.pack(pady=10)
    min_leaf_entry.insert(0, min_samples_leaf)
    min_leaf_entry.pack(pady=10)

    random_state_entry = customtkinter.CTkEntry(extra_trees_window)
    random_state_entry.pack(pady=10)
    random_state_entry.insert(0, random_state)
    random_state_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(extra_trees_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)


def open_knn_window():
    new_window = customtkinter.CTkToplevel()
    new_window.title("New Window")
    label = customtkinter.CTkLabel(new_window, text="This is a new window")
    label.pack(padx=20, pady=20)

def open_tsknn_window():
    new_window = customtkinter.CTkToplevel()
    new_window.title("New Window")
    new_window.attributes('-topmost', True)
    label = customtkinter.CTkLabel(new_window, text="This is a new window")
    label.pack(padx=20, pady=20)