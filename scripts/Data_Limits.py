import pdb
import numpy as np
import argparse
import pandas as pd
import os

def Limit_Whole(x_data,y_data,a):
    index = np.arange(0,(len(y_data)-(a-1)),a)
    Max_yarray, Min_yarray = [],[]
    Max_xarray, Min_xarray = [],[]

    #pdb.set_trace()
    for i in index:
        #pdb.set_trace()
        temp = y_data[i:i+(a-1)]
        Max_yarray.append(np.float(np.max(temp)))
        Max_xarray.append(np.float(x_data[np.where(temp==np.max(temp))]))
        Min_yarray.append(np.float(np.min(temp)))
        Min_xarray.append(np.float(x_data[np.where(temp==np.min(temp))]))
    
    return Max_yarray,Min_yarray,Max_xarray,Min_xarray

def Limit_Partial(x_data,y_data,a,Max_xarray,Min_xarray,Max_yarray,Min_yarray):
   
    Max_yarray.append(np.float(np.max(Data)))
    Max_xarray.append(np.float(x_data[np.where(y_data==np.max(y_data))]))
    Min_yarray.append(np.float(np.min(Data)))
    Min_xarray.append(np.float(x_data[np.where(y_data==np.min(y_data))]))

    return Max_yarray,Min_yarray,Max_xarray,Min_xarray
    
def get_discharge_information(folder_name):
    
    parameters = folder_name.split("/")[1].split(".")[0].split("_")[1:5]
    d = '_'
    info = d.join(parameters)

    return info 

def main():
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFILE', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-i', type = int, dest = 'INTERVAL', help = 'size of data interval to compute probabilitmy calculation on')
    args = parser.parse_args()
    
    info = get_discharge_information(args.INFILE)
    
    Results = pd.read_csv(args.INFILE)
    xData_Pandas = Results.iloc[:,1]
    x_data = np.asarray(xData_Pandas.values)
    yData_Pandas = Results.iloc[:,2]
    y_data = np.asarray(yData_Pandas.values)

    #pdb.set_trace()

    #a is the size of the sample of data over which we want to find the success rate
    a = args.INTERVAL
    
    mod = len(y_data)%a


    if mod == 0:
        Max_yarray_Final,Min_yArray_Final,Max_xarray_Final,Min_xarray_Final = Limit_Whole(x_data,y_data,a)

    else :
        
        y_data_1 = y_data[0:-mod]
        x_data_1 = x_data[0:-mod]
        y_data_2 = y_data[-mod:]
        x_data_2 = x_data[-mod:]
        
        Max_ytab,Min_ytab,Max_xtab,Min_xtab = Limit_Whole(x_data_1,y_data_1,a)
        
        Max_yarray_Final,Min_yarray_Final,Max_xarray_Final,Min_xarray_Final = Limit_Partial(x_data_2,y_data_2,a,Max_tab,Min_tab)
    
    Max_yArray_Final = np.asarray(Max_yarray_Final)
    Min_yArray_Final = np.asarray(Min_yarray_Final)
    Max_xArray_Final = np.asarray(Max_xarray_Final)
    Min_xArray_Final = np.asarray(Min_xarray_Final)

    MAX_DATA = np.column_stack((Max_xArray_Final,Max_yArray_Final))
    MIN_DATA = np.column_stack((Min_xArray_Final,Min_yArray_Final))

    pd.DataFrame(MAX_DATA, columns = ['x','y']).to_csv(os.path.join('Limits',"Max_{}".format(info)))
    pd.DataFrame(MIN_DATA, columns = ['x','y']).to_csv(os.path.join('Limits','Min_{}'.format(info)))  

main()
