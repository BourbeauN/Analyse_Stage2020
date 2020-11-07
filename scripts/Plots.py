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
    outfile = args.INFILE.split('/')[-1].replace('.csv','.pdf')
    
    foldername = args.INFILE
    experiment = foldername.split("/")[1].split(".")[0]
    parameter = foldername.split("/")[0]

    #Obtaining data in arrays
    Results = pd.read_csv(args.INFILE)
    x_data =  Results.iloc[:,1]
    y_data = Results.iloc[:,2]
    
    pdb.set_trace()

    ###PLOTS###
    plt.plot(x_data, y_data,'.',markersize = 1, color = 'crimson', linewidth = 0)
    plt.xlabel("Elapsed time (minutes)")
    plt.ticklabel_format(axis="y", style="sci")
    plt.ylabel("{}".format(parameter))
    plt.savefig(os.path.join("PLOTS/{}_{}".format(parameter,experiment),outfile))

main()
