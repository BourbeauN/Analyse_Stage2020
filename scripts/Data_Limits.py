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
        print(i)
	        pdb.set_trace()
        temp_y = y_data[i:i+(a-1)]
        temp_x = x_data[i:i+(a-1)]
        #if i == 5985:
	        #pdb.set_trace()
        if np.sum(~np.isnan(temp_y)) != 0 :

            not_nan = temp_y[np.where(~np.isnan(temp_y))[0]]

            max_index = np.where(not_nan == np.max(not_nan))[0][0]
            min_index = np.where(not_nan == np.min(not_nan))[0][0]

            Max_yarray.append(temp_y[max_index])
            Max_xarray.append(temp_x[max_index])
            Min_yarray.append(temp_y[min_index])
            Min_xarray.append(temp_x[min_index])

    return Max_yarray,Min_yarray,Max_xarray,Min_xarray

def Limit_Partial(x_data,y_data,Max_yarray,Min_yarray,Max_xarray,Min_xarray):

    if np.sum(~np.isnan(y_data)) != 0 :    

        max_index = np.where(y_data == np.max(y_data))[0][0]
        min_index = np.where(y_data == np.min(y_data))[0][0]

        Max_yarray.append(y_data[max_index])
        Max_xarray.append(x_data[max_index])
        Min_yarray.append(y_data[min_index])
        Min_xarray.append(x_data[min_index])

    return Max_yarray,Min_yarray,Max_xarray,Min_xarray
    
def get_discharge_information(folder_name):
    
    parameter = folder_name.split("/")[1].split(".")[0].split("_")[2:]
    d = "_"
    folder = folder_name.split("/")[1].split(".")[0].split("_")[0:2]

    param = d.join(parameter)
    fol = d.join(folder)

    return param,fol

def main():
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest = 'INFILE', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-i', type = int, dest = 'INTERVAL', help = 'size of data interval to compute probabilitmy calculation on')
    args = parser.parse_args()
    
    param,fol = get_discharge_information(args.INFILE)
    
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
        Max_yarray_Final,Min_yarray_Final,Max_xarray_Final,Min_xarray_Final = Limit_Whole(x_data,y_data,a)

    else :
        
        y_data_1 = y_data[0:-mod]
        x_data_1 = x_data[0:-mod]
        y_data_2 = y_data[-mod:]
        x_data_2 = x_data[-mod:]
        #pdb.set_trace()
        
        Max_ytab,Min_ytab,Max_xtab,Min_xtab = Limit_Whole(x_data_1,y_data_1,a)
        
        if np.sum(~np.isnan(y_data_2)) == 0:
            Max_yarray_Final,Min_yarray_Final,Max_xarray_Final,Min_xarray_Final = Limit_Partial(x_data_2,y_data_2,Max_ytab,Min_ytab,Max_xtab,Min_xtab)
        else :
            Max_yarray_Final = Max_ytab
            Min_yarray_Final = Min_ytab
            Max_xarray_Final = Max_xtab
            Min_xarray_Final = Min_xtab
    #pdb.set_trace()
    Max_yArray_Final = np.asarray(Max_yarray_Final)
    Min_yArray_Final = np.asarray(Min_yarray_Final)
    Max_xArray_Final = np.asarray(Max_xarray_Final)
    Min_xArray_Final = np.asarray(Min_xarray_Final)

    DATA = np.column_stack((Max_xArray_Final,Max_yArray_Final,Min_xArray_Final,Min_yArray_Final))

    pd.DataFrame(DATA, columns =
    ['x_max','y_max','x_min','y_min']).to_csv(os.path.join('Limits/{}'.format(fol),"{}.csv".format(param)))
      
main()
