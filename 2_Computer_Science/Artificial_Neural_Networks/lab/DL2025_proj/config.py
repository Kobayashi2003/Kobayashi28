from utils import get_weight_path, get_weight_list

# __all__ = ["resnet18", "resnet34", "resnet50", "resnet101", "resnet152","resnext50_32x4d","resnext101_32x8d","resnext101_64x4d","wide_resnet50_2","wide_resnet101_2",
#            "vit_b_16","vit_b_32","vit_l_16","vit_l_32","vit_h_14"]

NET_NAME = 'resnet34'
VERSION = 'v1.0'
DEVICE = '0'

PRE_TRAINED = True
# 1,2,3,4,5
CURRENT_FOLD = 1
GPU_NUM = len(DEVICE.split(','))
FOLD_NUM = 5

CUB_TRAIN_MEAN = [0.48560741861744905, 0.49941626449353244, 0.43237713785804116]
CUB_TRAIN_STD = [0.2321024260764962, 0.22770540015765814, 0.2665100547329813]

CKPT_PATH = './ckpt/{}/fold{}'.format(VERSION, CURRENT_FOLD)
WEIGHT_PATH = get_weight_path(CKPT_PATH)
# print(WEIGHT_PATH)
WEIGHT_PATH_LIST = get_weight_list('./ckpt/{}/'.format(VERSION))


# Arguments when trainer initial
INIT_TRAINER = {
    'net_name': NET_NAME,
    'lr': 1e-4,
    'n_epoch': 50,
    'num_classes': 200,
    'image_size': 224,
    'batch_size': 64,
    'train_mean': CUB_TRAIN_MEAN,
    'train_std': CUB_TRAIN_STD,
    'num_workers': 2,
    'device': DEVICE,
    'pre_trained': PRE_TRAINED,
    'weight_decay': 1e-4,
    'momentum': 0.9,
    'gamma': 0.1,
    'milestones': [20, 40],
    'T_max': 5,
    'use_fp16': True,
    'dropout': 0.1
}

# Arguments when perform the trainer 
SETUP_TRAINER = {
    'output_dir': './ckpt/{}'.format(VERSION),
    'log_dir': './log/{}'.format(VERSION),
    'optimizer': 'Adam',
    'loss_fun': 'Cross_Entropy',
    'class_weight': None,
    'lr_scheduler': 'MultiStepLR'
}
