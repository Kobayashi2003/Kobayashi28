import os
import numpy as np
from PIL import Image
import cv2
from sklearn.preprocessing import LabelEncoder

def load_images_from_folder(folder_path, img_size=(224, 224), convert_to_grayscale=False):
    """
    Load all images from a folder and its subfolders
    
    Args:
        folder_path: Path to the main folder
        img_size: Tuple of (width, height) to resize images
        convert_to_grayscale: Whether to convert images to grayscale
        
    Returns:
        images: List of loaded and processed images
        labels: List of corresponding labels (folder names)
        class_names: List of unique class names
    """
    images = []
    labels = []
    
    for class_folder in os.listdir(folder_path):
        class_path = os.path.join(folder_path, class_folder)
        if not os.path.isdir(class_path):
            continue
            
        for img_file in os.listdir(class_path):
            img_path = os.path.join(class_path, img_file)
            if not img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            try:
                img = cv2.imread(img_path)
                if img is None:
                    continue
                    
                img = cv2.resize(img, img_size)
                
                if convert_to_grayscale:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    img = np.expand_dims(img, axis=-1)
                else:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                images.append(img)
                labels.append(class_folder)
            except Exception as e:
                print(f"Error loading {img_path}: {e}")
    
    # Convert labels to numerical format
    encoder = LabelEncoder()
    encoded_labels = encoder.fit_transform(labels)
    
    return np.array(images), np.array(encoded_labels), encoder.classes_

def load_dataset(data_dir, img_size=(224, 224), convert_to_grayscale=False):
    """
    Load train, validation and test datasets
    
    Args:
        data_dir: Root directory containing train, valid, test folders
        img_size: Tuple of (width, height) to resize images
        convert_to_grayscale: Whether to convert images to grayscale
        
    Returns:
        Dictionary containing train, valid, test data and labels
    """
    train_dir = os.path.join(data_dir, 'train')
    valid_dir = os.path.join(data_dir, 'valid')
    test_dir = os.path.join(data_dir, 'test')
    
    X_train, y_train, class_names = load_images_from_folder(train_dir, img_size, convert_to_grayscale)
    X_valid, y_valid, _ = load_images_from_folder(valid_dir, img_size, convert_to_grayscale)
    X_test, y_test, _ = load_images_from_folder(test_dir, img_size, convert_to_grayscale)
    
    return {
        'X_train': X_train, 
        'y_train': y_train,
        'X_valid': X_valid, 
        'y_valid': y_valid,
        'X_test': X_test, 
        'y_test': y_test,
        'class_names': class_names
    }
