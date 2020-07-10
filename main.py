import torch 
import pdb
import os
import numpy as np
#import matplotlib.pyplot as plt


## New functions
def load_data():
    path = 'C:/Users/Naomi/Documents/GitHub/Analyse_Stage2020/5kv_100nspicpic'
    time,voltage,current = [],[],[]
    
    for filename in os.listdir(path)[:10]:
        
        v1,v2,v3 = np.loadtxt(os.path.join(path, filename),skiprows=12,delimiter = ',', unpack = True)
        time.append(v1)
        voltage.append(v2)
        current.append(v3)
        a=1
        
    return np.array(time), np.array(voltage), np.array(current)

##

########This is a debugger
def main():
        data = load_data()
        pdb.set_trace()
        
main()
