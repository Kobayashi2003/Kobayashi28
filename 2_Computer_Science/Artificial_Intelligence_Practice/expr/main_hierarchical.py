import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import time

# 导入自定义模块
from data_utils import load_data, standardize_features, extract_basic_features, extract_advanced_features
from hierarchical_classifier import HierarchicalClassifier

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='基于分层分类的岩石图像分类')
    
    # 数据集参数
    parser.add_argument('--data-dir', type=str, default='./RockData',
                       help='数据集目录路径')
    parser.add_argument('--use-augmented', action='store_true',
                       help='使用增强数据集（如果可用）')
    
    # 特征提取参数
    parser.add_argument('--advanced-features', action='store_true',
                       help='使用高级特征提取（纹理、颜色、形状）')
    
    # 分层分类参数
    parser.add_argument('--min-clusters', type=int, default=2,
                       help='每个岩石类型的最小聚类数')
    parser.add_argument('--max-clusters', type=int, default=5,
                       help='每个岩石类型的最大聚类数')
    
    # 输出参数
    parser.add_argument('--output-dir', type=str, default='./output',
                       help='结果输出目录')
    
    return parser.parse_args()

def main():
    # 解析命令行参数
    args = parse_args()
    
    # 设置路径
    if args.use_augmented and os.path.exists('./AugmentedRockData'):
        data_dir = './AugmentedRockData'
        print("使用增强数据集")
    else:
        data_dir = args.data_dir
        print(f"使用数据集: {data_dir}")
    
    train_dir = os.path.join(data_dir, 'train')
    valid_dir = os.path.join(data_dir, 'valid')
    test_dir = os.path.join(data_dir, 'test')
    
    # 创建输出目录
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(args.output_dir, f"hierarchical_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取岩石类别
    rock_classes = sorted([d for d in os.listdir(train_dir) 
                         if os.path.isdir(os.path.join(train_dir, d))])
    print(f"岩石类型: {rock_classes}")
    print(f"总类别数: {len(rock_classes)}")
    
    # 选择特征提取器
    if args.advanced_features:
        feature_extractor = extract_advanced_features
        print("使用高级特征提取")
    else:
        feature_extractor = extract_basic_features
        print("使用基本特征提取")
    
    # 加载并提取特征
    print("\n加载并提取特征...")
    X_train, y_train = load_data(train_dir, rock_classes, feature_extractor)
    X_valid, y_valid = load_data(valid_dir, rock_classes, feature_extractor)
    X_test, y_test = load_data(test_dir, rock_classes, feature_extractor)
    
    print(f"训练集: {X_train.shape[0]} 样本, {X_train.shape[1]} 特征")
    print(f"验证集: {X_valid.shape[0]} 样本")
    print(f"测试集: {X_test.shape[0]} 样本")
    
    # 标准化特征
    print("\n标准化特征...")
    (X_train_scaled, X_valid_scaled, X_test_scaled), scaler = standardize_features(
        X_train, X_valid, X_test)
    
    # 初始化分层分类器
    hierarchical_clf = HierarchicalClassifier(output_dir=output_dir)
    
    # 第一阶段：对每个岩石类型进行聚类
    hierarchical_clf.fit_clusters(
        X_train_scaled, y_train, rock_classes, 
        min_clusters=args.min_clusters, 
        max_clusters=args.max_clusters
    )
    
    # 第二阶段：基于子类标签训练全局分类器
    hierarchical_clf.fit_global_classifier(
        X_train_scaled, y_train, 
        X_valid_scaled, y_valid
    )
    
    # 在测试集上评估模型
    accuracy, y_pred = hierarchical_clf.evaluate(X_test_scaled, y_test, rock_classes)
    
    # 保存模型
    hierarchical_clf.save_model(f'hierarchical_model_{timestamp}.pkl')
    
    # 比较原始类别预测结果和子类预测结果
    print("\n分层分类总结:")
    print(f"岩石类型数量: {len(rock_classes)}")
    
    # 计算子类总数
    total_subclasses = len(hierarchical_clf.subclass_info)
    print(f"子类总数: {total_subclasses}")
    
    # 计算每个岩石类型的平均子类数
    avg_subclasses_per_type = np.mean([count for count in hierarchical_clf.cluster_counts.values()])
    print(f"每种岩石类型的平均子类数: {avg_subclasses_per_type:.2f}")
    
    # 输出每种岩石类型的子类数
    print("\n各岩石类型的子类数:")
    for i, rock_type in enumerate(rock_classes):
        print(f"{rock_type}: {hierarchical_clf.cluster_counts.get(i, 0)} 个子类")
    
    print(f"\n所有结果保存到 {output_dir}")
    print("实验完成!")

if __name__ == "__main__":
    main() 