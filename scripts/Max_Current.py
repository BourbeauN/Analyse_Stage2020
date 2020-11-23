import pandas as pd
import argparse
import numpy as np
import os
import pdb

##Data loading function

def load_data(filename):    
    
    Results = pd.read_csv(filename, skiprows = 10)

    time = Results['TIME']
    voltage = Results['CH1']
    current = Results['CH2']
    
    return np.array(time), np.array(voltage), np.array(current) 

def max_current(path):
    
    Current_Tab = []    
    count = 0
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    for i, f in enumerate(files) :
        time, voltage, current = load_data(os.path.join(path,f))
        max_value = np.amax(current)
        
        if count%100 == 0:
            print(count)
        
        count += 1

        Current_Tab.append([f,max_value])
        
    return np.asarray(Current_Tab)

def main ():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFILE', help = 'discharge file')
    args = parser.parse_args()
    outfile = args.INFILE.split('/')[-1] 

    MAX_CURRENT_TAB = max_current(args.INFILE)

    pd.DataFrame(MAX_CURRENT_TAB, columns = ['Filename', 'Max Current']).to_csv(os.path.join('AudrenAnalysis/Max_Current','{}.csv'.format(outfile))) 

main()
