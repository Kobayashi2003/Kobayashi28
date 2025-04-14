import os
import numpy as np
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torch.amp import autocast, GradScaler

from sklearn.metrics import classification_report, accuracy_score

from utils import (
    load_dataset, 
    check_for_augmented_data, 
    save_augmented_data, 
    save_error_analysis
)

class TransformDataset(Dataset):
    def __init__(self, images, labels, transform=None):
        self.images = images
        self.labels = labels
        self.transform = transform
        
    def __len__(self):
        return len(self.images)
        
    def __getitem__(self, idx):
        image = self.images[idx]
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
            
        return image, label

class RockCNN(nn.Module):
    def __init__(self, num_classes):
        super(RockCNN, self).__init__()
        
        # Feature extraction layers
        self.features = nn.Sequential(
            # First conv block
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(0.25),
            
            # Second conv block
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(0.25),
            
            # Third conv block
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(0.25),
        )
        
        # Classifier layers
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 40 * 40, 512),  # For input size 320x320
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x
    
    def predict(self, x):
        self.eval()
        with torch.no_grad():
            outputs = self(x)
            _, predicted = torch.max(outputs, 1)
        return predicted.cpu().numpy()

def prepare_dataset(data_dir, img_size, output_dir, augment_factor):
    # Use existing augmented data if available
    augmented_data_filename = os.path.join(output_dir, f"augmented_data_{img_size[0]}x{img_size[1]}.pkl")
    augmented_data = check_for_augmented_data(augmented_data_filename)
    
    if augmented_data is not None:
        X_train = augmented_data['X_train']
        y_train = augmented_data['y_train']
        X_valid = augmented_data['X_valid']
        y_valid = augmented_data['y_valid']
        X_test = augmented_data['X_test']
        y_test = augmented_data['y_test']
        class_names = augmented_data['class_names']
        print(f"Using existing augmented dataset with {len(X_train)} training samples.")
    else:
        # Load dataset
        print("Loading dataset...")
        data = load_dataset(data_dir, img_size=img_size)
        X_train, y_train = data['X_train'], data['y_train']
        X_valid, y_valid = data['X_valid'], data['y_valid']
        X_test, y_test = data['X_test'], data['y_test']
        class_names = data['class_names']
        print(f"Dataset loaded: {len(X_train)} train, {len(X_valid)} valid, {len(X_test)} test samples.")
        
        # For CNN we don't need to use the augment_dataset function
        # as we'll perform augmentation on-the-fly during training
        
        # Save original data for future use
        augmented_data = {
            'X_train': X_train, 'y_train': y_train,
            'X_valid': X_valid, 'y_valid': y_valid,
            'X_test': X_test, 'y_test': y_test,
            'class_names': class_names
        }
        save_augmented_data(augmented_data, augmented_data_filename)
    
    return X_train, y_train, X_valid, y_valid, X_test, y_test, class_names

def process_data_for_cnn(X_train, y_train, X_valid, y_valid, X_test, y_test, batch_size=32, num_workers=4, pin_memory=True):
    train_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(30),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    valid_test_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    train_dataset = TransformDataset(X_train, y_train, train_transform)
    valid_dataset = TransformDataset(X_valid, y_valid, valid_test_transform)
    test_dataset = TransformDataset(X_test, y_test, valid_test_transform)
    
    train_loader = DataLoader(
        train_dataset, 
        batch_size=batch_size, 
        shuffle=True, 
        num_workers=num_workers, 
        pin_memory=pin_memory,
        persistent_workers=True if num_workers > 0 else False,
        prefetch_factor=2 if num_workers > 0 else None
    )
    
    valid_loader = DataLoader(
        valid_dataset, 
        batch_size=batch_size, 
        shuffle=False, 
        num_workers=num_workers, 
        pin_memory=pin_memory,
        persistent_workers=True if num_workers > 0 else False,
        prefetch_factor=2 if num_workers > 0 else None
    )
    
    test_loader = DataLoader(
        test_dataset, 
        batch_size=batch_size, 
        shuffle=False, 
        num_workers=num_workers, 
        pin_memory=pin_memory,
        persistent_workers=True if num_workers > 0 else False,
        prefetch_factor=2 if num_workers > 0 else None
    )
    
    return train_loader, valid_loader, test_loader

