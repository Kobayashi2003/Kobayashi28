import torch
from torch import nn

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(
                in_channels=1,
                out_channels=16,
                kernel_size=5,
                stride=1,
                padding=2,
            ),
            nn.ReLU(),
            nn.MaxUnpool2d(kernel_size=2),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(16, 32, 5, 1, 2),
            nn.ReLU(),
            nn.MaxUnpool2d(2),
        )
        self.out = nn.Linear(32 * 7 * 7, 10)

    
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)
        output = self.out(x)
        return output, x


if __name__ == '__main__':
    # read images from ./cnn_images/train
    # labal is the folder name 
    # baihe dangshen gouqi huaihua jinyinhua

    import os
    import numpy as np
    from PIL import Image

    baihe_imgs = []
    for img in os.listdir('./cnn_images/train/baihe'):
        img = Image.open('./cnn_images/train/baihe/' + img)
        img = img.resize((28, 28))
        img = np.array(img)
        baihe_imgs.append(img)

    baihe_imgs = np.array(baihe_imgs)
    baihe_imgs = torch.from_numpy(baihe_imgs)
    baihe_imgs = baihe_imgs.float()
    baihe_imgs = baihe_imgs.unsqueeze(1)

    dangshen_imgs = []
    for img in os.listdir('./cnn_images/train/dangshen'):
        img = Image.open('./cnn_images/train/dangshen/' + img)
        img = img.resize((28, 28))
        img = np.array(img)
        dangshen_imgs.append(img)

    dangshen_imgs = np.array(dangshen_imgs)
    dangshen_imgs = torch.from_numpy(dangshen_imgs)
    dangshen_imgs = dangshen_imgs.float()
    dangshen_imgs = dangshen_imgs.unsqueeze(1)

    gouqi_imgs = []
    for img in os.listdir('./cnn_images/train/gouqi'):
        img = Image.open('./cnn_images/train/gouqi/' + img)
        img = img.resize((28, 28))
        img = np.array(img)
        gouqi_imgs.append(img)

    gouqi_imgs = np.array(gouqi_imgs)
    gouqi_imgs = torch.from_numpy(gouqi_imgs)
    gouqi_imgs = gouqi_imgs.float()
    gouqi_imgs = gouqi_imgs.unsqueeze(1)

    huaihua_imgs = []
    for img in os.listdir('./cnn_images/train/huaihua'):
        img = Image.open('./cnn_images/train/huaihua/' + img)
        img = img.resize((28, 28))
        img = np.array(img)
        huaihua_imgs.append(img)

    huaihua_imgs = np.array(huaihua_imgs)
    huaihua_imgs = torch.from_numpy(huaihua_imgs)
    huaihua_imgs = huaihua_imgs.float()
    huaihua_imgs = huaihua_imgs.unsqueeze(1)

    jinyinhua_imgs = []
    for img in os.listdir('./cnn_images/train/jinyinhua'):
        img = Image.open('./cnn_images/train/jinyinhua/' + img)
        img = img.resize((28, 28))
        img = np.array(img)
        jinyinhua_imgs.append(img)

    jinyinhua_imgs = np.array(jinyinhua_imgs)
    jinyinhua_imgs = torch.from_numpy(jinyinhua_imgs)
    jinyinhua_imgs = jinyinhua_imgs.float()
    jinyinhua_imgs = jinyinhua_imgs.unsqueeze(1)

    # train the model
    cnn = CNN()
    optimizer = torch.optim.Adam(cnn.parameters(), lr=0.01)
    loss_func = nn.CrossEntropyLoss()

    for epoch in range(100):
        for i in range(10):
            output = cnn(baihe_imgs[i])
            loss = loss_func(output, torch.tensor([0]))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            output = cnn(dangshen_imgs[i])
            loss = loss_func(output, torch.tensor([1]))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            output = cnn(gouqi_imgs[i])
            loss = loss_func(output, torch.tensor([2]))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            output = cnn(huaihua_imgs[i])
            loss = loss_func(output, torch.tensor([3]))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            output = cnn(jinyinhua_imgs[i])
            loss = loss_func(output, torch.tensor([4]))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    # test the model
    test_imgs = []
    for img in os.listdir('./cnn_images/test/' + img):
        img = Image.open('./cnn_images/test/' + img)
        img = img.resize((28, 28))
        img = np.array(img)
        test_imgs.append(img)

    test_imgs = np.array(test_imgs)
    test_imgs = torch.from_numpy(test_imgs)
    test_imgs = test_imgs.float()
    test_imgs = test_imgs.unsqueeze(1)

    for i in range(10):
        output = cnn(test_imgs[i])
        print(output)
