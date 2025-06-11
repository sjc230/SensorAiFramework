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
                              X_train=X_train,X_test=X_test,y_train=y_train,y_test=y_test,
                              scoring="neg_mean_squared_error",save_best=True)

# Linear Regression Window
def open_linear_window():
    fit_intecept = 'True'

    def retrieve_data():
        fi = fit_entry.get()

        fit_list = parse_text_entry(fi,'bool')

        name = "Linear Regression"
        linear = pipeBuild_LinearRegression(fit_intercept=fit_list)
        add_to_regress_queue(name,linear)
        print("Linear Regression Model Created")

    linear_window = customtkinter.CTkToplevel()
    linear_window.title("Linear Regression Pipe Builder")
    linear_window.geometry("500x400")
    linear_window.attributes('-topmost', True)

    fit_label = customtkinter.CTkLabel(linear_window, text="Fit Intercept: True, False")
    fit_label.pack(pady=10)

    fit_entry = customtkinter.CTkEntry(linear_window)
    fit_entry.pack(pady=10)
    fit_entry.insert(0, fit_intecept)
    fit_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(linear_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=10)

# Gamma Regression Windo
def open_gamma_window():
    alpha = 1
    fit_intecept = 'True'
    solver = 'lbfgs'
    max_iter = 100
    tol = 0.0001

    def retrieve_data():
        a = alpha_entry.get()
        fi = fit_entry.get()
        s = solver_entry.get()
        mi = max_iter_entry.get()
        t = tol_entry.get()

        alpha_list = parse_text_entry(a,'int')
        fit_list = parse_text_entry(fi,'bool')
        solver_list = parse_text_entry(s,'string')
        max_iter_list = parse_text_entry(mi,'int')
        tol_list = parse_text_entry(t,'float')

        name = "Gamma Regression"
        gamma = pipeBuild_GammaRegressor(alpha=alpha_list,fit_intercept=fit_list, solver=solver_list,max_iter=max_iter_list, tol=tol_list)
        add_to_regress_queue(name,gamma)
        print("Gamma Regression Model Created")

    gamma_window = customtkinter.CTkToplevel()
    gamma_window.title("Gamma Regression Pipe Builder")
    gamma_window.geometry("500x550")
    gamma_window.attributes('-topmost', True)

    alpha_label = customtkinter.CTkLabel(gamma_window, text="Alpha: positive integers")
    alpha_label.pack(pady=10)

    alpha_entry = customtkinter.CTkEntry(gamma_window)
    alpha_entry.pack(pady=10)
    alpha_entry.insert(0, alpha)
    alpha_entry.pack(pady=10)

    fit_label = customtkinter.CTkLabel(gamma_window, text="Fit Intercept: True, False")
    fit_label.pack(pady=10)

    fit_entry = customtkinter.CTkEntry(gamma_window)
    fit_entry.pack(pady=10)
    fit_entry.insert(0, fit_intecept)
    fit_entry.pack(pady=10)

    solver_label = customtkinter.CTkLabel(gamma_window, text="Solver: lbfgs, newton-cholesky")
    solver_label.pack(pady=10)

    solver_entry = customtkinter.CTkEntry(gamma_window)
    solver_entry.pack(pady=10)
    solver_entry.insert(0, solver)
    solver_entry.pack(pady=10)

    max_iter_label = customtkinter.CTkLabel(gamma_window, text="Max Iterations: integers")
    max_iter_label.pack()
    
    max_iter_entry = customtkinter.CTkEntry(gamma_window)
    max_iter_entry.pack(pady=10)
    max_iter_entry.insert(0, max_iter)
    max_iter_entry.pack(pady=10)

    tol_label = customtkinter.CTkLabel(gamma_window, text="Tolerance: floats only")
    tol_label.pack(pady=10)

    tol_entry = customtkinter.CTkEntry(gamma_window)
    tol_entry.pack(pady=10)
    tol_entry.insert(0, tol)
    tol_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(gamma_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=10)

# Poisson Regression Windo
def open_poisson_window():
    alpha = 1
    fit_intecept = 'True'
    solver = 'lbfgs'
    max_iter = 100
    tol = 0.0001

    def retrieve_data():
        a = alpha_entry.get()
        fi = fit_entry.get()
        s = solver_entry.get()
        mi = max_iter_entry.get()
        t = tol_entry.get()

        alpha_list = parse_text_entry(a,'int')
        fit_list = parse_text_entry(fi,'bool')
        solver_list = parse_text_entry(s,'string')
        max_iter_list = parse_text_entry(mi,'int')
        tol_list = parse_text_entry(t,'float')

        name = "Poisson Regression"
        poisson = pipeBuild_PoissonRegressor(alpha=alpha_list,fit_intercept=fit_list, solver=solver_list,max_iter=max_iter_list, tol=tol_list)
        add_to_regress_queue(name,poisson)
        print("Poisson Regression Model Created")

    poisson_window = customtkinter.CTkToplevel()
    poisson_window.title("Poisson Regression Pipe Builder")
    poisson_window.geometry("500x550")
    poisson_window.attributes('-topmost', True)

    alpha_label = customtkinter.CTkLabel(poisson_window, text="Alpha: positive integers")
    alpha_label.pack(pady=10)

    alpha_entry = customtkinter.CTkEntry(poisson_window)
    alpha_entry.pack(pady=10)
    alpha_entry.insert(0, alpha)
    alpha_entry.pack(pady=10)

    fit_label = customtkinter.CTkLabel(poisson_window, text="Fit Intercept: True, False")
    fit_label.pack(pady=10)

    fit_entry = customtkinter.CTkEntry(poisson_window)
    fit_entry.pack(pady=10)
    fit_entry.insert(0, fit_intecept)
    fit_entry.pack(pady=10)

    solver_label = customtkinter.CTkLabel(poisson_window, text="Solver: lbfgs, newton-cholesky")
    solver_label.pack(pady=10)

    solver_entry = customtkinter.CTkEntry(poisson_window)
    solver_entry.pack(pady=10)
    solver_entry.insert(0, solver)
    solver_entry.pack(pady=10)

    max_iter_label = customtkinter.CTkLabel(poisson_window, text="Max Iterations: integers")
    max_iter_label.pack()
    
    max_iter_entry = customtkinter.CTkEntry(poisson_window)
    max_iter_entry.pack(pady=10)
    max_iter_entry.insert(0, max_iter)
    max_iter_entry.pack(pady=10)

    tol_label = customtkinter.CTkLabel(poisson_window, text="Tolerance: floats only")
    tol_label.pack(pady=10)

    tol_entry = customtkinter.CTkEntry(poisson_window)
    tol_entry.pack(pady=10)
    tol_entry.insert(0, tol)
    tol_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(poisson_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=10)

