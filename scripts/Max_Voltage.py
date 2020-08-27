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

def max_voltage(path):
    
    Voltage_Tab = []    
    
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    for i, f in enumerate(files) :
        time, voltage, current = load_data(os.path.join(path,f))
        max_value = np.amax(voltage)
        
        Voltage_Tab.append([f,max_value])
        if f%50==0:
            print(f)
        
    return np.asarray(Voltage_Tab)


def main ():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFILE', help = 'discharge file')
    args = parser.parse_args()
    outfile = args.INFILE.split('/')[-1] 
    
    pdb.set_trace()

    MAX_TENSION_TAB = max_voltage(args.INFILE)

    pd.DataFrame(MAX_TENSION_TAB, columns = ['Filename', 'Max Voltage']).to_csv(os.path.join('Voltage_Discharge','{}'.format(outfile))) 

main()
