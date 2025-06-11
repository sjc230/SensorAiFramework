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

# Gamma Regression Window
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

# Poisson Regression Window
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

# Tweedie Regression Window
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


# LARS Window
def open_lars_window():
    fit_intecept = 'True'
    max_iter = 100    
    cv = 5    

    def retrieve_data():
        fi = fit_entry.get()
        mi = max_iter_entry.get()
        c = cv_entry.get()

        fit_list = parse_text_entry(fi,'bool')
        max_iter_list = parse_text_entry(mi,'int')
        cv_list = parse_text_entry(c,'int')

        name = "LARS Regression"
        lars = pipeBuild_LarsCV(fit_intercept=fit_list, max_iter=max_iter_list, cv=cv_list)
        add_to_regress_queue(name,lars)
        print("LARS Regression Model Created")

    lars_window = customtkinter.CTkToplevel()
    lars_window.title("LARS Regression Pipe Builder")
    lars_window.geometry("500x500")
    lars_window.attributes('-topmost', True)

    fit_label = customtkinter.CTkLabel(lars_window, text="Fit Intercept: True, False")
    fit_label.pack(pady=10)

    fit_entry = customtkinter.CTkEntry(lars_window)
    fit_entry.pack(pady=10)
    fit_entry.insert(0, fit_intecept)
    fit_entry.pack(pady=10)

    max_iter_label = customtkinter.CTkLabel(lars_window, text="Max Iterations: integers")
    max_iter_label.pack()
    
    max_iter_entry = customtkinter.CTkEntry(lars_window)
    max_iter_entry.pack(pady=10)
    max_iter_entry.insert(0, max_iter)
    max_iter_entry.pack(pady=10)

    cv_label = customtkinter.CTkLabel(lars_window, text="Cross Validation: None or integers")
    cv_label.pack(pady=5)

    cv_entry = customtkinter.CTkEntry(lars_window)
    cv_entry.pack(pady=10)
    cv_entry.insert(0, cv)
    cv_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(lars_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=10)

# LASSO Window
def open_lasso_window():
    fit_intecept = 'True'
    max_iter = 100    
    cv = 5    

    def retrieve_data():
        fi = fit_entry.get()
        mi = max_iter_entry.get()
        c = cv_entry.get()

        fit_list = parse_text_entry(fi,'bool')
        max_iter_list = parse_text_entry(mi,'int')
        cv_list = parse_text_entry(c,'int')

        name = "LASSO Regression"
        lasso = pipeBuild_LassoCV(fit_intercept=fit_list, max_iter=max_iter_list, cv=cv_list)
        add_to_regress_queue(name,lasso)
        print("LASSO Regression Model Created")

    lasso_window = customtkinter.CTkToplevel()
    lasso_window.title("LASSO Regression Pipe Builder")
    lasso_window.geometry("500x500")
    lasso_window.attributes('-topmost', True)

    fit_label = customtkinter.CTkLabel(lasso_window, text="Fit Intercept: True, False")
    fit_label.pack(pady=10)

    fit_entry = customtkinter.CTkEntry(lasso_window)
    fit_entry.pack(pady=10)
    fit_entry.insert(0, fit_intecept)
    fit_entry.pack(pady=10)

    max_iter_label = customtkinter.CTkLabel(lasso_window, text="Max Iterations: integers")
    max_iter_label.pack()
    
    max_iter_entry = customtkinter.CTkEntry(lasso_window)
    max_iter_entry.pack(pady=10)
    max_iter_entry.insert(0, max_iter)
    max_iter_entry.pack(pady=10)

    cv_label = customtkinter.CTkLabel(lasso_window, text="Cross Validation: None or integers")
    cv_label.pack(pady=5)

    cv_entry = customtkinter.CTkEntry(lasso_window)
    cv_entry.pack(pady=10)
    cv_entry.insert(0, cv)
    cv_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(lasso_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=10)

