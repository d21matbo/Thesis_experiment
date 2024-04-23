import pandas as pd
import scipy.stats as stats
import numpy as np

def split_on_model(df: pd.DataFrame):
    df_b = df.drop(df.filter(regex='L'), axis=1)
    df_l = df.drop(df.filter(regex='B'), axis=1)
    return df_b, df_l

def mean_confidence_interval(data, confidence=0.95):
    df = pd.DataFrame()
    for d in data:
        a = 1.0 * np.array(data[d])
        n = len(a)
        m, se = np.mean(a), stats.sem(a)
        h = se * stats.t.ppf((1 + confidence) / 2., n-1)
        df = pd.concat([df, pd.DataFrame({d:[-h,+h]})], axis=1)
    return df

def anova(*data): # * indicates, 0, 1 , 2 .. arguments
    if len(data) == 2:
        statistic, pvalue = stats.f_oneway(data[0], data[1])
    elif len(data) == 3:
        statistic, pvalue = stats.f_oneway(data[0], data[1], data[2])
    elif len(data) == 4:
        statistic, pvalue = stats.f_oneway(data[0], data[1], data[2], data[3])
#     print("ANOVA Statistic " + str(statistic) + " and p-value " + str(pvalue))
#     if pvalue < statistic:
#         return True
#     else:
#         return False
    return statistic, pvalue