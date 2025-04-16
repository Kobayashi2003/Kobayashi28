import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models import resnet18, resnet34, resnet50, resnet101, resnet152
from torchvision.models import ResNet18_Weights, ResNet34_Weights, ResNet50_Weights
from torchvision.models import ResNet101_Weights, ResNet152_Weights

class ResNetModel(nn.Module):
    """
    ResNet model for fine-grained classification
    
    Args:
        net_name: name of the ResNet variant (resnet18, resnet34, etc.)
        num_classes: number of output classes
        dropout: dropout rate for the fully connected layer
        pretrained: whether to load pretrained weights
    """
    def __init__(self, net_name='resnet50', num_classes=200, dropout=0.2, pretrained=True):
        super(ResNetModel, self).__init__()
        
        # Dictionary of available models and weights
        self.models = {
            'resnet18': (resnet18, ResNet18_Weights.IMAGENET1K_V1),
            'resnet34': (resnet34, ResNet34_Weights.IMAGENET1K_V1),
            'resnet50': (resnet50, ResNet50_Weights.IMAGENET1K_V2),
            'resnet101': (resnet101, ResNet101_Weights.IMAGENET1K_V2),
            'resnet152': (resnet152, ResNet152_Weights.IMAGENET1K_V2),
        }
        
        # Select the appropriate model
        if net_name not in self.models:
            raise ValueError(f"Model {net_name} not supported. Choose from: {list(self.models.keys())}")
        
        model_fn, weights = self.models[net_name]
        
        # Load model with or without pretrained weights
        if pretrained:
            self.model = model_fn(weights=weights)
        else:
            self.model = model_fn(weights=None)
        
        # Get the input features of the last fully connected layer
        in_features = self.model.fc.in_features
        
        # Replace the last fully connected layer
        self.model.fc = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(in_features, num_classes)
        )
        
        # Initialize the weights of the new layer
        nn.init.xavier_normal_(self.model.fc[1].weight)
        
    def forward(self, x):
        """Forward pass through the network"""
        return self.model(x)
    
    def get_cam_weights(self):
        """
        Get weights for Class Activation Mapping
        
        Returns:
            weights of the final fully connected layer
        """
        return self.model.fc[1].weight
    
    def get_layer_output(self, x, layer_name='layer4'):
        """
        Get the output of a specific layer
        
        Args:
            x: input tensor
            layer_name: name of the layer
            
        Returns:
            output of the specified layer
        """
        # Obtain intermediate features
        outputs = {}
        
        def hook_fn(module, input, output):
            outputs[layer_name] = output
        
        # Register hook
        if layer_name == 'layer4':
            hook = self.model.layer4.register_forward_hook(hook_fn)
        elif layer_name == 'layer3':
            hook = self.model.layer3.register_forward_hook(hook_fn)
        elif layer_name == 'layer2':
            hook = self.model.layer2.register_forward_hook(hook_fn)
        elif layer_name == 'layer1':
            hook = self.model.layer1.register_forward_hook(hook_fn)
            
        # Forward pass
        out = self.model(x)
        
        # Remove hook
        hook.remove()
        
        return outputs[layer_name]
