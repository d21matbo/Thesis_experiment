from sklearn.cluster import KMeans
import pandas as pd
from sklearn.metrics import rand_score, adjusted_rand_score
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Creates a range object with the seed values that is used to maintain repeatability (total 100 seeds)
seeds = range(0, 500, 5)
print("Seeds:", *seeds)

# Creates a list with the algorithms that is used to create the models
algorithms = ['bias', 'lloyd']
print("Algorithms:", *algorithms)

# Creates a range object with the years that is used in the data set
years = range(2013, 2024)
print("Years:", *years)

# Reads the entries for the event locations, used when algorithm = 'bias'
event_locations = pd.read_csv('./csv/event.txt', sep=',', header=None, names=['Latitude','Longitude','Level'])
if len(event_locations) != 2:
    print('2 entries are required in \'event.txt\'')
    exit()

for year in years:
    file = f"./csv/data{year}.txt"
    df = pd.read_csv(file, sep=",", header=None, names=['Latitude','Longitude','Level','Route'])
    df.Level /= 100
    
    for algo in algorithms:
        save_file = f"./res/{algo}{year}.txt"
        
        target = df['Route']
        data = df.drop(['Route'], axis=1)
        clusters = max(target) + 1

        if algo == 'bias':
            if year == (2020 or 2021):
                data = pd.concat((event_locations.drop([0]), data))
            else:
                data = pd.concat((event_locations.drop([1]), data))

        ri = []
        ari = []
        for seed in seeds:
            model = KMeans(n_clusters=clusters, n_init='auto', random_state=seed, algorithm=algo)
            model.fit(data)

            ri.append(rand_score(target, model.labels_))
            ari.append(adjusted_rand_score(target, model.labels_))

        values = dict(RI = ri, ARI = ari)
        save_df = pd.DataFrame(values)
        save_df.to_csv(save_file, sep=",", header=None, index=False)