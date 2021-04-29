import numpy as np
import time
import math
import networkx as nx
import matplotlib.pyplot as plt
from utils import *
from load_data import *
#from network import *
import argparse
import seaborn as sn
import pandas as pd
from sklearn import metrics
import collections
import torch
import torch.nn as nn
from torch.nn import BCEWithLogitsLoss
from torch.utils.data import DataLoader
from dgl import DGLGraph
import sys#; sys.argv=['']; del sys
import os
from dgllife.model import MPNNPredictor

# python -u mpnn_single_train.py --GPU_NUM 2 --task_name classification| tee log/mpnn_classification_case_default.txt;python -u mpnn_single_train.py --GPU_NUM 2 --task_name regression| tee log/mpnn_regression_case_default.txt;
parser = argparse.ArgumentParser(description='MPNN Single-task')
parser.add_argument('--GPU_NUM', type=int)
parser.add_argument('--task_name')
parser.add_argument('--sensor_no',default='default_sensor_no')
parser.add_argument('--sensorgemotry',default='sensorgemotry')

args = parser.parse_args()
args = args.__dict__

training_setting= {
    'random_seed': 0,
    'batch_size': 32,#64,#
    'num_epochs': 2000,#900,
    'node_in_feats': 1,
    'edge_in_feats': 1,
    #'output_dim': 120,
    'lr': 0.0001,#0.001,#
    'patience': 300,#20,
    'metric_name': 'l1',#'roc_auc',#
    'weight_decay': 0,
    #'n_task':40,
}
args.update(training_setting)

args['model_save_path']='model_saved/mpnn/'+args['task_name']+'_default_sensor_'
args['data_path_x']='data/data_mpnn_default_sensor/'

args['device']  = torch.device("cuda:"+str(args['GPU_NUM']) if torch.cuda.is_available() else 'cpu')
args['data_path_label']='data/label/'
args['n_task'] = 40 if args['task_name']=='classification' or args['task_name']=='regression_all' else 1
set_random_seed(args['random_seed'])
print('***n_task',args['n_task'])

#load dataset
train_loader,val_loader,test_loader=load_dataset(args,network_name='MPNNSmall')
#network
model = MPNNPredictor(node_in_feats=args['node_in_feats'],
              edge_in_feats=args['edge_in_feats'],
                 node_out_feats=64,#32,##node hidden dim
                 edge_hidden_feats=128,#32,#
                 n_tasks=args['n_task'],
                 num_step_message_passing=4,#6,
                 num_step_set2set=4,#6,
                 num_layer_set2set=2)#3):)
loss_fn = nn.CrossEntropyLoss() if args['task_name']=='classification' else nn.L1Loss(reduction='none')
optimizer = torch.optim.Adam(model.parameters(), lr=args['lr'], weight_decay=args['weight_decay'])
stopper = EarlyStopping(mode='lower', patience=args['patience'],
                    filename=args['model_save_path']+'early_stop.pth')
model.to(args['device'])

for epoch in range(args['num_epochs']):#250+100
    st=time.time()
    if epoch%5000==0 and epoch!=0:
        print('save')
        torch.save({'model_state_dict': model.state_dict(),
            'optimizer': optimizer.state_dict()}, args['model_save_path']+str(epoch)+'.pth')
    # Train
    run_a_train_epoch_single(args, epoch, model, train_loader, loss_fn, optimizer,task_name=args['task_name'])
    # Validation and early stop
    val_sc = run_an_eval_epoch_single(args, model, val_loader,task_name=args['task_name'])
    early_stop = stopper.step(val_sc, model,optimizer)
    print('epoch {:d}/{:d}, validation score(%) {:.4f}, best validation {:.4f}, time{:.1f}'.format(
        epoch + 1, args['num_epochs'], val_sc, stopper.best_score,time.time()-st))
        
torch.save({'model_state_dict': model.state_dict(),
        'optimizer': optimizer.state_dict()}, args['model_save_path']+'last.pth')

    
    
