import os
import torch
import numpy as np

def get_weight_path(ckpt_path):
    """
    Get the path to the latest checkpoint file
    
    Args:
        ckpt_path: path to checkpoint directory
    
    Returns:
        path to the latest checkpoint file
    """
    if not os.path.exists(ckpt_path):
        return None
    
    files = os.listdir(ckpt_path)
    if len(files) == 0:
        return None
    
    # Find the latest epoch
    epochs = [int(f.split('=')[1].split('.')[0]) for f in files if f.startswith('epoch=')]
    if len(epochs) == 0:
        return None
    
    latest_epoch = max(epochs)
    weight_path = os.path.join(ckpt_path, f'epoch={latest_epoch}.pth')
    return weight_path

def get_parameter_number(net):
    """
    Calculate the total number of parameters in the model
    
    Args:
        net: neural network model
    
    Returns:
        dictionary containing total and trainable parameters
    """
    total_num = sum(p.numel() for p in net.parameters())
    trainable_num = sum(p.numel() for p in net.parameters() if p.requires_grad)
    return {'Total': total_num, 'Trainable': trainable_num}

def accuracy(output, target, topk=(1,)):
    """
    Compute the top-k accuracy
    
    Args:
        output: model output logits
        target: ground truth labels
        topk: tuple of k values for top-k accuracy
    
    Returns:
        list of accuracies for each k
    """
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res

class AverageMeter(object):
    """
    Computes and stores the average and current value
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

class EarlyStopping:
    """
    Early stopping to stop training when validation performance stops improving
    
    Args:
        patience: number of epochs to wait for improvement
        verbose: whether to print messages
        delta: minimum change to qualify as improvement
        monitor: metric to monitor ('val_loss' or 'val_acc')
        best_score: initial best score
        op_type: 'min' for loss, 'max' for accuracy
    """
    def __init__(self, patience=10, verbose=True, delta=0, 
                 monitor='val_loss', best_score=None, op_type='min'):
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = best_score
        self.early_stop = False
        self.delta = delta
        self.monitor = monitor
        self.op_type = op_type
        
        if self.op_type == 'min':
            self.val_score_min = np.Inf
        else:
            self.val_score_min = -np.Inf
            
    def __call__(self, val_score):
        if self.op_type == 'min':
            score = -val_score
        else:
            score = val_score
            
        if self.best_score is None:
            self.best_score = score
            self.print_and_update(val_score)
        elif score <= self.best_score + self.delta:
            self.counter += 1
            print(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.print_and_update(val_score)
            self.counter = 0
            
    def print_and_update(self, val_score):
        if self.verbose:
            print(f'{self.monitor} decreased ({self.val_score_min:.6f} --> {val_score:.6f})')
        self.val_score_min = val_score
