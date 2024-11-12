# Select pairs according to the given threshold in time and baseline
# # used for time series analysis
#Zhao Xuan, Nov 16 2023

# "Usage: python select_pairs.py baseline_table.dat threshold_time_min threshold_time_max threshold_baseline"
#
#"  outputs:"
#"    intf.in tmp "
#

import pandas as pd
import numpy as np
import sys
import math


baseline_path = str(sys.argv[1])
#baseline_path = './baseline_table.dat'
dt1 = int(sys.argv[2])
dt2 = int(sys.argv[3])
db = int(sys.argv[4])

#print(baseline_path,dt,db)

df = pd.read_csv(baseline_path, sep=' ',header=None)
df1 = df.values
df_np = np.array(df1[:,:])
num = df_np.shape[0]

print(num)

t = df_np[:,2]
b = df_np[:,4]
n = df_np[:,0]
tmp = []
intf = []
#print(n)

for i in range(num) :
    for j in range(num) :
        if t[i] < t[j] and t[j] - t[i] > dt1 and t[j] - t[i] <= dt2 :
            db0 = math.sqrt((b[i]-b[j])**2)
            if db0 < db :                
                nx = (n[i]+':'+n[j])
                intf.append(nx)
                tmp1 = (t[i]/365.25+2014,b[i])
                tmp2 = (t[j]/365.25+2014,b[j])
                tmpn = ('NaN','NaN')
                tmp.append(tmp1)
                tmp.append(tmp2)
                tmp.append(tmpn)
tmp = np.array(tmp)
tmp = tmp.astype(str)
intf = np.array(intf)


b_line1 = []
b_line2 = []
for i in range(n.shape[0]) :
    if any(n[i] in element for element in intf) :
        b_line1.append(df_np[i])
    else:
        b_line2.append(df_np[i])
b_line1 = np.array(b_line1)
b_line2 = np.array(b_line2)


#print(tmp)

np.savetxt('tmp',tmp,fmt="%s")
np.savetxt('intf.in',intf,fmt="%s")
np.savetxt('b_line2',b_line2,fmt="%s")
np.savetxt('sbas_table',b_line1,fmt="%s")

