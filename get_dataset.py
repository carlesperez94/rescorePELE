import glob
import os
import pandas as pd



def retrieve(csv, csv2, structures_paths):
    row = []
    for folder in sorted(structures_paths):
        print(folder)
        input_met = os.path.join(folder, "metrics.out")
        input_clu = os.path.join(folder, "cluster.out")
        if not os.path.exists(input_met):
            continue
        df1 = pd.read_csv(csv)
        folname = folder.split("/")[-2]
        df1 = df1[df1["paths"] == os.path.join(folname, "rep_structure.pdb")]
        with open(input_met,"r") as f:
            for line in f:
                if line.startswith('Heavy atoms'):
                    atoms = int(line.split(':')[-1].strip())
                elif line.startswith('Molecular weight'):
                    weight = float(line.split(':')[-1].strip())
                elif line.startswith('N. rotatable bonds'):
                    rotamers = int(line.split(':')[-1].strip())
                elif line.startswith('N. clusters'):
                    clusters = int(line.split(':')[-1].strip())
                elif line.startswith('Global Mean Tot. E.'):
                    globte = float(line.split(':')[-1].strip())
                elif line.startswith('Global Mean Int. E.'):
                    globie = float(line.split(':')[-1].strip())

        with open(input_clu, 'r') as f:
            for line in f:
                if line.startswith('Cluster size'):
                    csize = int(line.split(':')[-1].strip())
                if line.startswith('Mean Tot. E.'):
                    meante = float(line.split(':')[-1].strip())
                if line.startswith('Mean Int. E.'):
                    meanie = float(line.split(':')[-1].strip())
                if line.startswith('Mean RMSD'):
                    meanr = float(line.split(':')[-1].strip())
                if line.startswith('Min Tot. E.'):
                    minte = float(line.split(':')[-1].strip())
                if line.startswith('Min Int. E.'):
                    minie = float(line.split(':')[-1].strip())
                if line.startswith('Min RMSD'):
                    minr = float(line.split(':')[-1].strip())
                if line.startswith('Max Tot. E.'):
                    maxte = float(line.split(':')[-1].strip())
                if line.startswith('Max Int. E.'):
                    maxie = float(line.split(':')[-1].strip())
                if line.startswith('Max RMSD'):
                    maxr = float(line.split(':')[-1].strip())
        try:
            score = df1["scores"].values[0]
            internal = df1["internals"].values[0]
        except IndexError:
            print("WARNING: {} does not contain score.".format(input))
            continue

        try:
            row.append([folname, atoms, weight, rotamers, clusters, globte, globie, csize, meante, meanie, meanr, minte, minie, minr, maxte, maxie, maxr, score, internal])
        except NameError:
            print("WARNING: some descriptors were not found in {}".format(folname))

    df = pd.DataFrame(row, columns=["path", "atoms", "weight", "rotamers", "clusters", "globte", "globie", "csize", "meante", "meanie", "meanr", "minte", "minie", "minr", "maxte", "maxie", "maxr", "gscore", "ginternal"])
    df.to_csv("dataset.csv")
