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


# python -u mlp_train.py --GPU_NUM 3| tee log/mlp.txt


parser = argparse.ArgumentParser(description='Molecule Regression')
parser.add_argument('--GPU_NUM', type=int)
parser.add_argument('--w1', type=float, default =1) #classification loss
parser.add_argument('--w2', type=float, default =1) #regression loss
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
args['data_path_x']='data/data_mlp/'
args['data_path_label']='data/label/'
args['model_save_path']='model_saved/mlp/'
# initialize the NN
model = Net()
model.to(args['device'])

loss_fn_cn =nn.CrossEntropyLoss(reduction='none')
loss_fn_a =nn.L1Loss(reduction='none')
optimizer = torch.optim.Adam(model.parameters(), lr=args['lr'])

#load dataset
train_loader,val_loader,test_loader=load_dataset(args,network_name='MLP')



###########################################################Training 시작
# initialize tracker for minimum validation loss
valid_loss_min = np.Inf  # set initial "min" to infinity
#number of epochs to train the model
ep_list=[2000,4000,6000] #save time
n_epochs = args['num_epochs']
for epoch in range(n_epochs):
    st=time.time()
    train_loss = 0
    valid_loss = 0
    train_meter_cn = Meter()
    train_meter_a = Meter()
    eval_meter_cn = Meter()
    eval_meter_a = Meter()
    
    model.train()
    for data,label_cn,label_a in train_loader:
        data = data.to(args['device'])
        label_cn = label_cn.to(args['device'])
        label_a = label_a.to(args['device'])
        
        optimizer.zero_grad()
        output = model(data)
        output_cn = output[0].to(args['device'])
        output_a = output[1].to(args['device'])
        # loss
        loss_cn = (loss_fn_cn(output_cn, label_cn).float()).mean()
        loss_area = (loss_fn_a(output_a,label_a).float()).mean()
        loss=args['w1']*loss_cn+args['w2']*loss_area
        loss.backward(); del loss
        optimizer.step()
        #meter update
        _, output_cn = torch.max(output_cn, 1)
        train_meter_cn.update(output_cn, label_cn)
        train_meter_a.update(output_a, label_a)
        
    # validdation
    model.eval()  
    model_result=[]
    targets = []
    total_score=[]
    for data,label_cn,label_a in val_loader:
        data = data.to(args['device'])
        label_cn = label_cn.to(args['device'])
        label_a = label_a.to(args['device'])
        output = model(data)
        output_cn = output[0].to(args['device'])
        output_a = output[1].to(args['device'])
        #validation loss 
        loss_cn = (loss_fn_cn(output_cn, label_cn).float()).mean()
        loss_area = (loss_fn_a(output_a,label_a).float()).mean()
        loss=args['w1']*loss_cn+args['w2']*loss_area
        total_score.append(loss.item())
        #meter update
        _, output_cn = torch.max(output_cn, 1)
        eval_meter_cn.update(output_cn, label_cn)
        eval_meter_a.update(output_a, label_a)
    
    train_loss_a=np.mean(train_meter_a.compute_metric('rmse'))#train_meter.compute_metric('acc')
    train_loss_cn = train_meter_cn.compute_metric('acc')
    valid_loss_a=np.mean(eval_meter_a.compute_metric('rmse'))
    valid_loss_cn = eval_meter_cn.compute_metric('acc')
    print('Epoch: {}, Training area: {:.6f},  acc: {:.3f}, Validation Loss: {:.6f}, acc: {:.3f}, '
          'time{:.1f}'.format(epoch+1, train_loss_a, train_loss_cn, valid_loss_a,valid_loss_cn, time.time()-st))
    
    # save model
    valid_loss=np.average(total_score)#valid_loss_cn
    if valid_loss < valid_loss_min:
        print('***Validation loss decreased ({:.6f} --> {:.6f}).  Saving model ...'.format(valid_loss_min,valid_loss))
        torch.save({'model_state_dict': model.state_dict(),
            'optimizer': optimizer.state_dict()}, args['model_save_path']+'model.pth')
        valid_loss_min = valid_loss
        
torch.save({'model_state_dict': model.state_dict(),
            'optimizer': optimizer.state_dict()}, args['model_save_path']+'last.pth')
###########################################################Training 종료



###########################################################결과 확인
state=torch.load(args['model_save_path']+'model.pth') 
model.load_state_dict(state['model_state_dict'])
#optimizer.load_state_dict(state['optimizer'])
model.eval()
cn_p,cn_t,area_p,area_t=predict_mlp(args,model,test_loader,task_name='mtl')
getting_results(cn_p,cn_t,area_p,area_t,show_plot=False,f_name='mlp_mtl_'+args['sensor_no'])