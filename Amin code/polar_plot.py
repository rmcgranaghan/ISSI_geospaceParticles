import numpy as np 
import tensorflow as tf 
import pandas as pd 
from matplotlib import pyplot as plt 
import datetime as dt 

#Input merged data with mag
dataset_file = '/home/amin.taziny/research/code/mag_data/output/ANN_dataset_merged.csv'
dataset_raw = pd.read_csv(dataset_file, index_col=0)

dataset = dataset_raw.copy()

#Drop columns that are not needed
dataset = dataset.drop(columns = ['DATE', 'TIME', 'Day','ELE_TOTAL_ENERGY_FLUX_STD', \
								  'ELE_AVG_ENERGY','ELE_AVG_ENERGY_STD', 'SC_AACGM_LON','SC_AACGM_LTIME'])

#Make Day and Ltime data sinusoidal and add that to original dataset 
day = dataset_raw.pop('Day')
sc_aacgm_ltime = dataset_raw.pop('SC_AACGM_LTIME') 

day_sin = np.sin((day/365)*2*np.pi)
day_cos = np.cos((day/365)*2*np.pi)
aacgm_ltime_sin = np.sin((sc_aacgm_ltime/24)*2*np.pi)
aacgm_ltime_cos = np.cos((sc_aacgm_ltime/24)*2*np.pi)

dataset['Day_sin'] = day_sin
dataset['Day_cos'] = day_cos
dataset['aacgm_ltime_sin'] = aacgm_ltime_sin
dataset['aacgm_ltime_cos'] = aacgm_ltime_cos

print(dataset.shape)

#Take the log of the DMSP Totel Ele flux
dataset['ELE_TOTAL_ENERGY_FLUX'] = np.log10(dataset['ELE_TOTAL_ENERGY_FLUX'])

#Take absolute value of latitude dataset
dataset['SC_AACGM_LAT'] = abs(dataset['SC_AACGM_LAT'])

#Split datasets into train and test
dataset_train = dataset.sample(frac=0.75, random_state=0)
dataset_test = dataset.drop(dataset_train.index)

#Split features from labels
dmsp_train_label = dataset_train.pop('ELE_TOTAL_ENERGY_FLUX')
dmsp_test_label = dataset_test.pop('ELE_TOTAL_ENERGY_FLUX')

#Inspection of data
dataset_train_stats = dataset_train.describe().transpose()
dmsp_train_label_stats = dmsp_train_label.describe().transpose()

print(dmsp_train_label_stats)
#Normalize the data
def norm(x):
	return (x - dataset_train_stats['mean']) / dataset_train_stats['std']

def dmsp_norm(x):
	return (x - dmsp_train_label_stats['mean']) / dmsp_train_label_stats['std']

normed_dataset_train = norm(dataset_train)
normed_dataset_test = norm(dataset_test)
normed_dataset = normed_dataset_train.append(normed_dataset_test, ignore_index=True)

normed_dmsp_train_label = dmsp_norm(dmsp_train_label)
normed_dmsp_test_label = dmsp_norm(dmsp_test_label)
normed_dmsp = normed_dmsp_train_label.append(normed_dmsp_test_label, ignore_index=True)

#Number of grid points 
Nl = 50
Nmlt = 51
l = np.linspace(45,90,Nl)
mlt = np.linspace(0,2*np.pi,Nmlt)


