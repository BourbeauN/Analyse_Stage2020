import pdb
import numpy as np
import argparse
import pandas as pd
import os

def Limit_Whole(Data,a):
    index = np.arange(0,(len(Data)-(a-1)),a)
    Max_array, Min_array = [],[]
    #pdb.set_trace()
    for i in index:
        #pdb.set_trace()
        temp = Data[i:i+(a-1)]
        Max_array.append(np.float(np.max(temp)))
        Min_array.append(np.float(np.min(temp)))
    
    return Max_array,Min_array

def Limit_Partial(Data,a,Max_array,Min_array):
   
    Max_array.append(np.float(np.max(Data)))
    Min_array.append(np.float(np.min(Data)))
    
    return Max_array,Min_array
    
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
        Max_array_Final,Min_Array_Final = Limit_Whole(Data,a)

    else :
        
        Data_1 = Data[0:-mod]
        Data_2 = Data[-mod:]
        
        Max_tab,Min_tab = Limit_Whole(Data_1,a)
        
        Max_array_Final,Min_array_Final = Limit_Partial(Data_2,a,Max_tab,Min_tab)
    
    Max_Array_Final = np.asarray(Max_array_Final)
    Min_Array_Final = np.asarray(Min_array_Final)
    
    ydata_range = 20*np.arange(0,len(Max_Array_Final),1)

    DATA = np.column_stack((ydata_range,Max_Array_Final,Min_Array_Final))

    pd.DataFrame(DATA, columns = ['ID','Upper Limit','Lower Limit']).to_csv(os.path.join('Limits',"{}_{}_{}_{}_{}.csv".format(a,info[0],info[1],info[2],info[3])))
        
main()