# train.py
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
import pandas as pd
import numpy as np
from PIL import Image
import argparse
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold
import time
from tensorboardX import SummaryWriter
from torch.cuda.amp import autocast, GradScaler

from model import ResNetModel
from utils import AverageMeter, accuracy, get_parameter_number, EarlyStopping
from config import INIT_TRAINER, SETUP_TRAINER, TRAIN_CSV_PATH, TEST_CSV_PATH, RESULT_DIR, FOLD_NUM

class BirdDataset(Dataset):
    """
    Dataset for CUB-200 birds
    
    Args:
        csv_path: path to CSV file with image paths and labels
        transform: image transformations
    """
    def __init__(self, csv_path, transform=None):
        self.df = pd.read_csv(csv_path)
        self.transform = transform
        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        img_path = self.df.iloc[idx]['id']
        label = self.df.iloc[idx]['label']
        
        # Handle relative paths
        if not os.path.isabs(img_path):
            img_path = os.path.join('..', img_path)
            
        image = Image.open(img_path).convert('RGB')
        
        if self.transform:
            image = self.transform(image)
            
        return image, label

def get_transforms(image_size, train_mean, train_std, is_training=True):
    """
    Get transforms for data augmentation
    
    Args:
        image_size: input image size
        train_mean: normalization mean
        train_std: normalization std
        is_training: whether to use training augmentations
        
    Returns:
        composed transforms
    """
    if is_training:
        return transforms.Compose([
            transforms.RandomResizedCrop(size=image_size),
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1),
            transforms.ToTensor(),
            transforms.Normalize(train_mean, train_std)
        ])
    else:
        return transforms.Compose([
            transforms.Resize(int(image_size * 1.14)),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Normalize(train_mean, train_std)
        ])

def train_one_epoch(model, criterion, optimizer, train_loader, device, scaler, use_fp16=True):
    """
    Train for one epoch
    
    Args:
        model: neural network model
        criterion: loss function
        optimizer: optimizer
        train_loader: training data loader
        device: device to use (cpu/cuda)
        scaler: gradient scaler for mixed precision
        use_fp16: whether to use mixed precision
        
    Returns:
        average loss and accuracy
    """
    model.train()
    losses = AverageMeter()
    top1 = AverageMeter()
    
    for images, targets in train_loader:
        images, targets = images.to(device), targets.to(device)
        
        # Mixed precision training
        if use_fp16:
            with autocast():
                outputs = model(images)
                loss = criterion(outputs, targets)
                
            # Update metrics
            acc1, = accuracy(outputs, targets, topk=(1,))
            losses.update(loss.item(), images.size(0))
            top1.update(acc1.item(), images.size(0))
            
            # Backpropagation with gradient scaling
            optimizer.zero_grad()
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            # Regular training
            outputs = model(images)
            loss = criterion(outputs, targets)
            
            # Update metrics
            acc1, = accuracy(outputs, targets, topk=(1,))
            losses.update(loss.item(), images.size(0))
            top1.update(acc1.item(), images.size(0))
            
            # Regular backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    
    return losses.avg, top1.avg

def validate(model, criterion, val_loader, device):
    """
    Validate the model
    
    Args:
        model: neural network model
        criterion: loss function
        val_loader: validation data loader
        device: device to use (cpu/cuda)
        
    Returns:
        average loss and accuracy
    """
    model.eval()
    losses = AverageMeter()
    top1 = AverageMeter()
    
    with torch.no_grad():
        for images, targets in val_loader:
            images, targets = images.to(device), targets.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, targets)
            
            # Update metrics
            acc1, = accuracy(outputs, targets, topk=(1,))
            losses.update(loss.item(), images.size(0))
            top1.update(acc1.item(), images.size(0))
    
    return losses.avg, top1.avg

