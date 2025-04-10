import os
import numpy as np
import cv2
from tqdm import tqdm
import random
import shutil
from pathlib import Path
import argparse
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

"""
Data Augmentation for Rock Image Classification

This script performs various augmentation techniques on the rock images to increase
the dataset size, helping to improve model generalization.

Augmentation techniques include:
1. Rotation
2. Flip (horizontal and vertical)
3. Color adjustments (brightness, contrast, saturation)
4. Blur/Sharpen
5. Random cropping and resizing
6. Adding noise
"""

# Define augmentation parameters
AUGMENTATION_PARAMS = {
    'rotations': [90, 180, 270],            # Rotation angles
    'flip': True,                           # Apply flipping
    'brightness_range': (0.8, 1.2),         # Brightness adjustment range
    'contrast_range': (0.8, 1.2),           # Contrast adjustment range
    'saturation_range': (0.8, 1.2),         # Saturation adjustment range
    'apply_blur': True,                     # Apply Gaussian blur
    'add_noise': True,                      # Add random noise
    'random_crop_factor': 0.8,              # Crop randomly to 80% of original size
    'augmentations_per_image': 5            # Number of augmentations per original image
}

def create_directory_structure(base_input_dir, base_output_dir):
    """Create the directory structure for augmented images"""
    if os.path.exists(base_output_dir):
        print(f"Warning: Output directory {base_output_dir} already exists. Augmented images will be added.")
    
    # Create output directory
    os.makedirs(base_output_dir, exist_ok=True)
    
    # Create train, valid, test directories
    for split in ['train', 'valid', 'test']:
        split_dir = os.path.join(base_output_dir, split)
        os.makedirs(split_dir, exist_ok=True)
        
        # Create class subdirectories
        input_split_dir = os.path.join(base_input_dir, split)
        if os.path.exists(input_split_dir):
            class_dirs = [d for d in os.listdir(input_split_dir) 
                          if os.path.isdir(os.path.join(input_split_dir, d))]
            for class_dir in class_dirs:
                os.makedirs(os.path.join(split_dir, class_dir), exist_ok=True)

def rotate_image(image, angle):
    """Rotate image by specified angle"""
    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (width, height), 
                         borderMode=cv2.BORDER_REFLECT)

def apply_flip(image, direction):
    """Flip image horizontally or vertically"""
    if direction == 'horizontal':
        return cv2.flip(image, 1)
    elif direction == 'vertical':
        return cv2.flip(image, 0)
    else:
        return image

def adjust_brightness(image, factor):
    """Adjust image brightness"""
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Brightness(pil_img)
    pil_img = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def adjust_contrast(image, factor):
    """Adjust image contrast"""
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Contrast(pil_img)
    pil_img = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def adjust_saturation(image, factor):
    """Adjust image saturation"""
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Color(pil_img)
    pil_img = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def apply_blur(image, kernel_size=5):
    """Apply Gaussian blur to image"""
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def apply_sharpen(image):
    """Apply sharpening to image"""
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    pil_img = pil_img.filter(ImageFilter.SHARPEN)
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def add_gaussian_noise(image, mean=0, std=15):
    """Add Gaussian noise to image"""
    gauss_noise = np.random.normal(mean, std, image.shape).astype(np.uint8)
    noisy_img = cv2.add(image, gauss_noise)
    return noisy_img

def random_crop_and_resize(image, crop_factor):
    """Randomly crop and resize back to original dimensions"""
    height, width = image.shape[:2]
    
    # Calculate crop dimensions
    crop_height = int(height * crop_factor)
    crop_width = int(width * crop_factor)
    
    # Calculate random crop position
    top = random.randint(0, height - crop_height)
    left = random.randint(0, width - crop_width)
    
    # Crop image
    cropped = image[top:top+crop_height, left:left+crop_width]
    
    # Resize back to original dimensions
    return cv2.resize(cropped, (width, height), interpolation=cv2.INTER_CUBIC)

