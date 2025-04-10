import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import seaborn as sns
import time

class HierarchicalClassifier:
    """
    分层分类器：先对每种岩石类型进行内部聚类生成子类标签，然后再进行全局分类
    """
    
    def __init__(self, output_dir='./output/hierarchical'):
        """
        初始化分层分类器
        
        Parameters:
        -----------
        output_dir : str
            输出目录
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # 初始化模型
        self.cluster_models = {}  # 每个岩石类型的聚类模型
        self.global_classifier = None  # 全局分类器
        self.rock_types = None  # 岩石类型列表
        self.cluster_counts = {}  # 每个岩石类型的聚类数
        self.scaler = StandardScaler()  # 特征标准化
        
        # 记录子类信息
        self.subclass_info = {}  # 子类与原始类的映射
        self.subclass_mapping = {}  # 子类标签映射
        self.inverse_mapping = {}  # 从子类标签到原始岩石类型的映射
        
    def fit_clusters(self, X_train, y_train, rock_types, min_clusters=2, max_clusters=5):
        """
        对每种岩石类型进行聚类，生成子类标签
        
        Parameters:
        -----------
        X_train : array-like
            训练特征
        y_train : array-like
            训练标签
        rock_types : list
            岩石类型列表
        min_clusters : int
            每个岩石类型的最小聚类数
        max_clusters : int
            每个岩石类型的最大聚类数
        """
        self.rock_types = rock_types
        print("\n对各岩石类型进行内部聚类...")
        
        # 标准化特征
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # 为每种岩石类型训练聚类模型
        next_subclass_label = 0
        for i, rock_type in enumerate(rock_types):
            # 获取当前岩石类型的样本
            mask = (y_train == i)
            if np.sum(mask) < max_clusters:
                print(f"警告: 岩石类型 '{rock_type}' 的样本数量 ({np.sum(mask)}) 小于最大聚类数 ({max_clusters})，设置最大聚类数为样本数")
                max_clusters_for_type = max(min_clusters, np.sum(mask))
            else:
                max_clusters_for_type = max_clusters
                
            X_type = X_train_scaled[mask]
            
            if len(X_type) <= 1:
                print(f"岩石类型 '{rock_type}' 的样本数量不足，跳过聚类")
                self.cluster_models[i] = None
                self.cluster_counts[i] = 1
                
                # 记录子类信息
                self.subclass_info[next_subclass_label] = {
                    'rock_type_idx': i,
                    'rock_type': rock_type,
                    'subclass_idx': 0,
                    'samples': np.sum(mask)
                }
                self.subclass_mapping[i] = {0: next_subclass_label}
                self.inverse_mapping[next_subclass_label] = i
                next_subclass_label += 1
                continue
            
            # 使用轮廓系数寻找最佳聚类数
            best_score = -1
            best_n_clusters = min_clusters
            scores = []
            
            for n_clusters in range(min_clusters, min(max_clusters_for_type + 1, len(X_type))):
                kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                cluster_labels = kmeans.fit_predict(X_type)
                
                # 至少两个样本才能计算轮廓系数
                if len(np.unique(cluster_labels)) > 1:
                    score = silhouette_score(X_type, cluster_labels)
                    scores.append(score)
                    if score > best_score:
                        best_score = score
                        best_n_clusters = n_clusters
                else:
                    scores.append(0)
            
            # 训练最佳聚类模型
            kmeans = KMeans(n_clusters=best_n_clusters, random_state=42, n_init=10)
            kmeans.fit(X_type)
            self.cluster_models[i] = kmeans
            self.cluster_counts[i] = best_n_clusters
            
            print(f"岩石类型 '{rock_type}': 最佳聚类数 = {best_n_clusters}, 轮廓系数 = {best_score:.4f}")
            
            # 记录子类信息
            subclass_mapping = {}
            for subclass_idx in range(best_n_clusters):
                self.subclass_info[next_subclass_label] = {
                    'rock_type_idx': i,
                    'rock_type': rock_type,
                    'subclass_idx': subclass_idx,
                    'samples': np.sum(kmeans.labels_ == subclass_idx)
                }
                subclass_mapping[subclass_idx] = next_subclass_label
                self.inverse_mapping[next_subclass_label] = i
                next_subclass_label += 1
                
            self.subclass_mapping[i] = subclass_mapping
            
            # 可视化聚类结果
            if X_type.shape[1] >= 2:
                # 使用PCA或获取前两个特征
                from sklearn.decomposition import PCA
                pca = PCA(n_components=2)
                X_type_2d = pca.fit_transform(X_type)
                
                plt.figure(figsize=(10, 6))
                for cluster in range(best_n_clusters):
                    plt.scatter(
                        X_type_2d[kmeans.labels_ == cluster, 0],
                        X_type_2d[kmeans.labels_ == cluster, 1],
                        label=f'Cluster {cluster}'
                    )
                plt.title(f"岩石类型 '{rock_type}' 的聚类结果")
                plt.xlabel('Component 1')
                plt.ylabel('Component 2')
                plt.legend()
                plt.tight_layout()
                plt.savefig(os.path.join(self.output_dir, f'clusters_{rock_type}.png'))
                plt.close()
            
            # 可视化评估指标
            plt.figure(figsize=(8, 4))
            plt.plot(range(min_clusters, min(max_clusters_for_type + 1, len(X_type))), scores, 'o-')
            plt.axvline(x=best_n_clusters, color='r', linestyle='--')
            plt.xlabel('聚类数')
            plt.ylabel('轮廓系数')
            plt.title(f"岩石类型 '{rock_type}' 的最佳聚类数")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, f'silhouette_{rock_type}.png'))
            plt.close()
            
        # 打印子类信息
        print("\n子类信息:")
        for subclass_label, info in self.subclass_info.items():
            print(f"子类 {subclass_label}: 岩石类型 '{info['rock_type']}', 子类 {info['subclass_idx']}, 样本数 {info['samples']}")
            
        # 可视化子类分布
        subclass_counts = [info['samples'] for info in self.subclass_info.values()]
        subclass_labels = [f"{info['rock_type']}-{info['subclass_idx']}" for info in self.subclass_info.values()]
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(subclass_counts)), subclass_counts)
        plt.xlabel('子类')
        plt.ylabel('样本数')
        plt.title('各子类样本分布')
        plt.xticks(range(len(subclass_counts)), subclass_labels, rotation=90)
        
        # 在柱状图上添加岩石类型色彩标记
        for i, (bar, info) in enumerate(zip(bars, self.subclass_info.values())):
            bar.set_color(plt.cm.tab10(info['rock_type_idx'] % 10))
            
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'subclass_distribution.png'))
        plt.close()
        
        return self
        
    def transform_to_subclasses(self, X, y=None):
        """
        将样本转换为子类标签
        
        Parameters:
        -----------
        X : array-like
            特征
        y : array-like, optional
            原始类标签
            
        Returns:
        --------
        subclass_labels : array-like
            子类标签
        """
        if self.cluster_models is None:
            raise ValueError("必须先调用fit_clusters")
            
        X_scaled = self.scaler.transform(X)
        subclass_labels = np.zeros(len(X), dtype=int)
        
        if y is not None:
            # 如果提供了原始标签，直接使用它们
            for i in range(len(X)):
                rock_type_idx = y[i]
                model = self.cluster_models[rock_type_idx]
                
                if model is None:
                    # 如果该岩石类型没有聚类模型，使用默认子类
                    subclass_idx = 0
                else:
                    # 预测子类
                    features = X_scaled[i].reshape(1, -1)
                    subclass_idx = model.predict(features)[0]
                    
                # 映射到全局子类标签
                subclass_labels[i] = self.subclass_mapping[rock_type_idx][subclass_idx]
        else:
            # 如果没有提供原始标签，尝试所有聚类模型并选择最接近的中心点
            # 这种方法不太精确，但可以在预测时使用
            for i in range(len(X)):
                best_distance = float('inf')
                best_subclass = 0
                
                for rock_type_idx, model in self.cluster_models.items():
                    if model is None:
                        continue
                        
                    features = X_scaled[i].reshape(1, -1)
                    subclass_idx = model.predict(features)[0]
                    center = model.cluster_centers_[subclass_idx]
                    distance = np.linalg.norm(X_scaled[i] - center)
                    
                    if distance < best_distance:
                        best_distance = distance
                        best_subclass = self.subclass_mapping[rock_type_idx][subclass_idx]
                        
                subclass_labels[i] = best_subclass
                
        return subclass_labels
    
    def fit_global_classifier(self, X_train, y_train, X_valid=None, y_valid=None):
        """
        基于子类标签训练全局分类器
        
        Parameters:
        -----------
        X_train : array-like
            训练特征
        y_train : array-like
            训练标签
        X_valid : array-like, optional
            验证特征
        y_valid : array-like, optional
            验证标签
        """
        print("\n训练全局分类器...")
        
        # 转换为子类标签
        y_train_sub = self.transform_to_subclasses(X_train, y_train)
        
        # 训练随机森林分类器
        self.global_classifier = RandomForestClassifier(
            n_estimators=100, 
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42,
            class_weight='balanced'
        )
        
        self.global_classifier.fit(X_train, y_train_sub)
        
        # 评估训练集性能
        y_train_pred = self.global_classifier.predict(X_train)
        train_accuracy = accuracy_score(y_train_sub, y_train_pred)
        print(f"训练集准确率: {train_accuracy:.4f}")
        
        # 评估验证集性能
        if X_valid is not None and y_valid is not None:
            y_valid_sub = self.transform_to_subclasses(X_valid, y_valid)
            y_valid_pred = self.global_classifier.predict(X_valid)
            valid_accuracy = accuracy_score(y_valid_sub, y_valid_pred)
            print(f"验证集准确率: {valid_accuracy:.4f}")
            
            # 计算映射回原始类别后的准确率
            y_valid_pred_original = np.array([self.inverse_mapping[label] for label in y_valid_pred])
            valid_accuracy_original = accuracy_score(y_valid, y_valid_pred_original)
            print(f"验证集原始类别准确率: {valid_accuracy_original:.4f}")
            
        # 保存特征重要性
        if hasattr(self.global_classifier, 'feature_importances_'):
            plt.figure(figsize=(10, 6))
            importances = self.global_classifier.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            plt.bar(range(len(importances)), importances[indices])
            plt.title('特征重要性')
            plt.xlabel('特征索引')
            plt.ylabel('重要性')
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'feature_importance.png'))
            plt.close()
            
        return self
    
    def predict(self, X):
        """
        预测样本的子类标签
        
        Parameters:
        -----------
        X : array-like
            特征
            
        Returns:
        --------
        predictions : array-like
            预测的子类标签
        """
        if self.global_classifier is None:
            raise ValueError("必须先调用fit_global_classifier")
            
        return self.global_classifier.predict(X)
    
    def predict_original_class(self, X):
        """
        预测样本的原始类别
        
        Parameters:
        -----------
        X : array-like
            特征
            
        Returns:
        --------
        predictions : array-like
            预测的原始类别
        """
        subclass_predictions = self.predict(X)
        original_predictions = np.array([self.inverse_mapping[label] for label in subclass_predictions])
        return original_predictions
    
    def predict_proba(self, X):
        """
        预测样本属于各子类的概率
        
        Parameters:
        -----------
        X : array-like
            特征
            
        Returns:
        --------
        probabilities : array-like
            预测的概率
        """
        if self.global_classifier is None:
            raise ValueError("必须先调用fit_global_classifier")
            
        return self.global_classifier.predict_proba(X)
    
    def evaluate(self, X_test, y_test, class_names, filename_suffix=''):
        """
        在测试集上评估模型性能
        
        Parameters:
        -----------
        X_test : array-like
            测试特征
        y_test : array-like
            测试标签
        class_names : list of str
            类别名称
        filename_suffix : str, default=''
            文件名后缀
            
        Returns:
        --------
        accuracy : float
            准确率
        y_pred : array-like
            预测结果
        """
        if self.global_classifier is None:
            raise ValueError("必须先调用fit_global_classifier")
            
        # 预测子类标签
        y_pred_sub = self.predict(X_test)
        
        # 映射回原始类别
        y_pred = np.array([self.inverse_mapping[label] for label in y_pred_sub])
        
        # 计算准确率
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\n测试集准确率: {accuracy:.4f}")
        
        # 生成分类报告
        class_report = classification_report(y_test, y_pred, target_names=class_names)
        print("\n分类报告:")
        print(class_report)
        
        # 保存分类报告
        report_file = f'hierarchical_classification_report{filename_suffix}.txt'
        with open(os.path.join(self.output_dir, report_file), 'w') as f:
            f.write(f"测试集准确率: {accuracy:.4f}\n\n")
            f.write(class_report)
            
        # 生成混淆矩阵
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names)
        plt.xlabel('预测标签')
        plt.ylabel('真实标签')
        plt.title('混淆矩阵')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'hierarchical_confusion_matrix{filename_suffix}.png'))
        plt.close()
        
        # 计算每个类的准确率
        class_accuracy = np.diag(cm) / np.sum(cm, axis=1)
        plt.figure(figsize=(12, 6))
        plt.bar(class_names, class_accuracy)
        plt.xlabel('类别')
        plt.ylabel('准确率')
        plt.title('各类别分类准确率')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'hierarchical_class_accuracy{filename_suffix}.png'))
        plt.close()
        
        # 子类到原始类的映射可视化
        subclass_labels = [f"{info['rock_type']}-{info['subclass_idx']}" for info in self.subclass_info.values()]
        subclass_original = [info['rock_type_idx'] for info in self.subclass_info.values()]
        
        # 计算子类预测准确率
        y_test_sub = self.transform_to_subclasses(X_test, y_test)
        subclass_accuracy = accuracy_score(y_test_sub, y_pred_sub)
        print(f"\n子类预测准确率: {subclass_accuracy:.4f}")
        
        # 统计每个子类的样本数
        unique_subclasses, subclass_counts = np.unique(y_test_sub, return_counts=True)
        
        # 创建子类混淆矩阵
        cm_sub = confusion_matrix(y_test_sub, y_pred_sub)
        plt.figure(figsize=(14, 12))
        sns.heatmap(cm_sub, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=[subclass_labels[i] for i in range(len(subclass_labels)) if i in unique_subclasses], 
                   yticklabels=[subclass_labels[i] for i in range(len(subclass_labels)) if i in unique_subclasses])
        plt.xlabel('预测子类')
        plt.ylabel('真实子类')
        plt.title('子类混淆矩阵')
        plt.xticks(rotation=90)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'subclass_confusion_matrix{filename_suffix}.png'))
        plt.close()
        
        return accuracy, y_pred
    
    def save_model(self, filename='hierarchical_model.pkl'):
        """
        保存模型
        
        Parameters:
        -----------
        filename : str, default='hierarchical_model.pkl'
            文件名
        """
        model_data = {
            'cluster_models': self.cluster_models,
            'global_classifier': self.global_classifier,
            'rock_types': self.rock_types,
            'cluster_counts': self.cluster_counts,
            'scaler': self.scaler,
            'subclass_info': self.subclass_info,
            'subclass_mapping': self.subclass_mapping,
            'inverse_mapping': self.inverse_mapping,
        }
        
        model_path = os.path.join(self.output_dir, filename)
        joblib.dump(model_data, model_path)
        print(f"\n模型已保存到 {model_path}")
        
    def load_model(self, model_path):
        """
        加载模型
        
        Parameters:
        -----------
        model_path : str
            模型路径
        """
        model_data = joblib.load(model_path)
        
        self.cluster_models = model_data['cluster_models']
        self.global_classifier = model_data['global_classifier']
        self.rock_types = model_data['rock_types']
        self.cluster_counts = model_data['cluster_counts']
        self.scaler = model_data['scaler']
        self.subclass_info = model_data['subclass_info']
        self.subclass_mapping = model_data['subclass_mapping']
        self.inverse_mapping = model_data['inverse_mapping']
        
        print(f"模型已从 {model_path} 加载") 