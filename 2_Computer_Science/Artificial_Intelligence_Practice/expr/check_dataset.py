import os
import cv2
import argparse
import time
from tqdm import tqdm

def check_image(img_path):
    """检查图像是否可以被OpenCV正确读取"""
    try:
        img = cv2.imread(img_path)
        if img is None:
            return False, "图像无法读取（可能是格式问题或数据损坏）"
        
        if img.size == 0:
            return False, "图像为空（零大小）"
            
        # 检查图像是否为彩色图像
        if len(img.shape) < 3 or img.shape[2] != 3:
            return False, f"图像不是3通道彩色图像: {img.shape}"
            
        # 成功读取
        return True, f"图像尺寸: {img.shape[1]}x{img.shape[0]}, 通道: {img.shape[2]}"
    except Exception as e:
        return False, f"处理图像时出错: {str(e)}"

def check_dataset(data_dir, verbose=True):
    """检查数据集目录中的所有图像"""
    if not os.path.exists(data_dir):
        print(f"错误: 数据集目录不存在: {data_dir}")
        return False
        
    # 获取类别目录
    class_dirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    if not class_dirs:
        print(f"错误: 在 {data_dir} 中未找到类别子目录")
        return False
        
    print(f"发现 {len(class_dirs)} 个类别子目录:")
    
    total_images = 0
    valid_images = 0
    errors = []
    
    # 检查每个类别目录
    for class_name in class_dirs:
        class_dir = os.path.join(data_dir, class_name)
        
        # 获取所有图像文件
        image_files = [f for f in os.listdir(class_dir) 
                       if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        
        class_valid = 0
        class_errors = []
        
        print(f"\n检查类别 '{class_name}': 找到 {len(image_files)} 个图像文件")
        
        # 检查每个图像
        for img_file in tqdm(image_files, desc=f"检查 {class_name} 图像", disable=not verbose):
            img_path = os.path.join(class_dir, img_file)
            total_images += 1
            
            is_valid, message = check_image(img_path)
            if is_valid:
                valid_images += 1
                class_valid += 1
            else:
                errors.append((img_path, message))
                class_errors.append((img_file, message))
                
        # 显示类别状态
        print(f"  - 有效图像: {class_valid}/{len(image_files)} ({(class_valid/max(1,len(image_files)))*100:.1f}%)")
        
        if class_errors and verbose:
            print(f"  - 错误图像:")
            for img_file, err_msg in class_errors[:10]:  # 只显示前10个错误
                print(f"    * {img_file}: {err_msg}")
            
            if len(class_errors) > 10:
                print(f"    * ... 还有 {len(class_errors)-10} 个错误 (省略)")
    
    # 显示总体状态
    print("\n=== 数据集检查摘要 ===")
    print(f"总图像数: {total_images}")
    print(f"有效图像数: {valid_images} ({(valid_images/max(1,total_images))*100:.1f}%)")
    print(f"无效图像数: {total_images - valid_images}")
    
    # 如果有很多错误，显示前面的一些作为示例
    if errors and verbose:
        print("\n错误示例:")
        for i, (img_path, msg) in enumerate(errors[:20]):
            print(f"{i+1}. {img_path}: {msg}")
        
        if len(errors) > 20:
            print(f"... 还有 {len(errors)-20} 个错误 (省略)")
    
    return valid_images > 0

def main():
    parser = argparse.ArgumentParser(description='检查数据集中的图像是否有效')
    parser.add_argument('--data-dir', type=str, default='./RockData',
                       help='数据集根目录')
    parser.add_argument('--verbose', action='store_true',
                       help='显示详细信息')
    args = parser.parse_args()
    
    print(f"检查数据集: {args.data_dir}")
    
    # 检查训练集、验证集和测试集（如果存在）
    for subset in ['train', 'valid', 'test']:
        subset_dir = os.path.join(args.data_dir, subset)
        if os.path.exists(subset_dir):
            print(f"\n===== 检查{subset}集 =====")
            check_dataset(subset_dir, args.verbose)
        else:
            print(f"\n警告: {subset}集目录不存在: {subset_dir}")
    
    print("\n检查完成!")

if __name__ == "__main__":
    main() 