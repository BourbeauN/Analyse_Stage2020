import pdb
import numpy as np
import argparse
import pandas as pd
import os

def DV_Count(dv) :
    count = 0
    dv_nan=[]
    for i in range(len(dv)):
        if dv[i]==1:
            count += 1
            #print(dv[i],count)
            if ((dv[i+1])*1) != 1:                   
                dv_postnan = dv[i+1]        
                dv_nan.append([count,dv_postnan])
        else:
            count = 0    
        
    dv_nan = np.asarray(dv_nan)
    
    return dv_nan

def get_discharge_information(folder_name):
    
    information = folder_name.split("/")[1].split(".")[0].split("_")[2:]
    d = '_'
    info = d.join(information)
    return info 

def main():
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFILE', help = 'file folder corresponding to experimental set with discharge infos')
    args = parser.parse_args()
    
    DV_nan = DV_Count(args.INFILE)
    
    info = get_discharge_information(args.INFILE)
    
    pd.DataFrame(DV_nan, columns = ['Count','Discharge_Voltage']).to_csv(os.path.join('Analysis/DV_nan/{}'.format(info)))
    