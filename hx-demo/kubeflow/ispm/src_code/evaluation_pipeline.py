
"""
evaluation stage for ILE forecasting model
====================
"""

import os
from typing import List
from src_user.models.initialDNN import initialDNN

import torch
import torch.nn as nn
import torch.optim as optim
from src_user.utils.data import preprocess_data
import pandas as pd
from torcheval.metrics import MultilabelAccuracy

def main() -> None:
    
    
    # Declare the names of data files
    X_train_file = "X_train.pkl"
    Y_train_file = "y_train.pkl"
    # the user must read the data from the following folder:
    data_path = "/app/data"
    # the user must read the model from the following  folder:
    model_path = "/app/artifacts/model"

    local_X_train_path = os.path.join(data_path, X_train_file)
    local_Y_train_path = os.path.join(data_path, Y_train_file)
    
    df_X = pd.read_pickle(local_X_train_path) 
    df_y = pd.read_pickle(local_Y_train_path) 


    # model train
    df_X_preprocessed = preprocess_data(df_X, 'status')
    # print(df_X_preprocessed)
    df_y_preprocessed = preprocess_data(df_y, 'ground_truth')
    binary_features = df_X_preprocessed.iloc[:, :-2]  # All columns except the last two (assuming those are sin/cos)
    continuous_features = df_X_preprocessed.iloc[:, -2:]  # The last two columns (sin/cos)
    # Convert to numpy array
    X_train_binary = binary_features.values
    X_train_continuous = continuous_features.values
    y_train = df_y_preprocessed.values
    # And finally convert to torch tensor
    X_train_binary = torch.tensor(X_train_binary, dtype=torch.float32)
    X_train_continuous = torch.tensor(X_train_continuous, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32)

    # Model evaluation definition
    # Using Exact Match Ratio (EMR)
    metric = MultilabelAccuracy(criteria="exact_match")
    
    # Define the number of inputs and outputs
    binary_input_dim = 25
    continuous_input_dim = 2
    output_dim = 25

    # Create the model
    model = initialDNN(binary_input_dim, continuous_input_dim, output_dim)
    model_file = os.path.join(model_path, "model.pth")
    model.load_state_dict(torch.load(model_file))
    model.eval()

    with torch.no_grad():
        y_pred = model(X_train_binary, X_train_continuous)
        y_pred_binary = torch.where(y_pred >= 0.5, torch.tensor(1), torch.tensor(0))
        metric.update(y_pred_binary,y_train)
        print(f'The value for the EMR is: {metric.compute()}')
    

    return "ok"