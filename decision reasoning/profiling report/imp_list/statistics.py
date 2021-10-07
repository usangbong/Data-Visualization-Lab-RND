import pandas as pd
from scipy import stats
import numpy as np

df = pd.read_csv("static/data/missing.csv")
df.head()


########## Statistic on data quality


##### skewness
# Compute the sample skewness of a data set
# url: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skew.html
def custom_skewness(input) :
    output = stats.skew(df.iloc[:,input], nan_policy='omit')
    return output


##### kurtosis
# Compute the kurtosis of a dataset
# url: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kurtosis.html
#stats.kurtosis(df['col1'], fisher=True)
def custom_kurtosis(input) :
    output = stats.kurtosis(df.iloc[:,input], nan_policy='omit')
    return output


##### Kolmogorov-Smirnov test (KS test) of one sample
# Performs the one sample KS test for goodness of fit
# url: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kstest.html#scipy.stats.kstest
def custom_kstest(input) :
    output = stats.kstest(df.iloc[:,input], 'norm')
    return output


##### KS test between two samples
# Compute the KS test on two samples
# url: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html#scipy.stats.ks_2samp
#stats.ks_2samp(df['col1'],df['col2'], mode='auto')
def custom_ks2test(input1, input2, matrix, imputation) :
    output = stats.ks_2samp(matrix.iloc[:,input1], imputation.iloc[:,input2], mode='auto')    
    return output


##### Information entropy
# Calculate the entropy of a distribution for given probability values.
# url: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.entropy.html
#stats.entropy(df['col1'], base=2)
def custom_entropy(input) :
    output = stats.entropy(df.iloc[:,input], base=2)
    return output