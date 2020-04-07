import argparse
import shutil
import subprocess
import os
import template_builder as tb

SCHRODINGER = "/data/general_software/schrodinger2018-2/"
DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(DIR, "glide.in")
CPUS=4


def score_glide(pdb, template=TEMPLATE, cpus=4, schrodinger=SCHRODINGER, output=None):
    if not output:
        folder = os.path.basename(pdb).rsplit(".", 1)[0]
    else:
        folder = output
    if not os.path.exists(folder): os.mkdir(folder)
    with cd(folder):
        schrodinger_exec = os.path.join(schrodinger, "run")
        input = os.path.basename(template)
        shutil.copy(template, input)
        shutil.copy(pdb, ".")
        tb.TemplateBuilder(input, {"INPUT": pdb, "PRECISION": "SP" })
        #command = "{0} xglide.py {1} -HOST {2}:{3}".format(schrodinger_exec, input, "Calculon_slurm", cpus)
        command = "{0} xglide.py {1} -OVERWRITE -HOST localhost:40".format(schrodinger_exec, input)
        print(command)
        subprocess.call(command.split())
        


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)



def parse_args(parser):
    parser.add_argument("--struct", help="structure to rescore", nargs="+")
    parser.add_argument("--output", help="output folder", default="")
    parser.add_argument("--template", default=TEMPLATE, help="rescoring template")
    parser.add_argument("--cpus", default=CPUS, help="cpus to use")
    parser.add_argument("--schrodinger", default=SCHRODINGER, help="schrodinger root path")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parse_args(parser)
    args = parser.parse_args()
    score_glide(args.struct, args.template, args.cpus, args.schrodinger, args.output) 
