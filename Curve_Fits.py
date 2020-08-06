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
import math as mt

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
   
   #Tracks seconde part of time stamp
    print("for loop to obtain time stamp complete...")                 

    return time_deltas

def get_experiment_name(folder_name):
    
    tension = folder_name.split("_")[5]
    pulsewidth = folder_name.split("_")[6]

    return tension, pulsewidth    
    
def Sqrt_Fit(x,a,b,c):
    x = np.array(x)
    f = mt.sqrt((a*x)+b)+c
    return f

# def Exp_Fit(x,a,b,c,d):
#     g = a*np.exp((-1/(b*x))+c)+d
#     return g

# def Ln_Fit(x,a,b,c,d):
#     h = a*np.log((b*x)+c)+d
#     return h

def main():
    
    #Parser to run code in server
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest = "INFILE", help = ".csv results file")
    parser.add_argument("-m", dest = "MEDIUM", help = "in what medium is the experiment taking place", default = "water")
    parser.add_argument("-c", dest = "CONFIGURATION", help = "electrode configuration", default = "point-point")

    args = parser.parse_args()
    outfile = args.INFILE.split('/')[-1].replace('.csv','.pdf')
    
    Results = pd.read_csv(args.INFILE)
   
    fname = Results[Results.columns[1]].as_matrix()
    Plateau = Results[Results.columns[2]].as_matrix()

    ET_file = get_elapsed_time(fname)
    
    tension, pulsewidth = get_experiment_name(args.INFILE)
        
    Plateau_fl = Plateau[~np.isnan(Plateau)]
    ET_file_fl = ET_file[~np.isnan(Plateau)]

    print(len(Plateau_fl),len(Plateau),len(ET_file_fl),len(ET_file))

    
    ###CurveFits***
    popt1,pcov1=curve_fit(Sqrt_Fit,ET_file_fl,Plateau_fl)
    # popt2,pcov2=curve_fit(Exp_Fit, ET_file_fl,Plateau_fl)
    # popt3,pcov3=curve_fit(Ln_Fit,ET_file_fl,Plateau_fl)
    
    plt.figure(1)
    
    ###SCATTER PLOTS###
    plt.plot(ET_file_fl, Plateau_fl,'.',markersize = 1, color = 'black')
    
    # ###CURVEFIT PLOTS###
    # plt.plot(ET_file_fl,Sqrt_fit(ET_file_fl,popt1[0],popt1[1],popt1[2]),color = 'crimson', linewidth = 2, label="Square root fit")
    # plt.plot(ET_file_fl,Exp_fit(ET_file_fl,popt2[0],popt2[1],popt2[2],popt2[3]),color = 'darkturquoise', linewidth = 2, label="Exponential fit")
    # plt.plot(ET_file_fl,Ln_fit(ET_file_fl,popt3[0],pop3[1],popt3[2],pop3[3]),color = 'yellowgreen', linewidth = 2, label="Natural logarithm fit")
    
    ###PLOT SETTINGS###
    plt.xlabel("Elapsed time in seconds")
    plt.ticklabel_format(axis="x", style="sci")
    plt.ylabel("Plateau length in seconds")
    plt.title("Plateau length for {} {} in\n{} with {} configuration".format(tension,pulsewidth,args.MEDIUM,args.CONFIGURATION),y=1.08)
    plt.tight_layout()
    plt.savefig(os.path.join("OUT_FIG/PlateauLength_TimeElapsed",outfile))
    
main()