# LASSO-LARS Window
def open_lasso_lars_window():
    fit_intecept = 'True'
    max_iter = 100    
    cv = 5    

    def retrieve_data():
        fi = fit_entry.get()
        mi = max_iter_entry.get()
        c = cv_entry.get()

        fit_list = parse_text_entry(fi,'bool')
        max_iter_list = parse_text_entry(mi,'int')
        cv_list = parse_text_entry(c,'int')

        name = "LASSO-LARS Regression"
        lasso_lars = pipeBuild_LassoLarsCV(fit_intercept=fit_list, max_iter=max_iter_list, cv=cv_list)
        add_to_regress_queue(name,lasso_lars)
        print("LASSO-LARS Regression Model Created")

    lasso_lars_window = customtkinter.CTkToplevel()
    lasso_lars_window.title("LASSO-LARS Regression Pipe Builder")
    lasso_lars_window.geometry("500x500")
    lasso_lars_window.attributes('-topmost', True)

    fit_label = customtkinter.CTkLabel(lasso_lars_window, text="Fit Intercept: True, False")
    fit_label.pack(pady=10)

    fit_entry = customtkinter.CTkEntry(lasso_lars_window)
    fit_entry.pack(pady=10)
    fit_entry.insert(0, fit_intecept)
    fit_entry.pack(pady=10)

    max_iter_label = customtkinter.CTkLabel(lasso_lars_window, text="Max Iterations: integers")
    max_iter_label.pack()
    
    max_iter_entry = customtkinter.CTkEntry(lasso_lars_window)
    max_iter_entry.pack(pady=10)
    max_iter_entry.insert(0, max_iter)
    max_iter_entry.pack(pady=10)

    cv_label = customtkinter.CTkLabel(lasso_lars_window, text="Cross Validation: None or integers")
    cv_label.pack(pady=5)

    cv_entry = customtkinter.CTkEntry(lasso_lars_window)
    cv_entry.pack(pady=10)
    cv_entry.insert(0, cv)
    cv_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(lasso_lars_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=10)

# LASSO-LARS with Information Criteria Window
def open_lasso_lars_ic_window():
    criterion = 'aic'
    fit_intecept = 'True'
    max_iter = 100    

    def retrieve_data():
        cr = criterion_entry.get()
        fi = fit_entry.get()
        mi = max_iter_entry.get()

        criterion_list = parse_text_entry(cr,'string')
        fit_list = parse_text_entry(fi,'bool')
        max_iter_list = parse_text_entry(mi,'int')

        name = "LASSO-LARS IC"
        lasso_lars_ic = pipeBuild_LassoLarsIC(criterion=criterion_list,fit_intercept=fit_list, max_iter=max_iter_list)
        add_to_regress_queue(name,lasso_lars_ic)
        print("LASSO-LARS w/ Information Criterion Model Created")

    lasso_lars_ic_window = customtkinter.CTkToplevel()
    lasso_lars_ic_window.title("LASSO-LARS w/ Information Criterion Pipe Builder")
    lasso_lars_ic_window.geometry("500x500")
    lasso_lars_ic_window.attributes('-topmost', True)

    criterion_label = customtkinter.CTkLabel(lasso_lars_ic_window, text="Criterion: aic, bic")
    criterion_label.pack()

    criterion_entry = customtkinter.CTkEntry(lasso_lars_ic_window)
    criterion_entry.pack(pady=10)
    criterion_entry.insert(0, criterion)
    criterion_entry.pack(pady=10)

    fit_label = customtkinter.CTkLabel(lasso_lars_ic_window, text="Fit Intercept: True, False")
    fit_label.pack(pady=10)

    fit_entry = customtkinter.CTkEntry(lasso_lars_ic_window)
    fit_entry.pack(pady=10)
    fit_entry.insert(0, fit_intecept)
    fit_entry.pack(pady=10)

    max_iter_label = customtkinter.CTkLabel(lasso_lars_ic_window, text="Max Iterations: integers")
    max_iter_label.pack()
    
    max_iter_entry = customtkinter.CTkEntry(lasso_lars_ic_window)
    max_iter_entry.pack(pady=10)
    max_iter_entry.insert(0, max_iter)
    max_iter_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(lasso_lars_ic_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=10)


# Ridge Regression Window
def open_ridge_window():
    fit_intecept = 'True'
    cv = 'None'    

    def retrieve_data():
        c = cv_entry.get()
        fi = fit_entry.get()

        cv_list = parse_text_entry(c,'int')
        fit_list = parse_text_entry(fi,'bool')

        name = "Ridge Regression"
        ridge = pipeBuild_RidgeCV(cv=cv_list,fit_intercept=fit_list)
        add_to_regress_queue(name,ridge)
        print("Ridge Regression Model Created")

    ridge_window = customtkinter.CTkToplevel()
    ridge_window.title("Ridge Regression Pipe Builder")
    ridge_window.geometry("500x500")
    ridge_window.attributes('-topmost', True)

    fit_label = customtkinter.CTkLabel(ridge_window, text="Fit Intercept: True, False")
    fit_label.pack(pady=10)

    fit_entry = customtkinter.CTkEntry(ridge_window)
    fit_entry.pack(pady=10)
    fit_entry.insert(0, fit_intecept)
    fit_entry.pack(pady=10)

    cv_label = customtkinter.CTkLabel(ridge_window, text="Cross Validation: None or integers")
    cv_label.pack(pady=5)

    cv_entry = customtkinter.CTkEntry(ridge_window)
    cv_entry.pack(pady=10)
    cv_entry.insert(0, cv)
    cv_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(ridge_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=10)

