import numpy as np
import pickle
import datetime
import random
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score
from torch.utils.data import DataLoader
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import dgl
from dgl import DGLGraph


def collate(data):
    graphs, labels_c,labels_a = map(list, zip(*data))
    bg = dgl.batch(graphs)
    labels_c=np.array(labels_c)
    labels_a=np.array(labels_a)
    #print('collate',labels.shape,labels[:,0].dtype,labels[:,1:].dtype)
    #return bg,[torch.from_numpy(labels[:,0]).long(),torch.from_numpy(labels[:,1:]).float()]#torch.from_numpy(labels).float()
    #print('collate',labels_c.shape,labels_a.shape)
    return bg,torch.from_numpy(labels_c).long(),torch.from_numpy(labels_a).float()#torch.from_numpy(labels).float()


class MLPDataset(Dataset):
    def __init__(self, data, target_cn, target_a,transform=None):
        self.data = torch.from_numpy(data).float()
        self.target_cn = torch.from_numpy(target_cn).long()
        self.target_a = torch.from_numpy(target_a).float()
        self.transform = transform
    def __getitem__(self, index):
        x = self.data[index]
        y_cn = self.target_cn[index]
        y_a = self.target_a[index]
        if self.transform:
            x = self.transform(x)
        return x, y_cn, y_a
    def __len__(self):
        return len(self.data)  


def load_dataset(args,network_name):
    for m in ["train", "val", "test"]:
        is_shuffle=False if m =='test' else True
        
        if network_name == "MLP":
            data_path_x= args['data_path_x']
            data_path_label_c=data_path_label_a=args['data_path_label']
            mode_dataset = MLPDataset(np.load(data_path_x+'t_'+m+'.npz')['arr_0'],
                                             np.load(data_path_label_c+'c_label_'+m+'.npz')['arr_0'],
                                             np.load(data_path_label_a+'a_label_'+m+'.npz')['arr_0'])
            locals()[m+'_loader'] = DataLoader(dataset=mode_dataset,
                                                  batch_size=args['batch_size'],
                                                  shuffle=is_shuffle,
                                                  pin_memory=True)
        elif network_name == "MPNNSmall":
            mode_dataset = MPNNSmallDataset(args,mode=m)
            locals()[m+'_loader'] = DataLoader(dataset=mode_dataset,
                                                  batch_size=args['batch_size'],
                                                  shuffle=is_shuffle,
                                                  collate_fn=collate,
                                                  pin_memory=True)
            
        else:
            print('error')
            
    return locals()['train_loader'],locals()['val_loader'],locals()['test_loader']#train_loader,val_loader,test_loader


class MPNNSmallDataset(object):
    def __init__(self, args, mode):
        super(MPNNSmallDataset, self).__init__()
        data_path_x = args['data_path_x']
        data_path_label = args['data_path_label']
        self.device=args['device']
        self.graphs = []
        self.features=np.load(args['data_path_x']+'n_'+mode+'.npz')['arr_0']#node feature
        self.edge_data=np.load(data_path_x+'edge_data.npz')['arr_0']
        self.edge_f=np.load(data_path_x+'edge_feature.npz')['arr_0']
        
        self.labels_c=np.load(data_path_label+'c_label_'+mode+'.npz')['arr_0'].astype('double')
        self.labels_a=np.load(data_path_label+'a_label_'+mode+'.npz')['arr_0'].astype('double')
        self._generate()
        
    def __len__(self):
        """Return the number of graphs in the dataset."""
        return len(self.graphs)

    def __getitem__(self, idx):
        return self.graphs[idx], self.labels_c[idx],self.labels_a[idx]
    
    def _generate(self):
        # preprocess
        for i in range(len(self.labels_c)):
            g = DGLGraph([(i,j) for i,j in self.edge_data])
            g.ndata['n_feat'] = torch.from_numpy(self.features[i]).float()
            g.edata['e_feat'] =  torch.from_numpy(self.edge_f).float()
            g = g.to(self.device)
            self.graphs.append(g)
            



