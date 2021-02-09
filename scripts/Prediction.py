import pdb
import numpy as np
import os
import argparse
import pandas as pd


def Lin_predict(mean_current,p_w,delay):
    
    new_t = p_w - delay    
    y = mean_current*new_t
    
    return y

def get_information(filename):
    
    info = filename.split("/")[-1].split(".")[-2]
    p_w = float(filename.split("/")[-1].split(".")[-2].split("_")[1].replace("ns",""))
    
    return info,p_w

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-delay', dest = 'DELAY', help = 'file folder corresponding to experimental set with discharge infos')
    parser.add_argument('-mean', dest = 'MEAN', help = 'pick a value for voltage threshold')
    parser.add_argument('-inj', dest = 'INJECTED', help = 'pick a value for time threshold')
    args =   parser.parse_args()

    Delay_data = pd.read_csv(args.DELAY)
    Mean_data = pd.read_csv(args.MEAN)
    Inj_data = pd.read_csv(args.INJECTED)

    delay_d = Delay_data["Plateau"]
    mean_d = Mean_data["Mean"]
    inj_d = Inj_data["Absolute_Injected_Charges"]
    
    delay = np.asarray(delay_d.values)
    mean = np.asarray(mean_d.values)
    inj = np.asarray(inj_d.values)

    info,p_w = get_information(args.MEAN)

    p_w_array = np.zeros(len(mean))

    p_w_array += p_w*1e-9
    pred_y = Lin_predict(mean,p_w_array,delay)
    
    pred_y = np.asarray(pred_y)
  
    pd.DataFrame(pred_y).to_csv(os.path.join('Analysis/Prediction/{}.csv'.format(info)))
    
main()
