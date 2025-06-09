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

def add_to_class_queue(name,model):
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

def reset_class_queue():
    global class_queue_names
    global class_queue_models
    class_queue_names = []
    class_queue_models = []

def execute_class_gridsearch():
    global class_queue_names
    global class_queue_models

    X_train, y_train, X_test, y_test = load_gui_data()

    gridsearch_classifier(names=class_queue_names,pipes=class_queue_models,
                              X_train=X_train,X_test=X_test,y_train=y_train,y_test=y_test,
                              plot_number=3,scoring="neg_mean_squared_error",save_best=True)



# Decision Tree Window
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
        add_to_class_queue(name,decision_tree)
        print("Decision Tree Model Created")

    decision_tree_window = customtkinter.CTkToplevel()
    decision_tree_window.title("Decision Tree Pipe Builder")
    decision_tree_window.geometry("500x500")
    decision_tree_window.attributes('-topmost', True)

    criterion_label = customtkinter.CTkLabel(decision_tree_window, text="Criterion: gini, entropy, or log_loss")
    criterion_label.pack()

    criterion_entry = customtkinter.CTkEntry(decision_tree_window)
    criterion_entry.pack(pady=10)
    criterion_entry.insert(0, criterion)
    criterion_entry.pack(pady=10)

    splitter_label = customtkinter.CTkLabel(decision_tree_window, text="Splitter: best, random")
    splitter_label.pack()

    splitter_entry = customtkinter.CTkEntry(decision_tree_window)
    splitter_entry.pack(pady=10)
    splitter_entry.insert(0, splitter)
    splitter_entry.pack(pady=10)

    max_depth_label = customtkinter.CTkLabel(decision_tree_window, text="Maximum Tree Depth: integers")
    max_depth_label.pack()

    max_depth_entry = customtkinter.CTkEntry(decision_tree_window)
    max_depth_entry.pack(pady=10)
    max_depth_entry.insert(0, max_depth)
    max_depth_entry.pack(pady=10)

    random_label = customtkinter.CTkLabel(decision_tree_window, text="Random State: None or a single integer")
    random_label.pack()

    random_state_entry = customtkinter.CTkEntry(decision_tree_window)
    random_state_entry.pack(pady=10)
    random_state_entry.insert(0, random_state)
    random_state_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(decision_tree_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)
    

# Random Forest Window
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
        add_to_class_queue(name,random_forest)
        print("Random Forest Model Created")

    
    random_forest_window = customtkinter.CTkToplevel()
    random_forest_window.title("Raondom Forest Pipe Builder")
    random_forest_window.geometry("500x500")
    random_forest_window.attributes('-topmost', True)

    n_estimators_label = customtkinter.CTkLabel(random_forest_window, text="Number of Estimators: integers")
    n_estimators_label.pack() 

    n_estimators_entry = customtkinter.CTkEntry(random_forest_window)
    n_estimators_entry.pack(pady=10)
    n_estimators_entry.insert(0, n_estimators)
    n_estimators_entry.pack(pady=10)

    criterion_label = customtkinter.CTkLabel(random_forest_window, text="Criterion: gini, entropy, or log_loss")
    criterion_label.pack()

    criterion_entry = customtkinter.CTkEntry(random_forest_window)
    criterion_entry.pack(pady=10)
    criterion_entry.insert(0, criterion)
    criterion_entry.pack(pady=10)

    max_depth_label = customtkinter.CTkLabel(random_forest_window, text="Maximum Tree Depth: integers")
    max_depth_label.pack()

    max_depth_entry = customtkinter.CTkEntry(random_forest_window)
    max_depth_entry.pack(pady=10)
    max_depth_entry.insert(0, max_depth)
    max_depth_entry.pack(pady=10)

    random_label = customtkinter.CTkLabel(random_forest_window, text="Random State: None or a single integer")
    random_label.pack()

    random_state_entry = customtkinter.CTkEntry(random_forest_window)
    random_state_entry.pack(pady=10)
    random_state_entry.insert(0, random_state)
    random_state_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(random_forest_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)


