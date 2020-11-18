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
    parameter = folder_name.split("/")[1,:].split(".")[0]
    return parameter

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
    
    distribution_list = Distribution_info(args.DISTRIBUTION)
    parameter = get_information(args.LIMITS)
    
    for i in distribution_list:
        if i == "exp":
            popt_min,pcov_min = curve_fit(Exponential,x_min,y_min)  
            popt_max,pcov_max = curve_fit(Exponential,x_max,y_max)
            perr_min = np.sqrt(np.diag(pcov_min))
            perr_max = np.sqrt(np.diag(pcov_max))
            
            plt.figure(1)
            plt.plot(x_data,y_data,marker='.',markersize=1,color = 'black', linewidth=0)
            plt.plot(x_min,Exponential(x_min,popt_min[0],popt_min[1],popt_min[2],popt_min[3]),linewidth=1,color = "salmon",legend = "sigma {}".format(perr_min))
            plt.plot(x_max,Exponential(x_max,popt_max[0],popt_max[1],popt_max[2],popt_max[3]),linewidth=1,color = "crimson",legend = "sigma {}".format(perr_max))
            plt.savefig(os.path.join("PLOTS/{}_{}.pdf".format(parameter,args.DISTRIBUTION)))
            plt.savefig(os.path.join("PLOTS/{}_{}.png".format(parameter,args.DISTRIBUTION)))
            
        if i == "log":
            popt_min,pcov_min = curve_fit(Ln,x_min,y_min)  
            popt_max,pcov_max = curve_fit(Ln,x_max,y_max)
            perr_min = np.sqrt(np.diag(pcov_min))
            perr_max = np.sqrt(np.diag(pcov_max))
            
            plt.figure(1)
            plt.plot(x_data,y_data,marker='.',markersize=1,color = 'black', linewidth=0)
            plt.plot(x_min,Ln(x_min,popt_min[0],popt_min[1],popt_min[2],popt_min[3]),linewidth=1,color = "salmon",legend = "sigma {}".format(perr_min))
            plt.plot(x_max,Ln(x_max,popt_max[0],popt_max[1],popt_max[2],popt_max[3]),linewidth=1,color = "crimson",legend = "sigma {}".format(perr_max))
            plt.savefig(os.path.join("PLOTS/{}_{}.pdf".format(parameter.args.DISTRIBUTION)))
            plt.savefig(os.path.join("PLOTS/{}_{}.png".format(parameter,args.DISTRIBUTION)))
            
        if i == "sqrt":
            popt_min,pcov_min = curve_fit(Sqrt,x_min,y_min)  
            popt_max,pcov_max = curve_fit(Sqrt,x_max,y_max)
            perr_min = np.sqrt(np.diag(pcov_min))
            perr_max = np.sqrt(np.diag(pcov_max))
            
            plt.figure(1)
            plt.plot(x_data,y_data,marker='.',markersize=1,color = 'black', linewidth=0)
            plt.plot(x_min,Sqrt(x_min,popt_min[0],popt_min[1],popt_min[2],popt_min[3]),linewidth=1,color = "salmon",legend = "sigma {}".format(perr_min))
            plt.plot(x_max,Sqrt(x_max,popt_max[0],popt_max[1],popt_max[2],popt_max[3]),linewidth=1,color = "crimson",legend = "sigma {}".format(perr_max))
            plt.savefig(os.path.join("PLOTS/{}_{}.pdf".format(parameter.args.DISTRIBUTION)))
            plt.savefig(os.path.join("PLOTS/{}_{}.png".format(parameter,args.DISTRIBUTION)))
            
        if i == "quad":
            popt_min,pcov_min = curve_fit(Quadratic,x_min,y_min)  
            popt_max,pcov_max = curve_fit(Quadratic,x_max,y_max)
            perr_min = np.sqrt(np.diag(pcov_min))
            perr_max = np.sqrt(np.diag(pcov_max))
            
            plt.figure(1)
            plt.plot(x_data,y_data,marker='.',markersize=1,color = 'black', linewidth=0)
            plt.plot(x_min,Quadratic(x_min,popt_min[0],popt_min[1],popt_min[2],popt_min[3],popt_min[4]),linewidth=1,color = "salmon",legend = "sigma {}".format(perr_min))
            plt.plot(x_max,Quadratic(x_max,popt_max[0],popt_max[1],popt_max[2],popt_max[3],popt_min[4]),linewidth=1,color = "crimson",legend = "sigma {}".format(perr_max))
            plt.savefig(os.path.join("PLOTS/{}_{}.pdf".format(parameter.args.DISTRIBUTION)))
            plt.savefig(os.path.join("PLOTS/{}_{}.png".format(parameter,args.DISTRIBUTION)))     
            
        if i == "weibull":
            popt_min,pcov_min = curve_fit(Weibull,x_min,y_min)  
            popt_max,pcov_max = curve_fit(Weibull,x_max,y_max)
            perr_min = np.sqrt(np.diag(pcov_min))
            perr_max = np.sqrt(np.diag(pcov_max))
        
            plt.figure(1)
            plt.plot(x_data,y_data,marker='.',markersize=1,color = 'black', linewidth=0)
            plt.plot(x_min,Weibull(x_min,popt_min[0],popt_min[1]),linewidth=1,color = "salmon",legend = "sigma {}".format(perr_min))
            plt.plot(x_max,Weibull(x_max,popt_max[0],popt_max[1]),linewidth=1,color = "crimson",legend = "sigma {}".format(perr_max))
            plt.savefig(os.path.join("PLOTS/{}_{}.pdf".format(parameter.args.DISTRIBUTION)))
            plt.savefig(os.path.join("PLOTS/{}_{}.png".format(parameter,args.DISTRIBUTION)))
      
     
main()