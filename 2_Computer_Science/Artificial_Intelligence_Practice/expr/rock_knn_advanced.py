import os
import numpy as np
import cv2
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from skimage.feature import local_binary_pattern, graycomatrix, graycoprops
from skimage.color import rgb2gray

# Define data paths with relative paths
BASE_DIR = './AugmentedRockData'
TRAIN_DIR = os.path.join(BASE_DIR, 'train')
VALID_DIR = os.path.join(BASE_DIR, 'valid')
TEST_DIR = os.path.join(BASE_DIR, 'test')

# Create output directory if it doesn't exist
OUTPUT_DIR = './output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get all rock classes
rock_classes = sorted(os.listdir(TRAIN_DIR))
print(f"Rock types: {rock_classes}")
print(f"Total classes: {len(rock_classes)}")

# Define image size
IMAGE_SIZE = (150, 150)  # Image resize dimensions

def extract_advanced_features(image):
    """
    Extract multiple features from an image:
    1. Color histogram features
    2. LBP texture features
    3. GLCM texture features
    4. Shape features
    """
    features = []
    
    # Ensure image is valid
    if image is None or image.size == 0:
        return None
    
    # Resize image
    image_resized = cv2.resize(image, IMAGE_SIZE)
    
    # ---- 1. Color features ----
    # Calculate histograms in different color spaces
    color_spaces = [
        ('RGB', image_resized),
        ('HSV', cv2.cvtColor(image_resized, cv2.COLOR_BGR2HSV)),
        ('LAB', cv2.cvtColor(image_resized, cv2.COLOR_BGR2LAB))
    ]
    
    for name, color_space in color_spaces:
        for i in range(3):
            hist = cv2.calcHist([color_space], [i], None, [32], [0, 256])
            features.extend(hist.flatten())
    
    # ---- 2. LBP texture features ----
    # Convert to grayscale
    gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
    
    # Calculate LBP
    radius = 3
    n_points = 8 * radius
    lbp = local_binary_pattern(gray, n_points, radius, method='uniform')
    
    # Calculate LBP histogram
    lbp_hist, _ = np.histogram(lbp.ravel(), bins=n_points + 2, range=(0, n_points + 2))
    lbp_hist = lbp_hist.astype("float")
    lbp_hist /= (lbp_hist.sum() + 1e-6)  # Normalize
    features.extend(lbp_hist)
    
    # ---- 3. GLCM texture features ----
    # GLCM requires uint8 type image
    gray_uint8 = (gray * 255).astype(np.uint8)
    
    # Calculate GLCM matrix (Gray Level Co-occurrence Matrix)
    distances = [1, 3]  # Distance values
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]  # Angle values
    
    # Quantize gray levels to reduce computation
    gray_uint8 = (gray_uint8 // 32).astype(np.uint8)
    
    # Calculate GLCM
    glcm = graycomatrix(gray_uint8, distances, angles, levels=8, symmetric=True, normed=True)
    
    # Extract GLCM properties
    glcm_props = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation']
    for prop in glcm_props:
        features.extend(graycoprops(glcm, prop).flatten())
    
    # ---- 4. Shape features (edges and contours) ----
    # Use Canny edge detection
    edges = cv2.Canny(gray_uint8, 100, 200)
    edge_count = np.sum(edges > 0)
    edge_ratio = edge_count / (IMAGE_SIZE[0] * IMAGE_SIZE[1])
    features.append(edge_ratio)
    
    # Calculate image gradient histogram
    sobelx = cv2.Sobel(gray_uint8, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray_uint8, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
    gradient_hist, _ = np.histogram(gradient_magnitude, bins=8)
    gradient_hist = gradient_hist / np.sum(gradient_hist)
    features.extend(gradient_hist)
    
    return np.array(features)

def load_data(data_dir):
    """Load data and extract features"""
    X = []  # Features
    y = []  # Labels
    
    print(f"Loading {os.path.basename(data_dir)} data...")
    
    for class_idx, class_name in enumerate(rock_classes):
        class_dir = os.path.join(data_dir, class_name)
        if not os.path.isdir(class_dir):
            continue
        
        # Get image files
        files = [f for f in os.listdir(class_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"  {class_name}: {len(files)} images")
        
        for image_file in tqdm(files, desc=f"Processing {class_name}", leave=False):
            image_path = os.path.join(class_dir, image_file)
            
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                print(f"Could not read image: {image_path}")
                continue
            
            # Extract advanced features
            features = extract_advanced_features(image)
            if features is None:
                continue
                
            # Add to dataset
            X.append(features)
            y.append(class_idx)
    
    return np.array(X), np.array(y)

# Load training, validation and test data
print("Starting data loading and processing...")
X_train, y_train = load_data(TRAIN_DIR)
X_valid, y_valid = load_data(VALID_DIR)
X_test, y_test = load_data(TEST_DIR)

print(f"\nData loading completed:")
print(f"Training set: {X_train.shape[0]} images, Feature dimension: {X_train.shape[1]}")
print(f"Validation set: {X_valid.shape[0]} images")
print(f"Test set: {X_test.shape[0]} images")

# Feature standardization
print("\nStandardizing features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_valid_scaled = scaler.transform(X_valid)
X_test_scaled = scaler.transform(X_test)

# Use grid search to find best KNN parameters
print("\nUsing grid search to find optimal KNN parameters...")
param_grid = {
    'n_neighbors': [3, 5, 7, 9, 11, 13],
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan', 'minkowski']
}

knn = KNeighborsClassifier()
grid_search = GridSearchCV(knn, param_grid, cv=3, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train_scaled, y_train)

# Output best parameters
print("\nBest KNN parameters:")
print(grid_search.best_params_)
print(f"Validation best accuracy: {grid_search.best_score_:.4f}")

# Save grid search results
with open(os.path.join(OUTPUT_DIR, 'grid_search_results.txt'), 'w') as f:
    f.write(f"Best parameters: {grid_search.best_params_}\n")
    f.write(f"Best validation accuracy: {grid_search.best_score_:.4f}\n\n")
    f.write("All results:\n")
    for i, params in enumerate(grid_search.cv_results_['params']):
        f.write(f"{params}: {grid_search.cv_results_['mean_test_score'][i]:.4f}\n")

# Evaluate best model on test set
best_knn = grid_search.best_estimator_
y_pred = best_knn.predict(X_test_scaled)
test_accuracy = accuracy_score(y_test, y_pred)
print(f"\nTest set accuracy = {test_accuracy:.4f}")

# Output detailed classification report
print("\nClassification Report:")
class_report = classification_report(y_test, y_pred, target_names=rock_classes)
print(class_report)

# Save classification report
with open(os.path.join(OUTPUT_DIR, 'classification_report_advanced.txt'), 'w') as f:
    f.write(f"Test accuracy: {test_accuracy:.4f}\n\n")
    f.write(class_report)

# Plot confusion matrix
plt.figure(figsize=(12, 10))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=rock_classes, yticklabels=rock_classes)
plt.xlabel('Predicted label')
plt.ylabel('True label')
plt.title('Confusion Matrix')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'confusion_matrix_advanced.png'))
plt.close()

# Plot per-class accuracy
class_accuracy = np.diag(cm) / np.sum(cm, axis=1)
plt.figure(figsize=(12, 6))
plt.bar(rock_classes, class_accuracy)
plt.xlabel('Rock class')
plt.ylabel('Accuracy')
plt.title('Classification Accuracy by Class')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'class_accuracy.png'))
plt.close()

