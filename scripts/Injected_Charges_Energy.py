import pdb
import numpy as np
import scipy.integrate as sc
import os
import argparse
import pandas as pd
from scipy import integrate

def load_data(filename):

    #loading data    
    Results = pd.read_csv(filename, skiprows = 10)
    
    #creating arrays for time, voltage and current
    time = Results["TIME"]
    voltage = Results["CH1"]
    current = Results["CH2"]
    
    return time, voltage, current 

def Integration(path,dk,dv):
    
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    INJ, ENER = [], []

    progress = 0
     
    for i,f in enumerate(files) :
        
        CURR_TO_INT,TIME_TO_INT,VOLT_TO_INT = [],[],[]
        #print(f)
        time_inf, voltage_inf, current_inf = load_data(os.path.join(path,f))
        #pdb.set_trace()
        time_inf=np.asarray(time_inf)
        current_inf=np.asarray(current_inf)
        voltage_inf=np.asarray(voltage_inf)
        time = time_inf[(current_inf<1e208)&(voltage_inf<1e208)]
        voltage = voltage_inf[(current_inf<1e208)&(voltage_inf<1e208)]
        current = current_inf[(current_inf<1e208)&(voltage_inf<1e208)]        
        
        if len(time_inf)-len(time)<20:
            

            for k in range(dk, len(time)) :
                if ((voltage[k-dk] - voltage[k]) > dv) :
                    #pdb.set_trace()
                    index = k-dk
                    break
                else:
                    index = -200

            if index != -200:

                #pdb.set_trace()
        
                for j in range(index, len(time)) :
                    TIME_TO_INT.append(time[j])
                    CURR_TO_INT.append(np.abs(current[j]))
                    VOLT_TO_INT.append(np.abs(voltage[j]))           
        
                TIME_TO_INT = np.asarray(TIME_TO_INT)
                CURR_TO_INT = np.asarray(CURR_TO_INT)        
                VOLT_TO_INT = np.asarray(VOLT_TO_INT)

                POWER = CURR_TO_INT*VOLT_TO_INT

                INJ.append([f,integrate.simps(CURR_TO_INT,TIME_TO_INT)])
                ENER.append([f,integrate.simps(POWER,TIME_TO_INT)])
                #print(progress)
                if progress%100 == 0:
                    print(progress)
                progress += 1
        
    return np.asarray(INJ),np.asarray(ENER)

def main():
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-dv',type = int,  dest = 'VOLTAGE_THRESHOLD', help = 'pick a value for voltage threshold')
    parser.add_argument('-dk',type = int,  dest = 'INDEX_THRESHOLD', help = 'pick a value for time threshold')
    args =   parser.parse_args()
    outfile = args.INFOLDER.split('/')[-1] 
    
    dk = args.INDEX_THRESHOLD
    dv = args.VOLTAGE_THRESHOLD   
    
    #if args.METHOD == 'all':
    INJECTED_CHARGES,INJECTED_ENERGY = Integration(args.INFOLDER,dk,dv)
    print("finished calculating now saving ... ")
    pd.DataFrame(INJECTED_CHARGES, columns = ['Filename','Injected_Charges']).to_csv(os.path.join('AudrenAnalysis/Injected_Charges',"{}.csv".format(outfile)))
    pd.DataFrame(INJECTED_ENERGY, columns = ['Filename','Energy']).to_csv(os.path.join('AudrenAnalysis/Energy',"{}.csv".format(outfile)))

main()