def train_or_load_model(train_loader, valid_loader, num_classes, output_dir, device, epochs=30, learning_rate=0.001, 
                       use_amp=True, multi_gpu=False):
    model_path = os.path.join(output_dir, "cnn_model.pth")
    
    if os.path.exists(model_path):
        print(f"Loading existing CNN model from {model_path}")
        try:
            model = RockCNN(num_classes)
            model.load_state_dict(torch.load(model_path, map_location=device))
            model = model.to(device)
            return model
        except Exception as e:
            print(f"Error loading model: {e}. Training new model...")
    
    print("Training new CNN model...")
    model = RockCNN(num_classes).to(device)
    
    if multi_gpu and torch.cuda.device_count() > 1:
        print(f"Using {torch.cuda.device_count()} GPUs!")
        model = nn.DataParallel(model)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=3, verbose=True)
    
    scaler = GradScaler() if use_amp and torch.cuda.is_available() else None
    device_type = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    best_val_acc = 0.0
    patience_counter = 0
    max_patience = 10
    
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        train_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs} [Train]")
        for inputs, labels in train_bar:
            inputs, labels = inputs.to(device, non_blocking=True), labels.to(device, non_blocking=True)
            
            if scaler:
                with autocast(device_type=device_type):
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
                
                optimizer.zero_grad()
                scaler.scale(loss).backward()
                scaler.step(optimizer)
                scaler.update()
            else:
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            train_bar.set_postfix({
                'loss': running_loss / (train_bar.n + 1),
                'acc': 100. * correct / total
            })
        
        train_loss = running_loss / len(train_loader)
        train_acc = 100. * correct / total
        
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            val_bar = tqdm(valid_loader, desc=f"Epoch {epoch+1}/{epochs} [Valid]")
            for inputs, labels in val_bar:
                inputs, labels = inputs.to(device, non_blocking=True), labels.to(device, non_blocking=True)
                
                if scaler:
                    with autocast(device_type=device_type):
                        outputs = model(inputs)
                        loss = criterion(outputs, labels)
                else:
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
                
                val_bar.set_postfix({
                    'loss': val_loss / (val_bar.n + 1),
                    'acc': 100. * val_correct / val_total
                })
        
        val_loss = val_loss / len(valid_loader)
        val_acc = 100. * val_correct / val_total
        
        print(f"Epoch {epoch+1}/{epochs} - "
              f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}% - "
              f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
        
        scheduler.step(val_acc)
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            patience_counter = 0
            
            torch.save(
                model.module.state_dict() if isinstance(model, nn.DataParallel) else model.state_dict(), 
                model_path
            )
            print(f"Model saved with improved validation accuracy: {val_acc:.2f}%")
        else:
            patience_counter += 1
            if patience_counter >= max_patience:
                print(f"Early stopping after {epoch+1} epochs without improvement")
                break
    
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        
    best_model = RockCNN(num_classes)
    best_model.load_state_dict(torch.load(model_path, map_location=device))
    best_model = best_model.to(device)
    
    return best_model

