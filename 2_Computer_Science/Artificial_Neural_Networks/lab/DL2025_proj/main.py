import os
import numpy as np
import argparse
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import time
import shutil
import torch
from trainer import VolumeClassifier
from data_utils.csv_reader import csv_reader_single
from config import INIT_TRAINER, SETUP_TRAINER, VERSION, CURRENT_FOLD, WEIGHT_PATH, WEIGHT_PATH_LIST, FOLD_NUM
from converter.common_utils import save_as_hdf5
from sklearn.model_selection import StratifiedKFold


def get_cross_validation(data_dict, k=5, shuffle=True, random_state=2025):
    """
    参数:
    data_dict (dict): 键为图片路径，值为类别标签的字典
    k (int): 折数
    shuffle (bool): 是否打乱数据
    random_state (int): 随机种子

    返回:
    list: 包含k个元组的列表，每个元组包含(训练路径列表, 验证路径列表)
    """
    paths = list(data_dict.keys())
    labels = [data_dict[path] for path in paths]

    skf = StratifiedKFold(n_splits=k, shuffle=shuffle, random_state=random_state)
    train_splits = []
    val_splits = []
    for train_idx, val_idx in skf.split(paths, labels):
        train_paths = [paths[i] for i in train_idx]
        val_paths = [paths[i] for i in val_idx]
        train_splits.append(train_paths)
        val_splits.append(val_paths)

    return train_splits, val_splits

# 获取模型参数数量的函数
def get_parameter_number(net):
    total_num = sum(p.numel() for p in net.parameters())
    trainable_num = sum(p.numel() for p in net.parameters() if p.requires_grad)
    return {'Total': total_num, 'Trainable': trainable_num}


