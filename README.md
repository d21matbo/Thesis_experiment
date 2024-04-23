# Experiment implementation
This repo contains the relevant Python scripts to run the experiment, create the visualisations and conduct the inferential statistics for the second research question (RQ2) in the thesis:  
__Comparison of heuristic and machine learning algorithms for a multi-objective vehicle routing problem__.
___
The installation steps required are the following:

1. Install the [GitHub Repo](https://github.com/d21matbo/scikit-learn) using the guide available at [Sklearn](https://scikit-learn.org/stable/developers/advanced_installation.html#building-from-source) (checkout branch 1.4.X)
2. Switch to the virtual environment set up in step 1, for use with this repository.
3. Install the additional Python libraries; pandas, matplotlib and Jinja2.
4. Create a folder named `csv`.
___
The `csv` folder must contain a file named `event.txt` with two entries for using different locations, providing values for *longitude*, *latitude* and *level*.

```CSV
12.3456789,98.7654321,0
10.3456789,90.7654321,0
```

Additional files named `dataYYYY.txt` where `YYYY` represents the year are required, containing entries with values for *longitude*, *latitude*, *level* and *route*.  
The number of files required can be changed by altering the `years` variable in `experiment.py` and `data_management.py`.
___
### experiment.py
Builds multiple k-means models and compares their labels against the baseline using the `rand_score` and `adjusted_rand_score` functions. Saves the results of each model in the folder `res`.

### data_management.py
Builds graphs and applies inferential statistics on the results available in the `res` folder