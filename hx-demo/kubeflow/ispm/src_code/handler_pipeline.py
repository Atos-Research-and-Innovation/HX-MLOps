import torch
from ts.torch_handler.base_handler import BaseHandler
from initialDNN import initialDNN
import datetime
import numpy as np

class MyHandler(BaseHandler):
    def __init__(self):
        super(MyHandler, self).__init__()
        self.model = None

    def initialize(self, context):
        self.manifest = context.manifest
        properties = context.system_properties
        model_dir = properties.get("model_dir")

        # Load model
        self.model = initialDNN(binary_input_dim=25, continuous_input_dim=2, output_dim=25)
        model_path = f"{model_dir}/model.pth"
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def preprocess(self, data):
        input_data = data[0]["body"] or data[0]["body"]
        input_data = input_data[0]
        timestamp = input_data[0]
        # We must know in advance what is the maximum value of the time, for that case is 86360
        # corresponds with 24 hours to seconds = 86400, and subtract 40 (interval seconds between samples)
        # print(timestamp)
        # Step 1: Convert ISO 8601 string to a datetime object
        timestamp = datetime.datetime.fromisoformat(timestamp)
        # Calculate the seconds since the start of the day
        seconds_since_midnight = (timestamp - timestamp.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        # Normalize the time to a range of 0 to 2*pi
        day_time_normalized = (seconds_since_midnight / 86360) * 2 * np.pi  # 86400 seconds in a day
        # Apply sine and cosine transformations
        day_time_sin = float(np.sin(day_time_normalized))
        day_time_cos = float(np.cos(day_time_normalized))
        input_data.append(day_time_sin) # Append sin value
        input_data.append(day_time_cos) # Append cos value
        input_data=input_data[1:] # Remove timestamp

        return input_data

    def inference(self, input_data):
        input_data_binary = input_data[:25]
        input_data_continuous = input_data[25:]

        input_tensor_binary = torch.FloatTensor(input_data_binary).view(-1, 25)
        input_tensor_continuous = torch.FloatTensor(input_data_continuous).view(-1, 2)
        # Perform inference
        with torch.no_grad():
            output = self.model(input_tensor_binary, input_tensor_continuous)
        return output.numpy().tolist()

    def postprocess(self, data):

        # Apply sigmoid to get probabilities
        torch_data = torch.FloatTensor(data).view(-1, 25)
        probabilities = torch.sigmoid(torch_data)

        # Apply threshold to get binary outputs
        binary_output = (probabilities >= 0.5).int()
        return binary_output.numpy().tolist()