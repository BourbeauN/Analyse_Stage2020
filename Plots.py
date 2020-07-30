import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pdb
# import seaborn as sns
import argparse
from datetime import datetime
from sklearn import linear_model
from scipy.optimize import  curve_fit

def sigmoid(x, a, b):
    return 1.0 / (1.0 + np.exp(-a*(x-b)))


def get_elapsed_time(fnames):
    
    times = [f.split("_")[-1].split(".csv")[0] for f in fnames]
    
    datetimes = [datetime.strptime(time, "%Y%m%d%H%M%S%f") for time in times]
    
    time_deltas = [(t - datetimes[0]).total_seconds() for t in datetimes]

    return time_deltas

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", dest = "INFILE", help = ".csv results file")
    parser.add_argument("-dt", dest = "TTHRESH", default = 10, help = "time threshold")
    parser.add_argument("-dv", dest = "VTHRESH", default = 1000, help = "voltage threshold")
    
    args = parser.parse_args()
    Results = pd.read_csv(args.INFILE)
    Results = Results[Results.time_delta == args.TTHRESH][Results.voltage_delta == args.VTHRESH]
    
    Results["ET"] = get_elapsed_time(Results.fname)
    
    # non lineaer fitting
    X = np.array(Results["ET"])
    y = np.array(Results["plateau_length"]) / max(Results["plateau_length"])
    # remove nans
    X = X[y==y]
    y = y[y==y]
    pdb.set_trace()
    popt, pcov = curve_fit(sigmoid, X, y, method='dogbox', bounds=([0., 600.],[0.01, 1200.]))
    X_test = np.linspace(min(Results["ET"]), max(Results["ET"]), 100)
    Y_pred = sigmoid(X_test, *popt)
    plt.scatter(X, y, label = "data")
    plt.plot(X_test, Y_pred, label = "sigmoid fit")
    plt.xlabel("Elapsed time in seconds")
    plt.ylabel("Plateau length in seconds")
    plt.title("Plateau length in f. of elapsed time for {}".format(args.INFILE))
    plt.show()

main()

def ScatterPlot():
    pass 
