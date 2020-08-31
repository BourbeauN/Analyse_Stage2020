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
    
    #Converting time difference to seconds
    for d in range(len(datetimes)): 
        
        time_deltas[d] = (datetimes[d] - datetimes[0]).total_seconds()
        
        #print to follow evolution of code during execution
        if d%50 == 0 :
            print(time_deltas[d])
   
   #Tracks seconde part of time stamp
    print("for loop to obtain time stamp complete...")                 

    return time_deltas,datetimes

#/Get the parameters of the experience analyzed for plot title
def get_experiment_name(folder_name):
    
    tension = folder_name.split("_")[3]
    pulsewidth = folder_name.split("_")[4]
    configuration = folder_name.split("_")[5]
    medium = folder_name.split("_")[6]

    return tension, pulsewidth, configuration, medium    
    
def main():
    
    #Parser to run code in server
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest = "INFILE", help = ".csv results file")

    args = parser.parse_args()
    outfile = args.INFILE.split('/')[-1].replace('.csv','.pdf')
    
    Results = pd.read_csv(args.INFILE)
    fname =  Results['Filename']
    ET_file,timestamps = get_elapsed_time(fname)
    Plateau = Results['Plateau']
    tension, pulsewidth, configuration, medium = get_experiment_name(args.INFILE)
    
    #Create list to append filtered data
    ET,Max_Voltage_Fin = [],[]
        
    #List of folders in need of data filtering
    ## Manually append when there are new folders to filter
    ## Add corresponding file filter to TimeStamp_Filter list with the same position
    Data_Filter = ["TAB_PLATEAU_VOLTDIS/VOLT_DIS_20kv_500ns_point-point_water_5000dv_15dk.csv","TAB_PLATEAU_VOLTDIS/VOLT_DIS_5kv_500ns_point-point_water_3000dv_15dk.csv","TAB_PLATEAU_VOLTDIS/VOLT_DIS_20kv_500ns_point-point_heptane_5000dv_15dk.csv"]

    #File from which to start analyzing
    ##Certain experiments have saved old data in the folder with the new data
    TimeStamp_Filter = ["20200630101319295","20200821110000743","20200703110232131"]

    filename = str(args.INFILE)
    
    ##If the experiment doesnt need to be filtered, this step is to assign a baseline value to the filter
    file_filter = fname[0]
    
    #To filter through the files in need of filtering and changing file_filter with the TimeStamp_Filter value associated with the filtered infolder
    for i in range(len(Data_Filter)):
        
        if filename == Data_Filter[i]:
            file_filter = TimeStamp_Filter[i]
    
    #Transforming the file_filter to be analyzed with datetime
    timetemp = file_filter.split("_")[-1].split(".csv")[0]
    
    #converting str to float with numerical value
    timethresh = datetime.strptime(timetemp,"%Y%m%d%H%M%S%f")

    #Filtering of files in analyzed folder
    for i in range(len(timestamps)):
        if timestamps[i] >= timethresh:
            ET.append(ET_file[i])
            Max_Voltage_Fin.append(Plateau[i])
    
    #Transforming final lists of data to array
    ET = np.asarray(ET)
    Max_Voltage_Fin = np.asarray(Max_Voltage_Fin)
    
    #Present an explicit error message
    if len(Plateau) != len (ET):
        print("array lengths dont match")
    
    ###PLOTS###
    
    plt.plot(ET_file, Plateau,'.',markersize = 1, color = 'crimson')
    plt.xlabel("Elapsed time in seconds")
    plt.ticklabel_format(axis="x", style="sci")
    plt.ylabel("Plateau length in seconds")
    plt.title("Plateau length for {} {} in\n{} with {} configuration".format(tension,pulsewidth,medium,configuration),y=1.08)
    plt.tight_layout()
    plt.savefig(os.path.join("OUT_FIG/PlateauLength_TimeElapsed/Savitsky_Golay",outfile))

main()