def inference(model, test_loader, device):
    """
    Run inference on test data
    
    Args:
        model: neural network model
        test_loader: test data loader
        device: device to use (cpu/cuda)
        
    Returns:
        predictions, true labels, and probabilities
    """
    model.eval()
    all_preds = []
    all_labels = []
    all_probs = []
    
    with torch.no_grad():
        for images, targets in test_loader:
            images, targets = images.to(device), targets.to(device)
            
            outputs = model(images)
            probs = torch.nn.functional.softmax(outputs, dim=1)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(targets.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
    
    return np.array(all_preds), np.array(all_labels), np.array(all_probs)

def get_optimizer(optimizer_name, model, lr, weight_decay):
    """
    Get optimizer based on name
    
    Args:
        optimizer_name: name of the optimizer
        model: neural network model
        lr: learning rate
        weight_decay: weight decay factor
        
    Returns:
        optimizer
    """
    if optimizer_name == 'Adam':
        return optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    elif optimizer_name == 'SGD':
        return optim.SGD(model.parameters(), lr=lr, momentum=INIT_TRAINER['momentum'], 
                         weight_decay=weight_decay)
    elif optimizer_name == 'AdamW':
        return optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    else:
        raise ValueError(f"Optimizer {optimizer_name} not supported")

def get_scheduler(scheduler_name, optimizer):
    """
    Get learning rate scheduler based on name
    
    Args:
        scheduler_name: name of the scheduler
        optimizer: optimizer
        
    Returns:
        scheduler
    """
    if scheduler_name == 'MultiStepLR':
        return optim.lr_scheduler.MultiStepLR(optimizer, 
                                             milestones=INIT_TRAINER['milestones'], 
                                             gamma=INIT_TRAINER['gamma'])
    elif scheduler_name == 'CosineAnnealingLR':
        return optim.lr_scheduler.CosineAnnealingLR(optimizer, 
                                                   T_max=INIT_TRAINER['n_epoch'])
    elif scheduler_name == 'ReduceLROnPlateau':
        return optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', 
                                                   factor=0.1, patience=5)
    else:
        raise ValueError(f"Scheduler {scheduler_name} not supported")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Train ResNet for fine-grained classification')
    parser.add_argument('-m', '--mode', default='train', choices=['train', 'test', 'train-cross'],
                       help='Mode: train, test, or train-cross for cross-validation')
    parser.add_argument('-f', '--fold', type=int, default=1, help='Fold number for cross-validation')
    parser.add_argument('-b', '--batch_size', type=int, default=INIT_TRAINER['batch_size'], 
                       help='Batch size')
    parser.add_argument('-e', '--epochs', type=int, default=INIT_TRAINER['n_epoch'], 
                       help='Number of epochs')
    parser.add_argument('-lr', '--learning_rate', type=float, default=INIT_TRAINER['lr'], 
                       help='Learning rate')
    args = parser.parse_args()
    
    # Update parameters based on args
    INIT_TRAINER['batch_size'] = args.batch_size
    INIT_TRAINER['n_epoch'] = args.epochs
    INIT_TRAINER['lr'] = args.learning_rate
    
    # Set device
    device = torch.device(f"cuda:{INIT_TRAINER['device']}" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Create output directories
    os.makedirs(SETUP_TRAINER['output_dir'], exist_ok=True)
    os.makedirs(SETUP_TRAINER['log_dir'], exist_ok=True)
    os.makedirs(RESULT_DIR, exist_ok=True)
    
    # Initialize model
    model = ResNetModel(
        net_name=INIT_TRAINER['net_name'],
        num_classes=INIT_TRAINER['num_classes'], 
        dropout=INIT_TRAINER['dropout'], 
        pretrained=INIT_TRAINER['pre_trained']
    )
    model = model.to(device)
    
    # Print model info
    print(f"Model: {INIT_TRAINER['net_name']}")
    print(get_parameter_number(model))
    
    # Loss function
    criterion = nn.CrossEntropyLoss()
    
    # Training transforms
    train_transform = get_transforms(
        INIT_TRAINER['image_size'],
        INIT_TRAINER['train_mean'],
        INIT_TRAINER['train_std'],
        is_training=True
    )
    
    # Validation transforms
    val_transform = get_transforms(
        INIT_TRAINER['image_size'],
        INIT_TRAINER['train_mean'],
        INIT_TRAINER['train_std'],
        is_training=False
    )
    
    if args.mode == 'train':
        # Single fold training
        print("Starting training in single fold mode...")
        
        # Create datasets
        train_dataset = BirdDataset(TRAIN_CSV_PATH, transform=train_transform)
        
        # Split training data for validation
        train_df = pd.read_csv(TRAIN_CSV_PATH)
        train_indices, val_indices = next(StratifiedKFold(n_splits=5, shuffle=True, random_state=42).split(
            train_df, train_df['label']))
        
        # Save fold datasets for reference
        train_subset_df = train_df.iloc[train_indices].reset_index(drop=True)
        val_subset_df = train_df.iloc[val_indices].reset_index(drop=True)
        
        os.makedirs(os.path.join(SETUP_TRAINER['log_dir'], 'split'), exist_ok=True)
        train_subset_df.to_csv(os.path.join(SETUP_TRAINER['log_dir'], 'split', 'train.csv'), index=False)
        val_subset_df.to_csv(os.path.join(SETUP_TRAINER['log_dir'], 'split', 'val.csv'), index=False)
        
        # Create temporary CSV files for the datasets
        train_path = os.path.join(SETUP_TRAINER['log_dir'], 'split', 'train.csv')
        val_path = os.path.join(SETUP_TRAINER['log_dir'], 'split', 'val.csv')
        
        # Create new datasets using the split files
        train_split_dataset = BirdDataset(train_path, transform=train_transform)
        val_split_dataset = BirdDataset(val_path, transform=val_transform)
        
        # Create data loaders
        train_loader = DataLoader(
            train_split_dataset, 
            batch_size=INIT_TRAINER['batch_size'],
            shuffle=True,
            num_workers=INIT_TRAINER['num_workers'],
            pin_memory=True
        )
        
        val_loader = DataLoader(
            val_split_dataset,
            batch_size=INIT_TRAINER['batch_size'],
            shuffle=False,
            num_workers=INIT_TRAINER['num_workers'],
            pin_memory=True
        )
        
        # Initialize TensorBoard
        writer = SummaryWriter(SETUP_TRAINER['log_dir'])
        
        # Initialize optimizer and scheduler
        optimizer = get_optimizer(
            SETUP_TRAINER['optimizer'],
            model,
            INIT_TRAINER['lr'],
            INIT_TRAINER['weight_decay']
        )
        
        scheduler = get_scheduler(SETUP_TRAINER['lr_scheduler'], optimizer)
        
        # Initialize gradient scaler for mixed precision
        scaler = GradScaler()
        
        # Initialize early stopping
        early_stopping = EarlyStopping(patience=10, monitor='val_acc', op_type='max')
        
        # Training loop
        best_acc = 0.0
        start_time = time.time()
        
        for epoch in range(INIT_TRAINER['n_epoch']):
            epoch_start = time.time()
            
            # Train
            train_loss, train_acc = train_one_epoch(
                model, criterion, optimizer, train_loader, device, scaler, INIT_TRAINER['use_fp16']
            )
            
            # Validate
            val_loss, val_acc = validate(model, criterion, val_loader, device)
            
            epoch_time = time.time() - epoch_start
            
            # Update learning rate
            if isinstance(scheduler, optim.lr_scheduler.ReduceLROnPlateau):
                scheduler.step(val_loss)
            else:
                scheduler.step()
            
            # Log metrics
            writer.add_scalar('train/loss', train_loss, epoch)
            writer.add_scalar('train/acc', train_acc, epoch)
            writer.add_scalar('val/loss', val_loss, epoch)
            writer.add_scalar('val/acc', val_acc, epoch)
            writer.add_scalar('lr', optimizer.param_groups[0]['lr'], epoch)
            
            # Print progress
            print(f"Epoch {epoch+1}/{INIT_TRAINER['n_epoch']} [{epoch_time:.1f}s], "
                  f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%, "
                  f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
            
            # Save checkpoint if better
            if val_acc > best_acc:
                best_acc = val_acc
                os.makedirs(SETUP_TRAINER['output_dir'], exist_ok=True)
                checkpoint = {
                    'epoch': epoch,
                    'state_dict': model.state_dict(),
                    'optimizer': optimizer.state_dict(),
                    'best_acc': best_acc
                }
                torch.save(checkpoint, os.path.join(SETUP_TRAINER['output_dir'], f'epoch={epoch}.pth'))
                print(f"Saved new best model with accuracy: {best_acc:.2f}%")
            
            # Check early stopping
            early_stopping(val_acc)
            if early_stopping.early_stop:
                print("Early stopping triggered")
                break
        
        total_time = time.time() - start_time
        writer.close()
        print(f"Finished training in {total_time:.2f}s with best validation accuracy: {best_acc:.2f}%")
    
    elif args.mode == 'train-cross':
        # Cross-validation training
        print(f"Starting training in {FOLD_NUM}-fold cross-validation mode...")
        
        train_df = pd.read_csv(TRAIN_CSV_PATH)
        skf = StratifiedKFold(n_splits=FOLD_NUM, shuffle=True, random_state=42)
        
        for fold, (train_idx, val_idx) in enumerate(skf.split(train_df, train_df['label']), 1):
            if fold != args.fold and args.fold != 0:
                continue
                
            print(f"Training fold {fold}/{FOLD_NUM}")
            
            # Create fold-specific directories
            fold_output_dir = os.path.join(SETUP_TRAINER['output_dir'], f'fold{fold}')
            fold_log_dir = os.path.join(SETUP_TRAINER['log_dir'], f'fold{fold}')
            os.makedirs(fold_output_dir, exist_ok=True)
            os.makedirs(fold_log_dir, exist_ok=True)
            
            # Initialize TensorBoard
            writer = SummaryWriter(fold_log_dir)
            
            # Create temporary dataframes for the datasets
            train_subset_df = train_df.iloc[train_idx].reset_index(drop=True)
            val_subset_df = train_df.iloc[val_idx].reset_index(drop=True)
            
            # Save fold datasets for reference
            train_subset_df.to_csv(os.path.join(fold_log_dir, f'train_fold{fold}.csv'), index=False)
            val_subset_df.to_csv(os.path.join(fold_log_dir, f'val_fold{fold}.csv'), index=False)
            
            # Create datasets
            train_dataset = BirdDataset(os.path.join(fold_log_dir, f'train_fold{fold}.csv'), transform=train_transform)
            val_dataset = BirdDataset(os.path.join(fold_log_dir, f'val_fold{fold}.csv'), transform=val_transform)
            
            # Create data loaders
            train_loader = DataLoader(
                train_dataset, 
                batch_size=INIT_TRAINER['batch_size'],
                shuffle=True,
                num_workers=INIT_TRAINER['num_workers'],
                pin_memory=True
            )
            
            val_loader = DataLoader(
                val_dataset,
                batch_size=INIT_TRAINER['batch_size'],
                shuffle=False,
                num_workers=INIT_TRAINER['num_workers'],
                pin_memory=True
            )
            
            # Initialize a new model for each fold
            model = ResNetModel(
                net_name=INIT_TRAINER['net_name'],
                num_classes=INIT_TRAINER['num_classes'], 
                dropout=INIT_TRAINER['dropout'], 
                pretrained=INIT_TRAINER['pre_trained']
            )
            model = model.to(device)
            
            # Initialize optimizer and scheduler
            optimizer = get_optimizer(
                SETUP_TRAINER['optimizer'],
                model,
                INIT_TRAINER['lr'],
                INIT_TRAINER['weight_decay']
            )
            
            scheduler = get_scheduler(SETUP_TRAINER['lr_scheduler'], optimizer)
            
            # Initialize gradient scaler for mixed precision
            scaler = GradScaler()
            
            # Initialize early stopping
            early_stopping = EarlyStopping(patience=10, monitor='val_acc', op_type='max')
            
            # Training loop
            best_acc = 0.0
            start_time = time.time()
            
            for epoch in range(INIT_TRAINER['n_epoch']):
                epoch_start = time.time()
                
                # Train
                train_loss, train_acc = train_one_epoch(
                    model, criterion, optimizer, train_loader, device, scaler, INIT_TRAINER['use_fp16']
                )
                
                # Validate
                val_loss, val_acc = validate(model, criterion, val_loader, device)
                
                epoch_time = time.time() - epoch_start
                
                # Update learning rate
                if isinstance(scheduler, optim.lr_scheduler.ReduceLROnPlateau):
                    scheduler.step(val_loss)
                else:
                    scheduler.step()
                
                # Log metrics
                writer.add_scalar('train/loss', train_loss, epoch)
                writer.add_scalar('train/acc', train_acc, epoch)
                writer.add_scalar('val/loss', val_loss, epoch)
                writer.add_scalar('val/acc', val_acc, epoch)
                writer.add_scalar('lr', optimizer.param_groups[0]['lr'], epoch)
                
                # Print progress
                print(f"Fold {fold}, Epoch {epoch+1}/{INIT_TRAINER['n_epoch']} [{epoch_time:.1f}s], "
                      f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%, "
                      f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
                
                # Save checkpoint if better
                if val_acc > best_acc:
                    best_acc = val_acc
                    checkpoint = {
                        'epoch': epoch,
                        'state_dict': model.state_dict(),
                        'optimizer': optimizer.state_dict(),
                        'best_acc': best_acc
                    }
                    torch.save(checkpoint, os.path.join(fold_output_dir, f'epoch={epoch}.pth'))
                    print(f"Saved new best model with accuracy: {best_acc:.2f}%")
                
                # Check early stopping
                early_stopping(val_acc)
                if early_stopping.early_stop:
                    print(f"Fold {fold} early stopping triggered")
                    break
            
            total_time = time.time() - start_time
            writer.close()
            print(f"Finished training fold {fold} in {total_time:.2f}s with best validation accuracy: {best_acc:.2f}%")
    
    elif args.mode == 'test':
        # Testing mode
        print("Starting inference on test set...")
        
        # Handle fold path for loading weights
        checkpoint_path = os.path.join(SETUP_TRAINER['output_dir'])
        if args.fold > 0:
            checkpoint_path = os.path.join(checkpoint_path, f'fold{args.fold}')
        
        if not os.path.exists(checkpoint_path):
            print(f"No checkpoint found in {checkpoint_path}")
            return
            
        checkpoint_files = [f for f in os.listdir(checkpoint_path) if f.endswith('.pth')]
        if not checkpoint_files:
            print(f"No checkpoint files found in {checkpoint_path}")
            return
        
        # Get the latest checkpoint
        checkpoint_files.sort(key=lambda x: int(x.split('=')[1].split('.')[0]))
        latest_checkpoint = os.path.join(checkpoint_path, checkpoint_files[-1])
        
        # Load checkpoint
        checkpoint = torch.load(latest_checkpoint)
        model.load_state_dict(checkpoint['state_dict'])
        print(f"Loaded checkpoint from {latest_checkpoint}")
        
        # Create test dataset and loader
        test_dataset = BirdDataset(TEST_CSV_PATH, transform=val_transform)
        test_loader = DataLoader(
            test_dataset,
            batch_size=INIT_TRAINER['batch_size'],
            shuffle=False,
            num_workers=INIT_TRAINER['num_workers'],
            pin_memory=True
        )
        
        # Run inference
        start_time = time.time()
        predictions, true_labels, probabilities = inference(model, test_loader, device)
        inference_time = time.time() - start_time
        
        # Compute metrics
        report = classification_report(true_labels, predictions, output_dict=True)
        accuracy = report['accuracy'] * 100
        
        # Save confusion matrix
        cm = confusion_matrix(true_labels, predictions)
        np.save(os.path.join(RESULT_DIR, f'fold{args.fold}_confusion_matrix.npy'), cm)
        
        # Save results
        results_file = os.path.join(RESULT_DIR, f'fold{args.fold}_results.csv')
        test_df = pd.read_csv(TEST_CSV_PATH)
        results_df = pd.DataFrame({
            'id': test_df['id'],
            'true': true_labels,
            'pred': predictions,
            'prob': [p.max() for p in probabilities]
        })
        results_df.to_csv(results_file, index=False)
        
        # Save report
        report_df = pd.DataFrame(report).transpose()
        report_df.to_csv(os.path.join(RESULT_DIR, f'fold{args.fold}_report.csv'))
        
        print(f"Inference completed in {inference_time:.2f}s")
        print(f"Test accuracy: {accuracy:.2f}%")
        print(f"Results saved to {results_file}")
        print(f"Classification report saved to {os.path.join(RESULT_DIR, f'fold{args.fold}_report.csv')}")

if __name__ == "__main__":
    main()
