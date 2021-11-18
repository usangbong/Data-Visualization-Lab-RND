import numpy as np

class RBFtimenet(object):
    # This is one layer RBFnn, one-dims
    def __init__(self, timelag = 10, lr = 0.01, epochs = 100, inferStds = True, seed = 1234):
        self.lr = lr
        self.epochs = epochs
        self.inferStds = inferStds
        self.seed = seed
        self.timelag = timelag
        np.random.seed(self.seed)


    def cluster(self, X):
        # simple cluster means and stds list about time series data
        clusters = [np.mean(x) for x in X]
        stds = [np.std(x) for x in X]

        return clusters, stds

    def rbf(self, x, clusters, stds):
        return np.exp(-1 / (2 * stds**2) * (x-clusters)**2)

    def fit(self, X, y):

        self.c, self.s = self.cluster(X)

        self.w = np.random.randn(len(X), self.timelag)
        self.b = np.random.randn(len(X),1)

        # training
        loss_list = []
        loss_mean_list = []
        F_list_epoch = []
        for epoch in range(self.epochs):
            loss_list2 = []
            print('{} epoch train'.format(epoch))
            pred_list = []
            for i in range(len(X)):
                rbf_x = np.array([self.rbf(x, self.c[i], self.s[i]) for x in X[i]])
                F = rbf_x.T.dot(self.w[i]) + self.b[i]
                loss = -(y[i] - F)

                # loss predict value save
                loss_list2.append(np.abs(loss))
                pred_list.append(F)

                # weight, bias, center, sigma update
                self.w[i] += self.lr * rbf_x.reshape(10,) * loss
                self.b[i] += self.lr * loss
                self.c[i] += self.lr * loss
                self.s[i] += self.lr * loss

            F_list_epoch.append(pred_list)
            loss_list.append(loss_list2)
            loss_mean_list.append(np.mean(loss_list2))
            print("{} epoch loss:".format(epoch), np.mean(loss_list2))
            print('---------------------------------------')
            print()

            if epoch >= 5 and (loss_mean_list[epoch] > min(loss_mean_list[epoch - 5:epoch - 1])):
                print("early stopping at {} epoch".format(epoch))
                return loss_mean_list, F_list_epoch, loss_list

            else:
                continue

        return loss_mean_list, F_list_epoch, loss_list

def data_split(X, timelag = 10):
    data = []
    Y = []
    for i in range(len(X) - (timelag+1)):
        data.append(X[i : i + timelag])
        Y.append(X[i + timelag + 1])

    return data, Y



'''
# example

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# data load
df = pd.read_csv('C:/Users/chanyoung/Desktop/Neural-GC-master/lorenz_96_10_10_1000.csv')
X = df['a'].values

# data fit
X_, Y = data_split(X)
rbfnet = RBFtimenet(timelag = 10,lr=1e-2,epochs = 100)
loss_mean_list, F_list_epoch, loss_list = rbfnet.fit(X_, Y)

# data plot
fig, axarr = plt.subplots(1, 2, figsize=(16, 5))

axarr[0].plot(F_list_epoch[98],'-o', label='RBF-Net')
axarr[0].plot(Y,'-o', label='True')
axarr[0].set_xlabel('T')
axarr[0].set_title('Entire time series')

axarr[1].plot(F_list_epoch[98][:50],'-o', label='true')
axarr[1].plot(Y[:50],'-o', label='true')

axarr[1].set_xlabel('T')
axarr[1].set_title('First 50 time points')

plt.tight_layout()
plt.show()
'''