# Bayesian Ridge Regression Window
def open_bayes_ridge_window():
    alpha_init = 'None'
    lambda_init = 'None' 
    fit_intecept = 'True'       

    def retrieve_data():
        ai = alpha_init_entry.get()
        fi = fit_entry.get()
        li = lambda_init_entry.get()

        alpha_init_list = parse_text_entry(ai,'int')
        fit_list = parse_text_entry(fi,'bool')
        lambda_init_list = parse_text_entry(li,'int')

        name = "Bayesian Ridge"
        bayridge = pipeBuild_BayesianRidge(alpha_init=alpha_init_list,fit_intercept=fit_list, lambda_init=lambda_init_list)
        add_to_regress_queue(name,bayridge)
        print("Bayesian Ridge Model Created")

    bayes_ridge_window = customtkinter.CTkToplevel()
    bayes_ridge_window.title("Bayesian Ridge Pipe Builder")
    bayes_ridge_window.geometry("500x500")
    bayes_ridge_window.attributes('-topmost', True)

    alpha_init_label = customtkinter.CTkLabel(bayes_ridge_window, text="Initial Alpha Value: None or integers")
    alpha_init_label.pack()

    alpha_init_entry = customtkinter.CTkEntry(bayes_ridge_window)
    alpha_init_entry.pack(pady=10)
    alpha_init_entry.insert(0, alpha_init)
    alpha_init_entry.pack(pady=10)

    lambda_init_label = customtkinter.CTkLabel(bayes_ridge_window, text="Initial Lambda Value: None or integers")
    lambda_init_label.pack()
    
    lambda_init_entry = customtkinter.CTkEntry(bayes_ridge_window)
    lambda_init_entry.pack(pady=10)
    lambda_init_entry.insert(0, lambda_init)
    lambda_init_entry.pack(pady=10)

    fit_label = customtkinter.CTkLabel(bayes_ridge_window, text="Fit Intercept: True, False")
    fit_label.pack(pady=10)

    fit_entry = customtkinter.CTkEntry(bayes_ridge_window)
    fit_entry.pack(pady=10)
    fit_entry.insert(0, fit_intecept)
    fit_entry.pack(pady=10)    

    add_to_queue_button = customtkinter.CTkButton(bayes_ridge_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=10)


# Elastic Net Window
def open_elastic_net_window():
    selection = 'cyclic' 
    fit_intecept = 'True'       

    def retrieve_data():
        s = selection_entry.get()
        fi = fit_entry.get()

        selection_list = parse_text_entry(s,'string')
        fit_list = parse_text_entry(fi,'bool')

        name = "Elastic Net"
        enet = pipeBuild_ElasticNetCV(selection=selection_list,fit_intercept=fit_list)
        add_to_regress_queue(name,enet)
        print("Elastic Nete Model Created")

    enet_window = customtkinter.CTkToplevel()
    enet_window.title("Elastic Net Builder")
    enet_window.geometry("500x500")
    enet_window.attributes('-topmost', True)

    selection_label = customtkinter.CTkLabel(enet_window, text="Selection: cyclic, random")
    selection_label.pack()

    selection_entry = customtkinter.CTkEntry(enet_window)
    selection_entry.pack(pady=10)
    selection_entry.insert(0, selection)
    selection_entry.pack(pady=10)

    fit_label = customtkinter.CTkLabel(enet_window, text="Fit Intercept: True, False")
    fit_label.pack(pady=10)

    fit_entry = customtkinter.CTkEntry(enet_window)
    fit_entry.pack(pady=10)
    fit_entry.insert(0, fit_intecept)
    fit_entry.pack(pady=10)    

    add_to_queue_button = customtkinter.CTkButton(enet_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=10)

# Quantile Window
def open_quantile_window():
    alpha = 0.5 
    fit_intecept = 'True'       

    def retrieve_data():
        a = alpha_entry.get()
        fi = fit_entry.get()

        alpha_list = parse_text_entry(a,'float')
        fit_list = parse_text_entry(fi,'bool')

        name = "Quantile Regressor"
        enet = pipeBuild_QuantileRegressor(alpha=alpha_list,fit_intercept=fit_list)
        add_to_regress_queue(name,enet)
        print("Quantile Regressor Model Created")

    quant_window = customtkinter.CTkToplevel()
    quant_window.title("Quantile Regressor Pipe Builder")
    quant_window.geometry("500x500")
    quant_window.attributes('-topmost', True)

    alpha_label = customtkinter.CTkLabel(quant_window, text="Alpha: floats")
    alpha_label.pack()

    alpha_entry = customtkinter.CTkEntry(quant_window)
    alpha_entry.pack(pady=10)
    alpha_entry.insert(0, alpha)
    alpha_entry.pack(pady=10)

    fit_label = customtkinter.CTkLabel(quant_window, text="Fit Intercept: True, False")
    fit_label.pack(pady=10)

    fit_entry = customtkinter.CTkEntry(quant_window)
    fit_entry.pack(pady=10)
    fit_entry.insert(0, fit_intecept)
    fit_entry.pack(pady=10)    

    add_to_queue_button = customtkinter.CTkButton(quant_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=10)