# Extra Trees Window
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
        add_to_class_queue(name,extra_trees)
        print("Extra Trees Model Created")

    
    extra_trees_window = customtkinter.CTkToplevel()
    extra_trees_window.title("Extra Trees Pipe Builder")
    extra_trees_window.geometry("500x550")
    extra_trees_window.attributes('-topmost', True)

    n_estimators_label = customtkinter.CTkLabel(extra_trees_window, text="Number of Estimators: integers")
    n_estimators_label.pack()  

    n_estimators_entry = customtkinter.CTkEntry(extra_trees_window)
    n_estimators_entry.pack(pady=10)
    n_estimators_entry.insert(0, n_estimators)
    n_estimators_entry.pack(pady=10)

    criterion_label = customtkinter.CTkLabel(extra_trees_window, text="Criterion: gini, entropy, or log_loss")
    criterion_label.pack()

    criterion_entry = customtkinter.CTkEntry(extra_trees_window)
    criterion_entry.pack(pady=10)
    criterion_entry.insert(0, criterion)
    criterion_entry.pack(pady=10)

    max_depth_label = customtkinter.CTkLabel(extra_trees_window, text="Maximum Tree Depth: integers")
    max_depth_label.pack()

    max_depth_entry = customtkinter.CTkEntry(extra_trees_window)
    max_depth_entry.pack(pady=10)
    max_depth_entry.insert(0, max_depth)
    max_depth_entry.pack(pady=10)


    min_split_label = customtkinter.CTkLabel(extra_trees_window, text="Minimum Sample # for Node Splits: integers")
    min_split_label.pack()

    min_split_entry = customtkinter.CTkEntry(extra_trees_window)
    min_split_entry.pack(pady=10)
    min_split_entry.insert(0, min_samples_split)
    min_split_entry.pack(pady=10)

    min_leaf_label = customtkinter.CTkLabel(extra_trees_window, text="Minimum Sample # Required for a Leaf: integers")
    min_leaf_label.pack()

    min_leaf_entry = customtkinter.CTkEntry(extra_trees_window)
    min_leaf_entry.pack(pady=10)
    min_leaf_entry.insert(0, min_samples_leaf)
    min_leaf_entry.pack(pady=10)

    random_label = customtkinter.CTkLabel(extra_trees_window, text="Random State: None or a single integer")
    random_label.pack()

    random_state_entry = customtkinter.CTkEntry(extra_trees_window)
    random_state_entry.pack(pady=10)
    random_state_entry.insert(0, random_state)
    random_state_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(extra_trees_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)


# K Nearest Neighbors Window
def open_knn_window():
    n_neighbors = 5
    weights = 'uniform'
    algorithm = 'auto'
    leaf_size = 30

    def retrieve_data():
        nn = nn_entry.get()
        wt = wt_entry.get()
        algo = algo_entry.get()
        leaf = leaf_entry.get()

        nn_list = parse_text_entry(nn,'int')
        wt_list = parse_text_entry(wt,'string')
        algo_list = parse_text_entry(algo,'string')
        leaf_list = parse_text_entry(leaf,'int')

        name = "K Nearest Neighbors"
        knn = pipeBuild_KNeighborsClassifier(n_neighbors=nn_list,weights=wt_list,algorithm=algo_list,leaf_size=leaf_list)
        add_to_class_queue(name,knn)
        print("K Nearest Neighbors Model Created")

    knn_window = customtkinter.CTkToplevel()
    knn_window.title("K Nearest Neighbors Pipe Builder")
    knn_window.geometry("500x500")
    knn_window.attributes('-topmost', True)

    nn_label = customtkinter.CTkLabel(knn_window, text="Number of Neighbors: integers only")
    nn_label.pack()

    nn_entry = customtkinter.CTkEntry(knn_window)
    nn_entry.pack(pady=10)
    nn_entry.insert(0, n_neighbors)
    nn_entry.pack(pady=10)

    wt_label = customtkinter.CTkLabel(knn_window, text="Weights: uniform, distance")
    wt_label.pack()

    wt_entry = customtkinter.CTkEntry(knn_window)
    wt_entry.pack(pady=10)
    wt_entry.insert(0, weights)
    wt_entry.pack(pady=10)

    algo_label = customtkinter.CTkLabel(knn_window, text="Algorithm: auto, ball_tree, kd_tree, brute")
    algo_label.pack()

    algo_entry = customtkinter.CTkEntry(knn_window)
    algo_entry.pack(pady=10)
    algo_entry.insert(0, algorithm)
    algo_entry.pack(pady=10)

    leaf_label = customtkinter.CTkLabel(knn_window, text="Leaf Size: integers only")
    leaf_label.pack()

    leaf_entry = customtkinter.CTkEntry(knn_window)
    leaf_entry.pack(pady=10)
    leaf_entry.insert(0, leaf_size)
    leaf_entry.pack(pady=10)

    add_to_queue_button = customtkinter.CTkButton(knn_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)


