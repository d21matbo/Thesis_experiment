import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from scripts.util import mean_confidence_interval

file_format = 'pdf'

def stacked_bar(with_label=True, show=False, save=True):
    if not (show or save):
        print('Either show or download must be True')
        return
    
    plt.clf()
    fig, ax = plt.subplots()
    barWidth = 0.8
    
    labels = ['2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023']
    test = {
        'Period 1': np.array([157, 163, 117, 147, 94, 87, 98, 30, 40, 311, 263]),
        'Period 2': np.array([101, 81, 79, 58, 31, 40, 11, 0, 0, 0, 0])
    }
    bottom = np.zeros(11)

    for p, data in test.items():
        a = ax.bar(labels, data, barWidth, label=p, bottom=bottom, zorder=5,
                   edgecolor='black', color='lightblue' if p =='Period 1' else 'lightgreen')
        bottom += data
    
    if with_label:
        threshold = 0
        for c in ax.containers:
            # Filter the labels
            labels = [int(v) if v > threshold else "" for v in c.datavalues]
            ax.bar_label(c, labels=labels, label_type="center", zorder=10)
    
    # Customise Y-axis, grid and legend
    plt.xticks(rotation=0)
    minor_ticks = np.arange(0, 350, 10)
    ax.yaxis.grid(True)
    ax.set_ylim([0,1])
    ax.set_yticks(minor_ticks, minor=True)
    ax.grid(which='minor', alpha=0.3)
    ax.legend()
    plt.ylabel('Number of passengers')

    if show:
        plt.show()
    if save:
        fig.savefig(f'./figures/passengers_per_year.{file_format}', format=file_format)
    plt.close()

def grouped_bar_charts(df1, df2, measurement, show=False, save=True, version=''):
    if not (show or save):
        print('Either show or download must be True')
        return
    if version == 'CI':
        bars_interval_1 = mean_confidence_interval(df1).iloc[1]
        bars_interval_2 = mean_confidence_interval(df2).iloc[1]
        version_name = ' + Confidence interval'
        file_name = 'barchart_ci_'
    elif version == 'STD':
        bars_interval_1 = df1.std()
        bars_interval_2 = df2.std()
        version_name = ' + Standard deviation'
        file_name = 'barchart_std_'
    elif version == 'SE':
        bars_interval_1 = df1.sem()
        bars_interval_2 = df2.sem()
        version_name = ' + Standard error'
        file_name = 'barchart_se_'
    else:
        bars_interval_1 = None
        bars_interval_2 = None
        version_name = ''
        file_name = 'barchart_'

    plt.clf()
    fig, ax = plt.subplots()
    x = np.arange(11)
    width = 0.4
    colors = ['lightblue', 'lightgreen']
    
    ax.bar(x-0.2, df1.mean(), width, color=colors[0], edgecolor='black', 
           yerr=bars_interval_1, capsize=4, zorder=5)

    ax.bar(x+0.2, df2.mean(), width, color=colors[1], edgecolor='black',
           yerr=bars_interval_2, capsize=4, zorder=5)
    
    plt.xticks(x, range(2013, 2024))

    # Customise Y-axis, grid and legend
    minor_ticks = np.arange(0, 1.01, 0.1)
    ax.yaxis.grid(True)
    ax.set_ylim([0,1])
    ax.set_yticks(minor_ticks, minor=True)
    ax.grid(which='minor', alpha=0.3)
    legend_elements = [Patch(facecolor=colors[0], edgecolor='black',
                         label='Biased'),
                  Patch(facecolor=colors[1], edgecolor='black',
                         label='Lloyd')]

    plt.ylabel(f'Measured {measurement}{version_name}')
    plt.legend(handles=legend_elements)
    if show:
        plt.show()
    if save:
        fig.savefig(f'./figures/{file_name}{measurement.lower()}.{file_format}', format=file_format)
    plt.close()

def box_plot(df: pd.DataFrame, measurement: str, show=False, save=True):
    if not (show or save):
        print('Either show or download must be True')
        return
    
    labels = df.columns
    fig, ax = plt.subplots()

    bp = ax.boxplot(df,
                    vert=True,
                    patch_artist=True,
                    labels=labels)

    # Add color to the boxes and create the legend handler
    i = 0
    colors = ['lightblue', 'lightgreen']
    for patch in bp['boxes']:
        patch.set_facecolor(colors[i%2])
        i += 1
    legend_elements = [Patch(facecolor=colors[0], edgecolor='black',
                            label='Biased'),
                    Patch(facecolor=colors[1], edgecolor='black',
                            label='Lloyd'),
                    Line2D([0], [0], color='orange', lw=1, label='Mean')]
    
    # Customise Y-axis, grid and legend
    if measurement == 'RI':
        plt.ylim([0, 1])
        minor_ticks = np.arange(0, 1.01, 0.1)
    elif measurement == 'ARI':
        plt.ylim([-0.5, 1])
        minor_ticks = np.arange(-0.5, 1.01, 0.1)
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    plt.xticks(rotation=45)
    ax.set_yticks(minor_ticks, minor=True)
    ax.grid(which='minor', alpha=0.3)
    plt.ylabel(f'Measured {measurement}')
    plt.legend(handles=legend_elements)

    if show:
        plt.show()
    if save:
        fig.savefig(f'./figures/boxplot_{measurement.lower()}.{file_format}', format=file_format)