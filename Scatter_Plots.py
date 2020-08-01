import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pdb
import argparse
from datetime import datetime

#This function gives the elapsed time since the first discharge of the discharge file being analyzed.
def get_elapsed_time(fnames):
    
    times = [f.split("_")[-1].split(".csv")[0] for f in fnames]
    
    datetimes = [datetime.strptime(time, "%Y%m%d%H%M%S%f") for time in times]
    
    time_deltas = [(t - datetimes[0]).total_seconds() for t in datetimes]

    return time_deltas

def main():
    
    #Parser to run code in server
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest = "INFILE", help = ".csv results file")
    parser.add_argument("-p", dest = "PLATEAU_FILE", help = "Chose file containing plateau_lengths with fixed thresholds")
    parser.add_argument("-dt", dest = "TIME_THRESHOLD", default = 10, help = "time threshold")
    parser.add_argument("-dv", dest = "VOLTAGE_THRESHOLD", default = 1000, help = "voltage threshold")
    
    args = parser.parse_args()
    
    Results = pd.read_csv(args.INFILE)    
    
    Results = Results[Results.time_delta == args.TIME_THRESHOLD][Results.voltage_delta == args.VOLTAGE_THRESHOLD]    
    ET_file = get_elapsed_time(Results.fname)
    
    if len(Results) != len (ET_file):
        print("array lengths dont match")
    
    ###PLOTS###
    plt.scatter(Results, ET_file)
    plt.xlabel("Elapsed time in seconds")
    plt.ylabel("Plateau length in seconds")
    plt.title("Plateau length in f. of elapsed time for {}".format(args.INFILE))
    plt.show()

main()