import numpy as np
import pandas as pd

#Code process to delete any NaNs from both panda databases.

# #Import the compiled OMNI and DMSP data
# omni_data = '/home/amin.taziny/research/code/data/omni_data.csv' 
# dmsp_data = '/home/amin.taziny/research/code/data/dmsp_data.csv' 

# omni = pd.read_csv(omni_data)
# dmsp = pd.read_csv(dmsp_data)

#Create two example databases to test on 

def common_data(list1,list2):
	result = False
	row = [ ]

	for y in list2:
		if list1==y:
			result = True
			return result
	return result


elec_energy = np.array(np.arange(1,28)).reshape((9,3))
elec_energy_omni = np.array(np.arange(1,37)).reshape((9,4))

omni_fake = pd.DataFrame(data = elec_energy_omni, columns = ['Bz', 'solar wind', 'plasma speed', 'hello cats'])
omni_fake.iloc[0,1] = omni_fake.iloc[2,0] = omni_fake.iloc[4,2] = omni_fake.iloc[4,3] = np.nan

print(omni_fake)

dmsp_fake = pd.DataFrame(data = elec_energy, columns = ['elec_energy', 'avg_energy', 'coord'])
dmsp_fake.iloc[6,0] = dmsp_fake.iloc[8,2] = np.nan

print(dmsp_fake)

# #Not Optimized shitty way that you coded
# for index,row in omni_fake.iterrows():
# 	for i in row:
# 		if np.isnan(i) == True and (index in omni_fake.index) == True:
# 			omni_fake.drop(index, inplace = True)
# 			dmsp_fake.drop(index, inplace = True)

# for index,row in dmsp_fake.iterrows():
# 	for i in row:
# 		if (np.isnan(i) == True) and (index in dmsp_fake.index) == True:
# 			omni_fake.drop(index, inplace = True)
# 			dmsp_fake.drop(index, inplace = True)


#Super optimized way that keith showed you
dmsp_fake = dmsp_fake.dropna()
omni_fake = omni_fake.dropna()

print(omni_fake)
print(dmsp_fake)

print(np.shape(omni_fake),np.shape(dmsp_fake))

for i in omni_fake.index:
	if common_data(i, dmsp_fake.index) == False:
		if (i in omni_fake.index) == True:
			omni_fake =omni_fake.drop(index = i)

for i in dmsp_fake.index:
	if common_data(i, omni_fake.index) == False:
		if (i in dmsp_fake.index) == True:
			dmsp_fake = dmsp_fake.drop(index = i)


print(np.shape(omni_fake),np.shape(dmsp_fake))
print(omni_fake, '\n', dmsp_fake)
#for i in omni_fake.index:
#	print(i)
