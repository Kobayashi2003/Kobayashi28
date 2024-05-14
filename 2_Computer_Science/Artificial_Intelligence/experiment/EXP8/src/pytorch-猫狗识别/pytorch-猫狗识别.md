# 猫狗识别

阅读本文你将学会**如何使用 PyTorch 进行图像识别**


```python
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda, Compose
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
import numpy as np
```

## 数据读取与预处理

在对数据进行增强时注意是否合理哦！原本我使用了下面的代码对数据进行增强，试图解决数据不足的问题，经过测试我发现并非所有的增强操作都会产生正面影响。

对此，我做过几个对比小实验，保持其他参数不变，仅改变数据增强方式，最后实验结果如下：
- 不进行数据增强：79.2%
- 随机旋转：80.8%
- 随机旋转+高斯模糊模糊：83.3%
- 随机垂直翻转：73.3%


```python
train_datadir = './1-cat-dog/train/'
test_datadir  = './1-cat-dog/val/'

train_transforms = transforms.Compose([
    transforms.Resize([224, 224]),  # 将输入图片resize成统一尺寸
#     transforms.RandomRotation(degrees=(-10, 10)),  #随机旋转，-10到10度之间随机选
#     transforms.RandomHorizontalFlip(p=0.5),  #随机水平翻转 选择一个概率概率
#     transforms.RandomVerticalFlip(p=0.5),  #随机垂直翻转
#     transforms.RandomPerspective(distortion_scale=0.6, p=1.0), # 随机视角
#     transforms.GaussianBlur(kernel_size=(5, 9), sigma=(0.1, 5)),  #随机选择的高斯模糊模糊图像
    transforms.ToTensor(),          # 将PIL Image或numpy.ndarray转换为tensor，并归一化到[0,1]之间
    transforms.Normalize(           # 标准化处理-->转换为标准正太分布（高斯分布），使模型更容易收敛
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225])  # 其中 mean=[0.485,0.456,0.406]与std=[0.229,0.224,0.225] 从数据集中随机抽样计算得到的。
])

test_transforms = transforms.Compose([
    transforms.Resize([224, 224]),  # 将输入图片resize成统一尺寸
    transforms.ToTensor(),          # 将PIL Image或numpy.ndarray转换为tensor，并归一化到[0,1]之间
    transforms.Normalize(           # 标准化处理-->转换为标准正太分布（高斯分布），使模型更容易收敛
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225])  # 其中 mean=[0.485,0.456,0.406]与std=[0.229,0.224,0.225] 从数据集中随机抽样计算得到的。
])

train_data = datasets.ImageFolder(train_datadir,transform=train_transforms)

test_data  = datasets.ImageFolder(test_datadir,transform=test_transforms)

train_loader = torch.utils.data.DataLoader(train_data,
                                          batch_size=4,
                                          shuffle=True,
                                          num_workers=1)
test_loader  = torch.utils.data.DataLoader(test_data,
                                          batch_size=4,
                                          shuffle=True,
                                          num_workers=1)
```

关于 `transforms.Compose` 这部分更多的信息可以参考 https://pytorch-cn.readthedocs.io/zh/latest/torchvision/torchvision-transform/

如果你想知道还有哪些数据增强手段，可以看看这里： https://pytorch.org/vision/stable/transforms.html


```python
for X, y in test_loader:
    print("Shape of X [N, C, H, W]: ", X.shape)
    print("Shape of y: ", y.shape, y.dtype)
    break
```

    Shape of X [N, C, H, W]:  torch.Size([4, 3, 224, 224])
    Shape of y:  torch.Size([4]) torch.int64


## 定义模型


```python
import torch.nn.functional as F

# 找到可以用于训练的 GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using {} device".format(device))

# 定义模型
class LeNet(nn.Module):
    # 一般在__init__中定义网络需要的操作算子，比如卷积、全连接算子等等
    def __init__(self):
        super(LeNet, self).__init__()
        # Conv2d的第一个参数是输入的channel数量，第二个是输出的channel数量，第三个是kernel size
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        # 由于上一层有16个channel输出，每个feature map大小为5*5，所以全连接层的输入是16*5*5
        self.fc1 = nn.Linear(16*53*53, 120)
        self.fc2 = nn.Linear(120, 84)
        # 最终有2类，所以最后一个全连接层输出数量是2
        self.fc3 = nn.Linear(84, 2)
        self.pool = nn.MaxPool2d(2, 2)
    # forward这个函数定义了前向传播的运算，只需要像写普通的python算数运算那样就可以了
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        # 下面这步把二维特征图变为一维，这样全连接层才能处理
        x = x.view(-1, 16*53*53)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

model = LeNet().to(device)
print(model)
```

    Using cpu device
    LeNet(
      (conv1): Conv2d(3, 6, kernel_size=(5, 5), stride=(1, 1))
      (conv2): Conv2d(6, 16, kernel_size=(5, 5), stride=(1, 1))
      (fc1): Linear(in_features=44944, out_features=120, bias=True)
      (fc2): Linear(in_features=120, out_features=84, bias=True)
      (fc3): Linear(in_features=84, out_features=2, bias=True)
      (pool): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
    )


