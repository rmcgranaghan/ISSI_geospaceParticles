import numpy as np
import pandas as pd 


def getOmniData(year1, year2):

	omni_total = pd.DataFrame()

	for i in np.arange(year1, year2+1):

		#Load complete OMNI dataset
		loadtxt = np.loadtxt("data/omni/high_res_omni/omni_min{}.asc".format(i))

		#Convert dataset to Pandas Dataframe, label appropiate columns of desired parameters
		omni = pd.DataFrame({"Year":loadtxt[:,0], "Day":loadtxt[:,1], "Hour":loadtxt[:,2], "Minute":loadtxt[:,3], \
							 "Bx":loadtxt[:,14], "By":loadtxt[:,17], "Bz":loadtxt[:,18], "Plasma Flow Speed": loadtxt[:,21], \
							 "Bt": np.sqrt(np.power(loadtxt[:,14],2) + np.power(loadtxt[:,17],2)), \
							 "Clock Ang": np.degrees(np.arctan2(loadtxt[:,14], loadtxt[:,17]))})

		#Convert datatype to float and replace emply values with NaN
		omni = omni.astype('float')
		omni[omni == 9999.99] = np.nan
		omni[omni == 99999.9] = np.nan

		#Reduce dataset to average of desired timeframe resolution (minutes)
		time_avg = 1
		omni_avg = pd.DataFrame(omni.values.reshape(-1,time_avg,omni.shape[1]).mean(1), columns = omni.columns)

		#Append omni datasets to create total matrix of data
		omni_total = omni_total.append(omni_avg, ignore_index = True)

	#Export omni data into .csv file
	export_data = omni_total.to_csv(r'~/research/code/data/omni_data_2002.csv')

	return export_data

#Run function for requested years
getOmniData(2002,2002)

#Look into potentially changing time resolution/format to match DMSP 