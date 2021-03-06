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

def Integration(path, dv, dk):
    
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    INT_TAB = []
    
    progress = 0
    
    for i,f in enumerate(files) :
        
        TIME_TO_INT, Y_DATA = [], []

        time, voltage, current = load_data(os.path.join(path,f))
        
        for k in range(dk, len(time)) :
            if (voltage[k-dk] - voltage[k]) > dv:
                index = k
                break
        
        for j in range(index, len(time)) :
            #pdb.set_trace()
            TIME_TO_INT.append(time[j])
            Y_DATA.append(np.abs(current[j]*voltage[j]))
            
        INT_TAB.append([f,np.trapz(Y_DATA,TIME_TO_INT)])

        if progress%50==0:
            print(progress)

        progress += 1
     
    return np.asarray(INT_TAB)

def main():
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    #parser.add_argument('-m', dest = 'METHOD', default = 'all', help = 'Chose integration method, default is Trapeze and Simpson')
    parser.add_argument('-dv',type = int,  dest = 'VOLTAGE_THRESHOLD', help = 'pick a value for voltage threshold')
    parser.add_argument('-dk',type = int,  dest = 'INDEX_THRESHOLD', help = 'pick a value for time threshold')
    args = parser.parse_args()
    outfile = args.INFOLDER.split('/')[-1] 
    
    path = args.INFOLDER
    dk = args.INDEX_THRESHOLD
    dv = args.VOLTAGE_THRESHOLD  
    
    DATA = Integration(path, dv, dk)
    
    print("finished calculating now saving ... ")
    pd.DataFrame(DATA, columns = ['Filename', 'Integration']).to_csv(os.path.join('Energy',"{}.csv".format(outfile)))

main()
