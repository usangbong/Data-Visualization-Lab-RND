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

        self.init_weight = nn.Parameter(torch.rand(self.timelag, device=device))
        self.rbf_clt = self.init_clt()
        self.rbf_std = self.init_std()

        self.b = nn.Parameter(torch.rand(1, device=device))

    def init_clt(self):
        return nn.Parameter(torch.rand(1, device=device))

    def init_std(self):
        return nn.Parameter(torch.rand(1, device=device))

    def rbf(self, x, cluster, std):
        return torch.exp(-(x - cluster) * (x - cluster) / 2 * (std * std))

    def rbf_gradient(self, x, clt, std):
        return (-1 * (x - clt) * (x - clt) / (std * std)) * (torch.exp(-(x - clt) * (x - clt) / 2 * (std * std)))

    def forward(self, x):
        for i in range(len(x)):
            if i == 0:
                a = self.rbf(x[i], self.rbf_clt, self.rbf_std)
            else:
                a = torch.cat([a, self.rbf(x[i], self.rbf_clt, self.rbf_std)], dim=0)
        cause = self.init_weight * a

        return cause

def restore_parameters(model, best_model):
    '''Move parameter values from best_model to model.'''
    for params, best_params in zip(model.parameters(), best_model.parameters()):
        params.data = best_params





def train_RBFlayer(model, input_, lr, epochs, lookback=5, device=device):
    model.to(device)
    loss_fn = nn.MSELoss(reduction='mean')
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    train_loss_list = []

    best_it = None
    best_model = None
    best_loss = np.inf
    target = []
    for j in range(len(input_) - 2):
        target.append((input_[j + 2] - input_[j]) / 2)

    loss_list = []
    cause_list = []
    for epoch in range(epochs):
        cause = model(input_)
        cause_list.append(cause)
        grad = []

        for i in range(len(cause) - 2):
            grad.append((cause[i + 2] - cause[i]) / 2)

        loss = sum([loss_fn(grad[i], target[i]) for i in range(len(grad))])
        '''
        print("epoch {} cause loss {} :".format(epoch, loss / len(input_)))
        print("------------------------------------------------------")
        print()
        '''
        loss.backward()
        optimizer.step()
        model.zero_grad()

        loss_list.append(loss)
        mean_loss = loss / len(grad)
        train_loss_list.append(mean_loss)

        if mean_loss < best_loss:
            best_loss = mean_loss
            best_it = epoch
            best_model = deepcopy(model)

        elif (epoch - best_it) == lookback:
            if verbose:
                print('Stopping early')
            break
    print("epoch {} cause loss {} :".format(epoch, loss / len(input_)))
    print("------------------------------------------------------")

    best_cause = cause_list[best_it]
    restore_parameters(model, best_model)

    return best_model, loss_list, best_cause