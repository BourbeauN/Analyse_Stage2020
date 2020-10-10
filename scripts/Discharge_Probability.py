import pdb
import numpy as np
import argparse
import pandas as pd
import os

def Success_Rate_Whole(Data):
    index = np.arange(0,(len(Data)-(a-1)),a)
    Success_Probability=[]
    for i in range(len(index)):
        temp = Data[index[i],(index[i]+a)]
        count = np.sum(~np.isnan(temp))
        Succ = 1 - count/len(temp)
        Success_Probability.append(Succ)
    
    return Success_Probability

def Success_Rate_Partial(Data,Success_Rate):
    temp_count = np.sum(~np.isnan(Data))
    temp_succ = 1 - temp_count/len(Data)
    Success_Rate.append(temp_succ)
    
    return Success_Rate
    
def get_discharge_information(folder_name):
    
    info = folder_name.split("/")[1].split(".")[0].split("_")[1:]

    return info 

def main():
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFOLDER', help = 'file folder corresponding to experimental set with discharge infos')
    args = parser.parse_args()
    
    info = get_discharge_information(args.INFILE)
    
    Results = pd.read_csv(args.INFILE)
    Data = Results.iloc[1]
    #a is the size of the sample of data over which we want to find the success rate
    a = 20 
    
    if len(Data)%a == 0:
        Final_Probability = Success_Rate_Whole(Data)

    else :
        mod = len(Data)%a
        Data_1 = Data[0:-mod]
        Data_2 = Data[-mod:]
        
        Partial = Success_Rate_Whole(Data_1)
        
        Final_Probability = Success_Rate_Partial(Data_2,Partial)
    
    Final_Probability = np.asarray(Final_Probability)
    
    pd.DataFrame(Final_Probability, columns = ['Probability']).to_csv(os.path.join('Probability',"{}_{}.csv".format(a,info)))
        
main()