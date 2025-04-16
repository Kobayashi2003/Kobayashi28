import os
from utils import get_weight_path

# Model configuration
NET_NAME = 'resnet50'
VERSION = 'v1.0'
DEVICE = '0'
PRE_TRAINED = True
CURRENT_FOLD = 1
FOLD_NUM = 5

# CUB-200 dataset statistics
CUB_TRAIN_MEAN = [0.485, 0.456, 0.406]
CUB_TRAIN_STD = [0.229, 0.224, 0.225]

# Paths
CKPT_PATH = f'../output/ckpt/{VERSION}/fold{CURRENT_FOLD}'
WEIGHT_PATH = get_weight_path(CKPT_PATH)
LOG_DIR = f'../output/log/{VERSION}'

# Training parameters
INIT_TRAINER = {
    'net_name': NET_NAME,
    'lr': 1e-4,
    'n_epoch': 50,
    'num_classes': 200,
    'image_size': 224,
    'batch_size': 32,
    'train_mean': CUB_TRAIN_MEAN,
    'train_std': CUB_TRAIN_STD,
    'num_workers': 4,
    'device': DEVICE,
    'pre_trained': PRE_TRAINED,
    'weight_decay': 1e-4,
    'momentum': 0.9,
    'gamma': 0.1,
    'milestones': [20, 40],
    'use_fp16': True,
    'dropout': 0.2
}

# Training setup
SETUP_TRAINER = {
    'output_dir': f'../output/ckpt/{VERSION}',
    'log_dir': LOG_DIR,
    'optimizer': 'Adam',
    'loss_fun': 'Cross_Entropy',
    'class_weight': None,
    'lr_scheduler': 'MultiStepLR'
}

# Data paths
TRAIN_CSV_PATH = '../data/csv_file/cub_200_2011_train.csv'
TEST_CSV_PATH = '../data/csv_file/cub_200_2011_test.csv'
RESULT_DIR = f'../output/results/{VERSION}'
