import pandas as pd
import argparse
import numpy as np
import os
import pdb

##Data loading function

def load_data(filename):    
    
    time, voltage, current = np.loadtxt(filename, delimiter = ',', skiprows = 12, unpack = True)

    return np.array(time), np.array(voltage), np.array(current) 

def max_voltage(path):
    
    Voltage_Tab = []    
    
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    for i, f in enumerate(files) :
        time, voltage, current = load_data(os.path.join(path,f))
        max_value = np.amax(voltage)
        
        Voltage_Tab.append([f,max_value])
       
        
    return np.asarray(Voltage_Tab)


def main ():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFILE', help = 'discharge file')
    args = parser.parse_args()
    outfile = args.INFOLDER.split('/')[-1] 

    MAX_TENSION_TAB = max_voltage(args.INFILE)

    pd.DataFrame(MAX_TENSION_TAB, columns = ['Filename', 'Max Voltage']).to_csv(os.path.join('Voltage_Discharge_{}'.format(outfile))) 

main()