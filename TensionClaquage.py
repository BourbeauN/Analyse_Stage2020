import matplotlib.pyplot as plt
import numpy as np
import os
import pdb

##Data loading function
def load_data(filename):    
    
    time, voltage, current = np.array(np.loadtxt(filename, dtype = float, delimiter = ',', skiprows = 12, unpack = True))

    return time, voltage, current 

def max_voltage(path):
    
    Voltage_Tab = []    
    
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    for i, f in enumerate(files) :
        time, voltage, current = load_data(os.path.join(path,f))

    return (Voltage_Tab)


def main ():
    
    

