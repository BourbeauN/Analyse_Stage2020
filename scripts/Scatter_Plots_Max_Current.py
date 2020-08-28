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

    return time_deltas,datetimes

def get_experiment_name(folder_name):
    
    tension = folder_name.split("_")[1]
    pulsewidth = folder_name.split("_")[2]
    configuration = folder_name.split("_")[3]
    medium = folder_name.split("_")[4]

    return tension, pulsewidth,configuration,medium    
    
def main():
    
    #Parser to run code in server
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest = "INFILE", help = ".csv results file")
    parser.add_argument("-time", dest = "TIME", help = "time stamp to filter out data")
   
    args = parser.parse_args()
    outfile = args.INFILE.split('/')[-1].replace('.csv','.pdf')
    
    Results = pd.read_csv(args.INFILE)
    fname =  Results['Filename']
    ET_file,timestamps = get_elapsed_time(fname)
    Max_Current = Results['Max Current']
    tension, pulsewidth,configuration,medium = get_experiment_name(args.INFILE)
    
    ET,Max_Current_Fin = [],[]
    
    timestr = args.TIME
    timethresh = datetime.strptime(timestr,"%Y%m%d%H%M%S%f")
    
    for i in range(len(timestamps)):
        if timestamps[i] > timethresh:
            ET.append(ET_file[i])
            Max_Current_Fin.append(Max_Current[i])
    
    ET = np.asarray(ET)
    Max_Current_Fin = np.asarray(Max_Current_Fin)
    
    #Present an explicit error message
    if len(Max_Current) != len (ET_file):
        print("array lengths dont match")
    
    pdb.set_trace()

    ###PLOTS###
    
    plt.plot(ET, Max_Current_Fin,'.',markersize = 1, color = 'crimson')
    plt.xlabel("Elapsed time in seconds")
    plt.ticklabel_format(axis="x", style="sci")
    plt.ylabel("Current of discharge")
    plt.title("Plateau length for {} {} in\n{} with {} configuration".format(tension,pulsewidth,medium,configuration),y=1.08)
    plt.tight_layout()
    pdb.set_trace()
    plt.savefig(os.path.join("OUT_FIG/Max_Current",outfile))

main()

