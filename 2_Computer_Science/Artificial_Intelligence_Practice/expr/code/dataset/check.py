# Standard library imports
import os
import sys
import argparse
from collections import Counter

# Third-party imports - data analysis and scientific computing
import numpy as np
import pandas as pd

# Third-party imports - image processing
import cv2
from PIL import Image

# Third-party imports - visualization
import matplotlib.pyplot as plt

# Third-party imports - utilities
from tqdm import tqdm

def check_dataset(data_dir):
    """
    Check the dataset for issues and generate statistics
    
    Parameters:
    -----------
    data_dir : str
        Path to the dataset directory
        
    Returns:
    --------
    stats : dict
        Dictionary containing dataset statistics
    """
    print(f"\nChecking dataset in {data_dir}...")
    stats = {}
    
    # Check if directory exists
    if not os.path.exists(data_dir):
        print(f"Error: Dataset directory {data_dir} does not exist")
        return stats
    
    # Check for expected structure (train/valid/test)
    splits = ['train', 'valid', 'test']
    missing_splits = [split for split in splits if not os.path.exists(os.path.join(data_dir, split))]
    
    if missing_splits:
        print(f"Warning: Missing expected data splits: {missing_splits}")
    
    # Process each split
    stats['splits'] = {}
    total_images = 0
    corrupted_images = 0
    
    for split in splits:
        split_dir = os.path.join(data_dir, split)
        if not os.path.exists(split_dir):
            continue
            
        # Get class directories
        class_dirs = [d for d in os.listdir(split_dir) 
                     if os.path.isdir(os.path.join(split_dir, d))]
        
        if not class_dirs:
            print(f"Warning: No class directories found in {split_dir}")
            continue
        
        stats['splits'][split] = {
            'classes': {},
            'total_images': 0,
            'corrupted_images': 0,
            'image_sizes': Counter(),
            'image_formats': Counter()
        }
        
        # Process each class
        print(f"\nProcessing {split} set:")
        
        for class_name in class_dirs:
            class_dir = os.path.join(split_dir, class_name)
            
            # Get image files
            image_files = [f for f in os.listdir(class_dir)
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
            
            # Initialize class stats
            stats['splits'][split]['classes'][class_name] = {
                'count': len(image_files),
                'corrupted': 0,
                'sizes': Counter(),
                'formats': Counter()
            }
            
            # Check each image
            for img_file in tqdm(image_files, desc=f"  {class_name}", leave=False):
                img_path = os.path.join(class_dir, img_file)
                
                try:
                    # Try to open with PIL first (better for detecting corruption)
                    with Image.open(img_path) as img:
                        img_format = img.format
                        width, height = img.size
                    
                    # Also try OpenCV to detect other issues
                    cv_img = cv2.imread(img_path)
                    if cv_img is None:
                        raise Exception("OpenCV could not read image")
                    
                    # Count image format and size
                    size_key = f"{width}x{height}"
                    stats['splits'][split]['image_formats'][img_format] += 1
                    stats['splits'][split]['image_sizes'][size_key] += 1
                    stats['splits'][split]['classes'][class_name]['formats'][img_format] += 1
                    stats['splits'][split]['classes'][class_name]['sizes'][size_key] += 1
                    
                except Exception as e:
                    # Count corrupted image
                    stats['splits'][split]['corrupted_images'] += 1
                    stats['splits'][split]['classes'][class_name]['corrupted'] += 1
                    corrupted_images += 1
                    print(f"  Corrupted image: {img_path} - {str(e)}")
            
            # Update total images count
            stats['splits'][split]['total_images'] += len(image_files)
            total_images += len(image_files)
            
            # Print class summary
            print(f"  {class_name}: {len(image_files)} images, {stats['splits'][split]['classes'][class_name]['corrupted']} corrupted")
            
        # Print split summary
        print(f"\n{split} set summary:")
        print(f"  Total classes: {len(class_dirs)}")
        print(f"  Total images: {stats['splits'][split]['total_images']}")
        print(f"  Corrupted images: {stats['splits'][split]['corrupted_images']}")
        
        # Print image size distribution
        print("  Image size distribution:")
        for size, count in stats['splits'][split]['image_sizes'].most_common(5):
            print(f"    {size}: {count} images")
        
        # Print image format distribution
        print("  Image format distribution:")
        for fmt, count in stats['splits'][split]['image_formats'].most_common():
            print(f"    {fmt}: {count} images")
    
    # Overall dataset statistics
    stats['total_images'] = total_images
    stats['corrupted_images'] = corrupted_images
    stats['class_distribution'] = {
        split: {class_name: info['count'] 
               for class_name, info in stats['splits'][split]['classes'].items()}
        for split in stats['splits']
    }
    
    # Visualize class distribution
    visualize_class_distribution(stats)
    
    # Print overall summary
    print("\nOverall dataset summary:")
    print(f"  Total images: {total_images}")
    print(f"  Corrupted images: {corrupted_images} ({corrupted_images/total_images*100:.2f}%)")
    
    return stats

def visualize_class_distribution(stats):
    """Visualize class distribution across splits"""
    # Setup subplots
    splits = list(stats['splits'].keys())
    if not splits:
        return
        
    fig, axes = plt.subplots(len(splits), 1, figsize=(12, 5*len(splits)))
    if len(splits) == 1:
        axes = [axes]
    
    # Plot class distribution for each split
    for i, split in enumerate(splits):
        class_counts = stats['class_distribution'][split]
        
        # Sort by class name
        sorted_classes = sorted(class_counts.keys())
        counts = [class_counts[cls] for cls in sorted_classes]
        
        axes[i].bar(sorted_classes, counts)
        axes[i].set_title(f'Class Distribution - {split} set')
        axes[i].set_xlabel('Class')
        axes[i].set_ylabel('Number of images')
        axes[i].tick_params(axis='x', rotation=45)
        
        # Add count labels
        for j, count in enumerate(counts):
            axes[i].text(j, count + 0.5, str(count), ha='center')
    
    plt.tight_layout()
    plt.savefig('dataset_class_distribution.png')
    plt.close()
    
    # Create a stacked bar chart comparing splits
    if len(splits) > 1:
        # Get all unique classes
        all_classes = set()
        for split in splits:
            all_classes.update(stats['class_distribution'][split].keys())
        all_classes = sorted(all_classes)
        
        # Prepare data
        data = []
        for cls in all_classes:
            row = {'Class': cls}
            for split in splits:
                row[split] = stats['class_distribution'][split].get(cls, 0)
            data.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Plot stacked bar chart
        df.set_index('Class').plot(kind='bar', stacked=True, figsize=(12, 6))
        plt.title('Class Distribution Across Splits')
        plt.xlabel('Class')
        plt.ylabel('Number of images')
        plt.tight_layout()
        plt.savefig('dataset_split_comparison.png')
        plt.close()

def main():
    parser = argparse.ArgumentParser(description='Check dataset for issues and generate statistics')
    parser.add_argument('--data-dir', type=str, default='./data/RockData',
                       help='Path to the dataset directory')
    args = parser.parse_args()
    
    check_dataset(args.data_dir)

if __name__ == '__main__':
    main()
