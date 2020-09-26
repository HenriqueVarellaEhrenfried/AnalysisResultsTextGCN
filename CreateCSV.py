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
DATASETS = ["MR"]

def pretty_print(df):
    # more options can be specified also
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  
        print(df) 

def get_metrics(file_path, info):
    with open(file_path) as f:
        text = f.readlines()
    for line in text:
        if line[0:17] == "Test set results:":
            tokens = line.split(" ")
            test_result = {
                "cost":tokens[4], 
                "accuracy":tokens[6], 
                "dataset": info[3],
                "experiment": info[1],
                "name": info[4],
                "run": info[6].split(".")[0]
                }
            return (test_result)

def calculate_metrics(df):
    # TODO: Implment this method
    # Mean, Variation, Standart Deviation
    # Student T-test, Friedman test
    # print(df)
    
    all_results = []
    exp = []
    for i in range(0,25):
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
        all_results.append(results)
    
    results = pd.DataFrame(all_results)
    max_result = results.loc[(results["mean"] == numpy.max(results["mean"]))]

    ttest_ind_from_stats = stats.ttest_ind_from_stats(
        mean1= max_result["mean"].values[0],
        std1= max_result["standard_deviation"].values[0],
        nobs1= 10,
        mean2=0.7674,
        std2=0.002,
        nobs2=10
    )
    ttest_ind_from_stats_inv = stats.ttest_ind_from_stats(
        mean2= max_result["mean"].values[0],
        std2= max_result["standard_deviation"].values[0],
        nobs2= 10,
        mean1=0.7674,
        std1=0.002,
        nobs1=10
    )


 






all_results = []
for dataset in DATASETS:
    for run in range(0,10):
        mypath = PATH+dataset+"/RUN_"+str(run)
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        # EXPERIMENT_11_model_mr_DO05_run_6.txt
        for f in onlyfiles:
            info = f.split("_")
            # print(info)
            all_results.append(get_metrics(mypath+"/"+f, info))

# for a in all_results:
#     print(a)

df = pd.DataFrame(data = all_results)

df["cost"] = pd.to_numeric(df["cost"])
df["accuracy"] = pd.to_numeric(df["accuracy"])
df["experiment"] = pd.to_numeric(df["experiment"])
df["run"] = pd.to_numeric(df["run"])

df = df.sort_values(by=['experiment','run','dataset'])
df = df.reset_index(drop=True)

# calculate_metrics(df)
pretty_print(df)

