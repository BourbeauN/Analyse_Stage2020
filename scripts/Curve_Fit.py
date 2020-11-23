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
    f = a*np.log((b*x))+c+(d*0)
    return f

def Exponential(x,a,b,c,d):
    f = a*np.exp(b*x)+c+(d*0) 
    return f

def Quadratic(x,a,b,c,d):
    f = a*(x**2)+b*x+c+(d*0)
    return f

def Weibull(x,a,b,c,d):
    f = (a-np.exp(-((x/b)**c)))**d
    return f

def Linear(x,a,b,c,d):
    f = (a*x)+b + ((c+d)*0)
    return f

def ThirdDegree(x,a,b,c,d):
    f = (a*(x**3))+(b*(x**2))+(c*x)+d
    return f

def Sigmoid(x,a,b,c,d):
    f = a/(b+np.exp**(c*x))+d
    
    return f

def get_information(folder_name):
    param = folder_name.split("/")[1].split(".")[0].split("_")[0:2]
    filen = folder_name.split("/")[1].split(".")[0].split("_")[2:]
    d = "_"
    parameter = d.join(param)
    fname = d.join(filen)

    return parameter,fname

def Plots(x_min,x_max,y_min,y_max,x_data,y_data,popt_min,popt_max,pcov_min,pcov_max,parameter,fname,i):
    
    if i == 'exp':
        label_min = r'${}e^({}x)+{}$'.format(popt_min[0],popt_min[1],popt_min[2])
        label_max = r'${}e^({}x)+{}$'.format(popt_max[0],popt_max[1],popt_max[2])
    
    plt.figure(1)
    plt.plot(x_data,y_data*(10**6),marker='.',markersize=1,color = 'black', linewidth=0)
    plt.plot(x_min,Exponential(x_min,popt_min[0],popt_min[1],popt_min[2],popt_min[3]),linewidth=1,color = "salmon",label=label_min)
    plt.plot(x_max,Exponential(x_max,popt_max[0],popt_max[1],popt_min[2],popt_min[3]),linewidth=1,color = "crimson",label=label_max)
    plt.plot(x_min,y_min,marker='.',color='yellowgreen',linewidth=0)
    plt.plot(x_max,y_max,marker='.',color='yellowgreen',linewidth=0)
    plt.legend()
    plt.savefig(os.path.join("PLOTS/{}/{}_{}.pdf".format(parameter,fname,i)))    

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
            
            Plots(x_min,x_max,y_min,y_max,x_data,y_data,popt_min,popt_max,pcov_min,pcov_max,parameter,fname,i)
            
        if i == "log":
            popt_min,pcov_min = curve_fit(Ln,x_min,y_min,maxfev=10000)  
            popt_max,pcov_max = curve_fit(Ln,x_max,y_max,maxfev=10000)
            print('log',np.sqrt(np.diag(pcov_min)))
            print('log',np.sqrt(np.diag(pcov_max)))
            
            Plots(x_min,x_max,y_min,y_max,x_data,y_data,popt_min,popt_max,pcov_min,pcov_max,parameter,fname,i)
            
        if i == "sqrt":
            popt_min,pcov_min = curve_fit(Sqrt,x_min,y_min,maxfev=10000)  
            popt_max,pcov_max = curve_fit(Sqrt,x_max,y_max,maxfev=10000)
            print('sqrt',np.sqrt(np.diag(pcov_min)))
            print('sqrt',np.sqrt(np.diag(pcov_max)))

            Plots(x_min,x_max,y_min,y_max,x_data,y_data,popt_min,popt_max,pcov_min,pcov_max,parameter,fname,i)
            
        if i == "quad":
            popt_min,pcov_min = curve_fit(Quadratic,x_min,y_min,maxfev=10000)  
            popt_max,pcov_max = curve_fit(Quadratic,x_max,y_max,maxfev=10000)
            print('quad',np.sqrt(np.diag(pcov_min)))
            print('quad',np.sqrt(np.diag(pcov_max)))
            
            Plots(x_min,x_max,y_min,y_max,x_data,y_data,popt_min,popt_max,pcov_min,pcov_max,parameter,fname,i)
            
        if i == "weibull":
            popt_min,pcov_min = curve_fit(Weibull,x_min,y_min,maxfev=10000)  
            popt_max,pcov_max = curve_fit(Weibull,x_max,y_max,maxfev=10000)
            print('weibull',np.sqrt(np.diag(pcov_min)))
            print('weibull',np.sqrt(np.diag(pcov_max)))
        
            Plots(x_min,x_max,y_min,y_max,x_data,y_data,popt_min,popt_max,pcov_min,pcov_max,parameter,fname,i)
            
        if i == "lin":
            popt_min,pcov_min = curve_fit(Linear,x_min,y_min,maxfev=10000)
            popt_max,pcov_max = curve_fit(Linear,x_max,y_max,maxfev=10000)
            var_min = np.sqrt(np.diag(pcov_min))
            var_max = np.sqrt(np.diag(pcov_max))
            
            print('linear', var_max )
            print('linear', var_min )

            Plots(x_min,x_max,y_min,y_max,x_data,y_data,popt_min,popt_max,pcov_min,pcov_max,parameter,fname,i)
            
        if i == "Third" : 
            popt_min,pcov_min = curve_fit(ThirdDegree,x_min,y_min,maxfev=10000)
            popt_max,pcov_max = curve_fit(ThirdDegree,x_max,y_max,maxfev=10000)
            var_min = np.sqrt(np.diag(pcov_min))
            var_max = np.sqrt(np.diag(pcov_max))

            print("3rd degree max",var_max)
            print("3rd drgree mim",var_min)
            
            Plots(x_min,x_max,y_min,y_max,x_data,y_data,popt_min,popt_max,pcov_min,pcov_max,parameter,fname,i)
            
            
main()
