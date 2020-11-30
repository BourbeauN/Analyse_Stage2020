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

def Sqrt(x,a,b,c):
    f = a * np.sqrt((b*x)+c)
    return f

def Ln(x,a,b,c):
    f = a*np.log((b*x))+c
    return f

def Exponential(x,a,b,c):
    f = a*np.exp(b*x)+c 
    return f

def Quadratic(x,a,b,c):
    f = a*(x**2)+b*x+c
    return f

def Weibull(x,a,b,c,d):
    f = (a-np.exp(-((x/b)**c)))**d
    return f

def Linear(x,a,b):
    f = (a*x)+b
    return f

def ThirdDegree(x,a,b,c,d):
    f = (a*(x**3))+(b*(x**2))+(c*x)+d
    return f

def Sigmoid(x,a,b,c):
    f = a/(1+np.exp(b*x))+c
    
    return f
def radical(x,a,b,c,d):
    f = a*((x+b)**c)+d
    
    return f

def get_information(folder_name):
    param = folder_name.split("/")[1].split(".")[0].split("_")[0:2]
    filen = folder_name.split("/")[1].split(".")[0].split("_")[2:]
    d = "_"
    parameter = d.join(param)
    fname = d.join(filen)

    return parameter,fname

def Plots(x_min,x_max,y_min,y_max,x_data,y_data,popt_min,popt_max,pcov_min,pcov_max,parameter,fname,i):
    pdb.set_trace()
    plt.figure(1)
    if i == 'exp':
        label_min = r'$%fe^{%fx}+%f$' % (popt_min[0],popt_min[1],popt_min[2])
        label_max = r'$%fe^{%fx}+%f$' % (popt_max[0],popt_max[1],popt_max[2])
        plt.plot(x_min,Exponential(x_min,popt_min[0],popt_min[1],popt_min[2]),linewidth=1,color = "salmon",label=label_min)
        plt.plot(x_max,Exponential(x_max,popt_max[0],popt_max[1],popt_min[2]),linewidth=1,color = "crimson",label=label_max)
    
    if i == 'sqrt':
        label_min = r'$%f\sqrt{%bx}+%f' % (popt_min[0],popt_min[1],popt_min[2])
        label_max = r'$%f\sqrt{%bx}+%f' % (popt_max[0],popt_max[1],popt_min[2])
        plt.plot(x_min,Sqrt(x_min,popt_min[0],popt_min[1],popt_min[2]),linewidth=1,color = "salmon",label=label_min)
        plt.plot(x_max,Sqrt(x_max,popt_max[0],popt_max[1],popt_min[2]),linewidth=1,color = "crimson",label=label_max)
        
    if i == 'log':
        label_min = r'$%f\text{ln}(%fx)+%$' % (popt_min[0],popt_min[1],popt_min[2])
        label_max = r'$%f\text{ln}(%fx)+%$' % (popt_max[0],popt_max[1],popt_max[2])
        plt.plot(x_min,Ln(x_min,popt_min[0],popt_min[1],popt_min[2]),linewidth=1,color = "salmon",label=label_min)
        plt.plot(x_max,Ln(x_max,popt_max[0],popt_max[1],popt_min[2]),linewidth=1,color = "crimson",label=label_max)
    
    if i == 'quad':
        label_min = r'$%fx^{2}+%fx+%$' % (popt_min[0],popt_min[1],popt_min[2])
        label_max = r'$%fx^{2}+%fx+%$' % (popt_max[0],popt_max[1],popt_max[2])
        plt.plot(x_min,Quadratic(x_min,popt_min[0],popt_min[1],popt_min[2]),linewidth=1,color = "salmon",label=label_min)
        plt.plot(x_max,Quadratic(x_max,popt_max[0],popt_max[1],popt_min[2]),linewidth=1,color = "crimson",label=label_max)
    
    if i == 'weibull':
        label_min = r'$\Big[%f - e^{-\big(\frac{x}{%f}\big)^{%f}}\Big]^{%f}$' % (popt_min[0],popt_min[1],popt_min[2],popt_min[3])
        label_max = r'$\Big[%f - e^{-\big(\frac{x}{%f}\big)^{%f}}\Big]^{%f}$' % (popt_max[0],popt_max[1],popt_max[2],popt_max[3])
        plt.plot(x_min,Weibull(x_min,popt_min[0],popt_min[1],popt_min[2],popt_min[3]),linewidth=1,color = "salmon",label=label_min)
        plt.plot(x_max,Weibull(x_max,popt_max[0],popt_max[1],popt_min[2],popt_min[3]),linewidth=1,color = "crimson",label=label_max)
        
    if i == 'lin':
        label_min = r'$%fx+%f$' % (popt_min[0],popt_min[1])
        label_max = r'$%fx+%f$' % (popt_max[0],popt_max[1])
        plt.plot(x_min,Linear(x_min,popt_min[0],popt_min[1]),linewidth=1,color = "salmon",label=label_min)
        plt.plot(x_max,Linear(x_max,popt_max[0],popt_max[1]),linewidth=1,color = "crimson",label=label_max)
    
    if i == 'Third':
        label_min = r'$%fx^{3}+%fx^{2}+%fx+%f$' % (popt_min[0],popt_min[1],popt_min[2],popt_min[3])
        label_max = r'$%fx^{3}+%fx^{2}+%fx+%f$' % (popt_min[0],popt_min[1],popt_min[2],popt_min[3])
        plt.plot(x_min,ThirdDegree(x_min,popt_min[0],popt_min[1],popt_min[2],popt_min[3]),linewidth=1,color = "salmon",label=label_min)
        plt.plot(x_max,ThirdDegree(x_max,popt_max[0],popt_max[1],popt_min[2],popt_min[3]),linewidth=1,color = "crimson",label=label_max)
    
    if i == 'Sigmoid':
        label_min = r'$\frac{%f}{%f+e^{%fx}}+%f$' % (popt_min[0],popt_min[1],popt_min[2],popt_min[3])
        label_max = r'$\frac{%f}{%f+e^{%fx}}+%f$' % (popt_max[0],popt_max[1],popt_max[2],popt_max[3])
        plt.plot(x_min,Sigmoid(x_min,popt_min[0],popt_min[1],popt_min[2]),linewidth=1,color = "salmon",label=label_min)
        plt.plot(x_max,Sigmoid(x_max,popt_max[0],popt_max[1],popt_min[2]),linewidth=1,color = "crimson",label=label_max)
    
    if i == 'radical':
        label_min = r'$%f(x-%f)^{%f}+%f$' % (popt_min[0],popt_min[1],popt_min[2],popt_min[3])
        label_max = r'$%f(x-%f)^{%f}+%f$' % (popt_max[0],popt_max[1],popt_max[2],popt_max[3])
        plt.plot(x_min,radical(x_min,popt_min[0],popt_min[1],popt_min[2],popt_min[3]),linewidth=1,color = "salmon",label=label_min)
        #plt.plot(x_max,radical(x_max,popt_max[0],popt_max[1],popt_max[2],popt_max[3]),linewidth=1,color = "crimson",label=label_max)    

    plt.plot(x_data,y_data,marker='.',markersize=1,color = 'black', linewidth=0)
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
    #pdb.set_trace() 
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
            
            Plots(x_min,x_max,y_min,y_max,x_data,y_data,popt_min,popt_max,pcov_min,pcov_max,parameter,fname,i)            

            print("3rd degree max",var_max)
            print("3rd drgree mim",var_min)
        
        if i == 'Sigmoid':
            popt_min,pcov_min = curve_fit(Sigmoid,x_min,y_min,maxfev=10000)
            popt_max,pcov_max = curve_fit(Sigmoid,x_max,y_max,maxfev=10000)
            var_min = np.sqrt(np.diag(pcov_min))
            var_max = np.sqrt(np.diag(pcov_max))

            Plots(x_min,x_max,y_min,y_max,x_data,y_data,popt_min,popt_max,pcov_min,pcov_max,parameter,fname,i) 

            print("Sigmoid min variance",pcov_min)
            print("Sigmoid max variance",pcov_max)
            print("Sigmoid min parameters",popt_min)
            print("Sigmoid max parameters",popt_max)
        
        if i == 'none':
            plt.figure(1)
            plt.plot(x_data,y_data,color='black',marker='.',markersize=3,linewidth=0,label='data')
            plt.plot(x_min,y_min,color='yellowgreen',marker='.',markersize=3,linewidth=0)
            plt.plot(x_max,y_max,color='yellowgreen',marker='.',markersize=3,linewidth=0)
            plt.savefig(os.path.join('PLOTS/{}/{}_{}.pdf'.format(parameter,fname,i)))

        if i == 'radical':
            popt_min,pcov_min=curve_fit(radical,x_min,y_min,maxfev=10000)
            popt_max,pcov_max=curve_fit(radical,x_max,y_max,maxfev=10000)
            var_min = np.sqrt(np.diag(pcov_min))
            var_max = np.sqrt(np.diag(pcov_max))

            Plots(x_min,x_max,y_min,y_min,x_data,y_data,popt_min,popt_max,pcov_min,pcov_max,parameter,fname,i)

            print("Radical min variance",pcov_min)
            print("Radical max variance",pcov_max)
            print("Radical min parameter",popt_min)
            print("Radical max paramter",popt_min)    
            
main()
