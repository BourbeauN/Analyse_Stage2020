import pdb
import numpy as np
import matplotlib.pyplot as plt
import os
import panda as pd

##Function finds plateau by varying 2 parameters thresholds of voltage and time 
##If the value of these parameters is to extreme to code will print 'nan' and move on and keep tab of the 'nan' value
def find_plateau(voltage, time , volt_threshold, time_threshold):
        ## Beginning of plateau phase ##
        
        begin = np.where(voltage == np.ndarray.max(voltage))[0][0] ### to be validated ( tested on 10 )
        ## End of plateau phase ##
        for i in range(begin, len(voltage)):
            if np.abs(voltage[i] - voltage[i-time_threshold]) > volt_threshold:
                if (i + begin )  < len(voltage):
                    return time[begin], time[i + begin]
        return float("nan"), float("nan") 


##Function to automatically load file from directory
def load_data(filename):    
    
    time, voltage, current = np.array(np.loadtxt(filename, dtype = float, delimiter = ',', skiprows = 12, unpack = True))

    return time, voltage, current 

##Compute the find_plateau function on the file loaded with the load_data function
def compute_plateaus_on_data(path):
    
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    # list of voltage deltas  
    dv = np.arange(5, 150, 5)
    
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

## Main function that computes the previous concatenated functions and stores the results of the different iterations in
## a matrix that is saved for future analysis (i.e heat map)
def main():
    
    #nao_path = "/Users/Naomi/Documents/GitHub/Analyse_Stage2020/Git_5kv_100nspicpic"
    leo_path = "5kv_100nspicpic" 
    RESULTS_TABLE = compute_plateaus_on_data(leo_path)
    pd.DataFrame(RESULTS_TABLE, columns = ["fname", "time_delta", "voltage_delta", "plateau_length", "success"]).to_csv("out_test_1.csv") 

main()