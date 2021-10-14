def lower_upper(df, column):
    df = df.loc[:, [column]]
    df = df.dropna()

    q25 = np.quantile(df[column], 0.25)
    q75 = np.quantile(df[column], 0.75)

    iqr = q75 - q25
    cut_off = iqr * 1.5
    lower, upper = q25 - cut_off, q75 + cut_off
    return lower, upper

def quality_issue(df):
    df = df[sorted(df.columns)]

    missing = df.isnull().sum().tolist()
    extreme = []
    for column in df:
        lower, upper = lower_upper(df, column)
        data1 = df[df[column] > upper]
        data2 = df[df[column] < lower]

        extreme.append(data1.shape[0] + data2.shape[0])

    total = [x + y for x, y in zip(missing, extreme)]
    return missing, extreme, total

def quality_metric(df, column):
    kstest = statistics.custom_kstest(df, column).pvalue
    skewness = statistics.custom_skewness(df, column)
    kurtosis = statistics.custom_kurtosis(df, column)
    entropy = statistics.custom_entropy(df, column)

    return kstest, skewness, kurtosis, entropy

def quality_metric_total(df):
    output = [[], [], [], []]

    for i in range(0, len(column_list)):
        kstest, skewness, kurtosis, entropy = quality_metric(df, i)

        output[0].append(kstest)
        output[1].append(skewness)
        output[2].append(kurtosis)
        output[3].append(entropy)

    return output