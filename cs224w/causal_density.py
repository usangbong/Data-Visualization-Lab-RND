import numpy as np
from statsmodels.tsa.api import VAR, AR


def causal_density(data, target=None, lag=10):
    # data = dataflame (cause, target)
    # target = target
    # lag = time lag

    cause = list(data.columns.values).remove(target)
    model1 = VAR(data)
    data2 = data[target]
    model2 = AR(data2)

    model_fit1 = model1.fit(maxlags=lag)
    model_fit2 = model2.fit(maxlag=lag)

    model1_resid_var = np.var(model_fit1.resid[target].values)
    model2_resid_var = np.var(model_fit2.resid.values)

    CD = np.log(model2_resid_var / model1_resid_var)

    print("target :", target)
    print("cause : ", cause)
    print("causal density is :", CD)

    return CD

