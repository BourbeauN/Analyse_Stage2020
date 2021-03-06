import pdb
import numpy as np
import argparse
import pandas as pd
import os

def DV_Count(dv) :
    count = 0
    dv_nan=[]
    
    for i in range(len(dv)-1):
        if dv[i]/dv[i] !=1:
            count += 1
            if ((dv[i+1])/dv[i+1]) == 1:                   
                #pdb.set_trace()
                dv_postnan = dv[i+1]        
                dv_nan.append([count,dv_postnan,i+1])
        else:
            count = 0    
        
    dv_nan = np.asarray(dv_nan)
    
    return dv_nan

def get_discharge_information(folder_name):

    info = folder_name.split("/")[-1].split(".")[0]
    #d = '_'
    #info = d.join(information)
    return info 

def main():
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFILE', help = 'file folder corresponding to experimental set with discharge infos')
    args = parser.parse_args()
   
    Results = pd.read_csv(args.INFILE)
    index=Results.iloc[:,1]
    dv = Results.iloc[:,2]
    
    dv_data = np.asarray(dv.values) 
    
    DV_nan = DV_Count(dv_data)
    
    info = get_discharge_information(args.INFILE)
    
    pd.DataFrame(DV_nan, columns = ['Count','Discharge_Voltage','DischargeID']).to_csv(os.path.join('Analysis/DV_nan/{}.csv'.format(info)))

main()    
