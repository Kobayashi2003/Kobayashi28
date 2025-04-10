import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import time
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import cv2

# PyTorch imports
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
from torch.optim.lr_scheduler import ReduceLROnPlateau
import torchvision.models as models


class RockDataset(Dataset):
    """Dataset class for rock images"""
    
    def __init__(self, images, labels=None, transform=None):
        """
        Initialize the dataset
        
        Parameters:
        -----------
        images : list or array-like
            List of image paths or image arrays
        labels : array-like, optional
            Labels corresponding to images
        transform : callable, optional
            Optional transform to be applied on a sample
        """
        self.images = images
        self.labels = labels
        self.transform = transform
        self.is_path = isinstance(images[0], str) if images else False
        
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        if self.is_path:
            # Load image from path
            img_path = self.images[idx]
            image = cv2.imread(img_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        else:
            # Use pre-loaded image
            image = self.images[idx]
            
        if self.transform:
            image = self.transform(image)
            
        if self.labels is not None:
            label = self.labels[idx]
            return image, label
        else:
            return image


class SimpleCNN(nn.Module):
    """A simple CNN architecture for rock classification"""
    
    def __init__(self, num_classes, input_channels=3):
        """
        Initialize the CNN model
        
        Parameters:
        -----------
        num_classes : int
            Number of classes to classify
        input_channels : int, default=3
            Number of input channels (3 for RGB)
        """
        super(SimpleCNN, self).__init__()
        
        # Feature extraction layers
        self.features = nn.Sequential(
            # First convolutional block
            nn.Conv2d(input_channels, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Second convolutional block
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Third convolutional block
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Fourth convolutional block
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Global average pooling
            nn.AdaptiveAvgPool2d(1)
        )
        
        # Classifier layers
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
        
    def forward(self, x):
        """Forward pass"""
        x = self.features(x)
        x = self.classifier(x)
        return x


class CNNClassifier:
    """Convolutional Neural Network classifier for rock images"""
    
    def __init__(self, output_dir='./output', device=None):
        """
        Initialize CNN classifier
        
        Parameters:
        -----------
        output_dir : str, default='./output'
            Directory to save model and results
        device : str, optional
            Device to use for training ('cuda' or 'cpu')
        """
        self.model = None
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set device
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
            
        print(f"Using device: {self.device}")
        
        # Define transforms
        self.train_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        self.test_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Training history
        self.history = {
            'train_loss': [],
            'train_acc': [],
            'val_loss': [],
            'val_acc': []
        }
        
        # Class names
        self.class_names = None
    
    def train_simple_cnn(self, train_data, train_labels, val_data, val_labels, 
                        batch_size=32, epochs=20, learning_rate=0.001):
        """
        Train a simple CNN model from scratch
        
        Parameters:
        -----------
        train_data : array-like
            Training images or paths
        train_labels : array-like
            Training labels
        val_data : array-like
            Validation images or paths
        val_labels : array-like
            Validation labels
        batch_size : int, default=32
            Batch size for training
        epochs : int, default=20
            Number of training epochs
        learning_rate : float, default=0.001
            Learning rate for optimizer
        """
        # Get number of classes
        num_classes = len(np.unique(train_labels))
        self.class_names = [str(i) for i in range(num_classes)]
        
        print(f"\nTraining simple CNN from scratch...")
        print(f"Number of classes: {num_classes}")
        print(f"Training samples: {len(train_data)}")
        print(f"Validation samples: {len(val_data)}")
        
        # Create datasets and dataloaders
        train_dataset = RockDataset(train_data, train_labels, transform=self.train_transform)
        val_dataset = RockDataset(val_data, val_labels, transform=self.test_transform)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
        
        # Initialize model
        self.model = SimpleCNN(num_classes)
        self.model.to(self.device)
        
        # Loss function and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=3, verbose=True)
        
        # Training loop
        best_val_acc = 0.0
        best_model_wts = None
        
        for epoch in range(epochs):
            # Training phase
            self.model.train()
            train_loss = 0.0
            train_correct = 0
            train_total = 0
            
            for inputs, labels in train_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                
                # Zero gradients
                optimizer.zero_grad()
                
                # Forward pass
                outputs = self.model(inputs)
                loss = criterion(outputs, labels)
                
                # Backward pass and optimize
                loss.backward()
                optimizer.step()
                
                # Statistics
                train_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs, 1)
                train_total += labels.size(0)
                train_correct += (predicted == labels).sum().item()
            
            train_loss = train_loss / train_total
            train_acc = train_correct / train_total
            
            # Validation phase
            self.model.eval()
            val_loss = 0.0
            val_correct = 0
            val_total = 0
            
            with torch.no_grad():
                for inputs, labels in val_loader:
                    inputs, labels = inputs.to(self.device), labels.to(self.device)
                    
                    outputs = self.model(inputs)
                    loss = criterion(outputs, labels)
                    
                    val_loss += loss.item() * inputs.size(0)
                    _, predicted = torch.max(outputs, 1)
                    val_total += labels.size(0)
                    val_correct += (predicted == labels).sum().item()
            
            val_loss = val_loss / val_total
            val_acc = val_correct / val_total
            
            # Update scheduler
            scheduler.step(val_loss)
            
            # Save the best model
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_model_wts = self.model.state_dict().copy()
            
            # Print progress
            print(f"Epoch {epoch+1}/{epochs}: "
                  f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, "
                  f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
            
            # Store history
            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_loss'].append(val_loss)
            self.history['val_acc'].append(val_acc)
        
        # Load best model weights
        self.model.load_state_dict(best_model_wts)
        
        # Plot training history
        self._plot_training_history()
        
        return best_val_acc
    
    def train_transfer_learning(self, train_data, train_labels, val_data, val_labels, 
                               model_name='resnet50', batch_size=32, epochs=10, 
                               learning_rate=0.0001, freeze_backbone=True):
        """
        Train using transfer learning from a pre-trained model
        
        Parameters:
        -----------
        train_data : array-like
            Training images or paths
        train_labels : array-like
            Training labels
        val_data : array-like
            Validation images or paths
        val_labels : array-like
            Validation labels
        model_name : str, default='resnet50'
            Name of the pre-trained model to use
        batch_size : int, default=32
            Batch size for training
        epochs : int, default=10
            Number of training epochs
        learning_rate : float, default=0.0001
            Learning rate for optimizer
        freeze_backbone : bool, default=True
            Whether to freeze the backbone features
        """
        # Get number of classes
        num_classes = len(np.unique(train_labels))
        self.class_names = [str(i) for i in range(num_classes)]
        
        print(f"\nTraining using transfer learning with {model_name}...")
        print(f"Number of classes: {num_classes}")
        print(f"Training samples: {len(train_data)}")
        print(f"Validation samples: {len(val_data)}")
        print(f"Freezing backbone: {freeze_backbone}")
        
        # Create datasets and dataloaders
        train_dataset = RockDataset(train_data, train_labels, transform=self.train_transform)
        val_dataset = RockDataset(val_data, val_labels, transform=self.test_transform)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
        
        # Load pre-trained model
        if model_name == 'resnet18':
            self.model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        elif model_name == 'resnet50':
            self.model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        elif model_name == 'efficientnet_b0':
            self.model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
        else:
            raise ValueError(f"Unsupported model name: {model_name}")
        
        # Freeze backbone if requested
        if freeze_backbone:
            for param in self.model.parameters():
                param.requires_grad = False
        
        # Replace the classifier
        if model_name.startswith('resnet'):
            in_features = self.model.fc.in_features
            self.model.fc = nn.Linear(in_features, num_classes)
        elif model_name.startswith('efficientnet'):
            in_features = self.model.classifier[1].in_features
            self.model.classifier[1] = nn.Linear(in_features, num_classes)
        
        # Move model to device
        self.model.to(self.device)
        
        # Loss function and optimizer
        criterion = nn.CrossEntropyLoss()
        
        # If backbone is frozen, only optimize the classifier
        if freeze_backbone and model_name.startswith('resnet'):
            optimizer = optim.Adam(self.model.fc.parameters(), lr=learning_rate)
        elif freeze_backbone and model_name.startswith('efficientnet'):
            optimizer = optim.Adam(self.model.classifier.parameters(), lr=learning_rate)
        else:
            optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        
        scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=2, verbose=True)
        
        # Training loop
        best_val_acc = 0.0
        best_model_wts = None
        
        for epoch in range(epochs):
            # Training phase
            self.model.train()
            train_loss = 0.0
            train_correct = 0
            train_total = 0
            
            for inputs, labels in train_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                
                # Zero gradients
                optimizer.zero_grad()
                
                # Forward pass
                outputs = self.model(inputs)
                loss = criterion(outputs, labels)
                
                # Backward pass and optimize
                loss.backward()
                optimizer.step()
                
                # Statistics
                train_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs, 1)
                train_total += labels.size(0)
                train_correct += (predicted == labels).sum().item()
            
            train_loss = train_loss / train_total
            train_acc = train_correct / train_total
            
            # Validation phase
            self.model.eval()
            val_loss = 0.0
            val_correct = 0
            val_total = 0
            
            with torch.no_grad():
                for inputs, labels in val_loader:
                    inputs, labels = inputs.to(self.device), labels.to(self.device)
                    
                    outputs = self.model(inputs)
                    loss = criterion(outputs, labels)
                    
                    val_loss += loss.item() * inputs.size(0)
                    _, predicted = torch.max(outputs, 1)
                    val_total += labels.size(0)
                    val_correct += (predicted == labels).sum().item()
            
            val_loss = val_loss / val_total
            val_acc = val_correct / val_total
            
            # Update scheduler
            scheduler.step(val_loss)
            
            # Save the best model
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_model_wts = self.model.state_dict().copy()
            
            # Print progress
            print(f"Epoch {epoch+1}/{epochs}: "
                  f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, "
                  f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")
            
            # Store history
            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_loss'].append(val_loss)
            self.history['val_acc'].append(val_acc)
        
        # Load best model weights
        self.model.load_state_dict(best_model_wts)
        
        # Plot training history
        self._plot_training_history()
        
        return best_val_acc
    
    def evaluate(self, test_data, test_labels, class_names, filename_suffix=''):
        """
        Evaluate model on test data and generate reports
        
        Parameters:
        -----------
        test_data : array-like
            Test images or paths
        test_labels : array-like
            Test labels
        class_names : list of str
            Names of the classes
        filename_suffix : str, default=''
            Suffix to add to output filenames
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        
        self.class_names = class_names
        
        # Create dataset and dataloader
        test_dataset = RockDataset(test_data, test_labels, transform=self.test_transform)
        test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=4)
        
        # Evaluate model
        self.model.eval()
        all_preds = []
        all_labels = []
        all_probs = []
        
        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                
                outputs = self.model(inputs)
                probabilities = torch.softmax(outputs, dim=1)
                _, preds = torch.max(outputs, 1)
                
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
                all_probs.extend(probabilities.cpu().numpy())
        
        # Calculate accuracy
        test_accuracy = accuracy_score(all_labels, all_preds)
        print(f"\nTest set accuracy = {test_accuracy:.4f}")
        
        # Generate classification report
        class_report = classification_report(all_labels, all_preds, target_names=class_names)
        print("\nClassification Report:")
        print(class_report)
        
        # Save classification report
        report_file = f'classification_report{filename_suffix}.txt'
        with open(os.path.join(self.output_dir, report_file), 'w') as f:
            f.write(f"Test accuracy: {test_accuracy:.4f}\n\n")
            f.write(class_report)
        
        # Generate confusion matrix
        cm = confusion_matrix(all_labels, all_preds)
        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names)
        plt.xlabel('Predicted label')
        plt.ylabel('True label')
        plt.title('Confusion Matrix')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'confusion_matrix{filename_suffix}.png'))
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
        plt.savefig(os.path.join(self.output_dir, f'class_accuracy{filename_suffix}.png'))
        plt.close()
        
        # Plot ROC curves
        self._plot_roc_curves(np.array(all_probs), np.array(all_labels), filename_suffix)
        
        return test_accuracy, all_preds
    
    def _plot_roc_curves(self, y_scores, y_test, filename_suffix=''):
        """
        Plot ROC curves for multiclass classification
        
        Parameters:
        -----------
        y_scores : array-like
            Probability scores from model predictions
        y_test : array-like
            True labels
        filename_suffix : str, default=''
            Suffix to add to output filenames
        """
        from sklearn.metrics import roc_curve, auc
        from sklearn.preprocessing import label_binarize
        
        # Binarize the labels for multiclass ROC
        classes = np.unique(y_test)
        y_test_bin = label_binarize(y_test, classes=classes)
        n_classes = len(classes)
        
        # Compute ROC curve and ROC area for each class
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_scores[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])
        
        # Plot ROC curves
        plt.figure(figsize=(12, 8))
        
        # Plot individual class ROC curves
        for i, color in zip(range(n_classes), plt.cm.tab10.colors):
            plt.plot(fpr[i], tpr[i], color=color, lw=2,
                    label=f'{self.class_names[i]} (AUC = {roc_auc[i]:.2f})')
        
        # Plot random guess curve
        plt.plot([0, 1], [0, 1], 'k--', lw=2)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curves')
        plt.legend(loc="lower right")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'roc_curves{filename_suffix}.png'))
        plt.close()
    
    def _plot_training_history(self):
        """Plot training and validation loss and accuracy history"""
        plt.figure(figsize=(12, 5))
        
        # Plot training & validation loss
        plt.subplot(1, 2, 1)
        plt.plot(self.history['train_loss'], label='Training Loss')
        plt.plot(self.history['val_loss'], label='Validation Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Training and Validation Loss')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot training & validation accuracy
        plt.subplot(1, 2, 2)
        plt.plot(self.history['train_acc'], label='Training Accuracy')
        plt.plot(self.history['val_acc'], label='Validation Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.title('Training and Validation Accuracy')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'training_history.png'))
        plt.close()
    
    def save_model(self, filename='cnn_model.pth'):
        """
        Save the trained model
        
        Parameters:
        -----------
        filename : str, default='cnn_model.pth'
            Filename to save the model
        """
        if self.model is None:
            raise ValueError("No model to save")
            
        model_path = os.path.join(self.output_dir, filename)
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'class_names': self.class_names,
            'history': self.history
        }, model_path)
        
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path, model_architecture='resnet50', num_classes=None):
        """
        Load a trained model
        
        Parameters:
        -----------
        model_path : str
            Path to the saved model
        model_architecture : str, default='resnet50'
            Architecture of the model to load
        num_classes : int, optional
            Number of classes in the model
        """
        # Load model checkpoint
        checkpoint = torch.load(model_path, map_location=self.device)
        
        # If class_names is saved in the checkpoint, use it
        if 'class_names' in checkpoint:
            self.class_names = checkpoint['class_names']
            num_classes = len(self.class_names)
        elif num_classes is None:
            raise ValueError("Number of classes must be provided if not saved in model checkpoint")
        
        # Create the model
        if model_architecture == 'simple':
            self.model = SimpleCNN(num_classes)
        elif model_architecture == 'resnet18':
            self.model = models.resnet18(weights=None)
            self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)
        elif model_architecture == 'resnet50':
            self.model = models.resnet50(weights=None)
            self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)
        elif model_architecture == 'efficientnet_b0':
            self.model = models.efficientnet_b0(weights=None)
            self.model.classifier[1] = nn.Linear(self.model.classifier[1].in_features, num_classes)
        else:
            raise ValueError(f"Unsupported model architecture: {model_architecture}")
        
        # Load model weights
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.to(self.device)
        
        # Load training history if available
        if 'history' in checkpoint:
            self.history = checkpoint['history']
        
        print(f"Model loaded from {model_path}")
    
    def predict(self, images):
        """
        Make predictions with the trained model
        
        Parameters:
        -----------
        images : array-like
            Images to predict
        
        Returns:
        --------
        predictions : array
            Predicted class indices
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet")
            
        # Create dataset and dataloader
        dataset = RockDataset(images, transform=self.test_transform)
        dataloader = DataLoader(dataset, batch_size=32, shuffle=False, num_workers=4)
        
        # Make predictions
        self.model.eval()
        all_preds = []
        
        with torch.no_grad():
            for inputs in dataloader:
                inputs = inputs.to(self.device)
                outputs = self.model(inputs)
                _, preds = torch.max(outputs, 1)
                all_preds.extend(preds.cpu().numpy())
        
        return np.array(all_preds)
    
    def predict_proba(self, images):
        """
        Make probability predictions with the trained model
        
        Parameters:
        -----------
        images : array-like
            Images to predict
        
        Returns:
        --------
        probabilities : array
            Predicted class probabilities
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet")
            
        # Create dataset and dataloader
        dataset = RockDataset(images, transform=self.test_transform)
        dataloader = DataLoader(dataset, batch_size=32, shuffle=False, num_workers=4)
        
        # Make predictions
        self.model.eval()
        all_probs = []
        
        with torch.no_grad():
            for inputs in dataloader:
                inputs = inputs.to(self.device)
                outputs = self.model(inputs)
                probs = torch.softmax(outputs, dim=1)
                all_probs.extend(probs.cpu().numpy())
        
        return np.array(all_probs) 