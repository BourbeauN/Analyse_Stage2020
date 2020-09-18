import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import axes as ax
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

#Get the parameters of the experience analyzed for plot title
def get_experiment_name(folder_name):
    
    tension = folder_name.split("/")[2].split("_")[0]
    pulsewidth = folder_name.split("/")[2].split("_")[1]
    configuration = folder_name.split("/")[2].split("_")[2]
    medium = folder_name.split("/")[2].split(".csv")[0].split("_")[3]

    return tension, pulsewidth,configuration,medium    

def main():
    #Parser to run code in server
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", dest = "METHOD", help = "integration method")
    parser.add_argument("-f", dest = "INFILE", help = ".csv results file")
    args = parser.parse_args()
    outfile = args.INFILE.split('/')[-1].replace('.csv','.pdf')
    
    #Obtaining data in arrays
    Results = pd.read_csv(args.INFILE)
    fname =  Results['Filename']
    ET_file,timestamps = get_elapsed_time(fname)
    Integration = Results['Integration']
    
    #calling function for folder parameters for plot title
    tension, pulsewidth,configuration,medium = get_experiment_name(args.INFILE)
    #Create list to append filtered data
    temp_stamp,ET,Integration_Fin = [],[],[]
    #List of folders in need of data filtering
    ## Manually append when there are new folders to filter
    ## Add corresponding file filter to TimeStamp_Filter list with the same position
    Data_Filter = ["Injected_Charges/Trapeze/20kv_500ns_point-point_water.csv","Injected_Charges/Trapeze/5kv_500ns_point-point_water.csv","Injected_Charges/Trapeze/20kv_500ns_point-point_heptane.csv","Injected_Charges/Trapeze/20kv_100ns_point-point_water.csv",
                   "Injected_Charges/Simpson/20kv_500ns_point-point_water.csv","Injected_Charges/Simpson/5kv_500ns_point-point_water.csv","Injected_Charges/Simpson/20kv_500ns_point-point_heptane.csv","Injected_Charges/Simpson/20kv_100ns_point-point_water.csv",
                   "Injected_Charges/Romberg/20kv_500ns_point-point_water.csv","Injected_Charges/Romberg/5kv_500ns_point-point_water.csv","Injected_Charges/Romberg/20kv_500ns_point-point_heptane.csv","Injected_Charges/Romberg/20kv_100ns_point-point_water.csv"]

    #File from which to start analyzing
    ##Certain experiments have saved old data in the folder with the new data
    TimeStamp_Filter = ["b_20200630101319295","b_20200821105944770","b_20200703110232131","s_20200821095026045",
                        "b_20200630101319295","b_20200821105944770","b_20200703110232131","s_20200821095026045",
                        "b_20200630101319295","b_20200821105944770","b_20200703110232131","s_20200821095026045"]

    ##If the experiment doesnt need to be filtered, this step is to assign a baseline value to the filter
    
    filename = str(args.INFILE)
    timethreshold = fname[0].split("_")[-1].split(".csv")[-1]
    bound = "none"

   #To filter through the files in need of filtering and changing file_filter with the TimeStamp_Filter value associated with the filtered infolder
    for i in range(len(Data_Filter)):
        #pdb.set_trace()
        if filename == Data_Filter[i]:

            bound = TimeStamp_Filter[i].split("_")[0]
            timethreshold = TimeStamp_Filter[i].split("_")[1]
            timethresh_final = datetime.strptime(timethreshold,"%Y%m%d%H%M%S%f")
    
    #Filtering of files in analyzed folder
    for i in range(len(timestamps)):
        if bound == "b" and timestamps[i] >= timethresh_final or bound == "s" and timestamps[i] <= timethresh_final:
            
            temp_stamp.append(timestamps[i])
            Integration_Fin.append(Integration[i])
   
    for i in range(len(temp_stamp)):
        ET.append(((temp_stamp[i]-temp_stamp[0]).total_seconds()))

            #Transforming final lists of data to array
    ET = np.asarray(ET)
    Integration_Fin = np.asarray(Integration_Fin)

    if bound == "s" or bound == "b":
        ###PLOTS###
        plt.plot(ET/60, Integration_Fin*1e6,'.',markersize = 1, color = 'crimson', linewidth = 0)
        plt.xlabel("Elapsed time (minutes)")
        plt.ticklabel_format(axis="y", style="sci")
        plt.ylabel(r"Injected Charges ($\mu$C)")
        plt.title("Injected charges for {} {} in\n{} with {}configuration".format(tension,pulsewidth,medium,configuration))
        plt.savefig(os.path.join("OUT_FIG/Inj_Charges/{}".format(args.METHOD),outfile))

    else :
        ###PLOTS###
        plt.plot(ET_file/60, Integration*1e6,'.',markersize = 1, color = 'crimson', linewidth = 0)
        plt.xlabel("Elapsed time (minutes)")
        plt.ticklabel_format(axis="y", style="sci")
        plt.ylabel(r"Injected Charges ($\mu$C)")
        plt.title("Injected charges for {} {} in\n{} with {} configuration".format(tension,pulsewidth,medium,configuration))
        plt.savefig(os.path.join("OUT_FIG/Inj_Charges/{}".format(args.METHOD),outfile))

main()
