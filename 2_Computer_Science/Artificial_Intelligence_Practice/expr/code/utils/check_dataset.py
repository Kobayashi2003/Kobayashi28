import os
import cv2
import numpy as np
from collections import Counter

def check_dataset_structure(data_dir):
    """
    Check if dataset has the expected directory structure
    
    Args:
        data_dir: Root directory of the dataset
        
    Returns:
        bool: True if structure is valid, False otherwise
    """
    required_dirs = ['train', 'valid', 'test']
    
    # Check if main directories exist
    for dir_name in required_dirs:
        dir_path = os.path.join(data_dir, dir_name)
        if not os.path.isdir(dir_path):
            print(f"Error: {dir_path} is not a directory or doesn't exist")
            return False
    
    # Get class names from train directory
    train_dir = os.path.join(data_dir, 'train')
    class_names = [d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))]
    
    if len(class_names) == 0:
        print(f"Error: No class directories found in {train_dir}")
        return False
    
    # Check if all classes exist in all splits
    for split in required_dirs:
        split_dir = os.path.join(data_dir, split)
        split_classes = [d for d in os.listdir(split_dir) if os.path.isdir(os.path.join(split_dir, d))]
        
        missing_classes = set(class_names) - set(split_classes)
        if missing_classes:
            print(f"Error: Classes {missing_classes} missing from {split} split")
            return False
    
    print(f"Dataset structure is valid with {len(class_names)} classes: {', '.join(class_names)}")
    return True

def check_image_stats(data_dir):
    """
    Check image statistics for each class and split
    
    Args:
        data_dir: Root directory of the dataset
        
    Returns:
        dict: Statistics about the dataset
    """
    splits = ['train', 'valid', 'test']
    stats = {}
    
    # Get class names from train directory
    train_dir = os.path.join(data_dir, 'train')
    class_names = [d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))]
    
    # Check count of images in each class and split
    for split in splits:
        split_stats = {}
        split_dir = os.path.join(data_dir, split)
        
        for class_name in class_names:
            class_dir = os.path.join(split_dir, class_name)
            image_files = [f for f in os.listdir(class_dir) 
                          if os.path.isfile(os.path.join(class_dir, f)) and 
                          f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            split_stats[class_name] = len(image_files)
        
        stats[split] = split_stats
    
    # Print summary
    print("Dataset statistics:")
    for split, split_stats in stats.items():
        total = sum(split_stats.values())
        print(f"  {split}: {total} images")
        for class_name, count in split_stats.items():
            print(f"    {class_name}: {count} images ({count/total*100:.1f}%)")
    
    return stats

def check_image_dimensions(data_dir, sample_size=10):
    """
    Check image dimensions from a sample of images
    
    Args:
        data_dir: Root directory of the dataset
        sample_size: Number of images to sample from each class
        
    Returns:
        dict: Image dimension statistics
    """
    train_dir = os.path.join(data_dir, 'train')
    class_names = [d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))]
    
    dimensions = []
    
    for class_name in class_names:
        class_dir = os.path.join(train_dir, class_name)
        image_files = [f for f in os.listdir(class_dir) 
                      if os.path.isfile(os.path.join(class_dir, f)) and 
                      f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Sample images
        sample_files = image_files[:sample_size] if len(image_files) > sample_size else image_files
        
        for img_file in sample_files:
            img_path = os.path.join(class_dir, img_file)
            img = cv2.imread(img_path)
            if img is not None:
                h, w = img.shape[:2]
                dimensions.append((w, h))
    
    # Count occurrences of each dimension
    dim_counter = Counter(dimensions)
    most_common = dim_counter.most_common(5)
    
    print("Most common image dimensions (width, height):")
    for dim, count in most_common:
        print(f"  {dim}: {count} images")
    
    return dim_counter

def check_dataset(data_dir):
    """
    Run all dataset checks
    
    Args:
        data_dir: Root directory of the dataset
    """
    if not check_dataset_structure(data_dir):
        return
    
    check_image_stats(data_dir)
    check_image_dimensions(data_dir)
    
if __name__ == "__main__":
    # Example usage
    data_dir = "../data"
    check_dataset(data_dir)
