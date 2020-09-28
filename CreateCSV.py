from os import listdir
from os.path import isfile, join
import pandas as pd
import sys
import numpy
import scipy as sp
from scipy import stats

if len(sys.argv) < 2:
    print("ERROR >>", "You must specify the path")
    exit(1)

PATH = sys.argv[1]
# DATASETS = ["MR","R52"]
DATASETS = ["MR","Ohsumed","R8","R52"]

def pretty_print(df):
    # more options can be specified also
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  
        print(df) 

def get_metrics(file_path, info, dataset):
    # epochs = 0
    with open(file_path) as f:
        text = f.readlines()
    for line in text:
        if line[0:6] == "Epoch:" :
            epochs = line.split(" ")[1]
        if line[0:17] == "Test set results:":
            tokens = line.split(" ")
            test_result = {
                "cost":tokens[4], 
                "accuracy":tokens[6], 
                "epochs": int(epochs),
                "dataset": dataset,
                "experiment": info[1],
                "name": info[4],
                "run": info[6].split(".")[0]
                }
            return (test_result)

def calculate_basic_statistics(df, dataset):
    # Implment Basic statistics and save as csv
    
    all_results = []
    exp = []
    for i in range(0,19): # This for controls the experiments. Use 25 to get all CUSTOM
        experiment = df.loc[df['experiment'] == i]
        experiment_name = df.loc[df['experiment'] == i]["name"].values[0]
        exp.append(experiment["accuracy"])
        results = {}
        results["experiment"] = i
        results["name"] = experiment_name
        results["min"] = numpy.min(experiment["accuracy"])
        results["max"] = numpy.max(experiment["accuracy"])
        results["mean"] = numpy.mean(experiment["accuracy"])
        results["median"] = numpy.median(experiment["accuracy"])
        results["variance"] = numpy.var(experiment["accuracy"])
        results["standard_deviation"] = numpy.std(experiment["accuracy"])
        results["min_epochs"] = numpy.min(experiment["epochs"])
        results["max_epochs"] = numpy.max(experiment["epochs"])
        results["mean_epochs"] = numpy.mean(experiment["epochs"])
        results["median_epochs"] = numpy.median(experiment["epochs"])
        results["var_epochs"] = numpy.var(experiment["epochs"])
        results["std_epochs"] = numpy.std(experiment["epochs"])
        all_results.append(results)

    results = pd.DataFrame(all_results)
    results.to_csv(
        "./Basic_Statistics/"+dataset+".csv",
        sep=';',
        index=False
    )
    return results
    

def calculate_statistics(all_results, dataset):

    print("------ Working with dataset", dataset, "------\n")
    ORIGINAL_PAPER = {
        "MR": {"avg": 0.7674, "std": 0.0020},
        "Ohsumed": {"avg": 0.6836, "std": 0.0056},
        "R8": {"avg": 0.9707, "std": 0.0010},
        "R52": {"avg": 0.9356, "std": 0.0018}
    }

    results = pd.DataFrame(all_results)
    max_result = results.loc[(results["mean"] == numpy.max(results["mean"]))]
    print(results)
    print(max_result)

    ttest_ind_from_stats = stats.ttest_ind_from_stats(
        mean2= max_result["mean"].values[0],
        std2= max_result["standard_deviation"].values[0],
        nobs2= 10,
        mean1=ORIGINAL_PAPER[dataset]["avg"],
        std1=ORIGINAL_PAPER[dataset]["std"],
        nobs1=10
    )

    print(ttest_ind_from_stats)

 

all_results = []
for dataset in DATASETS:
    for run in range(0,10):
        mypath = PATH+dataset+"/RUN_"+str(run)
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        # EXPERIMENT_11_model_mr_DO05_run_6.txt
        for f in onlyfiles:
            info = f.split("_")
            # print(info)
            all_results.append(get_metrics(mypath+"/"+f, info, dataset))

df = pd.DataFrame(data = all_results)

df["cost"] = pd.to_numeric(df["cost"])
df["accuracy"] = pd.to_numeric(df["accuracy"])
df["experiment"] = pd.to_numeric(df["experiment"])
df["run"] = pd.to_numeric(df["run"])

df = df.sort_values(by=['experiment','run','dataset'])
df = df.reset_index(drop=True)

for dataset in DATASETS:
    experiments = df.loc[df['dataset'] == dataset]
    calculate_basic_statistics(experiments, dataset)
    

# pretty_print(df)

