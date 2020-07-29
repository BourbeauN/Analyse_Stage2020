import pdb
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
import pandas as pd

def find_plateau(voltage, time , volt_threshold, time_threshold):
        ## Beginning of plateau phase ##
        
        begin = np.where(voltage == np.ndarray.max(voltage))[0][0] ### to be validated ( tested on 10 )
        ## End of plateau phase ##
        for i in range(begin, len(voltage)):
            if np.abs(voltage[i] - voltage[i-time_threshold]) > volt_threshold:
                if (i + begin )  < len(voltage):
                    return time[begin], time[i + begin]
        return float("nan"), float("nan") 

def load_data(filename):    
    
    time, voltage, current = np.array(np.loadtxt(filename, dtype = float, delimiter = ',', skiprows = 12, unpack = True))

    return time, voltage, current 

def compute_plateaus_on_data(path):
    
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    # list of voltage deltas  
    dv = np.arange(200, 6000, 200)
    
    # time deltas  
    dt = np.arange(30) + 1 

    # RESULTS
    RESULTS_TABLE = []
    # cycle through all files 
    for i, f in enumerate(files) :
        time, voltage, current = load_data(os.path.join(path,f))
        # compute all results from all parameters
        for v_thresh in dv :
            for t_thresh in dt :
                start , end = find_plateau (voltage, time , v_thresh, t_thresh)
                if start==start and end==end : 
                    plateau = end - start
                    success = 1
                    # do smthing
                else : 
                    plateau = float("nan")
                    success = 0
                    #do nothing
                
                # store results
                print([i, f, t_thresh, v_thresh, plateau, success])
                RESULTS_TABLE.append([f, t_thresh, v_thresh, plateau, success])
    # return results
    return np.asarray(RESULTS_TABLE)

def main():

    parser = argparse.ArgumentParser()
    
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    
    args = parser.parse_args()
    
    outfile = args.INFOLDER.split('/')[-1] 
    
    # OUTDATED nao_path = "/Users/Naomi/Documents/GitHub/Analyse_Stage2020/Git_5kv_100nspicpic"
    # OUTDATED leo_path = "5kv_100nspicpic" 
    
    RESULTS_TABLE = compute_plateaus_on_data(args.INFOLDER)
    
    pd.DataFrame(RESULTS_TABLE, columns = ["fname", "time_delta", "voltage_delta", "plateau_length", "success"]).to_csv(os.path.join('OUT', "OUT_PLATEAUS_{}.csv".format(outfile))) 

main()
