import numpy as np
import time
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from dgl import DGLGraph
import math
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import seaborn as sn
import pandas as pd
from sklearn import metrics
import collections
import torch.nn as nn
import torch.nn.functional as F
from utils import *
from load_data import *
from network import *
import argparse

# python -u mlp_single_train.py --GPU_NUM 0 --task_name classification | tee log/mlp_classification_default.txt;python -u mlp_single_train.py --GPU_NUM 2 --task_name regression | tee log/mlp_regression_default.txt;

parser = argparse.ArgumentParser(description='Onlye Classification')
parser.add_argument('--GPU_NUM', type=int)
parser.add_argument('--task_name')
parser.add_argument('--sensor_no',default='default_sensor_no')
args = parser.parse_args()
args = args.__dict__
training_setting= {
    'random_seed': 0,
    'batch_size': 32,#64,#
    'num_epochs': 10000,#900,
    'lr': 0.0001,#0.001,#
}
args.update(training_setting)
args['device']  = torch.device("cuda:"+str(args['GPU_NUM']) if torch.cuda.is_available() else 'cpu')    
args['data_path_label']='data/label/'
args['data_path_x']='data/data_mlp/'
args['model_save_path']='model_saved/mlp/'+args['task_name']+'_'
# initialize the NN
if args['task_name'] == 'classification':
    model = MLPClassification()
    loss_fn =nn.CrossEntropyLoss(reduction='none')
if args['task_name'] == 'regression':
    model = MLPRegression()
    loss_fn =nn.L1Loss(reduction='none')
model.to(args['device'])
optimizer = torch.optim.Adam(model.parameters(), lr=args['lr'])

#load dataset
train_loader,val_loader,test_loader=load_dataset(args,network_name='MLP')

#training
valid_loss_min = np.Inf
n_epochs = args['num_epochs']
for epoch in range(n_epochs):
    st=time.time()
    train_loss = 0
    valid_loss = 0
    train_meter = Meter()
    eval_meter = Meter()
    
    model.train()
    for data,label_cn,label_a in train_loader:
        data = data.to(args['device'])
        label_cn = label_cn.to(args['device'])
        label_a = label_a.to(args['device'])
        
        optimizer.zero_grad()
        output = model(data)
        output = output.to(args['device'])
        # loss
        
        #meter update
        if args['task_name'] == 'classification':
            loss = (loss_fn(output, label_cn).float()).mean()
            _, output = torch.max(output, 1)
            train_meter.update(output, label_cn)
        elif args['task_name'] == 'regression':
            loss = (loss_fn(output,label_a).float()).mean()
            train_meter.update(output, label_a)
        loss.backward()
        optimizer.step()
        
    # validdation
    model.eval()  
    model_result=[]
    targets = []
    for data,label_cn,label_a in val_loader:
        data = data.to(args['device'])
        label_cn = label_cn.to(args['device'])
        label_a = label_a.to(args['device'])
        output = model(data)
        output = output.to(args['device'])
        if args['task_name'] == 'classification':
            _, output = torch.max(output, 1)
            eval_meter.update(output, label_cn)
        elif args['task_name'] == 'regression':
            eval_meter.update(output, label_a)
    if args['task_name'] == 'classification':
        train_loss = train_meter.compute_metric('acc')
        valid_loss = eval_meter.compute_metric('acc')
    elif args['task_name'] == 'regression':
        train_loss = np.mean(train_meter.compute_metric('rmse'))
        valid_loss = np.mean(eval_meter.compute_metric('rmse'))
    print('Epoch: {}, Training sc: {:.3f}, Validation sc: {:.3f}, '
          'time{:.1f}'.format(epoch+1, train_loss, valid_loss, time.time()-st))
    
    # save model
    if valid_loss < valid_loss_min:
        print('***Validation loss decreased ({:.6f} --> {:.6f}).  Saving model ...'.format(valid_loss_min,valid_loss))
        torch.save({'model_state_dict': model.state_dict(),
            'optimizer': optimizer.state_dict()}, args['model_save_path']+'model.pth')
        valid_loss_min = valid_loss
        
torch.save({'model_state_dict': model.state_dict(),
            'optimizer': optimizer.state_dict()}, args['model_save_path']+'last.pth')

