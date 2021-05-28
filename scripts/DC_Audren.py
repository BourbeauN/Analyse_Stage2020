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

def load_BV(filename):
    
    Results = pd.read_csv(filename,skiprows=1)
    BV = Results.iloc['Voltage']
    
    return BV   

def max_current(path1,path2):
    
    Current_Tab = []    
    count = 0
    # list of discharge files  
    files1 = sorted(os.listdir(path1))
    
    for i, f in enumerate(files1) :
        time, voltage, current = load_data(os.path.join(path1,f))
        pdb.set_trace() 
        BV = load_BV(path2)
        
        if BV[i] > 0 :
            max_value = np.amax(current)
        
        elif BV[i] < 0:
            max_value = np.amin(current)
    
        if count%100 == 0:
            print(count)
       
        pdb.set_trace()
 
        count += 1

        Current_Tab.append([f,max_value])
        
    return np.asarray(Current_Tab)

def main ():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFILE', help = 'discharge file')
    parser.add_argument('-b', dest = 'BREAKDOWN', help = 'breakdown voltage file')
    args = parser.parse_args()
    outfile = args.INFILE.split('/')[-1] 

    MAX_CURRENT_TAB = max_current(args.INFILE,args.BREAKDOWN)

    pd.DataFrame(MAX_CURRENT_TAB, columns = ['Filename', 'Max Current']).to_csv(os.path.join('Max_Current','{}.csv'.format(outfile))) 

main()
