import numpy as np
import time
import math
import networkx as nx
import matplotlib.pyplot as plt
from utils import *
from load_data import *
from network import MPNNPredictor
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


# python -u mpnn_small_train.py --GPU_NUM 3 | tee log/mpnn_case_default.txt

parser = argparse.ArgumentParser(description='Molecule Regression')
parser.add_argument('--GPU_NUM', type=int)
parser.add_argument('--w1', type=float,default=1)
parser.add_argument('--w2', type=float,default=1)
parser.add_argument('--sensor_no',default='default_sensor_no')

args = parser.parse_args().__dict__
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
    'n_task':41,
}
args.update(training_setting)

args['data_path_x']='data/data_mpnn_default_sensor/'
args['model_save_path']='model_saved/mpnn/default_'

args['device']  = torch.device("cuda:"+str(args['GPU_NUM']) if torch.cuda.is_available() else 'cpu')
args['data_path_label']='data/label/'
set_random_seed(args['random_seed'])
### Load dataset
train_loader,val_loader,test_loader=load_dataset(args,network_name='MPNNSmall')

model = MPNNPredictor(node_in_feats=args['node_in_feats'],
                      edge_in_feats=args['edge_in_feats'])#,
#                       node_out_feats=32,
#                       edge_hidden_feats=64,
#                       num_step_message_passing=4,
#                       num_step_set2set=2,
#                       num_layer_set2set=1)
#loss_fn =BCEWithLogitsLoss()#nn.L1Loss(reduction='none')
loss_fn_cablenumber =nn.CrossEntropyLoss()
loss_fn_area =nn.L1Loss(reduction='none')
optimizer = torch.optim.Adam(model.parameters(), lr=args['lr'], weight_decay=args['weight_decay'])
stopper = EarlyStopping(mode='lower', patience=args['patience'],filename=args['model_save_path']+'early_stop.pth')
model.to(args['device'])

for epoch in range(args['num_epochs']):#250+100
    st=time.time()
    if epoch%5000==0 and epoch!=0:
        print('save')
        torch.save({'model_state_dict': model.state_dict(),
            'optimizer': optimizer.state_dict()}, args['model_save_path']+str(epoch)+'.pth')
    # Train
    run_a_train_epoch_cr(args, epoch, model, train_loader, loss_fn_cablenumber, loss_fn_area, optimizer)
    # Validation and early stop
    val_score,val_score_reg,val_acc = run_an_eval_epoch_cr(args, model, val_loader, loss_fn_cablenumber, loss_fn_area)
    early_stop = stopper.step(val_score, model,optimizer)
    print('epoch {:d}/{:d}, validation {} {:.4f}, accuracy(%) {:.4f}, best validation {} {:.4f}, time{:.1f}'.format(
        epoch + 1, args['num_epochs'], args['metric_name'], val_score_reg,val_acc,args['metric_name'], stopper.best_score,time.time()-st))
    #if early_stop: break
torch.save({'model_state_dict': model.state_dict(),
        'optimizer': optimizer.state_dict()}, args['model_save_path']+'last.pth')

#evaluation
state=torch.load(args['model_save_path']+'early_stop.pth') 
model.load_state_dict(state['model_state_dict'])
model.eval()
cn_p,cn_t,area_p,area_t=predict_mpnn(args,model,test_loader)
getting_results(cn_p,cn_t,area_p,area_t,show_plot=False,f_name='mpnn_mtl_random_')


    
    
