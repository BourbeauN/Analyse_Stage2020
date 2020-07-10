import torch 
import pdb
import os
import numpy as np
import matplotlib.pyplot as plt


## New functions
def load_data():
    path = 'C:/Users/Naomi/Documents/Université/Stage 2020 - Ahmad Hamdan/Analyse/5kv_500ns-picpic'
    f = []
    
    for filename in os.listdir(path)[:10]:
        
        f.append(np.loadtxt(filename,skiprows=12))

    return f

##

########This is a debugger
def main():
        data = load_data()
        pdb.set_trace()
        
main()
