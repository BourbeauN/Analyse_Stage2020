import pdb
import numpy as np
import os
import argparse
import pandas as pd
from scipy.signal import savgol_filter

#def Savitsky_Golay(y):
    #return savgol_filter(y,9,2)

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
                
                return float(t)

    return float("nan") 
    
def load_data(filename):
    
    print('I try 1')
    
    Results = pd.read_csv(filename, skiprows = 11)
    
    time = Results['TIME']
    voltage = Results['CH1']
    current = Results['CH2']
    
    print('so hard and got this far 2')
    
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
        
        #voltage_filtered = Savitsky_Golay(voltage)
        
        end = find_plateau(voltage_filtered,time,dv,dt)       
    	   
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
    
    pd.DataFrame(RESULTS_TABLE, columns = ['Filename', 'Plateau']).to_csv(os.path.join('Temp/Filter_Test',"OUT_PLATEAUS_{}_{}dv_{}dt.csv".format(outfile,args.VOLTAGE_THRESHOLD,args.TIME_THRESHOLD))) 

#update
main()
