import os
import random
import pickle
import multiprocessing
from datetime import datetime

import cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

from skimage.feature import local_binary_pattern, graycomatrix, graycoprops

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


def load_dataset(data_dir, img_size=(224, 224)):
    """
    Load JPG images from dataset directory structure
    
    Args:
        data_dir (str): Path to dataset directory
        img_size (tuple): Target image size (width, height)
        
    Returns:
        dict: Dictionary containing loaded data and class names
    """
    result = {}
    encoder = LabelEncoder()
    
    train_dir = os.path.join(data_dir, 'train')
    class_folders = [d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))]
    result['class_names'] = class_folders
    
    for subset in ['train', 'valid', 'test']:
        subset_dir = os.path.join(data_dir, subset)
        images = []
        labels = []
        
        for class_name in class_folders:
            class_path = os.path.join(subset_dir, class_name)
            img_files = [f for f in os.listdir(class_path) if f.lower().endswith('.jpg')]
            
            for img_file in img_files:
                img_path = os.path.join(class_path, img_file)
                img = cv2.imread(img_path)
                img = cv2.resize(img, img_size)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                images.append(img)
                labels.append(class_name)
        
        X = np.array(images)
        
        if subset == 'train':
            y = encoder.fit_transform(labels)
        else:
            y = encoder.transform(labels)
        
        result[f'X_{subset}'] = X
        result[f'y_{subset}'] = y
    
    return result