# Nearest Cetroid Window
def open_nearest_centroid_window():
    metric = 'euclidean'
    shrink_treshold = 'None'

    def retrieve_data():
        met = metric_entry.get()
        shrink = shrink_entry.get()

        metric_list = parse_text_entry(met,'string')
        shrink_list = parse_text_entry(shrink,'float')

        name = "Nearest Centroid"
        nc = pipeBuild_NearestCentroid(metric=metric_list,shrink_threshold=shrink_list)
        add_to_class_queue(name,nc)
        print("Nearest Centroid Model Created")

    nc_window = customtkinter.CTkToplevel()
    nc_window.title("Nearest Centroid Pipe Builder")
    nc_window.geometry("500x500")
    nc_window.attributes('-topmost', True)

    nn_label = customtkinter.CTkLabel(nc_window, text="Distance Metric: euclidean, manhattan, chebyshev, minkowski")
    nn_label.pack()

    metric_entry = customtkinter.CTkEntry(nc_window)
    metric_entry.pack(pady=10)
    metric_entry.insert(0, metric)
    metric_entry.pack(pady=10)

    shrink_label = customtkinter.CTkLabel(nc_window, text="Shrink Threshold: None and floats")
    shrink_label.pack()

    shrink_entry = customtkinter.CTkEntry(nc_window)
    shrink_entry.pack(pady=10)
    shrink_entry.insert(0, shrink_treshold)
    shrink_entry.pack(pady=10)    

    add_to_queue_button = customtkinter.CTkButton(nc_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)


# Radius Nearest Neighbors
def open_radiusnn_window():
    radius = 1.0
    weights = 'uniform'
    algorithm = 'auto'
    leaf_size = 30
    p = 2
    metric = 'minkowski'

    def retrieve_data():
        rad = radius_entry.get()
        wt = weights_entry.get()
        algo = algo_entry.get()
        leaf = leaf_entry.get()
        power = power_entry.get()
        met = metric_entry.get()
        
        radius_list = parse_text_entry(rad,'float')
        weight_list = parse_text_entry(wt,'string')
        algo_list = parse_text_entry(algo,'string')
        leaf_list = parse_text_entry(leaf,'int')
        power_list = parse_text_entry(power,'int')
        metric_list = parse_text_entry(met,'string')
        

        name = "Radius Nearest Neighbors"
        rnn = pipeBuild_RadiusNeighborsClassifier(radius=radius_list,weights=weight_list,algorithm=algo_list,leaf_size=leaf_list,p=power_list,metric=metric_list)
        add_to_class_queue(name,rnn)
        print("Radius Nearest Neighbors Model Created")

    radiusnn_window = customtkinter.CTkToplevel()
    radiusnn_window.title("Radius Nearest Neighbor Pipe Builder")
    radiusnn_window.geometry("500x550")
    radiusnn_window.attributes('-topmost', True)

    radius_label = customtkinter.CTkLabel(radiusnn_window, text="Radius: floats only")
    radius_label.pack()

    radius_entry = customtkinter.CTkEntry(radiusnn_window)
    radius_entry.pack(pady=10)
    radius_entry.insert(0, radius)
    radius_entry.pack(pady=10)

    weights_label = customtkinter.CTkLabel(radiusnn_window, text="Weight: uniform, distance")
    weights_label.pack()

    weights_entry = customtkinter.CTkEntry(radiusnn_window)
    weights_entry.pack(pady=10)
    weights_entry.insert(0, weights)
    weights_entry.pack(pady=10)

    algo_label = customtkinter.CTkLabel(radiusnn_window, text="Algorithm: auto, ball_tree, kd_tree, brute")
    algo_label.pack()

    algo_entry = customtkinter.CTkEntry(radiusnn_window)
    algo_entry.pack(pady=10)
    algo_entry.insert(0, algorithm)
    algo_entry.pack(pady=10)

    leaf_label = customtkinter.CTkLabel(radiusnn_window, text="Leaf Size: integers only")
    leaf_label.pack()

    leaf_entry = customtkinter.CTkEntry(radiusnn_window)
    leaf_entry.pack(pady=10)
    leaf_entry.insert(0, leaf_size)
    leaf_entry.pack(pady=10)

    power_label = customtkinter.CTkLabel(radiusnn_window, text="Weight: uniform, distance")
    power_label.pack()

    power_entry = customtkinter.CTkEntry(radiusnn_window)
    power_entry.pack(pady=10)
    power_entry.insert(0, p)
    power_entry.pack(pady=10)

    metric_label = customtkinter.CTkLabel(radiusnn_window, text="Distance Metric: euclidean, manhattan, chebyshev, minkowski")
    metric_label.pack()

    metric_entry = customtkinter.CTkEntry(radiusnn_window)
    metric_entry.pack(pady=10)
    metric_entry.insert(0, metric)
    metric_entry.pack(pady=10)    

    add_to_queue_button = customtkinter.CTkButton(radiusnn_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)


