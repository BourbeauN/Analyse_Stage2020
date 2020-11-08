import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import pdb
import argparse
import os

def main():
    #Parser to run code in server
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest = "INFILE", help = ".csv results file")
    args = parser.parse_args()
    
    foldername = args.INFILE
    experiment = foldername.split("/")[1].split(".")[0]
    parameter = foldername.split("/")[1].split(".")[0].split("_")[0:-4]

    if len(parameter) != 1:
        s = ' '
        d = '_'
        p_title = s.join(parameter)

    else :
        p_title = parameter

    #Obtaining data in arrays
    Results = pd.read_csv(args.INFILE)
    x_data =  Results.iloc[:,1]
    y_data = Results.iloc[:,2]
    
    ###PLOTS###
    plt.plot(x_data, y_data,'.',markersize = 1, color = 'crimson', linewidth = 0)
    plt.xlabel("Elapsed time (minutes)")
    plt.ticklabel_format(axis="y", style="sci")
    plt.ylabel("{}".format(p_title))
    plt.savefig(os.path.join("PLOTS/{}.pdf".format(experiment)))
    plt.savefig(os.path.join("PLOTS/{}.png".format(experiment)))

main()
