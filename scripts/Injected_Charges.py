import pdb
import numpy as np
import scipy.integrate as sc
import os
import argparse
import pandas as pd

def load_data(filename):

    #loading data    
    Results = pd.read_csv(filename, skiprows = 10)
    
    #creating arrays for time, voltage and current
    time = Results["TIME"]
    voltage = Results["CH1"]
    current = Results["CH2"]
    
    return time, voltage, current 

def Integration(path,dk,dv):
    
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    CURR_TO_INT, TIME_TO_INT, INT = [],[],[]

    progress = 0
    
    for i,f in enumerate(files) :
        
        time, voltage, current = load_data(os.path.join(path,f))
        
        for k in range(dk, len(time)) :
            if (voltage[k-dk] - voltage[k]) > dv:
                index = k
        
        for j in range(index, len(time)) :
            TIME_TO_INT.append(time[j])
            CURR_TO_INT.append(np.abs(current[j]))
            
        INT.append([f,np.trapz(CURR_TO_INT,TIME_TO_INT)])
        
        if progress%200 == 0:
            print(progress)
        progress += 1
        
    return np.asarray(INT)

def main():
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-dv',type = int,  dest = 'VOLTAGE_THRESHOLD', help = 'pick a value for voltage threshold')
    parser.add_argument('-dk',type = int,  dest = 'INDEX_THRESHOLD', help = 'pick a value for time threshold')
    args = parser.parse_args()
    outfile = args.INFOLDER.split('/')[-1] 
    
    dk = args.INDEX_THRESHOLD
    dv = args.VOLTAGE_THRESHOLD   
    
    #if args.METHOD == 'all':
    INJECTED_CHARGES = Integration(args.INFOLDER,dv,dk)
    print("finished calculating now saving ... ")
    pd.DataFrame(INJECTED_CHARGES, columns = ['Filename', 'Injected_Charges']).to_csv(os.path.join('Injected_Charges',"{}.csv".format(outfile)))
    