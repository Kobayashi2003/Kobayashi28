import re
import os
import random
import matplotlib.pyplot as plt
from enum import Enum

import torch
import torch.nn as nn
from torchvision import transforms
from torch.utils.data import DataLoader

from cnn import CNN
from MyDataset import MyDataset

# Enum Lable
LABLE = Enum('ZhongYao', ['baihe', 'dangshen', 'gouqi', 'huaihua', 'jinyinhua'], start=0)

# Hyper Parameters
EPOCH = 5
BATCH_SIZE = 16
LR = 0.001

# Data Path
TRAIN_DATA_PATH = '../data/train'
TEST_DATA_PATH = '../data/test'

USE_LARGE_TEST_DATASET = False 

# Data Loader
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

def load_dataset(data_path, label_enum=None, is_train=True):
    datas, labels = [], []
    for item in os.listdir(data_path):
        if is_train:
            for img in os.listdir(os.path.join(data_path, item)):
                datas.append(os.path.join(data_path, item, img))
                labels.append(label_enum[item].value)
        else:
            datas.append(os.path.join(data_path, item))
            labels.append(label_enum[re.match(r'[a-zA-Z]+', item).group()].value)
    return MyDataset(datas, labels, transform=transform)

train_dataset = load_dataset(TRAIN_DATA_PATH, LABLE, is_train=True)
test_dataset = load_dataset(TEST_DATA_PATH, LABLE, is_train=False)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

# Select 100 samples from train dataset as large test dataset
large_test_samples = random.sample(list(zip(train_dataset.data, train_dataset.label)), 100)
large_test_dataset = MyDataset(*zip(*large_test_samples), transform=transform)

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Choose the test dataset based on the device
def prepare_test_dataset(dataset):
    test_x = torch.stack([dataset[i][0] for i in range(len(dataset))])
    test_y = torch.tensor([dataset[i][1] for i in range(len(dataset))])
    return test_x.to(device=device), test_y.to(device=device)

test_x, test_y = prepare_test_dataset(large_test_dataset if
                                        USE_LARGE_TEST_DATASET else test_dataset)

# CNN Model
cnn = CNN().to(device=device)

# Train
optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)
loss_func = nn.CrossEntropyLoss()

loss_record = []
accuracy_record = []

def test_model():
    with torch.no_grad():
        test_output = cnn(test_x)
        pred_y = torch.max(test_output, 1)[1].cpu().data.numpy()
        accuracy = (pred_y == test_y.cpu().data.numpy()).mean()
        return pred_y, accuracy

for epoch in range(EPOCH):
    for step, (x, y) in enumerate(train_loader):

        x = x.to(device=device)
        y = y.to(device=device)

        # forward
        output = cnn(x)
        # calculate loss
        loss = loss_func(output, y)
        # clear gradients for this training step before backward
        optimizer.zero_grad()
        # backpropagation, compute gradients
        loss.backward()
        # apply gradients
        optimizer.step()

        # Test 
        if step and step % 1 == 0:
            pred_y, accuracy = test_model()
            print('Epoch: ', epoch, '| train loss: %.4f' % loss.item(), '| test accuracy: %.2f' % accuracy)

            loss_record.append(loss.item())
            accuracy_record.append(accuracy)
else:
    print(f'Prediction:\t {pred_y}')
    print(f'Ground Truth:\t {test_y.cpu().data.numpy()}')

# Plotting loss and accuracy records
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(loss_record)
plt.title('Loss')
plt.xlabel('Step')
plt.ylabel('Loss')

plt.subplot(1, 2, 2)
plt.plot(accuracy_record)
plt.title('Accuracy')
plt.xlabel('Step')
plt.ylabel('Accuracy')

plt.show()
plt.close()
