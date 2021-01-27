import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import pdb
import argparse
import os
from scipy.optimize import curve_fit


def get_information(folder_name):
    param = folder_name.split("/")[1].split(".")[0].split("_")[0:2]
    filen = folder_name.split("/")[1].split(".")[0].split("_")[2:]
    d = "_"
    parameter = d.join(param)
    fname = d.join(filen)

    return parameter,fname

def Linear (x,a,b):
    f = a*x + b
    
    return f

def main():   
    #Parser to run code in server
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1", dest = "INFILE1", help = "data file corresponding to limits")
    parser.add_argument("-f2", dest = "INFILE2", help = "distribution to fit")
    
    args = parser.parse_args() 
    
    #Importing data file as a matrix
    
    Delay = pd.read_csv(args.f1)
    Inj = pd.read_csv(args.f2)
    y_data = Delay.iloc[:,2]
    x_data = np.arange(0,len(y_data),1)
    
    y_data_d = Inj.iloc[:,2]
    x_data_d = np.arange(0,len(y_data_d),1)
    
    parameter,fname = get_information(args.f1)
    
    popt_min,pcov_min = curve_fit(Linear,x_data,y_data,maxfev=10000)
    
    plt.figure(1)
    plt.plot(x_data_d,y_data_d,label='injected')
    plt.plot(x_data,Linear(x_data,popt_min[1],popt_min[2]),linewidth=1,color = "salmon",label="curve fit")
    plt.legend()
    
    plt.savefig(os.path.join("PLOTSPRED/{}/{}.pdf".format(parameter,fname)))
