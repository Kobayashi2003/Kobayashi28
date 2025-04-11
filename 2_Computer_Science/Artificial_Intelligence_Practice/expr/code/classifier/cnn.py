# Standard library imports
import os
import random
import time

# Third-party imports - data analysis and scientific computing
import numpy as np
import pandas as pd

# Third-party imports - machine learning and deep learning
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Third-party imports - image processing
from PIL import Image
import cv2

# Third-party imports - visualization
import matplotlib.pyplot as plt
import seaborn as sns

class RockDataset(Dataset):
    """Dataset class for rock image classification"""
    
    def __init__(self, image_paths, labels=None, transform=None):
        """
        Initialize dataset
        
        Parameters:
        -----------
        image_paths : list
            List of image file paths
        labels : list, optional
            List of class labels (integers)
        transform : callable, optional
            Transform to apply to images
        """
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
        
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        # Load image
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        
        # Apply transformations
        if self.transform:
            image = self.transform(image)
            
        # Return image with label if available, otherwise just image
        if self.labels is not None:
            return image, self.labels[idx]
        else:
            return image

class SimpleConvNet(nn.Module):
    """Simple Convolutional Neural Network"""
    
    def __init__(self, num_classes):
        super(SimpleConvNet, self).__init__()
        
        # Convolutional layers
        self.features = nn.Sequential(
            # First block
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Second block
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Third block
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Fourth block
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Global average pooling
            nn.AdaptiveAvgPool2d((1, 1))
        )
        
        # Classifier
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256, 64),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(64, num_classes)
        )
        
    def forward(self, x):
        # Feature extraction
        x = self.features(x)
        
        # Flatten
        x = torch.flatten(x, 1)
        
        # Classification
        x = self.classifier(x)
        return x