# Time Series KNN Window
def open_tsknn_window():
    n_neighbors = 5
    weights = 'uniform'
    metric = 'dtw'

    def retrieve_data():
        nn = nn_entry.get()
        wt = wt_entry.get()
        met = metric_entry.get()

        nn_list = parse_text_entry(nn,'int')
        wt_list = parse_text_entry(wt,'string')
        met_list = parse_text_entry(met,'string')

        name = "Time Series KNN"
        tsknn = pipeBuild_KNeighborsTimeSeriesClassifier(n_neighbors=nn_list, weights=wt_list, metric=met_list)
        add_to_class_queue(name,tsknn)
        print("Time Series KNN Model Created")

    tsknn_window = customtkinter.CTkToplevel()
    tsknn_window.title("Time Series KNN Pipe Builder")
    tsknn_window.geometry("500x500")
    tsknn_window.attributes('-topmost', True)

    nn_label = customtkinter.CTkLabel(tsknn_window, text="Number of Neighbors: integers only")
    nn_label.pack()

    nn_entry = customtkinter.CTkEntry(tsknn_window)
    nn_entry.pack(pady=10)
    nn_entry.insert(0, n_neighbors)
    nn_entry.pack(pady=10)

    wt_label = customtkinter.CTkLabel(tsknn_window, text="Weights: uniform, distance")
    wt_label.pack()

    wt_entry = customtkinter.CTkEntry(tsknn_window)
    wt_entry.pack(pady=10)
    wt_entry.insert(0, weights)
    wt_entry.pack(pady=10)

    metric_label = customtkinter.CTkLabel(tsknn_window, text="Distance Metric: dtw, softdtw, ctw, sqeuclidean, sax")
    metric_label.pack()

    metric_entry = customtkinter.CTkEntry(tsknn_window)
    metric_entry.pack(pady=10)
    metric_entry.insert(0, metric)
    metric_entry.pack(pady=10) 

    add_to_queue_button = customtkinter.CTkButton(tsknn_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)


