import os
import cv2
import numpy as np
from scipy.ndimage import rotate
import random
from sklearn.preprocessing import LabelEncoder

def horizontal_flip(image):
    """Apply horizontal flip to an image"""
    return cv2.flip(image, 1)

def vertical_flip(image):
    """Apply vertical flip to an image"""
    return cv2.flip(image, 0)

def random_rotation(image, max_angle=20):
    """Apply random rotation to an image"""
    angle = random.uniform(-max_angle, max_angle)
    return rotate(image, angle, reshape=False, mode='nearest')

def random_brightness(image, max_delta=0.2):
    """Apply random brightness adjustment to an image"""
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    delta = random.uniform(-max_delta, max_delta)
    hsv[:, :, 2] = hsv[:, :, 2] * (1.0 + delta)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

def random_contrast(image, lower=0.8, upper=1.2):
    """Apply random contrast adjustment to an image"""
    alpha = random.uniform(lower, upper)
    return np.clip(alpha * image, 0, 255).astype(np.uint8)

def random_crop_and_resize(image, min_crop_ratio=0.8, target_size=None):
    """Apply random crop and resize to an image"""
    h, w = image.shape[:2]
    if target_size is None:
        target_size = (w, h)
    
    crop_ratio = random.uniform(min_crop_ratio, 1.0)
    crop_h = int(h * crop_ratio)
    crop_w = int(w * crop_ratio)
    
    # Random crop coordinates
    top = random.randint(0, h - crop_h)
    left = random.randint(0, w - crop_w)
    
    # Crop and resize
    cropped = image[top:top+crop_h, left:left+crop_w]
    return cv2.resize(cropped, target_size)

def add_noise(image, noise_type="gaussian", var=0.01):
    """Add noise to an image"""
    image_float = image.astype(np.float32) / 255.0
    
    if noise_type == "gaussian":
        noise = np.random.normal(0, np.sqrt(var), image.shape)
        noisy = image_float + noise
    elif noise_type == "salt_and_pepper":
        s_vs_p = 0.5
        amount = var
        # Salt
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = tuple([np.random.randint(0, i - 1, int(num_salt)) for i in image.shape[:2]])
        image_float[coords[0], coords[1], :] = 1.0
        # Pepper
        num_pepper = np.ceil(amount * image.size * (1.0 - s_vs_p))
        coords = tuple([np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape[:2]])
        image_float[coords[0], coords[1], :] = 0.0
        noisy = image_float
    else:
        return image
    
    return np.clip(noisy * 255.0, 0, 255).astype(np.uint8)

def augment_image(image, augmentation_methods=None):
    """
    Apply multiple augmentation methods to an image
    
    Args:
        image: Input image
        augmentation_methods: List of augmentation methods to apply
        
    Returns:
        Augmented image
    """
    if augmentation_methods is None:
        # Default augmentation methods with probability of application
        augmentation_methods = [
            (horizontal_flip, 0.5),
            (random_rotation, 0.3),
            (random_brightness, 0.3),
            (random_contrast, 0.3),
            (random_crop_and_resize, 0.3),
            (add_noise, 0.2)
        ]
    
    augmented = image.copy()
    for method, probability in augmentation_methods:
        if random.random() < probability:
            if method == random_rotation:
                augmented = method(augmented, max_angle=20)
            elif method == random_brightness:
                augmented = method(augmented, max_delta=0.2)
            elif method == random_contrast:
                augmented = method(augmented, lower=0.8, upper=1.2)
            elif method == random_crop_and_resize:
                augmented = method(augmented, min_crop_ratio=0.8, target_size=(image.shape[1], image.shape[0]))
            elif method == add_noise:
                augmented = method(augmented, noise_type="gaussian", var=0.01)
            else:
                augmented = method(augmented)
    
    return augmented

