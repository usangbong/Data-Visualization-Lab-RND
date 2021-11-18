import torch
import torch.nn as nn
import numpy as np
from copy import deepcopy

device = "cuda" if torch.cuda.is_available() else "cpu"

class RBFlayer(nn.Module):
    def __init__(self, timelag):
        super(RBFlayer, self).__init__()

        self.timelag = timelag

        device = "cuda" if torch.cuda.is_available() else "cpu"
        torch.cuda.manual_seed(0)

        self.init_weight_cause = nn.Parameter(torch.rand(self.timelag, device=device))
        self.init_weight_target = nn.Parameter(torch.rand(self.timelag, device=device))
        self.cause_clt = self.init_clt()
        self.cause_std = self.init_clt()
        self.target_clt = nn.Parameter(torch.rand(1, device=device))
        self.target_std = nn.Parameter(torch.rand(1, device=device))

    def init_clt(self):
        return nn.Parameter(torch.rand(1, device=device))

    def init_std(self):
        return nn.Parameter(torch.rand(1, device=device))

    def rbf(self, x, cluster, std):
        return torch.exp(-(x - cluster) * (x - cluster) / 2 * (std * std))


    def forward(self, cause, target):

        for i in range(len(cause)):
            if i == 0:
                a = self.rbf(cause[i], self.cause_clt, self.cause_std)
            else:
                a = torch.cat([a, self.rbf(cause[i], self.cause_clt, self.cause_std)], dim=0)
        cause = self.init_weight_cause * a

        for j in range(len(target)):
            if j == 0:
                b = self.rbf(target[j], self.target_clt, self.target_std)
            else:
                b = torch.cat([b, self.rbf(target[j], self.target_clt, self.target_std)], dim=0)
        target = self.init_weight_target * b

        return cause, target


class RBFnet(nn.Module):
    def __init__(self, input_size , output_size, timelag):
        super(RBFnet,self).__init__()

        self.input_size = input_size      # number of data
        self.output_size = output_size
        self.timelag = timelag

        self.linear = nn.ModuleList([nn.Linear(self.timelag*2,1) for _ in range(self.input_size)])
        self.relu = nn.ReLU()
        self.networks = nn.ModuleList([RBFlayer(self.timelag) for _ in range(self.input_size)])

    def cause_target(self, cause, target):
        x = torch.cat((cause, target), 0)

        return x

    def GC(self, threshold=True):
        '''
        Extract learned Granger causality.
        Args:
          threshold: return norm of weights, or whether norm is nonzero.
        Returns:
          GC: (p x p) matrix. Entry (i, j) indicates whether variable j is
            Granger causal of variable i.
        '''
        GC = [torch.norm(net.init_weight_cause, dim=0)
              for net in self.networks]
        GC = torch.stack(GC)
        if threshold:
            return (GC > 0).int()
        else:
            return GC


    def forward(self, causes, targets):
        out_list = []
        for i in range(self.input_size):
            cause, target = self.networks[i](causes[i], targets[i])
            cause, target = self.relu(cause), self.relu(target)
            pred = torch.cat((cause, target),0)
            pred = self.linear[i](pred)
            out_list.append(pred)

        return out_list


def restore_parameters(model, best_model):
    '''Move parameter values from best_model to model.'''
    for params, best_params in zip(model.parameters(), best_model.parameters()):
        params.data = best_params

def rbf_p(x, clt, std):
    return (-2 * (x - clt) / (std * std)) * (torch.exp(-(x - clt) * (x - clt) / 2 * (std * std)))

def rbf_fn(x, cluster, std):
    return torch.exp(-(x - cluster) * (x - cluster) / 2*(std * std))

def rbf_grad_cause(model, input):

    rbf_grad_list = []
    for i in range(input.shape[0]):
        list_ = []
        clt = model.networks[i].cause_clt
        std = model.networks[i].cause_std

        for j in range(input.shape[1] - 2):
            list_.append(rbf_p(input[i][j + 1], clt, std))

        rbf_grad_list.append(list_)

    return torch.Tensor(rbf_grad_list)


def rbf_grad_target(model, input):

    rbf_grad_list = []
    for i in range(input.shape[0]):
        list_ = []
        clt = model.networks[i].target_clt
        std = model.networks[i].target_std

        for j in range(input.shape[1] - 2):
            list_.append(rbf_p(input[i][j + 1], clt, std))

        rbf_grad_list.append(list_)

    return torch.Tensor(rbf_grad_list)


def rbf_grad_num_cause(input):
    rbf_grad_list = []
    for j in range(input.shape[0]):
        list_ = []
        clt = model.networks[j].cause_clt
        std = model.networks[j].cause_std

        for i in range(input.shape[1] - 2):
            list_.append((rbf_fn(input[j][i+2],clt,std) - rbf_fn(input[j][i], clt, std)) /
                                        (input[j][i+2] - input[j][i]))

        rbf_grad_list.append(list_)

    return torch.Tensor(rbf_grad_list)

def rbf_grad_num_target(input):
    rbf_grad_list = []
    for j in range(input.shape[0]):
        list_ = []
        clt = model.networks[j].target_clt
        std = model.networks[j].target_std

        for i in range(input.shape[1] - 2):
            list_.append((rbf_fn(input[j][i+2],clt,std) - rbf_fn(input[j][i], clt, std)) /
                                        (input[j][i+2] - input[j][i]))

        rbf_grad_list.append(list_)

    return torch.Tensor(rbf_grad_list)

def train_rbf(model, input_causes, input_targets, Y, lr, epochs, lookback=5,device = device):
    # input_causes, input_targets : X
    # Y : Y
    model.to(device)
    loss_fn = nn.MSELoss(reduction='mean')
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    train_loss_list = []

    best_it = None
    best_model = None
    best_loss = np.inf

    for epoch in range(epochs):
        pred = model(input_causes, input_targets)
        loss_ = sum([loss_fn(pred[i], Y[i]) for i in range(len(Y))])
        loss_cause = loss_fn(rbf_grad_num_cause(input_causes), rbf_grad_cause(model, input_causes))
        print()
        loss_target = loss_fn(rbf_grad_num_target(input_targets), rbf_grad_target(model, input_targets))

        loss = loss_ + loss_cause + loss_target
        print("epoch {} loss {} :".format(epoch, loss / len(Y)))

        loss_.backward()
        optimizer.step()

        loss_cause.backward()
        optimizer.step()

        loss_target.backward()
        optimizer.step()

        model.zero_grad()


        mean_loss = loss / len(Y)
        train_loss_list.append(mean_loss)
        if mean_loss < best_loss:
            best_loss = mean_loss
            best_it = epoch
            best_model = deepcopy(model)
        elif (epoch - best_it) == lookback:
            if verbose:
                print('Stopping early')
            break

    restore_parameters(model, best_model)

    return train_loss_list , model
