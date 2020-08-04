import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import pdb
import argparse
from datetime import datetime
import os

#This function gives the elapsed time since the first discharge of the discharge file being analyzed.
def get_elapsed_time(fnames):

    datetimes = np.zeros_like(fnames)
    time_deltas = np.zeros_like(fnames)
    
    #For loop to get an array of floats corresponding to the timestamps of all discharges (fname)
    for f in range(len(fnames)):
        
        #converts filename to string
        j = str(fnames[f])
        
        #Takes filename from array to keep only the digits
        times = j.split("_")[-1].split(".csv")[0]
       
        #transforms the digits in a timestamp        
        datetimes[f] = datetime.strptime(times,"%Y%m%d%H%M%S%f")
    
    #Allows to track the first part of the time stamp 
    print("for loop to separate time string complete ...")
    
    for d in range(len(datetimes)): 
        
        time_deltas[d] = (datetimes[d] - datetimes[0]).total_seconds()
        if d%50 == 0 :
            print(time_deltas[d])
   
   #Tracks seconde part of time stamp
    print("for loop to obtain time stamp complete...")                 

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
   
    fname = Results[Results.columns[1]].as_matrix()
    Plateau = Results[Results.columns[2]].as_matrix()
    

    ET_file = get_elapsed_time(fname)
    
    #Present an explicit error message
    if len(Plateau) != len (ET_file):
        print("array lengths dont match")
    
    ###PLOTS###
    
    plt.plot(ET_file, Plateau,'.',markersize = 3, color = 'crimson')
    plt.xlabel("Elapsed time in seconds")
    plt.ylabel("Plateau length in seconds")
    plt.title("Plateau length in f. of elapsed time for \n{}".format(args.INFILE),y=1.08)
    plt.tight_layout()
    plt.savefig(os.path.join("OUT_FIG/PlateauLength_TimeElapsed",outfile))

main()
