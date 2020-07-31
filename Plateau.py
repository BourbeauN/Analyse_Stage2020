import pdb
import numpy as np
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

def compute_plateaus_on_data(path,dv,dt):
    
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    # RESULTS
    RESULTS_TABLE = []
    # cycle through all files 
    for f in enumerate(files) :
        
        time, voltage, current = load_data(os.path.join(path,f))
        pdb.set_trace()
        start, end = find_plateau (voltage, time , dv, dt)       
    	      
        if start != 'nan' and end != 'nan':
            plateau = end - start
        
        else :
            plateau = 'nan'
                      
        RESULTS_TABLE.append([plateau])

    return np.asarray(RESULTS_TABLE)

def main():
    
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-dv', dest = 'VOLTAGE_THRESHOLD', help = 'pick a value for voltage threshold')
    parser.add_argument('-dt', dest = 'TIME_THRESHOLD', help = 'pick a value for time threshold')
    args = parser.parse_args()
    outfile = args.INFOLDER.split('/')[-1] 
    
    # OUTDATED nao_path = "/Users/Naomi/Documents/GitHub/Analyse_Stage2020/Git_5kv_100nspicpic"
    # OUTDATED leo_path = "5kv_100nspicpic" 
    
    RESULTS_TABLE = compute_plateaus_on_data(args.INFOLDER,args.VOLTAGE_THRESHOLD, args.TIME_THRESHOLD)
    
    pd.DataFrame(RESULTS_TABLE).to_csv(os.path.join('OUT_TAB_FIXED_THRESH', "OUT_PLATEAUS_{}.csv".format(outfile))) 
