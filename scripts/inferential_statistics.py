import pandas as pd
from scripts.util import split_on_model, anova

def test_results(df: pd.DataFrame, confidence=0.95):
    results = list()
    statistics, pvalue = anova(*split_on_model(df))
    for year, f, p in zip(range(2013, 2024), statistics, pvalue):  
        entry = {'Year':year,
                'F-Statistics':f,
                'P-Value':p,
                'Diff':'True' if p < 1 - confidence else 'False'}
        results.append(entry)
         
    test_results = pd.DataFrame(results)
    print(test_results.to_latex(index=False))