def generate_augmented_image(image, aug_id):
    """Generate an augmented image using various techniques"""
    augmented = image.copy()
    
    # Apply random rotation
    if random.random() > 0.5 and AUGMENTATION_PARAMS['rotations']:
        angle = random.choice(AUGMENTATION_PARAMS['rotations'])
        augmented = rotate_image(augmented, angle)
    
    # Apply random flip
    if random.random() > 0.5 and AUGMENTATION_PARAMS['flip']:
        direction = random.choice(['horizontal', 'vertical'])
        augmented = apply_flip(augmented, direction)
    
    # Apply random brightness adjustment
    if random.random() > 0.5:
        brightness_factor = random.uniform(*AUGMENTATION_PARAMS['brightness_range'])
        augmented = adjust_brightness(augmented, brightness_factor)
    
    # Apply random contrast adjustment
    if random.random() > 0.5:
        contrast_factor = random.uniform(*AUGMENTATION_PARAMS['contrast_range'])
        augmented = adjust_contrast(augmented, contrast_factor)
    
    # Apply random saturation adjustment
    if random.random() > 0.5:
        saturation_factor = random.uniform(*AUGMENTATION_PARAMS['saturation_range'])
        augmented = adjust_saturation(augmented, saturation_factor)
    
    # Apply blur
    if random.random() > 0.7 and AUGMENTATION_PARAMS['apply_blur']:
        kernel_size = random.choice([3, 5, 7])
        augmented = apply_blur(augmented, kernel_size)
    
    # Apply sharpen
    if random.random() > 0.7:
        augmented = apply_sharpen(augmented)
    
    # Add noise
    if random.random() > 0.7 and AUGMENTATION_PARAMS['add_noise']:
        std = random.uniform(5, 20)
        augmented = add_gaussian_noise(augmented, std=std)
    
    # Random crop and resize
    if random.random() > 0.5:
        crop_factor = random.uniform(AUGMENTATION_PARAMS['random_crop_factor'], 0.95)
        augmented = random_crop_and_resize(augmented, crop_factor)
    
    return augmented

def augment_dataset(base_input_dir, base_output_dir):
    """Augment the dataset and save to output directory"""
    # Copy original dataset to output directory
    print("First copying the original dataset...")
    for split in ['train', 'valid', 'test']:
        input_split_dir = os.path.join(base_input_dir, split)
        output_split_dir = os.path.join(base_output_dir, split)
        
        if not os.path.exists(input_split_dir):
            print(f"Warning: {input_split_dir} does not exist. Skipping.")
            continue
        
        # Process each class directory
        class_dirs = [d for d in os.listdir(input_split_dir) 
                     if os.path.isdir(os.path.join(input_split_dir, d))]
        
        for class_dir in class_dirs:
            input_class_dir = os.path.join(input_split_dir, class_dir)
            output_class_dir = os.path.join(output_split_dir, class_dir)
            
            # Get all image files
            image_files = [f for f in os.listdir(input_class_dir)
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            print(f"Processing {split}/{class_dir}: {len(image_files)} original images")
            
            # Copy original images
            for img_file in image_files:
                src_path = os.path.join(input_class_dir, img_file)
                dst_path = os.path.join(output_class_dir, img_file)
                shutil.copy2(src_path, dst_path)
            
            # Only augment training images
            if split == 'train':
                # Augment each image multiple times
                for img_file in tqdm(image_files, desc=f"Augmenting {class_dir}"):
                    input_img_path = os.path.join(input_class_dir, img_file)
                    
                    # Read image
                    image = cv2.imread(input_img_path)
                    if image is None:
                        print(f"Warning: Could not read {input_img_path}. Skipping.")
                        continue
                    
                    # Generate multiple augmented versions
                    for aug_idx in range(AUGMENTATION_PARAMS['augmentations_per_image']):
                        augmented = generate_augmented_image(image, aug_idx)
                        
                        # Save augmented image
                        file_name, file_ext = os.path.splitext(img_file)
                        aug_file_name = f"{file_name}_aug_{aug_idx}{file_ext}"
                        output_img_path = os.path.join(output_class_dir, aug_file_name)
                        cv2.imwrite(output_img_path, augmented)

def print_dataset_stats(base_dir):
    """Print statistics about the dataset"""
    for split in ['train', 'valid', 'test']:
        split_dir = os.path.join(base_dir, split)
        if not os.path.exists(split_dir):
            continue
        
        total_images = 0
        print(f"\n{split.capitalize()} set statistics:")
        
        class_dirs = [d for d in os.listdir(split_dir) 
                     if os.path.isdir(os.path.join(split_dir, d))]
        
        for class_dir in sorted(class_dirs):
            class_path = os.path.join(split_dir, class_dir)
            image_files = [f for f in os.listdir(class_path)
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            print(f"  - {class_dir}: {len(image_files)} images")
            total_images += len(image_files)
        
        print(f"  Total {split} images: {total_images}")

def main():
    parser = argparse.ArgumentParser(description="Augment rock image dataset")
    parser.add_argument("--input", default="./RockData", help="Input dataset directory")
    parser.add_argument("--output", default="./AugmentedRockData", help="Output directory for augmented dataset")
    args = parser.parse_args()
    
    print(f"Input directory: {args.input}")
    print(f"Output directory: {args.output}")
    
    # Create output directory structure
    create_directory_structure(args.input, args.output)
    
    # Augment dataset
    augment_dataset(args.input, args.output)
    
    # Print statistics for the augmented dataset
    print("\nAugmented dataset statistics:")
    print_dataset_stats(args.output)
    
    print("\nData augmentation completed!")

if __name__ == "__main__":
    main() 