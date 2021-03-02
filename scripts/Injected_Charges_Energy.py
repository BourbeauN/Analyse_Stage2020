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
    
    INJ = integrate.trapz(current,time)
    return INJ    
    
def Integration(path,dv,dk):

    # list of discharge files  
    files = sorted(os.listdir(path))
    
    progress = 0
     
    PRE_TIME, PRE_CURR, PRE_VOLT = [],[],[]
    POST_TIME, POST_CURR, POST_VOLT = [],[],[]
    ABS_INJ,REG_INJ,NEG_INJ,DIS_INJ = [],[],[],[]        
    #pdb.set_trace() 
    ABS_ENE = []

    for i,f in enumerate(files) :

        #print(f)
        time_inf, voltage_inf, current_inf = load_data(os.path.join(path,f))
        
        time_inf=np.asarray(time_inf)
        current_inf=np.asarray(current_inf)
        voltage_inf=np.asarray(voltage_inf)
        time = time_inf[(abs(current_inf)<1e208)&(abs(voltage_inf)<1e208)]
        voltage = voltage_inf[(abs(current_inf)<1e208)&(abs(voltage_inf)<1e208)]
        current = current_inf[(abs(current_inf)<1e208)&(abs(voltage_inf)<1e208)]        
        #pdb.set_trace()
        if len(time_inf)-len(time)<20:
            
            for k in range(dk, len(time)) :
                if ((voltage[k-dk] - voltage[k]) > dv) :
                    #pdb.set_trace()
                    index = k-dk
                    break
                else:
                    index = -200

            if index > 0:

                #pdb.set_trace()
                POST_TIME = np.asarray(time[index:])
                POST_CURR = np.asarray(current[index:])
                POST_VOLT = np.asarray(voltage[index:])
                PRE_TIME = np.asarray(time[:index-500])
                PRE_CURR = np.asarray(current[:index-500])
                PRE_VOLT = np.asarray(voltage[:index-500])
                
                abs_inj = Injected(POST_TIME,abs(POST_CURR))
                reg_inj = Injected(POST_TIME,POST_CURR)
                dis_inj = Injected(PRE_TIME,abs(PRE_CURR))
                abs_ene = Injected(POST_TIME,np.abs(POST_CURR*POST_VOLT))
                neg_inj = 0.5*(abs_inj-reg_inj)
                
                #pdb.set_trace()
                ABS_INJ.append([f,abs_inj])
                REG_INJ.append([f,reg_inj])
                DIS_INJ.append([f,dis_inj]) 
                NEG_INJ.append([f,neg_inj])
                ABS_ENE.append([f,abs_ene])

                #pdb.set_trace() 
  
                #print(progress)
                if progress%100 == 0:
                    print(progress)
                progress += 1
    
    ABS_INJ = np.asarray(ABS_INJ)
    REG_INJ = np.asarray(REG_INJ)
    DIS_INJ = np.asarray(DIS_INJ)
    ABS_ENE = np.asarray(ABS_ENE)
    NEG_INJ = np.asarray(NEG_INJ)
 
    return ABS_INJ,REG_INJ,DIS_INJ,NEG_INJ,ABS_ENE

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
    ABS_INJ,REG_INJ,DIS_INJ,NEG_INJ,ABS_ENE = Integration(args.INFOLDER,dk,dv)
    print("finished calculating now saving ... ")
    pd.DataFrame(ABS_INJ, columns = ['Filename','Absolute_Injected_Charges']).to_csv(os.path.join('Audren/Distance_Analysis/Injected_Charges/Abs/{}.csv'.format(outfile)))
    pd.DataFrame(ABS_ENE, columns = ['Filename','Energy']).to_csv(os.path.join('Audren/Distance_Analysis/Injected_Energy/{}.csv'.format(outfile)))
    pd.DataFrame(REG_INJ, columns = ['Filename','Injected_Charges']).to_csv(os.path.join('Audren/Distance_Analysis/Injected_Charges/Reg/{}.csv'.format(outfile)))
    pd.DataFrame(DIS_INJ, columns = ['Filename','Injected_Charges']).to_csv(os.path.join('Audren/Distance_Analysis/Injected_Charges/Dis/{}.csv'.format(outfile)))
    pd.DataFrame(NEG_INJ, columns = ['Filename','ReInjected_Charges']).to_csv(os.path.join('Audren/Distance_Analysis/Injected_Charges/ReIn/{}.csv'.format(outfile)))
main()