if __name__ == "__main__":
    # 命令行参数解析设置
    parser = argparse.ArgumentParser()
    parser.add_argument('-m',
                        '--mode',
                        default='train',
                        choices=["train-cross","train", "inf","inf-cross"],
                        help='choose the mode',
                        type=str)
    parser.add_argument('-s',
                        '--save',
                        default='yes',
                        choices=['no', 'n', 'yes', 'y'],
                        help='save the forward middle features or not',
                        type=str)
    parser.add_argument('-n',
                        '--net_name',
                        default="resnet34",
                        choices=["resnet18", "resnet34", "resnet50", "resnet101", "resnet152","resnext50_32x4d","resnext101_32x8d","resnext101_64x4d","wide_resnet50_2","wide_resnet101_2",
           "vit_b_16","vit_b_32","vit_l_16","vit_l_32","vit_h_14"],
                        help='override the INIT_TRAINER[\'net_name\'] of config.py',
                        type=str)
    parser.add_argument('-l',
                        '--lr',
                        #default=None,
                        help='override the INIT_TRAINER[\'lr\'] of config.py',
                        type=float)
    parser.add_argument('-e',
                        '--n_epoch',
                        #default=None,
                        help='override the INIT_TRAINER[\'n_epoch\'] of config.py',
                        type=int)
    parser.add_argument('-c',
                        '--num_classes',
                        # default=None,
                        help='override the INIT_TRAINER[\'num_classes\'] of config.py',
                        type=int)
    parser.add_argument('-is',
                        '--image_size',
                        #default=None,
                        help='override the INIT_TRAINER[\'image_size\'] of config.py',
                        type=int)
    parser.add_argument('-bs',
                        '--batch_size',
                        default=16,
                        help='override the INIT_TRAINER[\'batch_size\'] of config.py',
                        type=int)
    args = parser.parse_args()
    
    # 根据命令行参数覆盖配置文件中的设置
    if args.net_name is not None:
        INIT_TRAINER['net_name'] = args.net_name
    if args.lr is not None:
        INIT_TRAINER['lr'] = args.lr
    if args.n_epoch is not None:
        INIT_TRAINER['n_epoch'] = args.n_epoch
    if args.num_classes is not None:
        INIT_TRAINER['num_classes'] = args.num_classes
    if args.image_size is not None:
        INIT_TRAINER['image_size'] = args.image_size
    if args.batch_size is not None:
        INIT_TRAINER['batch_size'] = args.batch_size

    # 设置混合精度训练
    INIT_TRAINER['use_fp16'] = True

    # 设置数据路径和分类器
    # if args.mode != 'train-cross' and args.mode != 'inf-cross':
    #     INIT_TRAINER['weight_path'] = WEIGHT_PATH
    #     classifier = VolumeClassifier(**INIT_TRAINER)


    # 训练部分
    ###############################################
    if 'train' in args.mode:
        ###### 读取数据
        csv_path = './csv_file/cub_200_2011.csv_train.csv'
        label_dict = csv_reader_single(csv_path, key_col='id', value_col='label')
        # path_list = list(label_dict.keys())
        train_splits, val_splits = get_cross_validation(label_dict)

        # 交叉验证训练模式
        if args.mode == 'train-cross':
            for fold in range(1, FOLD_NUM+1):
                print('===================fold %d==================='%(fold))
                # 初始化分类器
                # INIT_TRAINER['weight_path'] = WEIGHT_PATH_LIST[fold-1]
                classifier = VolumeClassifier(**INIT_TRAINER)
                print(get_parameter_number(classifier.net))

                # 设置当前折的训练和验证数据
                SETUP_TRAINER['train_path'] = train_splits[fold-1]
                SETUP_TRAINER['val_path'] = val_splits[fold-1]
                SETUP_TRAINER['label_dict'] = label_dict
                SETUP_TRAINER['cur_fold'] = fold

                # 开始训练并计时
                start_time = time.time()
                classifier.trainer(**SETUP_TRAINER)

                print('run time:%.4f' % (time.time() - start_time))
        
        # 单折训练模式
        elif args.mode == 'train':
            # 初始化分类器
            # INIT_TRAINER['weight_path'] = WEIGHT_PATH
            classifier = VolumeClassifier(**INIT_TRAINER)
            print(get_parameter_number(classifier.net))
            # 设置当前折的训练和验证数据
            SETUP_TRAINER['train_path'] = train_splits[CURRENT_FOLD-1]
            SETUP_TRAINER['val_path'] = val_splits[CURRENT_FOLD-1]
            SETUP_TRAINER['label_dict'] = label_dict
            SETUP_TRAINER['cur_fold'] = CURRENT_FOLD

            # 开始训练并计时
            start_time = time.time()
            classifier.trainer(**SETUP_TRAINER)

            print('run time:%.4f' % (time.time() - start_time))
    ###############################################

    # 推理
    ###############################################
    elif 'inf' in args.mode:
        # 读取测试数据
        test_csv_path = './csv_file/cub_200_2011.csv_test.csv'
        label_dict = csv_reader_single(test_csv_path, key_col='id', value_col='label')
        test_path = list(label_dict.keys())
        print('test len:',len(test_path))

        # 设置结果和特征保存路径
        save_dir = './analysis/result/{}'.format(VERSION)
        feature_dir = './analysis/mid_feature/{}'.format(VERSION)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # 单模型推理模式
        if args.mode == 'inf':
            # 初始化分类器并加载权重
            classifier = VolumeClassifier(**INIT_TRAINER)
            checkpoint = torch.load(WEIGHT_PATH)
            classifier.net.load_state_dict(checkpoint['state_dict'])
            save_path = os.path.join(save_dir,f'fold{str(CURRENT_FOLD)}.csv')
            
            # 开始推理并计时
            start_time = time.time()
            if args.save == 'no' or args.save == 'n':
                # 不保存中间特征
                result, _, _ = classifier.inference(test_path, label_dict)
                print('run time:%.4f' % (time.time() - start_time))
            else:
                # 保存中间特征
                result, feature_in, feature_out = classifier.inference(
                    test_path, label_dict, hook_fn_forward=True)
                print('run time:%.4f' % (time.time() - start_time))
                # 保存平均池化输出特征
                print(feature_in.shape, feature_out.shape)
                feature_save_path = os.path.join(feature_dir,f'fold{str(CURRENT_FOLD)}')
                if not os.path.exists(feature_save_path):
                    os.makedirs(feature_save_path)
                else:
                    shutil.rmtree(feature_save_path)
                    os.makedirs(feature_save_path)
                # 逐个样本保存特征
                for i in range(len(test_path)):
                    name = os.path.basename(test_path[i])
                    feature_path = os.path.join(feature_save_path, name.split(".")[0])
                    save_as_hdf5(feature_in[i], feature_path, 'feature_in')
                    save_as_hdf5(feature_out[i], feature_path, 'feature_out')
            
            # 保存预测结果
            result['path'] = test_path
            csv_file = pd.DataFrame(result)
            csv_file.to_csv(save_path, index=False)
            
            # 生成分类报告
            cls_report = classification_report(
                result['true'],
                result['pred'],
                output_dict=True)
            
            # 保存全连接层权重
            if INIT_TRAINER['net_name'].startswith('res') or INIT_TRAINER['net_name'].startswith('wide_res'):

                fc_weight_save_path = os.path.join(save_dir,f'fold{str(CURRENT_FOLD)}_fc_weight.npy')
                np.save(fc_weight_save_path, classifier.net.state_dict()['fc.weight'].cpu().numpy())
            
            # 保存分类报告为CSV
            report_save_path = os.path.join(save_dir,f'fold{str(CURRENT_FOLD)}_report.csv')
            report_csv_file = pd.DataFrame(cls_report)
            report_csv_file.to_csv(report_save_path)
        
        
        # 交叉验证推理模式
        elif args.mode == 'inf-cross':
            # 对每个折进行推理
            for fold in range(1,FOLD_NUM+1):
                print('===================fold %d==================='%(fold))
                # 初始化分类器并加载对应折的权重
                classifier = VolumeClassifier(**INIT_TRAINER)
                checkpoint = torch.load(WEIGHT_PATH_LIST[fold-1])
                classifier.net.load_state_dict(checkpoint['state_dict'])
                save_path = os.path.join(save_dir,f'fold{str(fold)}.csv')
                start_time = time.time()
                
                # 开始推理并计时
                if args.save == 'no' or args.save == 'n':
                    # 不保存中间特征
                    result, _, _ = classifier.inference(test_path, label_dict)
                    print('run time:%.4f' % (time.time() - start_time))
                else:
                    # 保存中间特征
                    result, feature_in, feature_out = classifier.inference(
                        test_path, label_dict, hook_fn_forward=True)
                    print('run time:%.4f' % (time.time() - start_time))
                    # 保存平均池化输出特征
                    print(feature_in.shape, feature_out.shape)
                    feature_save_path = os.path.join(feature_dir,f'fold{str(fold)}')
                    if not os.path.exists(feature_save_path):
                        os.makedirs(feature_save_path)
                    else:
                        shutil.rmtree(feature_save_path)
                        os.makedirs(feature_save_path)
                    # 逐个样本保存特征
                    for i in range(len(test_path)):
                        name = os.path.basename(test_path[i])
                        feature_path = os.path.join(feature_save_path, name.split(".")[0])
                        save_as_hdf5(feature_in[i], feature_path, 'feature_in')
                        save_as_hdf5(feature_out[i], feature_path, 'feature_out')
                
                # 保存预测结果
                result['path'] = test_path
                csv_file = pd.DataFrame(result)
                csv_file.to_csv(save_path, index=False)
                # 生成分类报告
                cls_report = classification_report(
                    result['true'],
                    result['pred'],
                    output_dict=True)
                
                # 保存全连接层权重
                if INIT_TRAINER['net_name'].startswith('res') or INIT_TRAINER['net_name'].startswith('wide_res'):
                    fc_weight_save_path = os.path.join(save_dir,f'fold{str(fold)}_fc_weight.npy')
                    np.save(fc_weight_save_path, classifier.net.state_dict()['fc.weight'].cpu().numpy())
                
                # 保存分类报告为CSV
                report_save_path = os.path.join(save_dir,f'fold{str(fold)}_report.csv')
                report_csv_file = pd.DataFrame(cls_report)
                report_csv_file.to_csv(report_save_path)
    ###############################################
