import matplotlib
matplotlib.use('Agg')
import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import pdb
import argparse
from datetime import datetime

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
    # print("for loop to separate time string complete ...")
    
    for d in range(len(datetimes)): 
        
        time_deltas[d] = (datetimes[d] - datetimes[0]).total_seconds()
        if d%50 == 0 :
            print(time_deltas[d])
   
   #Tracks seconde part of time stamp
    #print("for loop to obtain time stamp complete...")                 

    return time_deltas
def get_experiment_name(folder_name):
    
    tension = folder_name.split("_")[5]
    pulsewidth = folder_name.split("_")[6]
    configuration = folder_name.split("_")[7]
    medium = folder_name.split("_")[8]
    
    return tension, pulsewidth, configuration, medium

def main():
    
    # PARSER #
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest = 'parameter', help = 'chose a parameter to analyze')
    
    args = parser.parse_args()
    
    #Reading file
    Results1 = pd.read_csv(args.F1)
    Results2 = pd.read_csv(args.F2)
    Results3 = pd.read_csv(args.F3)
    Results4 = pd.read_csv(args.F4)
    
    #Obtaining filenames
    fname1 =  Results1['Filename']
    fname2 =  Results2['Filename']
    fname3 =  Results3['Filename']
    fname4 =  Results4['Filename']
    
    #Obtaining elapsed time for every discharge for every experiment#
    ET_file1 = get_elapsed_time(fname1)
    ET_file2 = get_elapsed_time(fname2)
    ET_file3 = get_elapsed_time(fname3)
    ET_file4 = get_elapsed_time(fname4)
    
    #Extracting plateau lengths from files
    Plateau1 = Results1['Plateau']
    Plateau2 = Results2['Plateau']
    Plateau3 = Results3['Plateau']
    Plateau4 = Results4['Plateau']
    
    #Experiment name from file name
    tension1, pulsewidth1 = get_experiment_name(args.F1)
    tension2, pulsewidth2 = get_experiment_name(args.F2)
    tension3, pulsewidth3 = get_experiment_name(args.F3)
    tension4, pulsewidth4 = get_experiment_name(args.F4)
    plt.figure(1)
    labels = [(tension1,pulsewidth1), (tension2,pulsewidth2),(tension3,pulsewidth3),(tension4,pulsewidth4)]
    plt.plot(ET_file1, Plateau1,',',markersize = 1, color = 'crimson', label = labels[0])
    plt.plot(ET_file2, Plateau2,',',markersize = 1, color = 'goldenrod', label = labels[1])
    plt.plot(ET_file3, Plateau3,',',markersize = 1, color = 'yellowgreen', label = labels[2])
    plt.plot(ET_file4, Plateau4,',',markersize = 1, color = 'teal', label = labels[3])
    
    plt.xlabel("Elapsed time in seconds")
    plt.ticklabel_format(axis="x", style="sci")
    plt.ylabel("Plateau length in seconds")
    plt.title("Plateau length for {} {} in\n{} with {} configuration".format("variying tensions ",
    "multiple pulse widths", "water", "point-point"),y=1.08)
    plt.legend()
    plt.tight_layout()
    now_str = datetime.now().timestamp() 
    plt.savefig(os.path.join("OUT_FIG/Multi_Plots/Multi_Plots_{}.pdf".format(now_str)))
    
    pdb.set_trace()
main()
