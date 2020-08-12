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
    LONG_TAB = []
    
    for i in range(len(Plateau)):
        
        if Plateau[i] > 4e-7:
            LONG_TAB.append(Fname[i])
        
        return LONG_TAB

def main():
            
    #Parser to read file
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest = "INFILE", help = ".csv results file")
    args = parser.parse_args()
    outfile = args.INFOLDER.split('/')[-1]
    
    #Importing data
    Fname,Plateau = File_Import(args.INFILE)
    
    #Identifying data sets that are wrong
    Discard_Tab = Adequate_File(Fname,Plateau)
    
    pd.DataFrame(Discard_Tab, columns = ['Filename', 'Plateau']).to_csv(os.path.join('Temp',
    "Discard_files.csv".format(outfile))) 
    
    
    return Discard_Tab

main()    