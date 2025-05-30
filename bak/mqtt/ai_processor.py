from sklearn.ensemble import IsolationForest
import numpy as np

def moving_average(data, window_size, time=None):
    smoothed_values = np.convolve(data, np.ones(window_size) / window_size, mode='valid')
    
    if time is not None:
        # Adjust time samples to match the length of the smoothed values
        smoothed_time_samples = time[window_size - 1:]  # Start from window_size-1 index
        return smoothed_values, smoothed_time_samples
    else:
        return smoothed_values
    
def detect_anomalies_isolation_forest(data):
    data = data.reshape(-1, 1)  # Reshape for the model
    model = IsolationForest(contamination=0.2)  # Adjust contamination as needed
    model.fit(data)
    predictions = model.predict(data)
    anomalies = np.where(predictions == -1)[0]  # Get indices of anomalies
    return anomalies
