import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = [10, 6]


# loading 'tips' dataset
tips = sns.load_dataset('tips')

tips.shape
tips.head()

tips.groupby(['sex', 'day']).size()

# Basic box plot
plt.boxplot(tips['tip'])
plt.show()

# setting outlier symbol, title, xlabel
plt.boxplot(tips['tip'], sym="bo")
plt.title('Box plot of tip')
plt.xticks([1], ['tip'])
plt.show()

# Horizontal Box plot with notched box & red color outliers
plt.boxplot(tips['tip'], 
            notch=1, # if 'True' then notched box plot
            sym='rs', # symbol: red square
            vert=0 # vertical : if 'False' then horizontal box plot
           )
plt.show()

