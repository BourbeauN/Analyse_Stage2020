import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import pdb
import argparse
from datetime import datetime
import os
from scipy.optimize import curve_fit
#import math as mti
from scipy.signal import savgol_filter

#This function gives the elapsed time since the first discharge of the discharge file being analyzed.
def get_elapsed_time(fnames):

    datetimes = np.zeros_like(fnames)
    time_deltas = np.zeros_like(fnames)

    #For loop to get an array of floats corresponding to the timestamps of all discharges (fname)
    for f in range(len(fnames)):
        
        #converts filename to string
        j = fnames[f]
        
        #Takes filename from array to keep only the digits
        times = j.split("_")[-1].split(".csv")[0]
       
        #transforms the digits in a timestamp        
        datetimes[f] = datetime.strptime(times,"%Y%m%d%H%M%S%f")
    
    #Allows to track the first part of the time stamp 
    print("for loop to separate time string complete ...")
    
    for d in range(len(datetimes)): 
        
        time_deltas[d] = (datetimes[d] - datetimes[0]).total_seconds()
   
   #Tracks seconde part of time stamp
    print("for loop to obtain time stamp complete...")                 

    return time_deltas

def get_experiment_name(folder_name):
    
    tension = folder_name.split("_")[5]
    pulsewidth = folder_name.split("_")[6]

    return tension, pulsewidth    
    
def Sqrt_Fit(x,a,b,c):

    for i in x:
    	i = np.float(i)

    print("not sure about being able to call the function")

    f = (a*((np.abs(x+b))**0.5)) + c

    return f

def Ln_Fit(x,a,b,c,d):
    h = a*np.log(np.array((b*x)+c, dtype = float))+d
    return h

def Data_Filter(y,window,pol_degree):
    return savgol_filter(y,window,pol_degree)
    
def main():   
    #Parser to run code in server
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest = "INFILE", help = ".csv results file")
    parser.add_argument("-m", dest = "MEDIUM", help = "in what medium is the experiment taking place", default = "water")
    parser.add_argument("-c", dest = "CONFIGURATION", help = "electrode configuration", default = "point-point")
    #arser.add_argument("-w", dest = "WINDOW", help = "window length to apply data filter")
    #arser.add_argument("-d", dest = "POLYNOMIALDEGREE", help = "polynomial degree of data filter")
    
    args = parser.parse_args()
    outfile = args.INFILE.split('/')[-1].replace('.csv','.pdf')
    
    #Importing data file as a matrix
    Results = pd.read_csv(args.INFILE)

    fname = Results.iloc[:,1]
    Plateau = Results.iloc[:,2].values.ravel()

    #calling function to obtain the elapsed time since the first discharge of every discharge
    ET_file = get_elapsed_time(fname)
    
    #calling function to obtain the experiment parameters (from the name) for the figure title 
    tension, pulsewidth = get_experiment_name(args.INFILE)

    #removing nans from plateau and then removing the adjacent elapsed time value from the elapsed time array
    Plateau_fl = Plateau[~np.isnan(Plateau)]
    ET_file_fl = ET_file[~np.isnan(Plateau)]

    #calling filter function to make the curvefit easier.
    #the numerical values in the Data_Filter function can be changed to modify the strength of the filter
    Plateau_filter_w15_d1 = Data_Filter(Plateau_fl,15,1)

    Plateau_filter_w15_d1 = np.array(Plateau_filter_w15_d1)
    ET_file_fl = np.asarray(ET_file_fl)
    
    print(Plateau_filter_w15_d1.dtype)
    print(ET_file_fl.dtype)
    
    popt1,pcov1 = curve_fit(Sqrt_Fit,ET_file_fl.ravel(),Plateau_filter_w15_d1.ravel())

    print("first curve_fit completed")

    popt3,pcov3 = curve_fit(Ln_Fit,ET_file_fl.ravel(),Plateau_filter_w15_d1.ravel())
    
    plt.figure(1)
    
    ###SCATTER PLOTS###
    plt.plot(ET_file_fl, Plateau_fl,'.',markersize = 1, color='black',label = "Data")
    plt.plot(ET_file_fl, Plateau_filter_w15_d1,'.',markersize = 1, color = 'darkmagenta',label = "w15_d1")
    #plt.plot(square_x,square_y, color = 'seagreen', label = 'square root function')
    #plt.plot(square_x,ln_y, color = 'darksalmon', label = 'natural logarithmic function')
    ###CURVEFIT PLOTS###
    plt.plot(ET_file_fl,Sqrt_Fit(ET_file_fl,popt1[0],popt1[1],popt1[2]),color = 'crimson', linewidth = 2, label="Square root fit")
    plt.plot(ET_file_fl,Ln_Fit(ET_file_fl,popt3[0],popt3[1],popt3[2],popt3[3]),color = 'yellowgreen', linewidth = 2, label="Natural logarithm fit")
    
    pdb.set_trace()
    ###PLOT SETTINGS###
    plt.xlabel("Elapsed time in seconds")
    plt.ticklabel_format(axis="y", style="sci")
    plt.ylabel("Plateau length in seconds")
    plt.title("Plateau length for {} {} in\n{} with {} configuration".format(tension,pulsewidth,args.MEDIUM,args.CONFIGURATION),y=1.08)
    plt.tight_layout()
    plt.legend()
    plt.savefig(os.path.join("OUT_FIG/PlateauLength_TimeElapsed",outfile))
    
main()