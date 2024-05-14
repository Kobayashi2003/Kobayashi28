from PIL import Image
from torch.utils.data import Dataset

from typing import Any

class MyDataset(Dataset):

    def __init__(self, data: list, label: list, transform: object = None) -> None:
        self.data = data
        self.label = label
        self.transform = transform

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index: int) -> Any:
        img = Image.open(self.data[index])
        label = self.label[index]
        if self.transform:
            img = self.transform(img)
        return img, label