# Visualize some predictions
def visualize_predictions():
    """Visualize some prediction results"""
    plt.figure(figsize=(15, 10))
    correct_count = 0
    incorrect_count = 0
    row_idx = 0
    
    for class_name in rock_classes:
        if row_idx >= 3:  # Only show first 3 rows
            break
            
        class_dir = os.path.join(TEST_DIR, class_name)
        if not os.path.isdir(class_dir):
            continue
            
        image_files = [f for f in os.listdir(class_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if not image_files:
            continue
            
        for i in range(3):  # Show 3 images per class
            if i >= len(image_files):
                break
                
            # Randomly select an image
            image_path = os.path.join(class_dir, image_files[i])
            image = cv2.imread(image_path)
            if image is None:
                continue
                
            # Extract features and predict
            features = extract_advanced_features(image)
            if features is None:
                continue
                
            # Standardize features
            features_scaled = scaler.transform([features])
            pred_idx = best_knn.predict(features_scaled)[0]
            pred_class = rock_classes[pred_idx]
            true_class = class_name
            
            # Check if prediction is correct
            is_correct = pred_class == true_class
            if is_correct:
                correct_count += 1
            else:
                incorrect_count += 1
                
            # Convert color channels from BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Show image and prediction result
            col_idx = i % 3
            plt.subplot(3, 3, row_idx * 3 + col_idx + 1)
            plt.imshow(image)
            title = f"True: {true_class}\nPred: {pred_class}"
            if is_correct:
                plt.title(title, color='green')
            else:
                plt.title(title, color='red')
            plt.axis('off')
        
        row_idx += 1
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'prediction_examples.png'))
    plt.close()
    print(f"Correct predictions: {correct_count}, Incorrect predictions: {incorrect_count}")

# Visualize prediction results
visualize_predictions()

# Save model and feature scaler
import joblib
joblib.dump(best_knn, os.path.join(OUTPUT_DIR, 'rock_knn_advanced_model.pkl'))
joblib.dump(scaler, os.path.join(OUTPUT_DIR, 'rock_knn_scaler.pkl'))
print("\nModel and scaler saved")

# Output conclusions
print("\nExperiment conclusions:")
print(f"1. Rock classification using KNN algorithm with best test accuracy: {test_accuracy:.4f}")
print(f"2. Best KNN parameters: {grid_search.best_params_}")
print("3. Feature extraction methods include: color histograms, LBP texture features, GLCM texture features, and shape features")

# If accuracy is not ideal, provide suggestions
if test_accuracy < 0.6:
    print("\nSuggestions to improve accuracy:")
    print("1. Add more training data or use data augmentation techniques")
    print("2. Try more complex feature extraction methods, such as deep learning features")
    print("3. Try other machine learning algorithms, such as SVM, Random Forest, etc.")
    print("4. Perform feature selection to reduce feature dimensionality and remove irrelevant features")

print(f"\nAll output files saved to '{OUTPUT_DIR}' directory.") 