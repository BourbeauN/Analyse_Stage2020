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

def Injected(time,current):
    
    INJ = integrate.simps(current,time)
    return INJ    

def Energy(time,current,voltage):
    
    current = np.asarray(current)
    voltage = np.asarray(voltage)
    power = current*voltage
    ENERGY = integrate(power,time)
    return ENERGY

def Integration(path,dk,dv):
    
    # list of discharge files  
    files = sorted(os.listdir(path))
    
    INJ, ENER = [], []

    progress = 0
     
    for i,f in enumerate(files) :
        
        PRE_TIME, PRE_CURR, PRE_VOLT = [],[],[]
        POST_TIME, POST_CURR, POST_VOLT = [],[],[]
        ABS_INJ,REG_INJ,NEG_INJ,DIS_CURR = [],[],[],[]        

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
        
                POST_TIME = np.asarray(time[index:])
                POST_CURR = np.asarray(current[index:])
                POST_VOLT = np.asarray(voltage[index:])
                PRE_TIME = np.asarray(time[:index])
                PRE_CURR = np.asarray(current[:index])
                PRE_VOLT = np.asarray(voltage[:index])

                abs_inj = Injected(POST_TIME,abs(POST_CURR))
                inj = Injected(POST_TIME,POST_CURR)
                dis_curr = Injected(PRE_TIME,abs(PRE_CURR))

                ABS_INJ.append([f,abs_inj])
                
                NEG_INJ = -0.5*(ABS_INJ-REG_INJ)

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
    pd.DataFrame(INJECTED_CHARGES, columns = ['Filename','Injected_Charges']).to_csv(os.path.join('Injected_Charges',"{}.csv".format(outfile)))
    pd.DataFrame(INJECTED_ENERGY, columns = ['Filename','Energy']).to_csv(os.path.join('Injected_Energy',"{}.csv".format(outfile)))

main()
