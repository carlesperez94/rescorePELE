import argparse
import time
import glob
import os
import rescore
import get_scores
import get_dataset
import build_model


def main(rescore_pdb, template, schr, cpus, score_yes=False, dataset=None, model=False,
         dataout="."):
    print(rescore_pdb)
    if rescore_pdb and not dataset:
        for pdb in rescore_pdb:
            dirname = os.path.basename(os.path.dirname(os.path.dirname(pdb)))
            output = os.path.join(dirname, "glide__rep_structure__rep_structure__dock_lib.maegz")
            if os.path.exists(output):
                print("{} already completed. Skipping...".format(dirname))
                continue
            rescore.score_glide(pdb, template=template, cpus=cpus, schrodinger=schr, output=dirname)
            while not glob.glob(os.path.join(dirname, "*.maegz")):
                time.sleep(10)
    if score_yes:
        get_scores.get_score(schr)
    if os.path.exists(dataset):
        if rescore_pdb:
            folders = []
            for pdb in rescore_pdb:
                folder_to_analyze = os.path.dirname(pdb)
                folders.append(folder_to_analyze)
            print(folders)
            get_dataset.retrieve(dataset, dataout, folders)
    if model:
        build_model.get("dataset.csv", "SARS.csv")

def parseargs(parser):
    parser.add_argument("--score",  action="store_true", help="score all folders in the present directory and make a csv summary")
    parser.add_argument("--dataset", default=None, help="CSV file with scores.")
    parser.add_argument("--model", action="store_true", help="build model")
    parser.add_argument("--dataout", default=".", help="Output dataframe path")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    rescore.parse_args(parser)
    parseargs(parser)
    args = parser.parse_args()
    if args.struct:
        pdb = [os.path.abspath(struct) for struct in args.struct]
    else:
        pdb = args.struct
    if args.dataset:
        if args.struct:
            pdb = [os.path.abspath(struct) for struct in args.struct]
        else:
            raise IOError("You must set the pdb folders to analyse in --struct")
    main(pdb, args.template, args.schrodinger, args.cpus, args.score, args.dataset, args.model, args.dataout)