# Support Vector Classifier Window
def open_svc_window():
    C = 1.0
    kernel = 'rbf'
    degree = 3
    gamma = 'scale'
    tol = 0.001

    def retrieve_data():
        c = reg_entry.get()
        k = kernel_entry.get()
        d = degree_entry.get()
        g = gamma_entry.get()
        t = tol_entry.get()
        
        reg_list = parse_text_entry(c,'float')
        kernel_list = parse_text_entry(k,'string')
        degree_list = parse_text_entry(d,'int')
        gamma_list = parse_text_entry(g,'string')
        tol_list = parse_text_entry(t,'float')        

        name = "Support Vector Classifier"
        svc = pipeBuild_SVC(C=reg_list,kernel=kernel_list,degree=degree_list,gamma=gamma_list,tol=tol_list,random_state=None)
        add_to_class_queue(name,svc)
        print("Support Vector Classifier Model Created")

    svc_window = customtkinter.CTkToplevel()
    svc_window.title("Support Vector Classifier Pipe Builder")
    svc_window.geometry("500x500")
    svc_window.attributes('-topmost', True)

    reg_label = customtkinter.CTkLabel(svc_window, text="Regularization Parameter: floats only")
    reg_label.pack()

    reg_entry = customtkinter.CTkEntry(svc_window)
    reg_entry.pack(pady=10)
    reg_entry.insert(0, C)
    reg_entry.pack(pady=10)

    kernel_label = customtkinter.CTkLabel(svc_window, text="Kernel: linear, poly, rbf, sigmoid")
    kernel_label.pack()

    kernel_entry = customtkinter.CTkEntry(svc_window)
    kernel_entry.pack(pady=10)
    kernel_entry.insert(0, kernel)
    kernel_entry.pack(pady=10)

    degree_label = customtkinter.CTkLabel(svc_window, text="Degree (for poly kernel): integers only")
    degree_label.pack()

    degree_entry = customtkinter.CTkEntry(svc_window)
    degree_entry.pack(pady=10)
    degree_entry.insert(0, degree)
    degree_entry.pack(pady=10)

    gamma_label = customtkinter.CTkLabel(svc_window, text="Gamma: scale, auto")
    gamma_label.pack()

    gamma_entry = customtkinter.CTkEntry(svc_window)
    gamma_entry.pack(pady=10)
    gamma_entry.insert(0, gamma)
    gamma_entry.pack(pady=10)

    tol_label = customtkinter.CTkLabel(svc_window, text="Tolerance: floats only")
    tol_label.pack()

    tol_entry = customtkinter.CTkEntry(svc_window)
    tol_entry.pack(pady=10)
    tol_entry.insert(0, tol)
    tol_entry.pack(pady=10)
   
    add_to_queue_button = customtkinter.CTkButton(svc_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)

# Nu Support Vector Classifier Window
def open_nusvc_window():
    nu = 0.5
    kernel = 'rbf'
    degree = 3
    gamma = 'scale'
    tol = 0.001

    def retrieve_data():
        n = nu_entry.get()
        k = kernel_entry.get()
        d = degree_entry.get()
        g = gamma_entry.get()
        t = tol_entry.get()
        
        nu_list = parse_text_entry(n,'float')
        kernel_list = parse_text_entry(k,'string')
        degree_list = parse_text_entry(d,'int')
        gamma_list = parse_text_entry(g,'string')
        tol_list = parse_text_entry(t,'float')        

        name = "Nu Support Vector Classifier"
        nusvc = pipeBuild_NuSVC(nu=nu_list,kernel=kernel_list,degree=degree_list,gamma=gamma_list,tol=tol_list,random_state=None)
        add_to_class_queue(name,nusvc)
        print("Nu Support Vector Classifier Model Created")

    nusvc_window = customtkinter.CTkToplevel()
    nusvc_window.title("Nu Support Vector Classifier Pipe Builder")
    nusvc_window.geometry("500x500")
    nusvc_window.attributes('-topmost', True)

    nu_label = customtkinter.CTkLabel(nusvc_window, text="Regularization Parameter: floats only")
    nu_label.pack()

    nu_entry = customtkinter.CTkEntry(nusvc_window)
    nu_entry.pack(pady=10)
    nu_entry.insert(0, nu)
    nu_entry.pack(pady=10)

    kernel_label = customtkinter.CTkLabel(nusvc_window, text="Kernel: linear, poly, rbf, sigmoid")
    kernel_label.pack()

    kernel_entry = customtkinter.CTkEntry(nusvc_window)
    kernel_entry.pack(pady=10)
    kernel_entry.insert(0, kernel)
    kernel_entry.pack(pady=10)

    degree_label = customtkinter.CTkLabel(nusvc_window, text="Degree (for poly kernel): integers only")
    degree_label.pack()

    degree_entry = customtkinter.CTkEntry(nusvc_window)
    degree_entry.pack(pady=10)
    degree_entry.insert(0, degree)
    degree_entry.pack(pady=10)

    gamma_label = customtkinter.CTkLabel(nusvc_window, text="Gamma: scale, auto")
    gamma_label.pack()

    gamma_entry = customtkinter.CTkEntry(nusvc_window)
    gamma_entry.pack(pady=10)
    gamma_entry.insert(0, gamma)
    gamma_entry.pack(pady=10)

    tol_label = customtkinter.CTkLabel(nusvc_window, text="Tolerance: floats only")
    tol_label.pack()

    tol_entry = customtkinter.CTkEntry(nusvc_window)
    tol_entry.pack(pady=10)
    tol_entry.insert(0, tol)
    tol_entry.pack(pady=10)
   
    add_to_queue_button = customtkinter.CTkButton(nusvc_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)

