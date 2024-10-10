import torch
import numpy as np

def torch_intersect(t1, t2):
    t1 = t1.cuda()
    t2 = t2.cuda()
    t1 = t1.unique()
    t2 = t2.unique()
        
    return torch.tensor(np.intersect1d(t1.cpu().numpy(), t2.cpu().numpy()))
