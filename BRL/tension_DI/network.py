import numpy as np
import pickle
import datetime
import torch
import torch.nn.functional as F
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import dgl
from dgl.nn.pytorch import Set2Set
from dgllife.model import MPNNGNN


# pylint: disable=W0221
class MPNNPredictor(nn.Module):
    """MPNN for regression and classification on graphs.
    MPNN is introduced in `Neural Message Passing for Quantum Chemistry
    <https://arxiv.org/abs/1704.01212>`__.
    Parameters
    ----------
    node_in_feats : int
        Size for the input node features.
    edge_in_feats : int
        Size for the input edge features.
    node_out_feats : int
        Size for the output node representations. Default to 64.
    edge_hidden_feats : int
        Size for the hidden edge representations. Default to 128.
    n_tasks : int
        Number of tasks, which is also the output size. Default to 1.
    num_step_message_passing : int
        Number of message passing steps. Default to 6.
    num_step_set2set : int
        Number of set2set steps. Default to 6.
    num_layer_set2set : int
        Number of set2set layers. Default to 3.
    """
    def __init__(self,
                 node_in_feats=3,
                 edge_in_feats=6,
                 node_out_feats=64,#32,##node hidden dim
                 edge_hidden_feats=128,#32,#
                 n_tasks=1,
                 num_step_message_passing=4,#6,
                 num_step_set2set=4,#6,
                 num_layer_set2set=2):#3):
        super(MPNNPredictor, self).__init__()

        self.gnn = MPNNGNN(node_in_feats=node_in_feats,
                           node_out_feats=node_out_feats,
                           edge_in_feats=edge_in_feats,
                           edge_hidden_feats=edge_hidden_feats,
                           num_step_message_passing=num_step_message_passing)
        self.readout = Set2Set(input_dim=node_out_feats,
                               n_iters=num_step_set2set,
                               n_layers=num_layer_set2set)
        #self.predict = nn.Sequential(
        #    nn.Linear(2 * node_out_feats, node_out_feats),
        #    nn.ReLU(),
        #    nn.Linear(node_out_feats, n_tasks)
        #)
        #v0
        #self.lin1 = nn.Linear(2 * node_out_feats, node_out_feats)
        #self.lin_last1 = nn.Linear(node_out_feats, 40)
        #self.lin_last2 = nn.Linear(node_out_feats, 1)
        #v1
        self.predict = nn.Sequential(
            nn.Linear(2 * node_out_feats, node_out_feats),
            nn.ReLU()
        )
        self.lin_last1 = nn.Linear(node_out_feats, 40)
        self.lin_last2 = nn.Linear(node_out_feats, 1)

    def forward(self, g, node_feats, edge_feats):
        """Graph-level regression/soft classification.
        Parameters
        ----------
        g : DGLGraph
            DGLGraph for a batch of graphs.
        node_feats : float32 tensor of shape (V, node_in_feats)
            Input node features.
        edge_feats : float32 tensor of shape (E, edge_in_feats)
            Input edge features.
        Returns
        -------
        float32 tensor of shape (G, n_tasks)
            Prediction for the graphs in the batch. G for the number of graphs.
        """
        node_feats = self.gnn(g, node_feats, edge_feats)
        graph_feats = self.readout(g, node_feats)
        #return self.predict(graph_feats)
        #v0
        #out = F.relu(self.lin1(graph_feats))
        #out1=self.lin_last1(out)#for classification
        #out2=self.lin_last2(out)#for regression
        #v1
        out = self.predict(graph_feats)
        out1=self.lin_last1(out)#for classification
        out2=self.lin_last2(out)#for regression
        return [out1,out2]
        
    
# define NN architecture
class Net(nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        
        self.fc1 = nn.Linear(10, 2048)#1024
        self.fc2 = nn.Linear(2048,2048)
        self.fc3 = nn.Linear(2048,2048)
        self.fc4 = nn.Linear(2048,2048)
        #self.fc5 = nn.Linear(2048,2048)
        #self.fc6 = nn.Linear(2048,2048)
        
        #self.fc_last1_1 = nn.Linear(4096,4096)
        #self.fc_last1_2 = nn.Linear(4096,4096)
        #self.fc_last1_3 = nn.Linear(4096,4096)
        
        #self.fc_last2_1 = nn.Linear(4096,4096)
        #self.fc_last2_2 = nn.Linear(4096,4096)
        
        
        self.fc_output1 = nn.Linear(2048,40)
        self.fc_output2 = nn.Linear(2048,1)
        self.droput = nn.Dropout(0.2)
        #self.sig=nn.Sigmoid()
        
    def forward(self,x):
        x = F.relu(self.fc1(x))
        x = self.droput(x)
        x = F.relu(self.fc2(x))
        x = self.droput(x)
        x = F.relu(self.fc3(x))
        x = self.droput(x)
        x = F.relu(self.fc4(x))
        x = self.droput(x)
        
        #x = F.relu(self.fc5(x))
        #x = F.relu(self.fc6(x))
        
        #x1 = F.relu(self.fc_last1_1(x))
        #x1 = F.relu(self.fc_last1_2(x1))
        #x1 = F.relu(self.fc_last1_3(x1))
        
        #x2 = F.relu(self.fc_last2_1(x))
        #x2 = F.relu(self.fc_last2_2(x2))
        
        x1 = self.fc_output1(x)
        x2 = self.fc_output2(x)#self.sig(self.fc_output2(x2))#x2 = self.fc4_2(x)
        return [x1,x2]#x


class MLPClassification(nn.Module):
    def __init__(self):
        super(MLPClassification,self).__init__()
        
        self.fc1 = nn.Linear(10, 2048)#1024
        self.fc2 = nn.Linear(2048,2048)
        self.fc3 = nn.Linear(2048,2048)
        self.fc4 = nn.Linear(2048,2048)
        
        self.fc_output1 = nn.Linear(2048,40)
        #self.fc_output2 = nn.Linear(2048,1)
        self.droput = nn.Dropout(0.2)
        #self.sig=nn.Sigmoid()
        
    def forward(self,x):
        x = F.relu(self.fc1(x))
        x = self.droput(x)
        x = F.relu(self.fc2(x))
        x = self.droput(x)
        x = F.relu(self.fc3(x))
        x = self.droput(x)
        x = F.relu(self.fc4(x))
        x = self.droput(x)
        
        x1 = self.fc_output1(x)
        #x2 = self.fc_output2(x)
        return x1

class MLPRegression(nn.Module):
    def __init__(self):
        super(MLPRegression,self).__init__()
        
        self.fc1 = nn.Linear(10, 2048)#1024
        self.fc2 = nn.Linear(2048,2048)
        self.fc3 = nn.Linear(2048,2048)
        self.fc4 = nn.Linear(2048,2048)
        
        #self.fc_output1 = nn.Linear(2048,40)
        self.fc_output2 = nn.Linear(2048,1)
        self.droput = nn.Dropout(0.2)
        #self.sig=nn.Sigmoid()
        
    def forward(self,x):
        x = F.relu(self.fc1(x))
        x = self.droput(x)
        x = F.relu(self.fc2(x))
        x = self.droput(x)
        x = F.relu(self.fc3(x))
        x = self.droput(x)
        x = F.relu(self.fc4(x))
        x = self.droput(x)
        
        #x1 = self.fc_output1(x)
        x2 = self.fc_output2(x)
        return x2
