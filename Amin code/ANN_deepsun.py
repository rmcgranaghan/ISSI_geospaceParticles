import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#Set numpy printing options
np.set_printoptions(linewidth = 200, suppress = True)
pd.set_option('display.max_columns', None)

#Input Omni & DMSP data
dmsp_raw = pd.DataFrame()
omni_raw = pd.DataFrame()

#Iterate between years to download corresponding data
years = np.arange(2002,2014)
years = np.delete(years,[7,9]) #Delete year 2011 because its in 2010 data file and delete 2009 as data is missing

for year in years:
	file_dmsp = '/home/amta3208/data/dmsp_data_{}.csv'.format(year)
	file_omni = '/home/amta3208/data/omni_data_{}.csv'.format(year)

	#Decided to combine two years into one file one day -- I'm too lazy to fix this
	if year == 2010:
		file_dmsp = '/home/amta3208/data/dmsp_data_2010_2011.csv'
		file_omni = '/home/amta3208/data/omni_data_2010_2011.csv'

	#Append data into large superset
	dmsp_raw = dmsp_raw.append(pd.read_csv(file_dmsp, index_col = 0), ignore_index = True)
	omni_raw = omni_raw.append(pd.read_csv(file_omni, index_col = 0), ignore_index = True)

#copy dataset
dmsp = dmsp_raw.copy()
omni = omni_raw.copy()

#Print shape of each dataset to make sure they match
print(dmsp.shape,omni.shape)

#Split datasets into train and test
dmsp_train = dmsp.sample(frac=0.05, random_state=0)
dmsp_test = dmsp.drop(dmsp_train.index)

omni_train = omni.sample(frac=0.05, random_state=0)
omni_test = omni.drop(omni_train.index)

#Take the log of dmsp data to reduce variance
dmsp_train = np.log10(dmsp_train)
dmsp_test = np.log10(dmsp_test)

#Inspection of data
dmsp_train_stats = dmsp_train.describe().transpose()
omni_train_stats = omni_train.describe().transpose()

#Normalize the data
def omni_norm(x):
	return (x - omni_train_stats['mean']) / omni_train_stats['std']

normed_omni_train = omni_norm(omni_train)
normed_omni_test = omni_norm(omni_test)

def dmsp_norm(x):
	return (x - dmsp_train_stats['mean']) / dmsp_train_stats['std']

normed_dmsp_train = dmsp_norm(dmsp_train)
normed_dmsp_test = dmsp_norm(dmsp_test)

#Split features from labels
normed_dmsp_train_label = normed_dmsp_train.pop('ELE_TOTAL_ENERGY_FLUX')
normed_dmsp_test_label = normed_dmsp_test.pop('ELE_TOTAL_ENERGY_FLUX')

print(normed_omni_train.shape,normed_dmsp_train_label.shape)
print(len(normed_omni_train.keys()))

#Define the model
def build_model():

	model = tf.keras.models.Sequential([ \
				 tf.keras.layers.Dense(256, activation = tf.nn.relu, input_shape = [len(normed_omni_train.keys())] ),\
				# tf.keras.layers.Dense(256, activation = tf.nn.relu, ), \
				 tf.keras.layers.Dense(1) \
				 ])

	optimizer = tf.keras.optimizers.RMSprop(0.01)

	model.compile(loss='mean_squared_error',
	                optimizer=optimizer,
	                metrics=['accuracy', 'mean_squared_error'])
	return model

model = build_model()

model.summary()

model.fit(normed_omni_train, normed_dmsp_train_label, epochs = 10)

print(model.evaluate(normed_omni_train, normed_dmsp_train_label))


# #Compile and train model using optimizer and loss function
# #Considering replacing optimizer function with improved Lavenberg-Marquardt Optimization method


# model.fit(training_images, training_labels, epochs=5)
# #test the model on the data it has yet to see
# model.evaluate(test_images,test_labels)
