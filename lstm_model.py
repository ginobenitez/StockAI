import torch
import torch.nn as nn

# LSTM Model definition
class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_layer_size=32, num_layers=2, output_size=1, dropout=0.2):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size

        self.linear_1 = nn.Linear(input_size, hidden_layer_size)
        self.relu = nn.ReLU()
        self.lstm = nn.LSTM(hidden_layer_size, hidden_size=self.hidden_layer_size, num_layers=num_layers, batch_first=True)
        self.dropout = nn.Dropout(dropout)
        self.linear_2 = nn.Linear(num_layers * hidden_layer_size, output_size)

    def forward(self, x):
        batchsize = x.shape[0]
        x = self.linear_1(x)
        x = self.relu(x)
        lstm_out, (h_n, c_n) = self.lstm(x)
        x = h_n.permute(1, 0, 2).reshape(batchsize, -1) 
        x = self.dropout(x)
        predictions = self.linear_2(x)
        return predictions[:,-1]
    
# Function to load the model (if you have pre-trained weights)
def load_model(config):
    model = LSTMModel(input_size=config["model"]["input_size"],
                      hidden_layer_size=config["model"]["lstm_size"],
                      num_layers=config["model"]["num_lstm_layers"],
                      output_size=1,
                      dropout=config["model"]["dropout"])
    # Load pre-trained model weights if you have them
    # model.load_state_dict(torch.load("model_weights.pth"))
    model.eval()
    return model
