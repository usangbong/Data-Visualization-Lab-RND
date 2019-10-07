#MiniSom
Self Organizing Mpas
https://github.com/JustGlowing/minisom
MiniSom is a minimalistic and Numpy based implementation of the Self Organizing Maps (SOM). SOM is a type of Artificial Neural Network able to convert complex, nonlinear statistical relationships between high-dimensional data items into simple geometric relationships on a low-dimensional display.

#Installation
pip install minisom
git clone https://github.com/JustGlowing/minisom.git
python setup.py install

#How to use it
In order to use MiniSom you need your data organized as a Numpy matrix where each row corresponds to an observation or as list of lists like the following:
data = [[ 0.80,  0.55,  0.22,  0.03],
        [ 0.82,  0.50,  0.23,  0.03],
        [ 0.80,  0.54,  0.22,  0.03],
        [ 0.80,  0.53,  0.26,  0.03],
        [ 0.79,  0.56,  0.22,  0.03],
        [ 0.75,  0.60,  0.25,  0.03],
        [ 0.77,  0.59,  0.22,  0.03]]
        
        
Then you can run MiniSom just as follows:
from minisom import MiniSom    
som = MiniSom(6, 6, 4, sigma=0.3, learning_rate=0.5) # initialization of 6x6 SOM
som.train_random(data, 100) # trains the SOM with 100 iterations

MiniSom implements two types of training. The random training (implemented by the method train_random), where the model is trained picking random samples from your data, and the batch training (implemented by the method train_batch), where the samples are picked in the order they are stored.

The weights of the network are randomly initialized by default. Two additional methods are provided to initialize the weights in a data driven fashion: random_weights_init and pca_weights_init.

#Uinsg the trained SOM
For an overview of all the features implemented in minisom you can browse the following examples: https://github.com/JustGlowing/minisom/tree/master/examples

Export a SOM and load it again
A model can be saved using pickle as follows

import pickle
som = MiniSom(7, 7, 4)

# ...train the som here

# saving the som in the file som.p
with open('som.p', 'wb') as outfile:
    pickle.dump(som, outfile)
    
and can be loaded as follows

with open('som.p', 'rb') as infile:
    som = pickle.load(infile)    