def extract_features_single(img, use_knn_style=True):
    """
    Extract comprehensive features for rock classification
    
    Args:
        img (ndarray): Input image in RGB format
        use_knn_style (bool): Whether to use the more comprehensive KNN-style features
        
    Returns:
        ndarray: Feature vector
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    img_lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    
    features = []
    
    # RGB statistics
    if use_knn_style:
        for i, channel in enumerate(cv2.split(img)):
            features.extend([
                np.mean(channel),
                np.std(channel),
                np.percentile(channel, 25),
                np.percentile(channel, 75),
                np.median(channel)
            ])
        
        # HSV features with special handling for hue's circular nature
        h, s, v = cv2.split(img_hsv)
        
        # Convert hue to Cartesian coordinates to handle circularity properly
        h_rad = h * (2 * np.pi / 180.0)
        h_sin = np.sin(h_rad)
        h_cos = np.cos(h_rad)
        
        features.extend([
            np.mean(h_sin), np.mean(h_cos),  
            np.std(h_sin), np.std(h_cos),    
            np.mean(s), np.std(s),           
            np.percentile(s, 25), np.percentile(s, 75),
            np.mean(v), np.std(v),           
            np.percentile(v, 25), np.percentile(v, 75)
        ])
    else:
        for i, channel in enumerate(cv2.split(img)):
            features.extend([
                np.mean(channel),
                np.std(channel),
                np.percentile(channel, 25),
                np.percentile(channel, 75)
            ])
        
        for i, channel in enumerate(cv2.split(img_hsv)):
            features.extend([
                np.mean(channel),
                np.std(channel),
                np.percentile(channel, 25),
                np.percentile(channel, 75)
            ])
    
    # LAB features
    for i, channel in enumerate(cv2.split(img_lab)):
        features.extend([
            np.mean(channel),
            np.std(channel),
            np.percentile(channel, 25),
            np.percentile(channel, 75)
        ])
    
    # Color histograms with fewer bins for better generalization
    hist_bins = 32
    
    # RGB histograms
    for i, channel in enumerate(cv2.split(img)):
        hist = cv2.calcHist([channel], [0], None, [hist_bins], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        features.extend(hist)
    
    # HSV histograms
    h, s, v = cv2.split(img_hsv)
    
    if use_knn_style:
        h_bins, s_bins, v_bins = 20, 15, 15  # Adaptive binning from KNN
    else:
        h_bins = s_bins = v_bins = hist_bins
    
    h_hist = cv2.calcHist([h], [0], None, [h_bins], [0, 180])
    s_hist = cv2.calcHist([s], [0], None, [s_bins], [0, 256])
    v_hist = cv2.calcHist([v], [0], None, [v_bins], [0, 256])
    
    h_hist = cv2.normalize(h_hist, h_hist).flatten()
    s_hist = cv2.normalize(s_hist, s_hist).flatten()
    v_hist = cv2.normalize(v_hist, v_hist).flatten()
    
    features.extend(h_hist)
    features.extend(s_hist)
    features.extend(v_hist)
    
    # Texture features
    img_gray_uint8 = cv2.normalize(img_gray, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Multi-scale LBP at different resolutions
    lbp_features = []
    radius_range = [1, 3, 5] if use_knn_style else [1, 3]
    for radius in radius_range:
        n_points = 8 * radius
        lbp = local_binary_pattern(img_gray_uint8, n_points, radius, method='uniform')
        hist, _ = np.histogram(lbp.ravel(), bins=n_points+2, range=(0, n_points+2), density=True)
        lbp_features.extend(hist)
    
    features.extend(lbp_features)
    
    # GLCM for texture patterns
    img_gray_quantized = (img_gray_uint8 // 32).astype(np.uint8)  # 8 gray levels
    
    glcm_features = []
    distances = [1, 3, 5] if use_knn_style else [1, 3]
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
    props = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']
    
    for d in distances:
        glcm = graycomatrix(img_gray_quantized, [d], angles, 8, symmetric=True, normed=True)
        for prop in props:
            glcm_features.append(graycoprops(glcm, prop).mean())
    
    features.extend(glcm_features)
    
    # Edge features
    if use_knn_style:
        # Enhanced edge detection with two thresholds
        edges_low = cv2.Canny(img_gray_uint8, 50, 150)
        edges_high = cv2.Canny(img_gray_uint8, 100, 200)
        
        edge_density_low = np.sum(edges_low > 0) / edges_low.size
        edge_density_high = np.sum(edges_high > 0) / edges_high.size
        edge_density_ratio = edge_density_low / (edge_density_high + 1e-10)
        
        features.extend([edge_density_low, edge_density_high, edge_density_ratio])
    else:
        # Basic edge detection
        edges = cv2.Canny(img_gray_uint8, 100, 200)
        edge_density = np.sum(edges > 0) / edges.size
        features.append(edge_density)
    
    # Granularity features
    gray_small = cv2.resize(img_gray_uint8, (100, 100))
    granularity_features = []
    
    kernel_sizes = [3, 5, 7, 9] if use_knn_style else [3, 5, 7]
    for kernel_size in kernel_sizes:
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        opened = cv2.morphologyEx(gray_small, cv2.MORPH_OPEN, kernel)
        closed = cv2.morphologyEx(gray_small, cv2.MORPH_CLOSE, kernel)
        
        open_diff = np.mean(np.abs(gray_small.astype(float) - opened.astype(float)))
        close_diff = np.mean(np.abs(gray_small.astype(float) - closed.astype(float)))
        
        granularity_features.extend([open_diff, close_diff])
    
    features.extend(granularity_features)
    
    # Region-based features
    h, w = img_gray.shape
    
    if use_knn_style:
        # 3x3 grid regions
        region_features = []
        for i in range(3):
            for j in range(3):
                start_h, end_h = i*h//3, (i+1)*h//3
                start_w, end_w = j*w//3, (j+1)*w//3
                
                region = img_gray[start_h:end_h, start_w:end_w]
                
                region_features.extend([
                    np.mean(region),
                    np.std(region),
                    np.max(region) - np.min(region)
                ])
        features.extend(region_features)
    else:
        # 2x2 grid regions
        regions = []
        for i in range(2):
            for j in range(2):
                region = img_gray[i*h//2:(i+1)*h//2, j*w//2:(j+1)*w//2]
                regions.append(region)
        
        for region in regions:
            region_stats = [
                np.mean(region),
                np.std(region),
                np.max(region) - np.min(region)
            ]
            features.extend(region_stats)
    
    feature_vector = np.array(features)
    feature_vector = np.nan_to_num(feature_vector)  # Handle any NaN values
    
    return feature_vector


def extract_features(images, dataset_name='dataset', filename=None, n_jobs=None, use_knn_style=True):
    """
    Extract features using parallel processing
    
    Args:
        images (ndarray): Array of input images
        dataset_name (str): Name of dataset (used for filename if provided)
        filename (str, optional): Path to save/load features. If None, features won't be saved.
        n_jobs (int, optional): Number of parallel processes to use
        use_knn_style (bool): Whether to use KNN-style features
        
    Returns:
        ndarray: Extracted features
    """
    n_samples = len(images)
    
    if filename is not None:
        # Create parent directory if it doesn't exist
        parent_dir = os.path.dirname(filename)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
            
        if os.path.exists(filename):
            print(f"Loading cached features from {filename}")
            try:
                with open(filename, 'rb') as f:
                    features = pickle.load(f)
                return features
            except Exception as e:
                print(f"Error loading cached features: {e}. Re-extracting...")
    
    if n_jobs is None:
        n_jobs = multiprocessing.cpu_count()
    n_jobs = min(n_jobs, multiprocessing.cpu_count())
    
    print(f"Extracting features from {n_samples} images using {n_jobs} processes...")
    
    # Create a partial function with the use_knn_style parameter
    from functools import partial
    extract_func = partial(extract_features_single, use_knn_style=use_knn_style)
    
    with multiprocessing.Pool(processes=n_jobs) as pool:
        features = list(tqdm(
            pool.imap(extract_func, images),
            total=n_samples,
            desc=f"Extracting {dataset_name} features"
        ))
    
    features = np.array(features)
    
    if filename is not None:
        try:
            print(f"Saving extracted features to {filename}")
            with open(filename, 'wb') as f:
                pickle.dump(features, f)
        except Exception as e:
            print(f"Error saving features: {e}")
    
    return features


def augment_image(image, use_knn_style=True):
    """
    Apply data augmentation focusing on color variations
    
    Args:
        image (ndarray): Input image to augment
        use_knn_style (bool): Whether to use the more comprehensive KNN-style augmentation
        
    Returns:
        ndarray: Augmented image
    """
    augmented = image.copy()
    
    if use_knn_style:
        # HSV color space augmentation (from KNN)
        if random.random() > 0.3:
            hsv = cv2.cvtColor(augmented, cv2.COLOR_RGB2HSV).astype(np.float32)
            
            if random.random() > 0.5:
                hue_shift = random.uniform(-20, 20)
                hsv[:,:,0] = (hsv[:,:,0] + hue_shift) % 180
            
            if random.random() > 0.4:
                sat_factor = random.uniform(0.6, 1.4)
                hsv[:,:,1] = np.clip(hsv[:,:,1] * sat_factor, 0, 255)
            
            if random.random() > 0.4:
                val_factor = random.uniform(0.7, 1.3)
                hsv[:,:,2] = np.clip(hsv[:,:,2] * val_factor, 0, 255)
                
            augmented = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
    
    # RGB shifting
    if random.random() > 0.5:
        for i in range(3):
            if random.random() > 0.5:
                shift = random.uniform(-20, 20)
                augmented[:,:,i] = np.clip(augmented[:,:,i].astype(float) + shift, 0, 255).astype(np.uint8)
    
    # Brightness and contrast changes
    if random.random() > 0.5:
        alpha = random.uniform(0.8, 1.2)  # Contrast
        beta = random.uniform(-20, 20)    # Brightness
        augmented = np.clip(alpha * augmented + beta, 0, 255).astype(np.uint8)
    
    # Rotation
    if random.random() > 0.5:
        angle = random.uniform(-30, 30) if use_knn_style else random.uniform(-20, 20)
        h, w = augmented.shape[:2]
        M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
        augmented = cv2.warpAffine(augmented, M, (w, h))
    
    # Flip
    if random.random() > 0.5:
        flip_mode = random.choice([-1, 0, 1])
        augmented = cv2.flip(augmented, flip_mode)
    
    # Crop and resize
    if random.random() > 0.5:
        h, w = augmented.shape[:2]
        crop_factor = random.uniform(0.75, 0.95) if use_knn_style else random.uniform(0.8, 0.95)
        crop_h = int(h * crop_factor)
        crop_w = int(w * crop_factor)
        
        top = random.randint(0, h - crop_h)
        left = random.randint(0, w - crop_w)
        
        cropped = augmented[top:top+crop_h, left:left+crop_w]
        augmented = cv2.resize(cropped, (w, h))
    
    # Noise addition
    if use_knn_style and random.random() > 0.7:
        noise = np.random.normal(0, random.uniform(1, 10), augmented.shape).astype(np.int16)
        augmented = np.clip(augmented.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return augmented


def augment_dataset(X, y, augment_factor=3, use_knn_style=True):
    """
    Create augmented dataset with multiple variations per sample
    
    Args:
        X (ndarray): Input images
        y (ndarray): Labels
        augment_factor (int): Number of augmentations per input image
        use_knn_style (bool): Whether to use KNN-style augmentation
        
    Returns:
        tuple: (augmented_images, augmented_labels)
    """
    n_samples = len(X)
    X_augmented = [X]
    y_augmented = [y]
    
    print(f"Augmenting dataset with factor {augment_factor}...")
    
    # Create a partial function with the use_knn_style parameter
    from functools import partial
    augment_func = partial(augment_image, use_knn_style=use_knn_style)
    
    for i in range(augment_factor):
        X_aug = []
        print(f"Creating augmentation set {i+1}/{augment_factor}")
        
        for j in tqdm(range(n_samples), desc=f"Augmentation batch {i+1}"):
            aug_img = augment_func(X[j])
            X_aug.append(aug_img)
        
        X_augmented.append(np.array(X_aug))
        y_augmented.append(y.copy())
    
    X_combined = np.vstack(X_augmented)
    y_combined = np.hstack(y_augmented)
    
    print(f"Dataset size: {len(X)} → {len(X_combined)} samples")
    return X_combined, y_combined


def check_for_augmented_data(filename):
    """
    Check if augmented data exists
    
    Args:
        filename (str): Path to the augmented data file
        
    Returns:
        dict or None: Loaded data or None if not found/error
    """
    if filename is not None and os.path.exists(filename):
        print(f"Loading existing augmented data from {filename}")
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading augmented data: {e}")
    return None


def save_augmented_data(data, filename):
    """
    Save augmented data
    
    Args:
        data (dict): Dictionary containing augmented data
        filename (str): Path to save the data. If None, data won't be saved.
    """
    if filename is None:
        return
        
    # Create parent directory if it doesn't exist
    parent_dir = os.path.dirname(filename)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    
    print(f"Saving augmented data to {filename}")
    try:
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
    except Exception as e:
        print(f"Error saving augmented data: {e}")


def save_error_analysis(X, y_true, y_pred, class_names, filename=None, subset_name="test", model_name="model"):
    """
    Save error analysis, including misclassified images and statistics
    
    Args:
        X (ndarray): Original images
        y_true (ndarray): True labels
        y_pred (ndarray): Predicted labels
        class_names (list): List of class names
        filename (str, optional): Directory path to save analysis. If None, won't save files.
        subset_name (str): Name of the dataset subset (train, valid, test)
        model_name (str): Name of the model for reporting
    """
    # If no filename is provided, create a timestamped directory name but don't save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    error_dir = None
    
    if filename is not None:
        error_dir = os.path.join(filename, f"error_analysis_{model_name}_{subset_name}_{timestamp}")
        os.makedirs(error_dir, exist_ok=True)
    
    errors = (y_true != y_pred)
    error_indices = np.where(errors)[0]
    
    if len(error_indices) == 0:
        print(f"No errors found in {subset_name} set!")
        return
    
    print(f"Found {len(error_indices)} misclassified {subset_name} images")
    if error_dir:
        print(f"Saving to {error_dir}")
    
    # Error statistics
    n_classes = len(class_names)
    error_counts = {i: 0 for i in range(n_classes)}
    class_counts = {i: np.sum(y_true == i) for i in range(n_classes)}
    
    # Create confusion matrix
    error_matrix = np.zeros((n_classes, n_classes), dtype=int)
    
    # Create directories for error types if saving files
    if error_dir:
        for c_true in range(n_classes):
            for c_pred in range(n_classes):
                if c_true != c_pred:
                    true_name = class_names[c_true]
                    pred_name = class_names[c_pred]
                    os.makedirs(os.path.join(error_dir, f"{true_name}_as_{pred_name}"), exist_ok=True)
    
    # Process each error
    for idx in error_indices:
        true_label = y_true[idx]
        pred_label = y_pred[idx]
        
        error_counts[true_label] += 1
        error_matrix[true_label, pred_label] += 1
        
        # Save error images if a directory is provided
        if error_dir:
            img = X[idx].copy()
            img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            
            true_class_name = class_names[true_label]
            pred_class_name = class_names[pred_label]
            
            h, w = img.shape[:2]
            label_h = max(60, int(h * 0.15))
            label_img = np.zeros((h + label_h, w, 3), dtype=np.uint8)
            label_img[0:h, 0:w] = img_bgr
            
            font_scale = 0.5
            thickness = 1
            cv2.putText(label_img, f"True: {true_class_name}", (10, h + 20),
                      cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), thickness)
            cv2.putText(label_img, f"Pred: {pred_class_name}", (10, h + 40),
                      cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), thickness)
            
            img_path = os.path.join(
                error_dir,
                f"{true_class_name}_as_{pred_class_name}",
                f"error_{idx}.jpg"
            )
            try:
                cv2.imwrite(img_path, label_img)
            except Exception as e:
                print(f"Error saving image {img_path}: {e}")
    
    # Save error summary
    if error_dir:
        try:
            with open(os.path.join(error_dir, "error_summary.txt"), "w") as f:
                f.write(f"Error Analysis for {subset_name} set ({model_name.upper()})\n")
                f.write(f"Total samples: {len(y_true)}\n")
                f.write(f"Total errors: {len(error_indices)} ({len(error_indices)/len(y_true)*100:.2f}%)\n\n")
                
                f.write("Errors by class:\n")
                for i, class_name in enumerate(class_names):
                    count = class_counts.get(i, 0)
                    error_rate = (error_counts.get(i, 0) / count * 100) if count > 0 else 0
                    f.write(f"{class_name}: {error_counts.get(i, 0)}/{count} ({error_rate:.2f}%)\n")
                
                f.write("\nMost common misclassifications:\n")
                error_pairs = []
                for true_idx in range(n_classes):
                    for pred_idx in range(n_classes):
                        if true_idx != pred_idx and error_matrix[true_idx, pred_idx] > 0:
                            error_pairs.append((true_idx, pred_idx, error_matrix[true_idx, pred_idx]))
                
                error_pairs.sort(key=lambda x: x[2], reverse=True)
                for true_idx, pred_idx, count in error_pairs[:10]:
                    true_name = class_names[true_idx]
                    pred_name = class_names[pred_idx]
                    f.write(f"{true_name} misclassified as {pred_name}: {count} instances\n")
        except Exception as e:
            print(f"Error writing summary file: {e}")
    
    # Create visualizations
    try:
        # Create error rate bar chart
        plt.figure(figsize=(12, 8))
        error_rates = []
        
        for i, class_name in enumerate(class_names):
            count = class_counts.get(i, 0)
            error_rate = (error_counts.get(i, 0) / count * 100) if count > 0 else 0
            error_rates.append(error_rate)
        
        plt.bar(class_names, error_rates)
        plt.title(f'Error Rates by Class - {subset_name} set ({model_name.upper()})')
        plt.ylabel('Error Rate (%)')
        plt.xlabel('Class')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if error_dir:
            plt.savefig(os.path.join(error_dir, "error_rates_by_class.png"))
        plt.close()
        
        # Create confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        fig, ax = plt.subplots(figsize=(12, 10))
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
        disp.plot(ax=ax, xticks_rotation=45)
        plt.title(f"Confusion Matrix - {subset_name} set ({model_name.upper()})")
        plt.tight_layout()
        
        if error_dir:
            plt.savefig(os.path.join(error_dir, "confusion_matrix.png"))
        plt.close()
    except Exception as e:
        print(f"Error creating visualization: {e}")
    
    if error_dir:
        print(f"Error analysis saved to {error_dir}")
    
    # Return error statistics for use without saving
    return {
        "total_samples": len(y_true),
        "error_count": len(error_indices),
        "error_rate": len(error_indices)/len(y_true)*100,
        "error_by_class": {class_names[i]: error_counts.get(i, 0) for i in range(n_classes)},
        "class_counts": {class_names[i]: class_counts.get(i, 0) for i in range(n_classes)}
    } 