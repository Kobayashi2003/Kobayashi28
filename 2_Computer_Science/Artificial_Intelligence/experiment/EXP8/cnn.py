# data path: ./data/train/<label>/*.jpg ./data/test/*.jpg (RGB)

import os
from PIL import Image
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

# from enum import Enum

# LABLE = Enum('label', ('baihe', 'dangshen', 'gouqi', 'huaihua', 'jinyinhua'))

LABLE = {
    'baihe': 0,
    'dangshen': 1,
    'gouqi': 2,
    'huaihua': 3,
    'jinyinhua': 4
}

# Hyper Parameters
EPOCH = 5
BATCH_SIZE = 10
LR = 0.001

# Data Path
TRAIN_DATA_PATH = './data/train'
TEST_DATA_PATH = './data/test'

# Data Loader
class MyDataset(Dataset):
    def __init__(self, data_path, transform=None):
        self.data_path = data_path
        self.transform = transform
        self.data = []
        self.label = []
        for label in os.listdir(data_path):
            for img in os.listdir(os.path.join(data_path, label)):
                self.data.append(os.path.join(data_path, label, img))
                self.label.append(LABLE[label])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img = Image.open(self.data[idx])
        label = self.label[idx]
        if self.transform:
            img = self.transform(img)
        return img, label
    
    def shuffle(self):
        import random
        c = list(zip(self.data, self.label))
        random.shuffle(c)
        self.data, self.label = zip(*c)


class MyTestDataset(Dataset):
    def __init__(self, data_path, transform=None):
        self.data_path = data_path
        self.transform = transform
        self.data = []
        self.label = []
        for img in os.listdir(data_path):
            self.data.append(os.path.join(data_path, img))
            self.label.append(LABLE[img.split('0')[0]])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img = Image.open(self.data[idx])
        label = self.label[idx]
        if self.transform:
            img = self.transform(img)
        return img, label

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

train_data = MyDataset(TRAIN_DATA_PATH, transform=transform)
train_data.shuffle()
train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)

test_data = MyTestDataset(TEST_DATA_PATH, transform=transform)
test_x = torch.stack([test_data[i][0] for i in range(len(test_data))])
test_y = torch.tensor([test_data[i][1] for i in range(len(test_data))])


# CNN Model
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 16, 5, 1, 2),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(16, 32, 5, 1, 2),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )   
        self.out = nn.Linear(32 * 64 * 64, 5)


    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)
        output = self.out(x)
        return output, x
    
cnn = CNN()

# Train
optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)
loss_func = nn.CrossEntropyLoss()

for epoch in range(EPOCH):
    for step, (x, y) in enumerate(train_loader):
        output = cnn(x)[0]
        loss = loss_func(output, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        test_output, last_layer = cnn(test_x)
        pred_y = torch.max(test_output, 1)[1].data.numpy()
        accuracy = float((pred_y == test_y.numpy()).astype(int).sum()) / float(test_y.size(0))
        print('Epoch: ', epoch, '| train loss: %.4f' % loss.data.numpy(), '| test accuracy: %.2f' % accuracy)

# Test
test_output, _ = cnn(test_x[:10])
pred_y = torch.max(test_output, 1)[1].data.numpy()
print(pred_y, 'prediction number')
print(test_y[:10].numpy(), 'real number')

