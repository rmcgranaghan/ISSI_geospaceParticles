import numpy as np
import pandas as pd
import cdflib
from os import path


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

	omni = omni_total
	
	#Export omni data into .csv file
	#export_data = omni_total.to_csv(r'~/research/code/data/omni_data.csv')

	return omni



def getDMSPdata(year1, year2, sat):

	dmsp_total = pd.DataFrame()

	months = np.array(range(1,13))
	days = np.array(range(1,32))
	ndays = 0
	#counter = 0

	for year in np.arange(year1, year2+1):
		print('\n','Year:',year)
		for month in months:
			if month==4 or month==6 or month==9 or month==11:
				ndays = 30

			elif month==2:
				if (year % 4 == 0):
					ndays = 29
				else:
					ndays = 28
			else: 
				ndays = 31

			print('\n' ,'Month',month)
			for day in range(1,ndays+1):
				
				#Import .CDF file
				file = '/home/amin.taziny/research/code/data/dmsp/dmspf{0}/ssj/precipitating-electrons-ions/{1}/dmsp-f{0}_ssj_precipitating-electrons-ions_{1}{2:02d}{3:02d}_v1.1.2.cdf'\
						.format(sat,year,month,days[day-1])
				
				if (path.exists(file) == True) and (path.getsize(file) > 404):
					#print(path.getsize(file))
					
					elec_flux = cdflib.CDF(file).varget(variable = 'ELE_TOTAL_ENERGY_FLUX')
					elec_flux_std = cdflib.CDF(file).varget(variable = 'ELE_TOTAL_ENERGY_FLUX_STD')
					elec_avg = cdflib.CDF(file).varget(variable = 'ELE_AVG_ENERGY')
					elec_avg_std = cdflib.CDF(file).varget(variable = 'ELE_AVG_ENERGY_STD')
					aacgm_lat  = cdflib.CDF(file).varget(variable = 'SC_AACGM_LAT')
					aacgm_lon  = cdflib.CDF(file).varget(variable = 'SC_AACGM_LON')
					aacgm_ltime  = cdflib.CDF(file).varget(variable = 'SC_AACGM_LTIME')

					dmsp_day = pd.DataFrame( {'ELE_TOTAL_ENERGY_FLUX':elec_flux, 'ELE_TOTAL_ENERGY_FLUX_STD':elec_flux_std, 'ELE_AVG_ENERGY':elec_avg, \
											  'ELE_AVG_ENERGY_STD':elec_avg_std, 'SC_AACGM_LAT':aacgm_lat, 'SC_AACGM_LON':aacgm_lon, 'SC_AACGM_LTIME':aacgm_ltime} )

					#Reduce dataset to average of desired timeframe resolution (seconds)
					time_avg = 60
					dmsp_avg_day = pd.DataFrame(dmsp_day.values.reshape(-1,time_avg,dmsp_day.shape[1]).mean(1), columns = dmsp_day.columns)

					dmsp_total = dmsp_total.append(dmsp_avg_day, ignore_index = True)
					#counter += 1
					#print(np.shape(dmsp_avg_day),np.shape(dmsp_total))
					#print(file)
				else:
					print(file)
					nan = np.full( (1440,), np.nan )
					dmsp_day_empty = pd.DataFrame( {'ELE_TOTAL_ENERGY_FLUX':nan, 'ELE_TOTAL_ENERGY_FLUX_STD':nan, 'ELE_AVG_ENERGY':nan, \
											  'ELE_AVG_ENERGY_STD':nan, 'SC_AACGM_LAT':nan, 'SC_AACGM_LON':nan, 'SC_AACGM_LTIME':nan} )

					dmsp_total = dmsp_total.append(dmsp_day_empty, ignore_index = True)
					#print(file)
					#print(np.shape(dmsp_day_empty), np.shape(dmsp_total))
					#counter += 1
					#print(colored(file, 'red'))

	
	dmsp = dmsp_total				
	#Export omni data into .csv file
	#export_data = dmsp_total.to_csv(r'~/research/code/data/dmsp_data.csv')
	return dmsp 
 

#Run functions for requested years
omni = getOmniData(2012,2012)
dmsp = getDMSPdata(2012,2012,16)


print(omni.shape,dmsp.shape)

#Add the 30 minute time difference to account for travel between sun & earth
dmsp = dmsp.drop(dmsp.index[:30])
omni = omni.drop(omni.index[-30:]) 

#Drop rows of each dataset where a NaN is found
dmsp = dmsp.dropna()
omni = omni.dropna()

#Print shape before iterating between both functions
print(omni.shape,dmsp.shape)

#Define function to determine if any value of number is found in another list
def common_data(list1,list2):
	result = False
	row = [ ]

	for y in list2:
		if list1==y:
			result = True
			return result
	return result

#print(np.array(omni.index)[:50])
#print(np.array(dmsp.index)[:50])

#counter = 0
#Determine matching indicies and delete those that are not found in both
for i in omni.index:
	
	if common_data(i, dmsp.index) == False:
		if (i in omni.index) == True:
			#counter +=1
			print(i, omni.shape,dmsp.shape, (i/(525600*1))*100, '%')
			omni =omni.drop(index = i)

	#if counter >= 500:
	#	break

print('#'*100)

#counter = 0
for i in dmsp.index:
	if common_data(i, omni.index) == False:
		if (i in dmsp.index) == True:
			#counter +=1
			print(i, omni.shape,dmsp.shape, (i/(525600*1))*100, '%')
			dmsp = dmsp.drop(index = i)

	#if counter >= 500:
		#break

print(np.shape(omni),np.shape(dmsp))
#print(np.array(omni.index)[:50],'\n', np.array(dmsp.index)[:50])

dmsp.to_csv(r'~/research/code/data/dmsp_data_2012.csv')
omni.to_csv(r'~/research/code/data/omni_data_2012.csv')
