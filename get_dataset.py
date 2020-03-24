import glob
import os
import pandas as pd



def retrieve(csv, csv2):
    row = []
    for folder in glob.glob("2H*"):
        input = os.path.join(folder,"filtering_results_bandwidth_50/metrics.out")
        df1 = pd.read_csv(csv)
        print(folder)
        df1 = df1[df1["paths"] == os.path.join(folder, "rep_structure.pdb")]
        with open(input,"r") as f:
              atoms, weight, total, interaction, rmsd, id  = f.readlines()[-1].split()[0:6]
              score = df1["scores"].values[0]
        row.append([folder, float(atoms), float(weight), float(total), float(interaction), float(score)])
    print(row)
    df = pd.DataFrame(row, columns=["path", "atoms", "wieght", "toten", "be", "internal"])
    df.to_csv("dataset.csv")
