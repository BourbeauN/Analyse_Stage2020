import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pdb
import argparse
from datetime import datetime
import os

#This function gives the elapsed time since the first discharge of the discharge file being analyzed.
def get_elapsed_time(fnames):
    
    for f in fnames:
        
	j = str(f)
	print(j)
	times = j.split("_")[-1].split(".csv")[0] 
    
    datetimes = [datetime.strptime(time, "%Y%m%d%H%M%S%f") for time in times]
    
    time_deltas = [(t - datetimes[0]).total_seconds() for t in datetimes]

    return time_deltas

def main():
    
    #Parser to run code in server
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest = "INFILE", help = ".csv results file")
    parser.add_argument("-dt", dest = "TIME_THRESHOLD", default = 10, help = "time threshold")
    parser.add_argument("-dv", dest = "VOLTAGE_THRESHOLD", default = 1000, help = "voltage threshold")
    args = parser.parse_args()
    outfile = args.INFILE.split('/')[-1].replace('.csv','.pdf')
    
    Results = pd.read_csv(args.INFILE)
   
    fname = Results[Results.columns[0]].as_matrix()
    Plateau = Results[Results.columns[1]].as_matrix()
    
    ET_file = get_elapsed_time(fname)
    
    if len(Plateau) != len (ET_file):
        print("array lengths dont match")
    
    ###PLOTS###
    plt.scatter(Plateau, ET_file)
    plt.xlabel("Elapsed time in seconds")
    plt.ylabel("Plateau length in seconds")
    plt.title("Plateau length in f. of elapsed time for {}".format(args.INFILE))
    plt.savefig(os.path.join("OUT_FIG/PlateauLength_TimeElapsed",outfile))

main()
