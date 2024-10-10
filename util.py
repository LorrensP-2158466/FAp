import torch
import numpy as np

def torch_intersect(basket, items):
    basket = basket.cuda()
    items = items.cuda()
    items = items.unique()
        
    return torch.tensor(np.intersect1d(basket.cpu().numpy(), items.cpu().numpy()))
