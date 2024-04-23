import pandas as pd
from scripts.create_figures import grouped_bar_charts, box_plot, stacked_bar
from scripts.util import split_on_model
from scripts.inferential_statistics import test_results

def main():
    df_merged_ri = pd.DataFrame()
    df_merged_ari = pd.DataFrame()
    years = range(2013, 2024)

    # Read and group all the results from the available years, separated by measurement (RI & ARI) 
    for year in years:
        file_bias = f'./res/bias{year}.txt'
        file_lloyd = f'./res/lloyd{year}.txt'
        df_bias = pd.read_csv(file_bias, sep=",", header=None, names=['RI', 'ARI'])
        df_lloyd = pd.read_csv(file_lloyd, sep=",", header=None, names=['RI', 'ARI'])
        
        tmp_ri = pd.concat([df_bias['RI'].rename(f"B-{year-2000}"), df_lloyd['RI'].rename(f"L-{year-2000}")], axis=1)
        tmp_ari = pd.concat([df_bias['ARI'].rename(f"B-{year-2000}"), df_lloyd['ARI'].rename(f"L-{year-2000}")], axis=1)
        df_merged_ri = pd.concat([df_merged_ri, tmp_ri], axis=1)
        df_merged_ari = pd.concat([df_merged_ari, tmp_ari], axis=1)

    # Generates stacked bar chart with the preset of passengers per period. (Part of the general results)
    stacked_bar()

    # Generates a bar chart with CI, S.E and STD for both measurements, where the models are grouped by year   
    for df_bias, df_lloyd, m in [(*split_on_model(df_merged_ri), 'RI'), (*split_on_model(df_merged_ari), 'ARI')]:
        for v in ['CI', 'SE', 'STD']:
            grouped_bar_charts(df_bias, df_lloyd, m, version=v, save=True)
            pass
    
    # Generates boxplots for the given dataframes
    box_plot(df_merged_ri, 'RI')
    box_plot(df_merged_ari, 'ARI')

    # Tests the results for a statistical difference
    test_results(df_merged_ri)
    test_results(df_merged_ari)

main()
