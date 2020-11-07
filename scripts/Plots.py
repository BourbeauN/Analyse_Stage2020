import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import pdb
import argparse
from datetime import datetime
import os

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
    
    #Converting time difference to seconds
    for d in range(len(datetimes)): 
        
        time_deltas[d] = (datetimes[d] - datetimes[0]).total_seconds()
        
        #print to follow evolution of code during execution
        if d%50 == 0 :
            print(time_deltas[d])
   
   #Tracks seconde part of time stamp
    print("for loop to obtain time stamp complete...")                 

    return time_deltas,datetimes


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
    
    test1, test2 = get_elapsed_time(x_data)
    
    pdb.set_trace()

    ###PLOTS###
    plt.plot(x_data, y_data,'.',markersize = 1, color = 'crimson', linewidth = 0)
    plt.xlabel("Elapsed time (minutes)")
    plt.ticklabel_format(axis="y", style="sci")
    plt.ylabel("{}".format(parameter))
    plt.savefig(os.path.join("PLOTS/{}_{}".format(parameter,experiment),outfile))

main()
