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
import sklearn.metrics as metrics
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import dgl
from dgl import DGLGraph

def set_random_seed(seed=0):
    """Set random seed.

    Parameters
    ----------
    seed : int
        Random seed to use
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)


def regress(args, model, bg):
    h = bg.ndata.pop('n_feat')
    e = bg.edata.pop('e_feat')
    h, e = h.to(args['device']), e.to(args['device'])
    return model(bg, h, e)


def run_a_train_epoch_cr(args, epoch, model, data_loader,
                      loss_criterion_cablenumber,loss_criterion_area, optimizer):
    model.train()
    train_meter = Meter()
    correct=0
    total=0
    for batch_id, batch_data in enumerate(data_loader):
        bg, labels_cablenumber,labels_area = batch_data
        labels_cablenumber = labels_cablenumber.to(args['device'])
        labels_area = labels_area.to(args['device'])
        labels=[labels_cablenumber,labels_area]
        prediction = regress(args, model, bg)
        
        loss_cablenumber = (loss_criterion_cablenumber(prediction[0], labels_cablenumber).float()).mean()
        loss_area = (loss_criterion_area(prediction[1],labels_area).float()).mean()
        loss=(args['w1']*loss_cablenumber+args['w2']*loss_area)
       
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        train_meter.update(prediction[1], labels_area)
        
        _, predicted = torch.max(prediction[0].data, 1)
        total += labels_cablenumber.size(0)
        correct += (predicted == labels_cablenumber).sum().item();del predicted
        
    total_score_acc=100-100 * correct / total
    total_score = np.mean(train_meter.compute_metric(args['metric_name']))
    print('epoch {:d}/{:d}, training {} {:.4f} / accuracy(%) {:.4f}'.format(
        epoch + 1, args['num_epochs'], args['metric_name'], total_score, total_score_acc)) 
    #print('epoch {:d}/{:d}, training total_score_acc {:.4f}'.format(epoch + 1, args['num_epochs'], total_score_acc)) 


def run_an_eval_epoch_cr(args, model, data_loader,loss_criterion_cablenumber,loss_criterion_area):
    model.eval()
    eval_meter = Meter()
    correct=0
    total=0
    total_score=[]
    with torch.no_grad():
        for batch_id, batch_data in enumerate(data_loader):
            bg, labels_cablenumber,labels_area = batch_data
            labels_cablenumber = labels_cablenumber.to(args['device'])
            labels_area = labels_area.to(args['device'])
            labels=[labels_cablenumber,labels_area]
            prediction = regress(args, model, bg)
            
            loss_cablenumber = (loss_criterion_cablenumber(prediction[0], labels_cablenumber).float()).mean()
            loss_area = (loss_criterion_area(prediction[1],labels_area).float()).mean()
            loss=(args['w1']*loss_cablenumber+args['w2']*loss_area)
            total_score.append(loss.item())
            
            eval_meter.update(prediction[1], labels_area)
            
            _, predicted = torch.max(prediction[0].data, 1)
            total += labels_cablenumber.size(0)
            correct += (predicted == labels_cablenumber).sum().item();del predicted
        total_score_acc=100-100 * correct / total
        total_score_reg = np.mean(eval_meter.compute_metric(args['metric_name']))
        total_score = np.average(total_score)
    return total_score,total_score_reg,total_score_acc


class Meter(object):
    """Track and summarize model performance on a dataset for
    (multi-label) binary classification."""
    def __init__(self):
        #self.mask = []
        self.y_pred = []
        self.y_true = []

    def update(self, y_pred, y_true):
        """Update for the result of an iteration

        Parameters
        ----------
        y_pred : float32 tensor
            Predicted molecule labels with shape (B, T),
            B for batch size and T for the number of tasks
        y_true : float32 tensor
            Ground truth molecule labels with shape (B, T)
        mask : float32 tensor
            Mask for indicating the existence of ground
            truth labels with shape (B, T)
        """
        self.y_pred.append(y_pred.detach().cpu())
        self.y_true.append(y_true.detach().cpu())
        #self.mask.append(mask.detach().cpu())
        
    def acc(self):
        y_pred = torch.cat(self.y_pred, dim=0)
        y_true = torch.cat(self.y_true, dim=0)
        #print('y_pred',y_pred.shape,'y_true',y_true.shape)
        
        correct = (y_pred == y_true).sum().item()
        score=100-100 * correct / len(y_pred)
        return score
    
    def rmse(self):
        #mask = torch.cat(self.mask, dim=0)
        y_pred = torch.cat(self.y_pred, dim=0)
        y_true = torch.cat(self.y_true, dim=0)
        n_data, n_tasks = y_true.shape
        scores = []
        for task in range(n_tasks):
            #task_w = mask[:, task]
            task_y_true = y_true[:, task]#[task_w != 0]
            task_y_pred = y_pred[:, task]#[task_w != 0]
            scores.append(np.sqrt(F.mse_loss(task_y_pred, task_y_true).cpu().item()))
        return scores
    
    def l1_loss(self, reduction):
        """Compute l1 loss for each task.

        Returns
        -------
        list of float
            l1 loss for all tasks
        reduction : str
            * 'mean': average the metric over all labeled data points for each task
            * 'sum': sum the metric over all labeled data points for each task
        """
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
    
    
    def f1score(self,threshold=0.0):
        #print('self.y_pred',len(self.y_pred))
        pred=torch.cat(self.y_pred, dim=0).numpy()
        target = torch.cat(self.y_true, dim=0).numpy()
        
        pred = np.array(pred > threshold, dtype=float)
        return {#'micro/precision': precision_score(y_true=target, y_pred=pred, average='micro'),
                #'micro/recall': recall_score(y_true=target, y_pred=pred, average='micro'),
                'micro/f1': f1_score(y_true=target, y_pred=pred, average='micro'),
                #'macro/precision': precision_score(y_true=target, y_pred=pred, average='macro'),
                #'macro/recall': recall_score(y_true=target, y_pred=pred, average='macro'),
                'macro/f1': f1_score(y_true=target, y_pred=pred, average='macro'),
                #'samples/precision': precision_score(y_true=target, y_pred=pred, average='samples'),
                #'samples/recall': recall_score(y_true=target, y_pred=pred, average='samples'),
                'samples/f1': f1_score(y_true=target, y_pred=pred, average='samples'),
                }
    

    def compute_metric(self, metric_name, reduction='mean'):
        """Compute metric for each task.

        Parameters
        ----------
        metric_name : str
            Name for the metric to compute.
        reduction : str
            Only comes into effect when the metric_name is l1_loss.
            * 'mean': average the metric over all labeled data points for each task
            * 'sum': sum the metric over all labeled data points for each task

        Returns
        -------
        list of float
            Metric value for each task
        """
        assert metric_name in ['acc','rmse','l1','f1score'], \
            'Expect metric name to be "acc", got {}'.format(metric_name)
        assert reduction in ['mean', 'sum']
        if metric_name == 'acc':
            return self.acc()
        if metric_name == 'rmse':
            return self.rmse()
        if metric_name == 'l1':
            return self.l1_loss(reduction)
        if metric_name == 'f1score':
            return self.f1score()

class EarlyStopping(object):
    """Early stop performing

    Parameters
    ----------
    mode : str
        * 'higher': Higher metric suggests a better model
        * 'lower': Lower metric suggests a better model
    patience : int
        Number of epochs to wait before early stop
        if the metric stops getting improved
    filename : str or None
        Filename for storing the model checkpoint
    """
    def __init__(self, mode='higher', patience=10, filename=None):
        if filename is None:
            dt = datetime.datetime.now()
            filename = 'model_saved/early_stop_{}_{:02d}-{:02d}-{:02d}.pth'.format(
                dt.date(), dt.hour, dt.minute, dt.second)

        assert mode in ['higher', 'lower']
        self.mode = mode
        if self.mode == 'higher':
            self._check = self._check_higher
        else:
            self._check = self._check_lower

        self.patience = patience
        self.counter = 0
        self.filename = filename
        self.best_score = None
        self.early_stop = False

    def _check_higher(self, score, prev_best_score):
        return (score > prev_best_score)

    def _check_lower(self, score, prev_best_score):
        return (score < prev_best_score)

    def step(self, score, model,optimizer):
        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(model,optimizer)
        elif self._check(score, self.best_score):
            self.best_score = score
            self.save_checkpoint(model,optimizer)
            self.counter = 0
        else:
            self.counter += 1
            print(
                f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        return self.early_stop

    def save_checkpoint(self, model,optimizer):
        '''Saves model when the metric on the validation set gets improved.'''
        torch.save({'model_state_dict': model.state_dict(),
            'optimizer': optimizer.state_dict()}, self.filename)

    def load_checkpoint(self, model):
        '''Load model saved with early stopping.'''
        model.load_state_dict(torch.load(self.filename)['model_state_dict'])


def predict_mlp(args,model,data_loader,task_name='mtl'):
    model.eval()
    cn_p=[];area_p=[];cn_t=[];area_t=[]
    for data,label_cn,label_a in data_loader:
        data = data.to(args['device'])
        label_cn = label_cn.to(args['device'])
        label_a = label_a.to(args['device'])
        # forward pass: compute predicted outputs by passing inputs to the model
        output = model(data)
        if task_name=='mtl':
            output_cn = output[0].to(args['device'])
            output_a = output[1].to(args['device'])
        elif task_name=='classification':
            output_cn = output.to(args['device'])
        elif task_name=='regression':
            output_a = output.to(args['device'])
        if task_name == 'mtl' or task_name == 'classification':
            cn_p.append(output_cn.cpu().detach().numpy())
        if task_name == 'mtl' or task_name == 'regression':
            area_p.append(output_a.cpu().detach().numpy())
        cn_t.append(label_cn.cpu().detach().numpy())
        area_t.append(label_a.cpu().detach().numpy())
    cn_t=np.concatenate(cn_t,axis=0)
    area_t=np.concatenate(area_t,axis=0)
    return_list=['',cn_t,'',area_t]
    if task_name == 'mtl' or task_name == 'classification':
        cn_p=np.concatenate(cn_p,axis=0)
        cn_p=np.argmax(cn_p,axis=1)
        return_list[0]=cn_p
    if task_name == 'mtl' or task_name == 'regression':
        area_p=np.concatenate(area_p,axis=0)
        return_list[2]=area_p
    return return_list#cn_p,cn_t,area_p,area_t

def predict_mpnn(args,model,data_loader,task_name='mtl'):
    model.eval()
    cn_p=[];area_p=[];cn_t=[];area_t=[]
    with torch.no_grad():
        for batch_id, batch_data in enumerate(data_loader):
            bg, labels_cablenumber,labels_area = batch_data
            labels_cablenumber = labels_cablenumber.to(args['device'])
            labels_area = labels_area.to(args['device'])
            #labels=[labels_cablenumber,labels_area]
            cn_t.append(labels_cablenumber.cpu().detach().numpy())
            area_t.append(labels_area.cpu().detach().numpy())
            prediction = regress(args, model, bg)
            if task_name=='mtl':
                cn_p.append(prediction[0].cpu().detach().numpy())
                area_p.append(prediction[1].cpu().detach().numpy())
            elif task_name=='classification':
                cn_p.append(prediction.cpu().detach().numpy())
            elif task_name=='regression':
                area_p.append(prediction.cpu().detach().numpy())
    cn_t=np.concatenate(cn_t,axis=0)
    area_t=np.concatenate(area_t,axis=0)
    return_list=['',cn_t,'',area_t]
    if task_name == 'mtl' or task_name == 'classification':
        cn_p=np.concatenate(cn_p,axis=0)
        cn_p=np.argmax(cn_p,axis=1)
        return_list[0]=cn_p
    if task_name == 'mtl' or task_name == 'regression':
        area_p=np.concatenate(area_p,axis=0)
        return_list[2]=area_p
    return return_list


def getting_results_regression_plot(y_t,y_p,f_name='results'):
    #for i in range(len(plot_label)):
    #    idx=np.where(plot_label==i)[0]
    #    plt.plot(y_t.flatten()[idx],y_p.flatten()[idx],'.',alpha=0.7)
    plt.plot(y_t.flatten(),y_p.flatten(),'.',color='dimgrey',alpha=0.7)
    plt.ylim(-0.1,1.1)
    plt.xlim(-0.1,1.1)
    #plt.xlabel('actual')
    #plt.ylabel('pred')
    plt.grid()
    plt.savefig('images/'+f_name+'.png', bbox_inches = 'tight', transparent=True)
    plt.show()


def getting_results_regression(y_t,y_p,show_plot=False,f_name='results'):
    mae = metrics.mean_absolute_error(y_t, y_p)
    mse = metrics.mean_squared_error(y_t, y_p)
    corr = np.corrcoef(y_t.flatten(),y_p.flatten())[0,1]
    rmse=np.sqrt(mse)
    print('---mae, rmse, corr')
    print("{:0.4f}".format(mae))
    print("{:0.4f}".format(rmse))
    print("{:0.4f}".format(corr))
    print('actual mean', np.mean(y_t),'| pred mean',np.mean(y_p))
    print('rmse/range',rmse/(np.max(y_t)-np.min(y_t)))
    print('mape',np.mean(np.abs(y_t-y_p)/y_t))
    iqr= np.subtract(*np.percentile(y_t, [75, 25]))
    print('rmse/iqr',rmse/iqr)
    print('rmse/mean',rmse/np.mean(y_t))
    print('actual min max', np.min(y_t),np.max(y_t))
    print('pred min max', np.min(y_p),np.max(y_p))
    if show_plot: getting_results_regression_plot(y_t,y_p,f_name)


def getting_results(cn_p,cn_t,area_p,area_t,show_plot=False,f_name='results'):    
    acc=np.sum(cn_p==cn_t)/len(cn_p)
    print('acc: ',acc)
    w_idx=np.where(cn_p!=cn_t)
    c_idx=np.where(cn_p==cn_t)
    getting_results_regression(area_t,area_p)
    if show_plot:
        t_area=area_t.copy();p_area=area_p.copy()
        #plt.plot(p_area.flatten(),t_area.flatten(),'.',color='darkblue',alpha=0.2)
        plt.plot(t_area[c_idx].flatten(),p_area[c_idx].flatten(),'.',color='deepskyblue',alpha=0.7)
        plt.plot(t_area[w_idx].flatten(),p_area[w_idx].flatten(),'.',color='crimson',alpha=0.7)
        #plt.ylim(np.min([a_p,a_t]), np.max([a_p,a_t]))
        #plt.xlim(np.min([a_p,a_t]), np.max([a_p,a_t]))
        plt.ylim(-0.1,1.1)
        plt.xlim(-0.1,1.1)
        #plt.xlabel('actual')
        #plt.ylabel('pred')
        plt.grid()
        plt.savefig('images/'+f_name+'.png', bbox_inches = 'tight', transparent=True)
        plt.show()
    
    
def run_a_train_epoch_single(args, epoch, model, data_loader,loss_criterion, optimizer,task_name):
    model.train()
    train_meter = Meter()
    correct=0
    total=0
    for batch_id, batch_data in enumerate(data_loader):
        bg, labels_cablenumber,labels_area = batch_data
        labels_cablenumber = labels_cablenumber.to(args['device'])
        labels_area = labels_area.to(args['device'])
        labels=[labels_cablenumber,labels_area]
        prediction = regress(args, model, bg)
        if task_name=='classification':
            loss_cablenumber = (loss_criterion(prediction, labels_cablenumber).float()).mean()
            loss = loss_cablenumber
            _, predicted = torch.max(prediction.data, 1)
            total += labels_cablenumber.size(0)
            correct += (predicted == labels_cablenumber).sum().item();del predicted
        elif task_name=='regression' or args['task_name']=='regression_all':
            loss_area = (loss_criterion(prediction,labels_area).float()).mean()
            loss=loss_area
            train_meter.update(prediction, labels_area)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    if task_name=='classification':
        total_score_acc=100-100 * correct / total
        print('epoch {:d}/{:d}, training accuracy(%) {:.4f}'.format(
            epoch + 1, args['num_epochs'], total_score_acc))
    elif task_name=='regression' or args['task_name']=='regression_all':
        total_score = np.mean(train_meter.compute_metric(args['metric_name']))
        print('epoch {:d}/{:d}, training {} {:.4f}'.format(
            epoch + 1, args['num_epochs'], args['metric_name'], total_score))
    
def run_an_eval_epoch_single(args, model, data_loader,task_name):
    model.eval()
    eval_meter = Meter()
    correct=0
    total=0
    with torch.no_grad():
        for batch_id, batch_data in enumerate(data_loader):
            bg, labels_cablenumber,labels_area = batch_data
            labels_cablenumber = labels_cablenumber.to(args['device'])
            labels_area = labels_area.to(args['device'])
            labels=[labels_cablenumber,labels_area]
            prediction = regress(args, model, bg)
            
            if task_name=='classification':
                _, predicted = torch.max(prediction.data, 1)
                total += labels_cablenumber.size(0)
                correct += (predicted == labels_cablenumber).sum().item();del predicted
            elif task_name == 'regression' or args['task_name']=='regression_all':
                eval_meter.update(prediction, labels_area)
            
        if task_name == 'classification':
            total_score_acc=100-100 * correct / total
            return total_score_acc
        elif task_name == 'regression' or args['task_name']=='regression_all':
            total_score = np.mean(eval_meter.compute_metric(args['metric_name']))
            return total_score

def get_cableidx():
    e='''    1        40        92        52    1
        2        42        91        49    1
        3        44        90        46    1
        4        46        89        43    1
        5        48        88        40    1
        6        50        88        38    1
        7        52        89        37    1
        8        54        90        36    1
        9        56        91        35    1
       10        58        92        34    1
       11        78       106        28    1
       12        76       105        29    1
       13        74       104        30    1
       14        72       103        31    1
       15        70       102        32    1
       16        68       102        34    1
       17        66       103        37    1
       18        64       104        40    1
       19        62       105        43    1
       20        60       106        46    1
       21         1        85        84    1
       22         3        84        81    1
       23         5        83        78    1
       24         7        82        75    1
       25         9        81        72    1
       26        11        81        70    1
       27        13        82        69    1
       28        15        83        68    1
       29        17        84        67    1
       30        19        85        66    1
       31        39        99        60    1
       32        37        98        61    1
       33        35        97        62    1
       34        33        96        63    1
       35        31        95        64    1
       36        29        95        66    1
       37        27        96        69    1
       38        25        97        72    1
       39        23        98        75    1
       40        21        99        78    2'''

    e = e.split()  
    e=np.array(e)
    e=e.astype('int')
    e=e.reshape((40,5))
    e=e[:,:3]
    return e;

