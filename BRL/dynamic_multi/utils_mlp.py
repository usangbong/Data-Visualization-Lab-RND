import datetime
import dgl
import numpy as np
import random
import torch
import torch.nn.functional as F

from dgl import model_zoo
from dgl.data.chem import smiles_to_bigraph, one_hot_encoding, RandomSplitter
from sklearn.metrics import roc_auc_score
from torch.utils.data import DataLoader
from dgl import model_zoo,DGLGraph
def set_random_seed(seed=0):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)

def chirality(atom):
    try:
        return one_hot_encoding(atom.GetProp('_CIPCode'), ['R', 'S']) + \
               [atom.HasProp('_ChiralityPossible')]
    except:
        return [False, False] + [atom.HasProp('_ChiralityPossible')]

class Meter(object):
    def __init__(self):
        #self.mask = []
        self.y_pred = []
        self.y_true = []

    def update(self, y_pred, y_true):
        self.y_pred.append(y_pred.detach().cpu())
        self.y_true.append(y_true.detach().cpu())
        #self.mask.append(mask.detach().cpu())
        
    def acc(self):
        y_pred = torch.cat(self.y_pred, dim=0)
        y_true = torch.cat(self.y_true, dim=0)
        
        correct = (y_pred == y_true).sum().item()
        score=100-100 * correct / len(y_pred)
        return score
    
    def l1_loss(self, reduction):
        #mask = torch.cat(self.mask, dim=0)
        y_pred = torch.cat(self.y_pred, dim=0)
        y_true = torch.cat(self.y_true, dim=0)
        n_tasks = y_true.shape[1]
        scores = []
        for task in range(n_tasks):
            #task_w = mask[:, task]
            task_y_true = y_true[:, task]#[task_w != 0]
            task_y_pred = y_pred[:, task]#[task_w != 0]
            scores.append(F.l1_loss(task_y_true, task_y_pred, reduction=reduction).item())
        return scores
    

    def compute_metric(self, metric_name, reduction='mean'):
        assert metric_name in ['acc','l1'], \
            'Expect metric name to be "acc", got {}'.format(metric_name)
        assert reduction in ['mean', 'sum']
        if metric_name == 'acc':
            return self.acc()
        if metric_name == 'l1':
            return self.l1_loss(reduction)