def evaluate_model(model, valid_loader, test_loader, X_test, y_test, class_names, output_dir, device, use_amp=True):
    print("Evaluating on validation set...")
    model.eval()
    val_all_preds = []
    val_all_labels = []
    
    device_type = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    with torch.no_grad():
        for inputs, labels in tqdm(valid_loader, desc="Validation"):
            inputs = inputs.to(device, non_blocking=True)
            
            if use_amp and torch.cuda.is_available():
                with autocast(device_type=device_type):
                    outputs = model(inputs)
            else:
                outputs = model(inputs)
                
            _, predicted = torch.max(outputs, 1)
            
            val_all_preds.extend(predicted.cpu().numpy())
            val_all_labels.extend(labels.numpy())
    
    y_valid_pred = np.array(val_all_preds)
    y_valid = np.array(val_all_labels)
    val_accuracy = accuracy_score(y_valid, y_valid_pred)
    print(f"Validation accuracy: {val_accuracy:.4f}")
    print(classification_report(y_valid, y_valid_pred, target_names=class_names, zero_division=0))
    
    print("Evaluating on test set...")
    model.eval()
    test_all_preds = []
    test_all_labels = []
    
    with torch.no_grad():
        for inputs, labels in tqdm(test_loader, desc="Test"):
            inputs = inputs.to(device, non_blocking=True)
            
            if use_amp and torch.cuda.is_available():
                with autocast(device_type=device_type):
                    outputs = model(inputs)
            else:
                outputs = model(inputs)
                
            _, predicted = torch.max(outputs, 1)
            
            test_all_preds.extend(predicted.cpu().numpy())
            test_all_labels.extend(labels.numpy())
    
    y_test_pred = np.array(test_all_preds)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    print(f"Test accuracy: {test_accuracy:.4f}")
    print(classification_report(y_test, y_test_pred, target_names=class_names, zero_division=0))
    
    save_error_analysis(X_test, y_test, y_test_pred, class_names, output_dir, "test", "cnn")
    
    class_accuracies = {}
    for cls_idx, cls_name in enumerate(class_names):
        cls_samples = (y_test == cls_idx)
        if np.sum(cls_samples) > 0:
            cls_acc = accuracy_score(y_test[cls_samples], y_test_pred[cls_samples])
            class_accuracies[cls_name] = cls_acc
    
    print("\nAccuracy by rock type:")
    for cls_name, acc in sorted(class_accuracies.items(), key=lambda x: x[1]):
        print(f"{cls_name}: {acc:.4f}")
    
    return y_valid_pred, y_test_pred, val_accuracy, test_accuracy, class_accuracies

def main():
    # Configuration
    data_dir = "../data"
    img_size = (320, 320)
    output_dir = "../output/cnn"
    augment_factor = 10  # Not directly used for CNN but kept for consistency
    batch_size = 16
    epochs = 30
    learning_rate = 0.001
    
    # GPU optimization settings
    use_amp = True  # Automatic Mixed Precision
    multi_gpu = True  # Use multiple GPUs if available
    num_workers = 4  # Number of data loading worker processes
    pin_memory = True  # Pin memory for faster GPU transfer
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Set device and optimize CUDA settings
    if torch.cuda.is_available():
        torch.backends.cudnn.benchmark = True  # Enable cuDNN auto-tuner
        torch.backends.cudnn.deterministic = False  # Disable deterministic mode for speed
        
        device = torch.device("cuda")
        print(f"Using CUDA device: {torch.cuda.get_device_name(0)}")
        print(f"Total GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        print(f"Available GPUs: {torch.cuda.device_count()}")
        
        torch.cuda.empty_cache()
    else:
        device = torch.device("cpu")
        print("CUDA not available, using CPU")
        # Disable GPU-specific optimizations
        use_amp = False
        multi_gpu = False
        pin_memory = False
    
    # Prepare dataset
    X_train, y_train, X_valid, y_valid, X_test, y_test, class_names = prepare_dataset(
        data_dir, img_size, output_dir, augment_factor
    )
    
    # Process data for CNN - use optimized data loading for GPU
    train_loader, valid_loader, test_loader = process_data_for_cnn(
        X_train, y_train, X_valid, y_valid, X_test, y_test, 
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=pin_memory
    )
    
    # Train or load model with GPU optimizations
    model = train_or_load_model(
        train_loader, valid_loader, len(class_names), output_dir, 
        device=device, 
        epochs=epochs, 
        learning_rate=learning_rate,
        use_amp=use_amp,
        multi_gpu=multi_gpu
    )
    
    # Evaluate model
    y_valid_pred, y_test_pred, val_accuracy, test_accuracy, class_accuracies = evaluate_model(
        model, valid_loader, test_loader, X_test, y_test, class_names, output_dir, 
        device=device,
        use_amp=use_amp
    )
    
    print(f"CNN analysis complete. Results saved in {output_dir}.")

if __name__ == "__main__":
    main()
