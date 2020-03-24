import argparse
import time
import glob
import os
import rescore
import get_scores
import get_dataset
import build_model


def main(rescore_pdb, template, schr, cpus, score_yes=False, dataset=False, model=False):
    if rescore_pdb:
        for pdb in rescore_pdb:
            output = os.path.basename(os.path.dirname(os.path.dirname(pdb)))
            if os.path.exists(output):
                print("Pass")
                continue
            rescore.score_glide(pdb, template=template, cpus=cpus, schrodinger=schr, output=output)
            while not glob.glob(os.path.join(output, "*.maegz")):
                time.sleep(10)
    if score_yes:
        get_scores.get_score(schr)
    if dataset:
        get_dataset.retrieve("output2/internal_energy.csv", ".")
    if model:
        build_model.get("dataset.csv", "SARS.csv")

def parseargs(parser):
    parser.add_argument("--score",  action="store_true", help="score all folders in the present directory and make a csv summary")
    parser.add_argument("--dataset", action="store_true", help="gather dataset")
    parser.add_argument("--model", action="store_true", help="build model")

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    rescore.parse_args(parser)
    parseargs(parser)
    args = parser.parse_args()
    if args.struct:
        pdb = [os.path.abspath(struct) for struct in args.struct]
    else:
        pdb = args.struct
    main(pdb, args.template, args.schrodinger, args.cpus, args.score, args.dataset, args.model)
