import torch.nn as nn

class CNN(nn.Module):
    def __init__(self, img_size=256, in_channels=3, out_channels=5, conv_layers_params=None):
        super(CNN, self).__init__()
        
        if conv_layers_params is None:
            conv_layers_params = [
                {'kernel_num': 16, 'kernel_size': 5, 'pool_size': 2},
                {'kernel_num': 32, 'kernel_size': 5, 'pool_size': 2}
            ]

        self.conv_layers = nn.ModuleList()
        current_channels = in_channels

        # Create convolutional layers based on provided parameters
        for params in conv_layers_params:
            self.conv_layers.append(nn.Sequential(
                nn.Conv2d(
                    in_channels=current_channels,
                    out_channels=params['kernel_num'],
                    kernel_size=params['kernel_size'],
                    stride=1,
                    padding=(params['kernel_size'] - 1) // 2
                ),
                nn.ReLU(),
                nn.MaxPool2d(params['pool_size'])
            ))
            current_channels = params['kernel_num']

        # Calculate the size of the flattened features after all conv and pool layers
        feature_size = self._calculate_feature_size(img_size, conv_layers_params)

        # Fully connected layer
        self.out = nn.Linear(feature_size, out_channels)

    def _calculate_feature_size(self, img_size, conv_layers_params):
        # Calculate the size of the flattened features after all conv and pool layers
        for params in conv_layers_params:
            padding = (params['kernel_size'] - 1) // 2
            img_size = (img_size - params['kernel_size'] + 2 * padding) // params['pool_size'] + 1
        return img_size**2 * conv_layers_params[-1]['kernel_num']

    def forward(self, x):
        # Pass input through each convolutional layer
        for conv_layer in self.conv_layers:
            x = conv_layer(x)

        # Flatten the output for the fully connected layer
        x = x.view(x.size(0), -1)

        # Pass through the fully connected layer
        output = self.out(x)
        return output
