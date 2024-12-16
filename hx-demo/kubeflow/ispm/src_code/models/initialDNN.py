import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# Define the neural network class
class initialDNN(nn.Module):
    """
    Class where the initial DNN is defined.
    """

    def __init__(self, binary_input_dim, continuous_input_dim, output_dim):
        super(initialDNN, self).__init__()
        # Binary feature pathway
        self.binary_fc1 = nn.Linear(binary_input_dim, 32)
        self.binary_fc2 = nn.Linear(32, 32)
        
        # Continuous feature pathway
        self.continuous_fc1 = nn.Linear(continuous_input_dim, 64)
        self.continuous_fc2 = nn.Linear(64, 64)
        self.continuous_fc3 = nn.Linear(64, 64)
        
        # Combined pathway
        self.fc1_combined = nn.Linear(96, 96)
        self.fc2_combined = nn.Linear(96, output_dim)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, binary_input, continuous_input):
        binary_out = self.relu(self.binary_fc1(binary_input))
        binary_out = self.relu(self.binary_fc2(binary_out))
        
        continuous_out = self.relu(self.continuous_fc1(continuous_input))
        continuous_out = self.relu(self.continuous_fc2(continuous_out))
        continuous_out = self.relu(self.continuous_fc3(continuous_out))
        
        combined_out = torch.cat((binary_out, continuous_out), dim=1)
        output = self.fc1_combined(combined_out)
        output = self.fc2_combined(output)  # No sigmoid
        return output