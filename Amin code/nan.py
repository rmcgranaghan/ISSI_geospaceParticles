import numpy as np
import pandas as pd


#Import the compiled OMNI and DMSP data
omni_data = '/home/amin.taziny/research/code/data/omni_data.csv' 
dmsp_data = '/home/amin.taziny/research/code/data/dmsp_data.csv' 

omni = pd.read_csv(omni_data)
dmsp = pd.read_csv(dmsp_data)

#Remove all rows that contain an NaN from both datasets  
for index,row in omni.iterrows():
	for i in row:
		if np.isnan(i) == True and (index in omni.index) == True:
			omni.drop(index, inplace = True)
			dmsp.drop(index, inplace = True)

for index,row in dmsp.iterrows():
	for i in row:
		if np.isnan(i) == True and (index in dmsp.index) == True:
			omni.drop(index, inplace = True)
			dmsp.drop(index, inplace = True)

print(np.shape(omni))
print(np.shape(dmsp))