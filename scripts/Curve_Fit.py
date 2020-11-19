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

def Distribution_info(dispars):
    dispars_elements = dispars.split(",")
    return dispars_elements

def Sqrt(x,a,b,c,d):
    f = a * np.sqrt((b*x)+c)+d
    return f

def Ln(x,a,b,c,d):
    f = a*np.log((b*x)+c)+d
    return f

def Exponential(x,a,b,c,d):
    f = a*np.exp((b*x)+c)+d 
    return f

def Quadratic(x,a,b,c,d,e):
    f = (a*(x+b)**2)+(c*(x+d))+e
    return f

def Weibull(x,a,b):
    f = (a/b)*((x/b)**(a-1))*(np.exp(-((x/b)**a)))
    return f

def get_information(folder_name):
    param = folder_name.split("/")[1].split(".")[0].split("_")[0:2]
    filen = folder_name.split("/")[1].split(".")[0].split("_")[2:]
    d = "_"
    parameter = d.join(param)
    fname = d.join(filen)

    return parameter,fname

def main():   
    #Parser to run code in server
    parser = argparse.ArgumentParser()
    parser.add_argument("-Lfile", dest = "LIMITS", help = ".csv results file")
    parser.add_argument("-f", dest = "INFILE", help = "data file corresponding to limits")
    parser.add_argument("-d", type = str, dest = "DISTRIBUTION", help = "distribution to fit")
    
    args = parser.parse_args() 
    
    #Importing data file as a matrix
    Limits = pd.read_csv(args.LIMITS)

    x_min = Limits["x_min"].values.ravel()
    x_max = Limits["x_max"].values.ravel()
    y_min = Limits["y_min"].values.ravel()
    y_max = Limits["y_max"].values.ravel()
    
    Data = pd.read_csv(args.INFILE)
    x_data = Data.iloc[:,1]
    y_data = Data.iloc[:,2]
    pdb.set_trace() 
    #distribution_list = Distribution_info(args.DISTRIBUTION)
    distribution_list = []
    distribution_list.append(args.DISTRIBUTION)
    parameter,fname = get_information(args.INFILE)
    

    for i in distribution_list:
        if i == "exp":
            popt_min,pcov_min = curve_fit(Exponential,x_min,y_min,maxfev=10000)  
            popt_max,pcov_max = curve_fit(Exponential,x_max,y_max,maxfev=10000)
            print('exp',np.sqrt(np.diag(pcov_min)))
            print('exp',np.sqrt(np.diag(pcov_max)))
            
            plt.figure(1)
            plt.plot(x_data,y_data,marker='.',markersize=1,color = 'black', linewidth=0)
            plt.plot(x_min,Exponential(x_min,popt_min[0],popt_min[1],popt_min[2],popt_min[3]),linewidth=1,color = "salmon")
            plt.plot(x_max,Exponential(x_max,popt_max[0],popt_max[1],popt_max[2],popt_max[3]),linewidth=1,color = "crimson")
            plt.legend()
            plt.savefig(os.path.join("PLOTS/{}/{}_{}.pdf".format(parameter,fname,i)))
            plt.savefig(os.path.join("PLOTS/{}/{}_{}.png".format(parameter,fname,i)))
            
        if i == "log":
            popt_min,pcov_min = curve_fit(Ln,x_min,y_min,maxfev=10000)  
            popt_max,pcov_max = curve_fit(Ln,x_max,y_max,maxfev=10000)
            print('log',np.sqrt(np.diag(pcov_min)))
            print('log',np.sqrt(np.diag(pcov_max)))
            
            plt.figure(1)
            plt.plot(x_data,y_data,marker='.',markersize=1,color = 'black', linewidth=0)
            plt.plot(x_min,Ln(x_min,popt_min[0],popt_min[1],popt_min[2],popt_min[3]),linewidth=1,color = "salmon")
            plt.plot(x_max,Ln(x_max,popt_max[0],popt_max[1],popt_max[2],popt_max[3]),linewidth=1,color = "crimson")
            plt.legend()
            plt.savefig(os.path.join("PLOTS/{}/{}_{}.pdf".format(parameter,fname,i)))
            plt.savefig(os.path.join("PLOTS/{}/{}_{}.png".format(parameter,fname,i)))
            
        if i == "sqrt":
            popt_min,pcov_min = curve_fit(Sqrt,x_min,y_min,maxfev=10000)  
            popt_max,pcov_max = curve_fit(Sqrt,x_max,y_max,maxfev=10000)
            print('sqrt',np.sqrt(np.diag(pcov_min)))
            print('sqrt',np.sqrt(np.diag(pcov_max)))
            print('min',popt_min)
	    print('max',popt_max)
            plt.figure(1)
            plt.plot(x_data,y_data,marker='.',markersize=1,color = 'black', linewidth=0)
            #plt.plot(x_min,Sqrt(x_min,popt_min[0],popt_min[1],popt_min[2],popt_min[3]),linewidth=1,color = "salmon")
            plt.plot(x_max,Sqrt(x_max,popt_max[0],popt_max[1],popt_max[2],popt_max[3]),linewidth=1,color = "crimson")
            plt.legend()
            plt.savefig(os.path.join("PLOTS/{}/{}_{}.pdf".format(parameter,fname,i)))
            plt.savefig(os.path.join("PLOTS/{}/{}_{}.png".format(parameter,fname,i)))
            
        if i == "quad":
            popt_min,pcov_min = curve_fit(Quadratic,x_min,y_min,maxfev=10000)  
            popt_max,pcov_max = curve_fit(Quadratic,x_max,y_max,maxfev=10000)
            print('quad',np.sqrt(np.diag(pcov_min)))
            print('quad',np.sqrt(np.diag(pcov_max)))
            
            plt.figure(1)
            plt.plot(x_data,y_data,marker='.',markersize=1,color = 'black', linewidth=0)
            #plt.plot(x_min,Quadratic(x_min,popt_min[0],popt_min[1],popt_min[2],popt_min[3],popt_min[4]),linewidth=1,color= "salmon")
            plt.plot(x_max,Quadratic(x_max,popt_max[0],popt_max[1],popt_max[2],popt_max[3],popt_min[4]),linewidth=1,color = "crimson")
            plt.legend()
            plt.savefig(os.path.join("PLOTS/{}/{}_{}.pdf".format(parameter,fname,i)))
            plt.savefig(os.path.join("PLOTS/{}/{}_{}.png".format(parameter,fname,i)))     
            
        if i == "weibull":
            popt_min,pcov_min = curve_fit(Weibull,x_min,y_min,maxfev=10000)  
            popt_max,pcov_max = curve_fit(Weibull,x_max,y_max,maxfev=10000)
            print('weibull',np.sqrt(np.diag(pcov_min)))
            print('weibull',np.sqrt(np.diag(pcov_max)))
        
            plt.figure(1)
            plt.plot(x_data,y_data,marker='.',markersize=1,color = 'black', linewidth=0)
            #plt.plot(x_min,Weibull(x_min,popt_min[0],popt_min[1]),linewidth=1,color = "salmon")
            plt.plot(x_max,Weibull(x_max,popt_max[0],popt_max[1]),linewidth=1,color = "crimson")
            plt.legend()
            plt.savefig(os.path.join("PLOTS/{}/{}_{}.pdf".format(parameter,fname,i)))
            plt.savefig(os.path.join("PLOTS/{}/{}_{}.png".format(parameter,fname,i)))
      
     
main()
