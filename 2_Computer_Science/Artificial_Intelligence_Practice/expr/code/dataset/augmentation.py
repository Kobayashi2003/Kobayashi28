# Standard library imports
import os
import random
import shutil
from pathlib import Path

# Third-party imports - data analysis and scientific computing
import numpy as np

# Third-party imports - image processing
import cv2
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

# Third-party imports - utilities
from tqdm import tqdm

class DataAugmenter:
    """Class for data augmentation on rock images"""
    
    def __init__(self, output_dir=None):
        """
        Initialize data augmenter
        
        Parameters:
        -----------
        output_dir : str or None
            Output directory for augmented data. If None, will be created automatically
        """
        self.output_dir = output_dir
        
        # Define default augmentation parameters
        self.params = {
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
    
    def set_params(self, **kwargs):
        """
        Set augmentation parameters
        
        Parameters:
        -----------
        **kwargs : dict
            Parameter key-value pairs to update
        """
        for key, value in kwargs.items():
            if key in self.params:
                self.params[key] = value
            else:
                print(f"Warning: Unknown parameter '{key}'")
        
        return self
    
    def create_directory_structure(self, base_input_dir):
        """
        Create the directory structure for augmented images
        
        Parameters:
        -----------
        base_input_dir : str
            Input directory containing the original dataset
        """
        # If output_dir is not provided, create a sibling directory to the input
        if self.output_dir is None:
            # Get the parent directory of the input
            input_parent = os.path.dirname(os.path.abspath(base_input_dir))
            # Get the basename of the input directory
            input_basename = os.path.basename(os.path.abspath(base_input_dir))
            # Create augmented directory name
            self.output_dir = os.path.join(input_parent, f"Augmented_{input_basename}")
        
        if os.path.exists(self.output_dir):
            print(f"Warning: Output directory {self.output_dir} already exists. Augmented images will be added.")
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create train, valid, test directories
        for split in ['train', 'valid', 'test']:
            split_dir = os.path.join(self.output_dir, split)
            os.makedirs(split_dir, exist_ok=True)
            
            # Create class subdirectories
            input_split_dir = os.path.join(base_input_dir, split)
            if os.path.exists(input_split_dir):
                class_dirs = [d for d in os.listdir(input_split_dir) 
                             if os.path.isdir(os.path.join(input_split_dir, d))]
                for class_dir in class_dirs:
                    os.makedirs(os.path.join(split_dir, class_dir), exist_ok=True)
        
        return self
    
    def _rotate_image(self, image, angle):
        """Rotate image by specified angle"""
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(image, rotation_matrix, (width, height), 
                             borderMode=cv2.BORDER_REFLECT)
    
    def _apply_flip(self, image, direction):
        """Flip image horizontally or vertically"""
        if direction == 'horizontal':
            return cv2.flip(image, 1)
        elif direction == 'vertical':
            return cv2.flip(image, 0)
        else:
            return image
    
    def _adjust_brightness(self, image, factor):
        """Adjust image brightness"""
        pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Brightness(pil_img)
        pil_img = enhancer.enhance(factor)
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    def _adjust_contrast(self, image, factor):
        """Adjust image contrast"""
        pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Contrast(pil_img)
        pil_img = enhancer.enhance(factor)
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    def _adjust_saturation(self, image, factor):
        """Adjust image saturation"""
        pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Color(pil_img)
        pil_img = enhancer.enhance(factor)
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    def _apply_blur(self, image, kernel_size=5):
        """Apply Gaussian blur to image"""
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
    def _apply_sharpen(self, image):
        """Apply sharpening to image"""
        pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        pil_img = pil_img.filter(ImageFilter.SHARPEN)
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    def _add_gaussian_noise(self, image, mean=0, std=15):
        """Add Gaussian noise to image"""
        gauss_noise = np.random.normal(mean, std, image.shape).astype(np.uint8)
        noisy_img = cv2.add(image, gauss_noise)
        return noisy_img
    
    def _random_crop_and_resize(self, image, crop_factor):
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
    
    def _generate_augmented_image(self, image):
        """Generate an augmented image using various techniques"""
        augmented = image.copy()
        
        # Apply random rotation
        if random.random() > 0.5 and self.params['rotations']:
            angle = random.choice(self.params['rotations'])
            augmented = self._rotate_image(augmented, angle)
        
        # Apply random flip
        if random.random() > 0.5 and self.params['flip']:
            direction = random.choice(['horizontal', 'vertical'])
            augmented = self._apply_flip(augmented, direction)
        
        # Apply random brightness adjustment
        if random.random() > 0.5:
            brightness_factor = random.uniform(*self.params['brightness_range'])
            augmented = self._adjust_brightness(augmented, brightness_factor)
        
        # Apply random contrast adjustment
        if random.random() > 0.5:
            contrast_factor = random.uniform(*self.params['contrast_range'])
            augmented = self._adjust_contrast(augmented, contrast_factor)
        
        # Apply random saturation adjustment
        if random.random() > 0.5:
            saturation_factor = random.uniform(*self.params['saturation_range'])
            augmented = self._adjust_saturation(augmented, saturation_factor)
        
        # Apply blur
        if random.random() > 0.7 and self.params['apply_blur']:
            kernel_size = random.choice([3, 5, 7])
            augmented = self._apply_blur(augmented, kernel_size)
        
        # Apply sharpen
        if random.random() > 0.7:
            augmented = self._apply_sharpen(augmented)
        
        # Add noise
        if random.random() > 0.7 and self.params['add_noise']:
            std = random.uniform(5, 20)
            augmented = self._add_gaussian_noise(augmented, std=std)
        
        # Random crop and resize
        if random.random() > 0.5:
            crop_factor = random.uniform(self.params['random_crop_factor'], 0.95)
            augmented = self._random_crop_and_resize(augmented, crop_factor)
        
        return augmented
    
    def augment_dataset(self, base_input_dir):
        """
        Augment the dataset and save to output directory.
        The original images will be preserved in their original location,
        and only augmented versions will be saved to the output directory.
        
        Parameters:
        -----------
        base_input_dir : str
            Input directory containing the original dataset
        """
        # Create output directory structure
        self.create_directory_structure(base_input_dir)
        
        print("Generating augmented dataset...")
        for split in ['train', 'valid', 'test']:
            input_split_dir = os.path.join(base_input_dir, split)
            output_split_dir = os.path.join(self.output_dir, split)
            
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
                        try:
                            # Read the image
                            img_path = os.path.join(input_class_dir, img_file)
                            original_img = cv2.imread(img_path)
                            
                            if original_img is None:
                                print(f"Warning: Could not read {img_path}. Skipping.")
                                continue
                            
                            # Get image name without extension
                            img_name, img_ext = os.path.splitext(img_file)
                            
                            # Generate multiple augmented versions
                            for aug_idx in range(self.params['augmentations_per_image']):
                                # Generate an augmented image
                                augmented_img = self._generate_augmented_image(original_img)
                                
                                # Create output filename
                                output_filename = f"{img_name}_aug_{aug_idx}{img_ext}"
                                output_path = os.path.join(output_class_dir, output_filename)
                                
                                # Save the augmented image
                                cv2.imwrite(output_path, augmented_img)
                                
                        except Exception as e:
                            print(f"Error processing {img_file}: {str(e)}")
        
        # Print dataset statistics
        self._print_dataset_stats()
        print(f"\nAugmented dataset saved to: {self.output_dir}")
        
        return self
    
    def _print_dataset_stats(self):
        """Print statistics about the augmented dataset"""
        print("\nAugmented dataset statistics:")
        for split in ['train', 'valid', 'test']:
            split_dir = os.path.join(self.output_dir, split)
            if not os.path.exists(split_dir):
                continue
            
            total_images = 0
            print(f"\n{split.capitalize()} set:")
            
            class_dirs = [d for d in os.listdir(split_dir) 
                         if os.path.isdir(os.path.join(split_dir, d))]
            
            for class_dir in sorted(class_dirs):
                class_path = os.path.join(split_dir, class_dir)
                image_files = [f for f in os.listdir(class_path)
                              if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                class_count = len(image_files)
                total_images += class_count
                print(f"  {class_dir}: {class_count} images")
            
            print(f"  Total: {total_images} images")
            
            # Count original vs augmented
            if split == 'train':
                original_count = len([f for class_dir in class_dirs 
                                   for f in os.listdir(os.path.join(split_dir, class_dir))
                                   if f.lower().endswith(('.jpg', '.jpeg', '.png')) 
                                   and '_aug_' not in f])
                augmented_count = total_images - original_count
                print(f"  Original: {original_count} images")
                print(f"  Augmented: {augmented_count} images")
                print(f"  Augmentation factor: {total_images / original_count:.2f}x")

def augment_rock_dataset(input_dir, output_dir=None, augmentations_per_image=5):
    """
    Convenience function to augment a rock dataset.
    The original images are preserved in their original locations,
    and only augmented versions are saved to the output directory.
    
    Parameters:
    -----------
    input_dir : str
        Input directory containing the original dataset
    output_dir : str or None
        Output directory for augmented data. If None, a sibling directory to input_dir will be created
    augmentations_per_image : int
        Number of augmented versions to generate per original image
        
    Returns:
    --------
    output_dir : str
        Path to the output directory where augmented dataset was saved
    """
    augmenter = DataAugmenter(output_dir=output_dir)
    augmenter.set_params(augmentations_per_image=augmentations_per_image)
    augmenter.augment_dataset(input_dir)
    
    return augmenter.output_dir

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Augment rock image dataset')
    parser.add_argument('--input-dir', type=str, default='./data/RockData',
                       help='Input directory containing original dataset')
    parser.add_argument('--output-dir', type=str, default=None,
                       help='Output directory for augmented dataset. If not specified, will create a sibling directory to input.')
    parser.add_argument('--augmentations', type=int, default=5,
                       help='Number of augmented versions to generate per original image')
    
    args = parser.parse_args()
    
    output_dir = augment_rock_dataset(args.input_dir, args.output_dir, args.augmentations)
    print(f"Augmented dataset saved to: {output_dir}")
