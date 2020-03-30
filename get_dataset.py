import glob
import os
import pandas as pd



def retrieve(csv, csv2, structures_paths):
    row = []
    for folder in sorted(structures_paths):
        print(folder)
        input_met = os.path.join(folder, "metrics.out")
        if not os.path.exists(input_met):
            continue
        df1 = pd.read_csv(csv)
        folname = folder.split("/")[-2]
        df1 = df1[df1["paths"] == os.path.join(folname, "rep_structure.pdb")]
        with open(input_met,"r") as f:
              atoms, weight, rotamers, total, interaction, rmsd, id  = f.readlines()[-1].split()[0:7]
              try:
                  score = df1["scores"].values[0]
              except IndexError:
                  print("WARNING: {} does not contain score.".format(input))
                  continue
              
        row.append([folname, float(atoms), float(weight), float(rotamers), float(total), float(interaction), float(score)])
    print(row)
    df = pd.DataFrame(row, columns=["path", "atoms", "weight", "rotamers", "toten", "be", "internal"])
    df.to_csv("dataset.csv")
