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
