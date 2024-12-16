
"""
Trainer stage for ILE forecasting model
====================
This is a simple DNN for forecasting the status of the extreme dge
nodes availability on the Infrastructure Layer Emulator.
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

    # Training the model
    
    # Define the number of inputs and outputs
    binary_input_dim = 25
    continuous_input_dim = 2
    output_dim = 25

    # Create the model
    model = initialDNN(binary_input_dim, continuous_input_dim, output_dim)

    # Load a checkpoint model to continue training it.
    # model.load_state_dict(torch.load('../infer/model_bin_cont_no_sigmoid.pth'))

    # Define the loss function and optimizer
    # criterion = nn.CrossEntropyLoss()
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.00005)

    num_epochs = 50
    batch_size = 32

    # Flag to let training
    training = 1
    # Flag to let model evaluation
    evaluation = 1
    # Flag to save the model
    model_save = 1

    eval_performance = 1

    if training == 1:
        for epoch in range(num_epochs):
            # Reset EMR value after each epoch to recalculate it.
            metric.reset()
            permutation = torch.randperm(X_train_binary.size()[0])
            
            for i in range(0, X_train_binary.size()[0], batch_size):
                indices = permutation[i:i+batch_size]
                batch_x_binary, batch_x_continuous, batch_y = X_train_binary[indices], X_train_continuous[indices], y_train[indices]

                # Zero the gradients
                optimizer.zero_grad()

                # Set it to train mode again
                model.train()
                # Forward pass
                outputs = model(batch_x_binary, batch_x_continuous)
                loss = criterion(outputs, batch_y)

                # Backward pass and optimize
                loss.backward()
                optimizer.step()
            
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

            # Set it to evaluation mode
            model.eval()
            with torch.no_grad():
                y_pred = model(X_train_binary, X_train_continuous)
                y_pred_binary = torch.where(y_pred >= 0.5, torch.tensor(1), torch.tensor(0))
                metric.update(y_pred_binary,y_train)
                eval_performance = metric.compute()
                print(f'The value for the EMR is: {eval_performance}')

                # Check if EMR is 1
                if eval_performance == 1:
                    print("EMR is 1. Saving the model and exiting...")
                    torch.save(model.state_dict(), '../infer/model_bin_cont_no_sigmoid_3.pth')
                    break  # Exit the inner loop (batches)
            
            # Exit the outer loop (epochs) if EMR is 1
            if eval_performance == 1:
                break  # Exit the outer loop (epochs)

    if model_save == 1: 
        # Declare the trained model path
        trained_model_file_name = "model.pth"
        # the user must write the data to the following folder:
        local_trained_model_path = os.path.join("/app", "artifacts", "model")
        if not os.path.exists(local_trained_model_path):
            os.makedirs(local_trained_model_path)
        # Save the model
        torch.save(model.state_dict(), os.path.join(local_trained_model_path, trained_model_file_name))