# Tweedie Regression Windo
def open_tweedie_window():
    power = 0
    alpha = 1
    fit_intecept = 'True'
    link = 'auto'
    solver = 'lbfgs'
    max_iter = 100
    tol = 0.0001

    def retrieve_data():
        p = power_entry.get()
        a = alpha_entry.get()
        fi = fit_entry.get()
        l = link_entry.get()
        s = solver_entry.get()
        mi = max_iter_entry.get()
        t = tol_entry.get()

        p = p.replace('(1,2)', 'None') if '(1,2)' in p else p

        power_list = parse_text_entry(p,'int')
        alpha_list = parse_text_entry(a,'int')
        fit_list = parse_text_entry(fi,'bool')
        link_list = parse_text_entry(l,'string')
        solver_list = parse_text_entry(s,'string')
        max_iter_list = parse_text_entry(mi,'int')
        tol_list = parse_text_entry(t,'float')

        power_list = ['(1,2)' if item is None else item for item in power_list]

        name = "Tweedie Regression"
        tweedie = pipeBuild_TweedieRegressor(power=power_list, alpha=alpha_list, fit_intercept=fit_list, link=link_list,
                                             solver=solver_list, max_iter=max_iter_list, tol=tol_list)
        add_to_regress_queue(name,tweedie)
        print("Tweedie Regression Model Created")

    tweedie_window = customtkinter.CTkToplevel()
    tweedie_window.title("Tweedie Regression Pipe Builder")
    tweedie_window.geometry("500x550")
    tweedie_window.attributes('-topmost', True)

    power_label = customtkinter.CTkLabel(tweedie_window, text="Power: 0, 1, 2, 3, (1,2)")
    power_label.pack()

    power_entry = customtkinter.CTkEntry(tweedie_window)
    power_entry.pack(pady=5)
    power_entry.insert(0, power)
    power_entry.pack(pady=5)

    alpha_label = customtkinter.CTkLabel(tweedie_window, text="Alpha: positive integers")
    alpha_label.pack(pady=5)

    alpha_entry = customtkinter.CTkEntry(tweedie_window)
    alpha_entry.pack(pady=5)
    alpha_entry.insert(0, alpha)
    alpha_entry.pack(pady=5)

    fit_label = customtkinter.CTkLabel(tweedie_window, text="Fit Intercept: True, False")
    fit_label.pack(pady=5)

    fit_entry = customtkinter.CTkEntry(tweedie_window)
    fit_entry.pack(pady=5)
    fit_entry.insert(0, fit_intecept)
    fit_entry.pack(pady=5)

    link_label = customtkinter.CTkLabel(tweedie_window, text="Link Function: auto, identity, log")
    link_label.pack()

    link_entry = customtkinter.CTkEntry(tweedie_window)
    link_entry.pack(pady=5)
    link_entry.insert(0, link)
    link_entry.pack(pady=5)

    solver_label = customtkinter.CTkLabel(tweedie_window, text="Solver: lbfgs, newton-cholesky")
    solver_label.pack(pady=5)

    solver_entry = customtkinter.CTkEntry(tweedie_window)
    solver_entry.pack(pady=5)
    solver_entry.insert(0, solver)
    solver_entry.pack(pady=5)

    max_iter_label = customtkinter.CTkLabel(tweedie_window, text="Max Iterations: integers")
    max_iter_label.pack()
    
    max_iter_entry = customtkinter.CTkEntry(tweedie_window)
    max_iter_entry.pack(pady=5)
    max_iter_entry.insert(0, max_iter)
    max_iter_entry.pack(pady=5)

    tol_label = customtkinter.CTkLabel(tweedie_window, text="Tolerance: floats only")
    tol_label.pack(pady=5)

    tol_entry = customtkinter.CTkEntry(tweedie_window)
    tol_entry.pack(pady=5)
    tol_entry.insert(0, tol)
    tol_entry.pack(pady=5)

    add_to_queue_button = customtkinter.CTkButton(tweedie_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=5)