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

def get_information(folder_name):
    
    parameter = folder_name.split("/")[1].split(".")[0]
    return parameter

def main():
    #Parser to run code in server
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest = "INFILE", help = ".csv results file")
    args = parser.parse_args()
    #Obtaining data in arrays
    
    Results = pd.read_csv(args.INFILE)
    fname =  Results['Filename']
    
    Data = Results.iloc[:,2]

    #pdb.set_trace()
    data = np.asarray(Data.values)

    foldername = args.INFILE.split("/")[1]
    
    ET_file,timestamps = get_elapsed_time(fname)

    parameter = get_information(args.INFILE)
    DATA = np.column_stack((ET_file,data))

    pd.DataFrame(DATA, columns = ['Elapsed_Time', 'Data']).to_csv(os.path.join('AudrenFinal',"{}_{}.csv".format(foldername,parameter)))

main()

