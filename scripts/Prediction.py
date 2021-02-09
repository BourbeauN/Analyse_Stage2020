import pdb
import numpy as np
import os
import argparse
import pandas as pd


def Lin_predict(mean_current,p_w,delay):
    
    y = mean_current(p_w-delay)
    
    return y

def get_information(filename):
    
    info = filename.split("/")[-1].split(".")[-2]
    p_w = float(filename.split("/")[-1].split(".")[-2].split("_")[1].replace("ns",""))
    
    return info,p_w

def main():
    ###PARSER###
    parser = argparse.ArgumentParser()
    parser.add_argument('-delay', dest = 'DELAY', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-mean', dest = 'MEAN', help = 'pick a value for voltage threshold')
    parser.add_argument('-inj', dest = 'INJECTED', help = 'pick a value for time threshold')
    args =   parser.parse_args()

    Delay_data = pd.read_csv(args.DELAY)
    Mean_data = pd.read_csv(args.MEAN)
    Inj_data = pd.read_csv(args.INJECTED)
    
    delay = Delay_data["Plateau"].values()
    mean = Mean_data["Mean"].values()
    inj= Inj_data["Injected_Charges"].values()
    
    pred_y = Lin_predict(mean,p_w,delay)
    
    pred_y = np.asarray(pred_y)
  
    pd.DataFrame(pred_y).to_csv(os.path.join('Analysis/Prediction/{}.csv'.format(info)))
    
main()