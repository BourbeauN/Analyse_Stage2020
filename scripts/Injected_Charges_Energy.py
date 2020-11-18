import pdb
import numpy as np
import scipy.integrate as sc
import os
import argparse
import pandas as pd
from scipy import integrate

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
    
    INJ, ENER = [], []

    progress = 0
     
    for i,f in enumerate(files) :
        
        #print(f)
        #pdb.set_trace()

        CURR_TO_INT,TIME_TO_INT,VOLT_TO_INT = [],[],[]

        time, voltage, current = load_data(os.path.join(path,f))
        
        for k in range(dk, len(time)) :
            if (voltage[k-dk] - voltage[k]) > dv:
                #pdb.set_trace()
                index = k-dk
                break
        #pdb.set_trace()

        for j in range(index, len(time)) :
            TIME_TO_INT.append(time[j])
            CURR_TO_INT.append(np.abs(current[j]))
            VOLT_TO_INT.append(np.abs(voltage[j]))           
        
        TIME_TO_INT = np.asarray(TIME_TO_INT)
        CURR_TO_INT = np.asarray(CURR_TO_INT)
        VOLT_TO_INT = np.asarray(VOLT_TO_INT)
        POWER = CURR_TO_INT*VOLT_TO_INT

        INJ.append([f,integrate.simps(CURR_TO_INT[CURR_TO_INT<1e208],TIME_TO_INT[CURR_TO_INT<1e208])])
        ENER.append([f,integrate.simps(POWER[POWER<1e208],TIME_TO_INT[POWER<1e208])])
        #print(progress)
        if progress%100 == 0:
            print(progress)
        progress += 1
        
    return np.asarray(INJ),np.asarray(ENER)

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
    INJECTED_CHARGES,INJECTED_ENERGY = Integration(args.INFOLDER,dk,dv)
    print("finished calculating now saving ... ")
    pd.DataFrame(INJECTED_CHARGES, columns = ['Filename','Injected_Charges']).to_csv(os.path.join('Injected_Charges',"{}.csv".format(outfile)))
    pd.DataFrame(INJECTED_ENERGY, columns = ['Filename','Energy']).to_csv(os.path.join('Energy',"{}.csv".format(outfile)))

main()