def augment_dataset(X, y, num_augmentations=1, augmentation_methods=None):
    """
    Apply data augmentation to a dataset
    
    Args:
        X: Input images of shape (n_samples, height, width, channels)
        y: Input labels of shape (n_samples,)
        num_augmentations: Number of augmented versions to create per image
        augmentation_methods: List of augmentation methods to apply
        
    Returns:
        X_augmented: Augmented images
        y_augmented: Corresponding labels
    """
    n_samples = X.shape[0]
    X_augmented = []
    y_augmented = []
    
    # Add original data
    X_augmented.append(X)
    y_augmented.append(y)
    
    # Add augmented data
    for i in range(num_augmentations):
        X_aug = []
        for j in range(n_samples):
            aug_img = augment_image(X[j], augmentation_methods)
            X_aug.append(aug_img)
        
        X_augmented.append(np.array(X_aug))
        y_augmented.append(y)
    
    # Combine all data
    X_combined = np.vstack(X_augmented)
    y_combined = np.hstack(y_augmented)
    
    return X_combined, y_combined

def augment_class_balanced(X, y, target_samples_per_class=None, augmentation_methods=None):
    """
    Augment data to achieve balanced classes
    
    Args:
        X: Input images of shape (n_samples, height, width, channels)
        y: Input labels of shape (n_samples,)
        target_samples_per_class: Target number of samples per class (if None, use max class count)
        augmentation_methods: List of augmentation methods to apply
        
    Returns:
        X_balanced: Balanced dataset with original and augmented images
        y_balanced: Corresponding labels
    """
    # Count samples per class
    unique_classes, class_counts = np.unique(y, return_counts=True)
    
    # Determine target count per class
    if target_samples_per_class is None:
        target_samples_per_class = np.max(class_counts)
    
    X_balanced = []
    y_balanced = []
    
    # For each class
    for class_idx, count in zip(unique_classes, class_counts):
        # Get samples of this class
        class_mask = (y == class_idx)
        X_class = X[class_mask]
        y_class = y[class_mask]
        
        # Add original samples
        X_balanced.append(X_class)
        y_balanced.append(y_class)
        
        # If we need more samples
        if count < target_samples_per_class:
            augmentations_needed = target_samples_per_class - count
            
            # Calculate how many times to augment each original sample on average
            augs_per_sample = int(np.ceil(augmentations_needed / count))
            
            # Create augmented samples
            for i in range(augs_per_sample):
                # Break if we have enough
                if len(X_balanced) * count >= target_samples_per_class:
                    break
                    
                X_aug = []
                for j in range(len(X_class)):
                    aug_img = augment_image(X_class[j], augmentation_methods)
                    X_aug.append(aug_img)
                
                X_balanced.append(np.array(X_aug))
                y_balanced.append(y_class)
                
            # Trim excess samples to match target exactly
            X_combined = np.vstack(X_balanced)
            y_combined = np.hstack(y_balanced)
            
            if len(y_combined) > target_samples_per_class:
                indices = np.arange(len(y_combined))
                np.random.shuffle(indices)
                indices = indices[:target_samples_per_class]
                X_balanced = [X_combined[indices]]
                y_balanced = [y_combined[indices]]
            else:
                X_balanced = [X_combined]
                y_balanced = [y_combined]
    
    # Combine all classes
    X_result = np.vstack([x for x in X_balanced if len(x) > 0])
    y_result = np.hstack([y for y in y_balanced if len(y) > 0])
    
    return X_result, y_result

if __name__ == "__main__":
    # Example usage
    from load_dataset import load_dataset
    
    data = load_dataset("../data")
    X_train, y_train = data['X_train'], data['y_train']
    
    # Basic augmentation
    X_aug, y_aug = augment_dataset(X_train, y_train, num_augmentations=2)
    print(f"Original dataset: {X_train.shape}, Augmented: {X_aug.shape}")
    
    # Balanced augmentation
    X_balanced, y_balanced = augment_class_balanced(X_train, y_train)
    print(f"Original dataset: {X_train.shape}, Balanced: {X_balanced.shape}")
    
    # Class distribution before and after
    unique, counts_before = np.unique(y_train, return_counts=True)
    unique, counts_after = np.unique(y_balanced, return_counts=True)
    
    print("Class distribution before balancing:")
    for u, c in zip(unique, counts_before):
        print(f"  Class {u}: {c} samples")
        
    print("Class distribution after balancing:")
    for u, c in zip(unique, counts_after):
        print(f"  Class {u}: {c} samples")
