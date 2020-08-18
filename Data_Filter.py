import pdb
import numpy as np
import os
import argparse
import pandas as pd

def File_Import(filename):

    #Calling results table
    Results = pd.read_csv(filename)
    
    Fname = Results.iloc[:,1]
    Plateau = Results.iloc[:,2].values.ravel()

    return Fname,Plateau

def Adequate_File(Fname,Plateau): 

    #Indexing Plateau lengths that are too long
    DISC_TAB = []
    GOOD_TAB = []

    for i in range(len(Plateau)):
        
        a = Fname[i]
        b = Plateau[i]
        
        if b > 4e-7:
                      
            DISC_TAB.append([a,b])
        
            if i==5:
                print(i.DISC_TAB,GOOD_TAB)
                
        else :
            
            GOOD_TAB.append([a,b])
            
            if i==5:
                print(i,DISC_TAB,GOOD_TAB)
        
        return np.asarray(DISC_TAB),np.asarray(GOOD_TAB)

def main():
    pdb.set_trace()

    #Parser to read file
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest = "INFILE", help = ".csv results file")
    args = parser.parse_args()
    outfile = args.INFILE.split('/')[-1].replace('.csv','')
    
    #Importing data
    Fname,Plateau = File_Import(args.INFILE)
    
    #Identifying data sets that are wrong
    Discard_Tab, Filtered_Tab = Adequate_File(Fname,Plateau)
    
    pd.DataFrame(Discard_Tab, columns = ['Filename', 'Plateau']).to_csv(os.path.join('Temp',"Discard_files_{}.csv".format(outfile))) 
    
    pd.DataFrame(Filtered_Tab, columns = ['Filename', 'Plateau']).to_csv(os.path.join('Temp',"Filtered_files_{}.csv".format(outfile))) 
    
    
    return Discard_Tab,Filtered_Tab

main()    
