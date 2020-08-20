import matplotlib
matplotlib.use('Agg')

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
    print("for loop to separate time string complete ...")
    
    for d in range(len(datetimes)): 
        
        time_deltas[d] = (datetimes[d] - datetimes[0]).total_seconds()
        if d%50 == 0 :
            print(time_deltas[d])
   
   #Tracks seconde part of time stamp
    print("for loop to obtain time stamp complete...")                 

    return time_deltas

def main():
    
    # PARSER #
    parser = argparse.ArgumentParser()
    parser.add_argument('-f1', dest = 'F1', help = 'File to plot')
    parser.add_argument('-f2', dest = 'F2', help = 'File to plot')
    parser.add_argument('-f3', dest = 'F3', help = 'File to plot')
    parser.add_argument('-f4', dest = 'F4', help = 'File to plot')

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
    tension1, pulsewidth1 = get_experiment_name(fname1)
    tension2, pulsewidth2 = get_experiment_name(fname2)
    tension3, pulsewidth3 = get_experiment_name(fname3)
    tension4, pulsewidth4 = get_experiment_name(fname4)

    plt.figure(1)
    
    plt.plot(ET_file1, Plateau1,',',markersize = 1, color = 'crimson')
    plt.plot(ET_file2, Plateau2,',',markersize = 1, color = 'goldenrod')
    plt.plot(ET_file3, Plateau3,',',markersize = 1, color = 'yellowgreen')
    plt.plot(ET_file4, Plateau4,',',markersize = 1, color = 'teal')
    
    plt.xlabel("Elapsed time in seconds")
    plt.ticklabel_format(axis="x", style="sci")
    plt.ylabel("Plateau length in seconds")
    plt.title("Plateau length for {} {} in\n{} with {} configuration".format(tension,pulsewidth,args.MEDIUM,args.CONFIGURATION),y=1.08)
    plt.tight_layout()
    plt.savefig(os.path.join("OUT_FIG/PlateauLength_TimeElapsed/Multi_Plots"))

main()