## 损失函数与优化器

定义一个损失函数和一个优化器。


```python
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)
```

## 定义训练函数

在单个训练循环中，模型对训练数据集进行预测（分批提供给它），并反向传播预测误差从而调整模型的参数。


```python
def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # 计算预测误差
        pred = model(X)
        loss = loss_fn(pred, y)

        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")
```

## 定义测试函数


```python
def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")
```

## 进行训练


```python
epochs = 20
for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    train(train_loader, model, loss_fn, optimizer)
    test(test_loader, model, loss_fn)
print("Done!")
```

    Epoch 1
    -------------------------------
    loss: 0.765885  [    0/  480]
    loss: 0.687276  [  400/  480]
    Test Error: 
     Accuracy: 52.5%, Avg loss: 0.685243 
    
    Epoch 2
    -------------------------------
    loss: 0.652565  [    0/  480]
    loss: 0.661249  [  400/  480]
    Test Error: 
     Accuracy: 67.5%, Avg loss: 0.661900 
    
    Epoch 3
    -------------------------------
    loss: 0.629588  [    0/  480]
    loss: 0.536548  [  400/  480]
    Test Error: 
     Accuracy: 68.3%, Avg loss: 0.608989 
    
    Epoch 4
    -------------------------------
    loss: 0.473581  [    0/  480]
    loss: 0.341041  [  400/  480]
    Test Error: 
     Accuracy: 70.8%, Avg loss: 0.528783 
    
    Epoch 5
    -------------------------------
    loss: 0.153299  [    0/  480]
    loss: 0.227830  [  400/  480]
    Test Error: 
     Accuracy: 78.3%, Avg loss: 0.490136 
    
    Epoch 6
    -------------------------------
    loss: 0.275428  [    0/  480]
    loss: 0.480467  [  400/  480]
    Test Error: 
     Accuracy: 74.2%, Avg loss: 0.504982 
    
    Epoch 7
    -------------------------------
    loss: 0.177029  [    0/  480]
    loss: 0.198866  [  400/  480]
    Test Error: 
     Accuracy: 78.3%, Avg loss: 0.539428 
    
    Epoch 8
    -------------------------------
    loss: 0.087402  [    0/  480]
    loss: 0.081733  [  400/  480]
    Test Error: 
     Accuracy: 81.7%, Avg loss: 0.470180 
    
    Epoch 9
    -------------------------------
    loss: 0.054239  [    0/  480]
    loss: 0.049218  [  400/  480]
    Test Error: 
     Accuracy: 80.0%, Avg loss: 0.448936 
    
    Epoch 10
    -------------------------------
    loss: 0.287717  [    0/  480]
    loss: 0.696647  [  400/  480]
    Test Error: 
     Accuracy: 80.0%, Avg loss: 0.447253 
    
    Epoch 11
    -------------------------------
    loss: 0.342855  [    0/  480]
    loss: 0.084907  [  400/  480]
    Test Error: 
     Accuracy: 81.7%, Avg loss: 0.474470 
    
    Epoch 12
    -------------------------------
    loss: 0.124892  [    0/  480]
    loss: 0.151610  [  400/  480]
    Test Error: 
     Accuracy: 77.5%, Avg loss: 0.456424 
    
    Epoch 13
    -------------------------------
    loss: 0.021801  [    0/  480]
    loss: 0.020646  [  400/  480]
    Test Error: 
     Accuracy: 78.3%, Avg loss: 0.599779 
    
    Epoch 14
    -------------------------------
    loss: 0.005602  [    0/  480]
    loss: 0.025274  [  400/  480]
    Test Error: 
     Accuracy: 85.0%, Avg loss: 0.440676 
    
    Epoch 15
    -------------------------------
    loss: 0.056227  [    0/  480]
    loss: 0.001794  [  400/  480]
    Test Error: 
     Accuracy: 81.7%, Avg loss: 0.627810 
    
    Epoch 16
    -------------------------------
    loss: 0.109221  [    0/  480]
    loss: 0.000464  [  400/  480]
    Test Error: 
     Accuracy: 80.0%, Avg loss: 0.573228 
    
    Epoch 17
    -------------------------------
    loss: 0.028971  [    0/  480]
    loss: 0.005886  [  400/  480]
    Test Error: 
     Accuracy: 82.5%, Avg loss: 0.568477 
    
    Epoch 18
    -------------------------------
    loss: 0.001403  [    0/  480]
    loss: 0.343260  [  400/  480]
    Test Error: 
     Accuracy: 84.2%, Avg loss: 0.549863 
    
    Epoch 19
    -------------------------------
    loss: 0.005389  [    0/  480]
    loss: 0.161802  [  400/  480]
    Test Error: 
     Accuracy: 82.5%, Avg loss: 0.576225 
    
    Epoch 20
    -------------------------------
    loss: 0.053033  [    0/  480]
    loss: 0.000415  [  400/  480]
    Test Error: 
     Accuracy: 82.5%, Avg loss: 0.645851 
    
    Done!



```python

```
