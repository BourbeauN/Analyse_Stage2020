
def load_data():
    path = 'C:/Users/Naomi/Documents/GitHub/Analyse_Stage2020/5kv_100nspicpic'
    discharges = []
    
    for filename in os.listdir(path)[:10]:
        
        time , volt , curr = np.loadtxt(os.path.join(path, filename),skiprows=12,delimiter = ',', unpack = True)
        discharges.append((filename, [np.array(time), np.array(volt), np.array(curr)])) 
    return discharges

