import pdb
import numpy as np
import argparse
import pandas as pd
import os

def Mean_Whole(Data,a):
    index = np.arange(0,(len(Data)-(a-1)),a)
    Mean_Value=[]
    #pdb.set_trace()
    for i in index:
        #pdb.set_trace()
        temp = ~np.isnan(Data[i:i+(a-1)])
        mean = np.mean(temp)
        Mean_Value.append(mean)
    
    return Mean_Value

def Mean_Partial(Data,Success_Rate,a):
    temp_data = ~np.isnan(Data)
    mean = np.mean(temp_data)
    Success_Rate.append(mean)
    
    return Success_Rate

def get_discharge_information(folder_name):
    
    param = folder_name.split("/")[1].split(".")[0].split("_")[0:2]
    d = '_'
    parameter = d.join(param)
    fname = folder_name.split("/")[1].split(".")[0].split("_")[2:6]
    filename = d.join(fname)

    return parameter,filename

def main():
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFILE', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-i', type = int, dest = 'INTERVAL', help = 'size of data interval to compute probabilitmy calculation on')
    args = parser.parse_args()
    
    parameter,fname = get_discharge_information(args.INFILE)
    
    Results = pd.read_csv(args.INFILE,skiprows=10)
    Data_Pandas = Results.iloc[:,2]
    Data = np.asarray(Data_Pandas.values)

    #pdb.set_trace()

    #a is the size of the sample of data over which we want to find the success rate
    a = args.INTERVAL
    
    mod = len(Data)%a

    if mod == 0:
        Final_Mean = Mean_Whole(Data,a)

    else :
        
        Data_1 = Data[0:-mod]
        Data_2 = Data[-mod:]
        
        Partial = Mean_Whole(Data_1,a)
        
        Final_Mean = Mean_Partial(Data_2,Partial,a)
    
    Final_Mean = np.asarray(Final_Mean)
    
    ydata_range = 20*np.arange(0,len(Final_Mean),1)

    DATA = np.column_stack((ydata_range,Final_Mean))

    pd.DataFrame(DATA, columns = ['ID','Mean']).to_csv(os.path.join("Moving_Mean/{}/{}.csv".format(parameter,fname)))
        
main()
