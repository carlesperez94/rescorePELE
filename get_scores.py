from rescore import *
import pandas as pd
import time
import glob



def get_score(schrodinger=SCHRODINGER):
    jobs = [] 
    for folder in sorted(glob.glob("*/")):
        print(folder)
        with cd(folder):
            log = glob.glob("*.log")[0]
            inputpdb = glob.glob("*.pdb")[0]
            inputglide = glob.glob("*.in")[0]
            output = glob.glob("*dock*lib.maegz")[0]
            schrodinger_exec = os.path.join(schrodinger, "utilities/glide_sort")
            command = "{0} -r report.txt {1}".format(schrodinger_exec, output)
            subprocess.call(command.split())
            with open("report.txt", "r") as f:
                lines = f.readlines()
                glide_score = [lines[i+2].split()[-16] for i, l in enumerate(lines) if "Intern  Conf#" in l][0]
                glide_internal = [lines[i+2].split()[-4] for i, l in enumerate(lines) if "Intern  Conf#" in l][0]
            glidejob = GlideScore(folder, glide_score, glide_internal, inputglide, log, inputpdb, output)
            while not os.path.exists("report.txt"):
                time.sleep(10)
            jobs.append(glidejob)
    paths = [os.path.join(job.folder, job.inputpdb) for job in jobs]
    scores = [job.score for job in jobs]
    internals = [job.internal for job in jobs]
    df = pd.DataFrame({"paths":paths, "scores": scores, "internals": internals})
    df.to_csv("glide.csv")


class GlideScore():

    def __init__(self, folder, score, internal, inputglide, log, inputpdb, output):
        self.folder = folder
        self.score = score
        self.internal = internal
        self.inputglide = inputglide
        self.log = log
        self.inputpdb = inputpdb
        self.output = output
               
if __name__ == "__main__":
    get_score()
