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
    
    fname = folder_name.split('/')[-1].split('.')[0]
    return fname

def Linear (x,a,b):
    f = (a*x) + b
    
    return f

def main():   
    #Parser to run code in server
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1", dest = "INFILE1", help = "data file corresponding to limits")
    parser.add_argument("-f2", dest = "INFILE2", help = "distribution to fit")
    
    args = parser.parse_args() 
    
    #Importing data file as a matrix
    
    Delay = pd.read_csv(args.INFILE1)
    Inj = pd.read_csv(args.INFILE2)
    y_data = Delay['Plateau'].values
    x_data = np.arange(0,len(y_data),1)
    
    y_data_d = Inj.iloc[:,2].values
    x_data_d = np.arange(0,len(y_data_d),1)
    
    #pdb.set_trace()
 
    fname = get_information(args.INFILE1)
    
    data_noNan,x_noNan = [],[]    
        
    for i in range(len(y_data_d)):
        if y_data[i]/y_data[i] == 1:
            data_noNan.append(y_data[i])
            x_noNan.append(x_data[i])

    data_noNan = np.asarray(data_noNan)
    x_noNan = np.asarray(x_noNan)    

    popt,pcov = curve_fit(Linear,x_noNan,data_noNan,maxfev=10000)
    lab = r'$%fx + %f$' % (popt[0],popt[1])
    pdb.set_trace()
    
    plt.figure(1)
    plt.plot(x_data_d,y_data_d,label='injected',marker = '.',markersize = 1,color = 'crimson')
    plt.plot(x_noNan,Linear(x_noNan,int(popt[0]),int(popt[1])),linewidth=0,marker = '.',markersize = 1,color = "salmon",label=lab)
    plt.legend()
    
    plt.savefig(os.path.join("PLOTSPRED/{}.pdf".format(fname)))

main()
