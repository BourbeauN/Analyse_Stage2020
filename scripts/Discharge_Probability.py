import pdb
import numpy as np
import argparse
import pandas as pd
import os

def Success_Rate_Whole(Data,a):
    index = np.arange(0,(len(Data)-(a-1)),a)
    Success_Probability=[]
    #pdb.set_trace()
    for i in index:
        #pdb.set_trace()
        temp = Data[i:i+(a-1)]
        count = np.sum(~np.isnan(temp))
        Succ = count/len(temp)
        Success_Probability.append(Succ)
    
    return Success_Probability

def Success_Rate_Partial(Data,Success_Rate,a):
    temp_count = np.sum(~np.isnan(Data))
    temp_succ = temp_count/len(Data)
    Success_Rate.append(temp_succ)
    
    return Success_Rate
    
def get_discharge_information(folder_name):
    
    info = folder_name.split("/")[1].split(".")[0].split("_")[1:5]

    return info 

def main():
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFILE', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-i', type = int, dest = 'INTERVAL', help = 'size of data interval to compute probabilitmy calculation on')
    args = parser.parse_args()
    
    info = get_discharge_information(args.INFILE)
    
    Results = pd.read_csv(args.INFILE,skiprows=10)
    Data_Pandas = Results.iloc[:,2]
    Data = np.asarray(Data_Pandas.values)

    #pdb.set_trace()

    #a is the size of the sample of data over which we want to find the success rate
    a = args.INTERVAL
    
    mod = len(Data)%a

    if mod == 0:
        Final_Probability = Success_Rate_Whole(Data,a)

    else :
        
        Data_1 = Data[0:-mod]
        Data_2 = Data[-mod:]
        
        Partial = Success_Rate_Whole(Data_1,a)
        
        Final_Probability = Success_Rate_Partial(Data_2,Partial,a)
    
    Final_Probability = np.asarray(Final_Probability)
    
    ydata_range = 20*np.arange(0,len(Final_Probability),1)

    DATA = np.column_stack((ydata_range,Final_Probability))

    pd.DataFrame(DATA, columns = ['ID','Probability']).to_csv(os.path.join('Probability',"{}_{}_{}_{}_{}.csv".format(a,info[0],info[1],info[2],info[3])))
        
main()