# Time Series Support Vector Classifier Window
def open_tssvc_window():
    C = 1.0
    kernel = 'gak'
    degree = 3
    gamma = 'None'
    tol = 0.001

    def retrieve_data():
        c = reg_entry.get()
        k = kernel_entry.get()
        d = degree_entry.get()
        g = gamma_entry.get()
        t = tol_entry.get()

             
        reg_list = parse_text_entry(c,'float')
        kernel_list = parse_text_entry(k,'string')
        degree_list = parse_text_entry(d,'int')
        gamma_list = parse_text_entry(g,'float')
        tol_list = parse_text_entry(t,'float')

        gamma_list = ['auto' if item is None else item for item in gamma_list]

        name = "Time Series SVC"
        svc = pipeBuild_TimeSeriesSVC(C=reg_list,kernel=kernel_list,degree=degree_list,gamma=gamma_list,tol=tol_list,random_state=None)
        add_to_class_queue(name,svc)
        print("Time Series SVC Model Created")

    svc_window = customtkinter.CTkToplevel()
    svc_window.title("Time Series SVC Pipe Builder")
    svc_window.geometry("500x500")
    svc_window.attributes('-topmost', True)

    reg_label = customtkinter.CTkLabel(svc_window, text="Regularization Parameter: None or floats")
    reg_label.pack()

    reg_entry = customtkinter.CTkEntry(svc_window)
    reg_entry.pack(pady=10)
    reg_entry.insert(0, C)
    reg_entry.pack(pady=10)

    kernel_label = customtkinter.CTkLabel(svc_window, text="Kernel: gak, linear, poly, rbf, sigmoid")
    kernel_label.pack()

    kernel_entry = customtkinter.CTkEntry(svc_window)
    kernel_entry.pack(pady=10)
    kernel_entry.insert(0, kernel)
    kernel_entry.pack(pady=10)

    degree_label = customtkinter.CTkLabel(svc_window, text="Degree (for poly kernel): integers only")
    degree_label.pack()

    degree_entry = customtkinter.CTkEntry(svc_window)
    degree_entry.pack(pady=10)
    degree_entry.insert(0, degree)
    degree_entry.pack(pady=10)

    gamma_label = customtkinter.CTkLabel(svc_window, text="Gamma: None or floats")
    gamma_label.pack()

    gamma_entry = customtkinter.CTkEntry(svc_window)
    gamma_entry.pack(pady=10)
    gamma_entry.insert(0, gamma)
    gamma_entry.pack(pady=10)

    tol_label = customtkinter.CTkLabel(svc_window, text="Tolerance: floats only")
    tol_label.pack()

    tol_entry = customtkinter.CTkEntry(svc_window)
    tol_entry.pack(pady=10)
    tol_entry.insert(0, tol)
    tol_entry.pack(pady=10)
   
    add_to_queue_button = customtkinter.CTkButton(svc_window, text="Add Model to Queue", command=retrieve_data)
    add_to_queue_button.pack(pady=20)