class CNNClassifier:
    """CNN classifier for rock images"""
    
    def __init__(self, output_dir='./output/cnn', device=None):
        """
        Initialize CNN classifier
        
        Parameters:
        -----------
        output_dir : str
            Output directory for results
        device : str, optional
            Device to use ('cuda' or 'cpu')
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set device
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
            
        print(f"Using device: {self.device}")
        
        # Default transformations
        self.train_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.RandomCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        self.test_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Initialize model, loss function, optimizer
        self.model = None
        self.criterion = None
        self.optimizer = None
        self.scheduler = None
        self.class_names = None
        
    def _create_model(self, model_name, num_classes, freeze_backbone=False):
        """
        Create and initialize the model
        
        Parameters:
        -----------
        model_name : str
            Model architecture to use
        num_classes : int
            Number of output classes
        freeze_backbone : bool
            Whether to freeze backbone for transfer learning
        
        Returns:
        --------
        model : nn.Module
            Initialized model
        """
        if model_name == 'simple':
            # Use custom simple CNN
            model = SimpleConvNet(num_classes)
        elif model_name == 'resnet18':
            # Use ResNet18
            model = models.resnet18(weights='DEFAULT')
            if freeze_backbone:
                for param in model.parameters():
                    param.requires_grad = False
            # Replace final fully connected layer
            model.fc = nn.Linear(model.fc.in_features, num_classes)
        elif model_name == 'resnet50':
            # Use ResNet50
            model = models.resnet50(weights='DEFAULT')
            if freeze_backbone:
                for param in model.parameters():
                    param.requires_grad = False
            # Replace final fully connected layer
            model.fc = nn.Linear(model.fc.in_features, num_classes)
        elif model_name == 'efficientnet_b0':
            # Use EfficientNet B0
            model = models.efficientnet_b0(weights='DEFAULT')
            if freeze_backbone:
                for param in model.parameters():
                    param.requires_grad = False
            # Replace classifier
            model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
        else:
            raise ValueError(f"Unsupported model architecture: {model_name}")
            
        return model
    
    def train(self, train_paths, train_labels, valid_paths, valid_labels, 
              class_names, model_name='resnet50', batch_size=32, epochs=10, 
              learning_rate=0.001, freeze_backbone=False):
        """
        Train the CNN model
        
        Parameters:
        -----------
        train_paths : list
            List of training image paths
        train_labels : array-like
            Training labels
        valid_paths : list
            List of validation image paths
        valid_labels : array-like
            Validation labels
        class_names : list
            List of class names
        model_name : str
            Model architecture to use
        batch_size : int
            Batch size for training
        epochs : int
            Number of training epochs
        learning_rate : float
            Initial learning rate
        freeze_backbone : bool
            Whether to freeze backbone for transfer learning
            
        Returns:
        --------
        history : dict
            Training history
        """
        # Save class names
        self.class_names = class_names
        num_classes = len(class_names)
        
        # Create datasets and dataloaders
        train_dataset = RockDataset(train_paths, train_labels, transform=self.train_transform)
        valid_dataset = RockDataset(valid_paths, valid_labels, transform=self.test_transform)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
        valid_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
        
        # Create model
        self.model = self._create_model(model_name, num_classes, freeze_backbone)
        self.model = self.model.to(self.device)
        
        # Define loss function and optimizer
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        
        # Learning rate scheduler
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='min', factor=0.5, patience=3, verbose=True)
        
        # Training history
        history = {
            'train_loss': [],
            'train_acc': [],
            'valid_loss': [],
            'valid_acc': []
        }
        
        # Training loop
        best_valid_loss = float('inf')
        best_valid_acc = 0.0
        
        for epoch in range(epochs):
            start_time = time.time()
            
            # Training phase
            self.model.train()
            train_loss = 0.0
            train_correct = 0
            train_total = 0
            
            for inputs, labels in train_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                
                # Zero the parameter gradients
                self.optimizer.zero_grad()
                
                # Forward pass
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                
                # Backward pass and optimize
                loss.backward()
                self.optimizer.step()
                
                # Track loss and accuracy
                train_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs, 1)
                train_correct += (predicted == labels).sum().item()
                train_total += labels.size(0)
            
            train_loss = train_loss / len(train_loader.dataset)
            train_acc = train_correct / train_total
            
            # Validation phase
            self.model.eval()
            valid_loss = 0.0
            valid_correct = 0
            valid_total = 0
            
            with torch.no_grad():
                for inputs, labels in valid_loader:
                    inputs, labels = inputs.to(self.device), labels.to(self.device)
                    
                    # Forward pass
                    outputs = self.model(inputs)
                    loss = self.criterion(outputs, labels)
                    
                    # Track loss and accuracy
                    valid_loss += loss.item() * inputs.size(0)
                    _, predicted = torch.max(outputs, 1)
                    valid_correct += (predicted == labels).sum().item()
                    valid_total += labels.size(0)
            
            valid_loss = valid_loss / len(valid_loader.dataset)
            valid_acc = valid_correct / valid_total
            
            # Update learning rate scheduler
            self.scheduler.step(valid_loss)
            
            # Save best model
            if valid_acc > best_valid_acc:
                best_valid_acc = valid_acc
                torch.save(self.model.state_dict(), os.path.join(self.output_dir, 'best_model.pth'))
                print(f"    Saved new best model with accuracy: {valid_acc:.4f}")
            
            # Update history
            history['train_loss'].append(train_loss)
            history['train_acc'].append(train_acc)
            history['valid_loss'].append(valid_loss)
            history['valid_acc'].append(valid_acc)
            
            # Print metrics
            elapsed_time = time.time() - start_time
            print(f"Epoch {epoch+1}/{epochs} [{elapsed_time:.1f}s]")
            print(f"    Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
            print(f"    Valid Loss: {valid_loss:.4f}, Valid Acc: {valid_acc:.4f}")
        
        # Plot training history
        self._plot_training_history(history)
        
        # Load best model
        self.model.load_state_dict(torch.load(os.path.join(self.output_dir, 'best_model.pth')))
        
        return history
    
    def evaluate(self, test_paths, test_labels, class_names):
        """
        Evaluate the model on test data
        
        Parameters:
        -----------
        test_paths : list
            List of test image paths
        test_labels : array-like
            Test labels
        class_names : list
            List of class names
            
        Returns:
        --------
        metrics : dict
            Evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet")
            
        # Create dataset and dataloader
        test_dataset = RockDataset(test_paths, test_labels, transform=self.test_transform)
        test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=4)
        
        # Set model to evaluation mode
        self.model.eval()
        
        # Initialize predictions and targets
        all_predictions = []
        all_targets = []
        
        # Evaluate model
        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                
                # Forward pass
                outputs = self.model(inputs)
                _, predicted = torch.max(outputs, 1)
                
                # Store predictions and targets
                all_predictions.extend(predicted.cpu().numpy())
                all_targets.extend(labels.cpu().numpy())
        
        # Calculate accuracy
        accuracy = accuracy_score(all_targets, all_predictions)
        print(f"\nTest accuracy: {accuracy:.4f}")
        
        # Generate classification report
        report = classification_report(all_targets, all_predictions, target_names=class_names)
        print("\nClassification Report:")
        print(report)
        
        # Save classification report
        with open(os.path.join(self.output_dir, 'classification_report.txt'), 'w') as f:
            f.write(f"Test accuracy: {accuracy:.4f}\n\n")
            f.write(report)
        
        # Generate confusion matrix
        cm = confusion_matrix(all_targets, all_predictions)
        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                  xticklabels=class_names, yticklabels=class_names)
        plt.xlabel('Predicted label')
        plt.ylabel('True label')
        plt.title('Confusion Matrix')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'confusion_matrix.png'))
        plt.close()
        
        # Calculate and plot per-class accuracy
        class_accuracy = np.diag(cm) / np.sum(cm, axis=1)
        plt.figure(figsize=(12, 6))
        plt.bar(class_names, class_accuracy)
        plt.xlabel('Class')
        plt.ylabel('Accuracy')
        plt.title('Classification Accuracy by Class')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'class_accuracy.png'))
        plt.close()
        
        return {
            'accuracy': accuracy,
            'predictions': all_predictions,
            'targets': all_targets,
            'class_accuracy': class_accuracy
        }
    
    def predict(self, image_paths):
        """
        Make predictions on new images
        
        Parameters:
        -----------
        image_paths : list
            List of image file paths
            
        Returns:
        --------
        predictions : array-like
            Predicted class indices
        probabilities : array-like
            Class probabilities
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet")
            
        # Create dataset and dataloader
        dataset = RockDataset(image_paths, transform=self.test_transform)
        dataloader = DataLoader(dataset, batch_size=32, shuffle=False, num_workers=4)
        
        # Set model to evaluation mode
        self.model.eval()
        
        # Initialize predictions and probabilities
        all_predictions = []
        all_probabilities = []
        
        # Make predictions
        with torch.no_grad():
            for inputs in dataloader:
                inputs = inputs.to(self.device)
                
                # Forward pass
                outputs = self.model(inputs)
                probabilities = torch.softmax(outputs, dim=1)
                _, predicted = torch.max(outputs, 1)
                
                # Store predictions and probabilities
                all_predictions.extend(predicted.cpu().numpy())
                all_probabilities.extend(probabilities.cpu().numpy())
        
        return np.array(all_predictions), np.array(all_probabilities)
    
    def save_model(self, filename='cnn_model.pth'):
        """Save the trained model"""
        if self.model is None:
            raise ValueError("No model to save")
            
        # Save model state dictionary
        model_path = os.path.join(self.output_dir, filename)
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'class_names': self.class_names
        }, model_path)
        
        print(f"Model saved to {model_path}")
        
        return model_path
    
    def load_model(self, model_path, model_name='resnet50', num_classes=None):
        """
        Load a previously trained model
        
        Parameters:
        -----------
        model_path : str
            Path to the saved model
        model_name : str
            Model architecture to use
        num_classes : int, optional
            Number of output classes
        """
        # Load checkpoint
        checkpoint = torch.load(model_path, map_location=self.device)
        
        # Get class names
        self.class_names = checkpoint.get('class_names', None)
        
        # If num_classes not provided, try to infer from class_names
        if num_classes is None:
            if self.class_names is not None:
                num_classes = len(self.class_names)
            else:
                raise ValueError("Number of classes must be provided")
        
        # Create model
        self.model = self._create_model(model_name, num_classes)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model = self.model.to(self.device)
        self.model.eval()
        
        print(f"Model loaded from {model_path}")
        
        return self.model
    
    def _plot_training_history(self, history):
        """Plot training history"""
        # Create figure with two subplots
        plt.figure(figsize=(12, 5))
        
        # Plot training and validation loss
        plt.subplot(1, 2, 1)
        plt.plot(history['train_loss'], label='Train')
        plt.plot(history['valid_loss'], label='Validation')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Training and Validation Loss')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot training and validation accuracy
        plt.subplot(1, 2, 2)
        plt.plot(history['train_acc'], label='Train')
        plt.plot(history['valid_acc'], label='Validation')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.title('Training and Validation Accuracy')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'training_history.png'))
        plt.close()
