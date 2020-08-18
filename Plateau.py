import pdb
import numpy as np
import os
import argparse
import pandas as pd

def find_plateau(voltage,time,voltage_threshold,time_threshold):
        ## Beginning of plateau phase ##
        
        dv = np.float(voltage_threshold)
        dt = np.float(time_threshold)
        
        ## End of plateau phase ##
        for k in range(len(voltage)):
            if np.abs(voltage[k] - voltage[k-np.int(dt)]) > dv:
                if k  < len(voltage):
                    
                    real_t = k - int(dt)
                    t = time[real_t]
                    
                    return t

        return float("nan"), float("nan") 
    
def load_data(filename):    
    
    time, voltage, current = np.array(np.loadtxt(filename, dtype = float, delimiter = ',', skiprows = 12, unpack = True))
    return time, voltage, current 

def compute_plateaus_on_data(path,dv,dt):
    
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    progress = 0
    
    # RESULTS
    RESULTS_TABLE = []
    # cycle through all files 
    for i,f in enumerate(files) :
        
        time, voltage, current = load_data(os.path.join(path,f))
        
        end = find_plateau(voltage,time,dv,dt)       
    	   
        if end != 'nan':
            plateau = end
        
        else :
            plateau = 'nan'
                     
        RESULTS_TABLE.append([f,plateau])
        
        progress +=1
        
        if progress%50 == 0:
            print(progress)
        
    return np.asarray(RESULTS_TABLE)

def main():
    
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-dv', dest = 'VOLTAGE_THRESHOLD', help = 'pick a value for voltage threshold')
    parser.add_argument('-dt', dest = 'TIME_THRESHOLD', help = 'pick a value for time threshold')
    args = parser.parse_args()
    outfile = args.INFOLDER.split('/')[-1] 
    
    RESULTS_TABLE = compute_plateaus_on_data(args.INFOLDER,args.VOLTAGE_THRESHOLD, args.TIME_THRESHOLD)
    
    print("Finished appending RESULTS_TABLE, saving ...")
    
    pd.DataFrame(RESULTS_TABLE, columns = ['Filename', 'Plateau']).to_csv(os.path.join('OUT_TAB_FIXED_THRESH',
    "OUT_PLATEAUS_{}_{}dv_{}dt.csv".format(outfile,args.VOLTAGE_THRESHOLD,args.TIME_THRESHOLD))) 

#update
main()
