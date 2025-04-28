import numpy as np
import matplotlib.pyplot as plt
import pickle
import pandas as pd
from sklearn.metrics import confusion_matrix
import seaborn as sns
import pickle
from pathlib import Path
from datetime import datetime
import yaml

# 此代码需要大改，但暂时可以用
def calc_mae(gt, pred):
    return np.mean(abs(np.array(gt) - np.array(pred)))

def plot_2vectors(label, pred, save=False, name=None, path=None, size=1):
    """lsit1: label, list2: prediction"""

    list1 = label
    list2 = np.array(pred)
    if list2.ndim == 2:
        mae = calc_mae(list1, list2[:, 0])
    else:
        mae = calc_mae(list1, list2)

    sorted_id = sorted(range(len(list1)), key=lambda k: list1[k])

    plt.clf()
    plt.text(0, np.min(list2), f'MAE={mae}')

    plt.scatter(np.arange(list2.shape[0]), list2[sorted_id], s=size, alpha=0.5, label=f'{name} prediction', color='blue')
    plt.scatter(np.arange(list1.shape[0]), list1[sorted_id], s=size, alpha=0.5, label=f'{name} label', color='red')
    plt.legend(loc='lower right')

    if save:
        if path is None:
            raise ValueError("If save is True, 'path' argument must be provided.")
        plt.savefig(f'{path}.jpg', dpi=300)
        print(f'Saved plot to {path}.jpg')
    #plt.show()
    return plt


def ls2pkl(filepath, data):
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)

def pkl2ls(filepath):
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
    return data

def dic2pkl(filepath, data):
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)

def dicl2ls(filepath):
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
    return data

def plot_noise_signal(original_signal, noisy_signal, title_name):
    plt.figure()
    plt.plot(noisy_signal, label='Noisy Signal')
    plt.plot(original_signal, label='Original Signal')
    plt.ylabel('Amplitude')
    plt.xlabel('Time')
    plt.title(title_name)
    plt.legend()
    plt.show()

def plot_decomposed_components(signal, components, title_name):
    n_components = len(components)

    plt.subplots(n_components+1, 1)
    plt.subplot(n_components+1, 1, 1)
    plt.title(title_name)

    plt.plot(signal, label='Original Signal', color='r')

    for cnt, component in enumerate(components):
        # print(cnt+1, n_components)
        plt.subplot(n_components+1, 1, cnt+2)
        plt.plot(component, label='Component'+str(cnt+1))
        plt.legend()
    plt.ylabel('Amplitude')
    plt.xlabel('Time')
    plt.show()

def plot_filtered_signal(filtered_signal, signal, title_name):
    plt.figure()
    plt.plot(signal, label='Original Signal', alpha=0.6)
    plt.plot(filtered_signal, label='Filtered Signal')
    plt.ylabel('Amplitude')
    plt.xlabel('Time')
    plt.title(title_name)
    plt.legend()
    plt.show()

def plot_sim_waves(signal, wave_name):
    plt.figure()
    plt.plot(signal, label=wave_name)
    plt.ylabel('Amplitude')
    plt.xlabel('Time')
    plt.title('Generated Wave')
    plt.legend()
    plt.show()

def plot_adp_filtered_signal(y, d_signal, error):
    plt.figure()

    plt.subplot(211)
    plt.title("Adaptation")
    plt.ylabel('Amplitude')
    plt.xlabel('Time')
    plt.plot(d_signal, "b", label="d_signal - target")
    plt.plot(y, "g", label="output")
    plt.legend()

    plt.subplot(212)
    plt.title("Filter error")
    plt.ylabel('Amplitude')
    plt.xlabel('Time')
    plt.plot(10 * np.log10(error ** 2), "r", label="error [dB]")
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_averaging_center(center, pieces):
    plt.figure()
    plt.title("Center of Signal Pieces")
    for piece in pieces:
        plt.plot(piece, alpha=0.35)
    plt.plot(center, "r", linewidth=2, label="Center")
    plt.ylabel('Amplitude')
    plt.xlabel('Time')
    plt.legend()
    plt.show()

def plot_confusion_matrix(y_true, y_pred, classes, title='Confusion Matrix', cmap='Blues'):
    """
    Plots the confusion matrix.

    Parameters:
        y_true (array-like): True labels.
        y_pred (array-like): Predicted labels.
        classes (list): List of class names.
        title (str, optional): Title for the plot. Defaults to 'Confusion Matrix'.
        cmap (str, optional): Colormap for the heatmap. Defaults to 'Blues'.
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap=cmap, xticklabels=classes, yticklabels=classes)
    plt.title(title)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.show()


# Load the model from a pickle file
def load_model(filename):
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    return model

# Save model to a pickle file
def save_model(model,filename):
    with open(filename, 'wb') as file:
        pickle.dump(model, file)
    return

# returns current time stamp string in yyyymmddhhmmss format
def get_timestamp_string():
    now = datetime.now()
    timestamp_string = now.strftime("%Y%m%d%H%M%S")
    return timestamp_string


# create a new directory based on name string and return the path
def create_directory(directory_name):
    directory_path = Path(directory_name)
    try:
        # Create the directory
        directory_path.mkdir()
        print(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return directory_path

def create_model_yaml(yaml_name,model_name,model_path,model_type,n_inputs,n_outputs):
    # Data to write to the YAML file (Python dictionary)
    data = {
        'name': model_name,
        'model_path': model_path, 
        'model_type': model_type,
        'inputs': n_inputs,
        'outputs': n_outputs
        }

    file = model_path + '/' + yaml_name

    # Open the YAML file in write mode
    with open(model_path + '/' + yaml_name, "w") as file:
        # Write the data to the YAML file
        yaml.dump(data, file, default_flow_style=False)
    return