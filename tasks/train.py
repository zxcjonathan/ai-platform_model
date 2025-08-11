# tasks/train.py

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms

# 這裡假設你的 train_model 函數已經存在
def train_model():
    """
    訓練一個簡單的 PyTorch 模型，並回傳模型儲存的路徑。
    """
    # 準備資料
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)

    # 建立模型
    class SimpleNN(nn.Module):
        def __init__(self):
            super(SimpleNN, self).__init__()
            self.flatten = nn.Flatten()
            self.fc1 = nn.Linear(28*28, 128)
            self.relu = nn.ReLU()
            self.fc2 = nn.Linear(128, 10)

        def forward(self, x):
            x = self.flatten(x)
            x = self.fc1(x)
            x = self.relu(x)
            x = self.fc2(x)
            return x

    model = SimpleNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    # 訓練模型
    print("訓練中...")
    for epoch in range(2):
        for i, (images, labels) in enumerate(train_loader):
            outputs = model(images)
            loss = criterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print(f"訓練中... Epoch: {epoch + 1}, Loss: {loss.item():.4f}")

    print("訓練完成！儲存模型...")
    # 儲存模型
    model_path = "./model.pth"
    torch.save(model.state_dict(), model_path)
    print(f"模型已儲存至 {model_path}")
    
    # 任務執行完畢，回傳模型儲存的路徑
    return model_path