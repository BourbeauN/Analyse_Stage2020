import numpy as np
import matplotlib
matplotlib.use('Agg')
import argparse
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd



parser = argparse.ArgumentParser()
parser.add_argument('-f', dest = 'INFILE', help = 'Results file from Plateau.py')
args = parser.parse_args()
Results = pd.read_csv(args.INFILE)

def get_information(folder_name):
    file = folder_name.split("/")[2].split(".")[0]
    param = folder_name.split("/")[0]
    
    return file,param

file,param = get_information(args.INFILE)
sns_plot = sns.heatmap(Results,annot=True)

sns_plot.savefig("Analysis/Heat_map/{}/{}.pdf".format(param,file))