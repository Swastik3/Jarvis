from torchvision.models import efficientnet_b7, EfficientNet_B7_Weights, efficientnet_b0, EfficientNet_B0_Weights
import torch.nn as nn
import torch
import time

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class HandTracker(nn.Module):
    def __init__(self):
        super().__init__()
        self.efficientnetb7 = efficientnet_b7(weights=EfficientNet_B7_Weights.DEFAULT) # inputsize: (633,600)
        self.efficientnetb0 = efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT) # inputsize: (224,224)
        pass

    def forward(self, x):
        return self.efficientnetb0(x) 

def main():
    model = HandTracker().cuda()
    print(model)
    t1 = time.time()
    x = torch.rand(1,3, 633, 600, device=device)
    t2 = time.time()
    print(t2-t1)
    print(x.shape)
    print(model(x).shape)

if __name__ == "__main__":
    main()
    