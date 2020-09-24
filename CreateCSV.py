from os import listdir
from os.path import isfile, join
import pandas as pd
import sys

if len(sys.argv) < 2:
    print("ERROR >>", "You must specify the path")
    exit(1)

PATH = sys.argv[1]
DATASETS = ["MR"]

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
    print(df)

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

df = pd.DataFrame(data = all_results).sort_values(by=['experiment','run'])

df["cost"] = pd.to_numeric(df["cost"])
df["accuracy"] = pd.to_numeric(df["accuracy"])
df["experiment"] = pd.to_numeric(df["experiment"])
df["run"] = pd.to_numeric(df["run"])

calculate_metrics(df)
