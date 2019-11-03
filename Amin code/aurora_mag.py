import tensorflow as tf
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import font_manager
import time
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.callbacks import LearningRateScheduler
from scipy.stats import linregress
from sklearn import metrics
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

#Set numpy printing options
np.set_printoptions(linewidth = 200, suppress = True)
pd.set_option('display.max_columns', None)

# #Input Omni & DMSP data
# dmsp_raw = pd.DataFrame()
# omni_raw = pd.DataFrame()

# #Iterate between years to download corresponding data
# years = np.arange(2002,2014)
# years = np.delete(years,[7,9]) #Delete year 2011 because its in 2010 data file and delete 2009 as data is missing

# for year in years:
# 	file_dmsp = '/home/amin.taziny/research/code/data/dmsp_data_{}.csv'.format(year)
# 	file_omni = '/home/amin.taziny/research/code/data/omni_data_{}.csv'.format(year)
# 	#file_dmsp = '/home/amta3208/data/dmsp_data_{}.csv'.format(year)
# 	#file_omni = '/home/amta3208/data/omni_data_{}.csv'.format(year)

# 	#Decided to combine two years into one file one day -- I'm too lazy to fix this
# 	if year == 2010:
# 		file_dmsp = '/home/amin.taziny/research/code/data/dmsp_data_2010_2011.csv'
# 		file_omni = '/home/amin.taziny/research/code/data/omni_data_2010_2011.csv'
# 		#file_dmsp = '/home/amta3208/data/dmsp_data_2010_2011.csv'
# 		#file_omni = '/home/amta3208/data/omni_data_2010_2011.csv'


# 	#Append data into large superset
# 	dmsp_raw = dmsp_raw.append(pd.read_csv(file_dmsp, index_col = 0), ignore_index = True)
# 	omni_raw = omni_raw.append(pd.read_csv(file_omni, index_col = 0), ignore_index = True)

# #copy dataset
# dmsp = dmsp_raw.copy()
# omni = omni_raw.copy()

# #Concat both datasets into superset
# dataset_raw = pd.concat([dmsp,omni], axis = 1)
# #dataset_raw.to_csv(r'~/research/code/mag_data/output/ANN_data.csv')


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


print(min(normed_dmsp_train_label),max(normed_dmsp_train_label))


#Define the model
def build_model():

	model = tf.keras.models.Sequential([ \
				 tf.keras.layers.Dense(64, activation = tf.nn.relu, input_shape = [len(normed_dataset_train.keys())] ),\
				# tf.keras.layers.Dense(256, activation = tf.nn.relu, ), \
				 tf.keras.layers.Dense(1) \
				 ])

	optimizer = tf.keras.optimizers.Adamax()
	#optimizer = tf.keras.optimizers.Adadelta()
	#optimizer = tf.keras.optimizers.RMSprop()
	#optimizer = tf.keras.optimizers.SGD()
	# optimizer = tf.keras.optimizers.Adam()

	model.compile(loss='mean_squared_error', \
	                optimizer=optimizer, \
	                metrics=['mae','mape'])


	return model

model = build_model()

model.summary()

#Making subplots of regression analysis
fig, axs = plt.subplots(2,2, figsize=(9,9))
plt.subplots_adjust(hspace=0.2, wspace=0.2)
hfont = {'fontname':'STIX-Bold'}

NAME = "Auroral_Electron_Flux_ANN_64x1_{0}_{1}".format(int(time.time()), 'Adamax')
tensorboard = TensorBoard(log_dir='logs/{}'.format(NAME))

history_train = model.fit(normed_dataset_train, normed_dmsp_train_label, epochs = 50, validation_split = 0.2, callbacks = [tensorboard])

# save model and architecture to single file
#model.save("ann_model.h5")
#print("Saved model to disk")

#training plot
pred_train = model.predict(normed_dataset_train)
slope, intercept, r_value, p_value, stderr = linregress(normed_dmsp_train_label,pred_train[:,0])
r2_score = metrics.r2_score(normed_dmsp_train_label,pred_train[:,0])
axs[0,0].scatter(normed_dmsp_train_label,pred_train, s=.01, c='darkblue')
axs[0,0].plot([normed_dmsp_train_label.min(),normed_dmsp_train_label.max()], [normed_dmsp_train_label.min(),normed_dmsp_train_label.max()], 'k--',lw=1.5)
axs[0,0].set_title('train R\u00b2={:.5f}'.format(r2_score), fontsize=14, fontweight='bold')
axs[0,0].legend(['Output = Target', 'Data'], loc='upper left', prop={'size': 11})
axs[0,0].set_xticks(ticks=[-2,0,2,4])
axs[0,0].set_yticks(ticks=[-2,0,2,4])
axs[0,0].xaxis.set_minor_locator(AutoMinorLocator(5))
axs[0,0].yaxis.set_minor_locator(AutoMinorLocator(5))
axs[0,0].tick_params(axis='both',direction='in', right = True, top = True, which ='both')
axs[0,0].set_ylabel('Output', fontsize=13)

#validation plot
validation_split = int(0.1*len(normed_dataset_train))
validation_omni = normed_dataset_train.iloc[:validation_split]
validation_dmsp = normed_dmsp_train_label.iloc[:validation_split]
pred_validation = model.predict(validation_omni)
r2_value_v = metrics.r2_score(validation_dmsp,pred_validation[:,0])
axs[0,1].scatter(validation_dmsp,pred_validation, s=.01, c='darkgreen')
axs[0,1].plot([validation_dmsp.min(),validation_dmsp.max()], [validation_dmsp.min(),validation_dmsp.max()], 'k--',lw=1.5)
axs[0,1].set_title('validation R\u00b2={:.5f}'.format(r2_value_v), fontsize=14, fontweight='bold')
axs[0,1].legend(['Output = Target', 'Data'], loc='upper left', prop={'size': 11})
axs[0,1].set_xticks(ticks=[-2,0,2,4])
axs[0,1].set_yticks(ticks=[-2,0,2,4])
axs[0,1].xaxis.set_minor_locator(AutoMinorLocator(5))
axs[0,1].yaxis.set_minor_locator(AutoMinorLocator(5))
axs[0,1].tick_params(axis='both',direction='in', right = True, top = True, which='both')

#test plot
pred_test = model.predict(normed_dataset_test)
r2_value_t = metrics.r2_score(normed_dmsp_test_label,pred_test[:,0])
axs[1,0].scatter(normed_dmsp_test_label,pred_test, s=.01, c='firebrick')
axs[1,0].plot([normed_dmsp_test_label.min(),normed_dmsp_test_label.max()], [normed_dmsp_test_label.min(),normed_dmsp_test_label.max()], 'k--',lw=1.5)
axs[1,0].set_title('test R\u00b2={:.5f}'.format(r2_value_t), fontsize=14, fontweight='bold')
axs[1,0].legend(['Output = Target', 'Data'], loc='upper left', prop={'size': 11})
axs[1,0].set_xlabel('Target',fontsize=13)
axs[1,0].set_ylabel('Output', fontsize=13)
axs[1,0].set_xticks(ticks=[-2,0,2,4])
axs[1,0].set_yticks(ticks=[-2,0,2,4])
axs[1,0].xaxis.set_minor_locator(AutoMinorLocator(5))
axs[1,0].yaxis.set_minor_locator(AutoMinorLocator(5))
axs[1,0].tick_params(axis='both',direction='in', right = True, top = True, which='both')

#all plot
pred_all = model.predict(normed_dataset)
r2_value_a = metrics.r2_score(normed_dmsp,pred_all[:,0])
corrcoef_a = np.corrcoef(normed_dmsp,pred_all[:,0])
axs[1,1].scatter(normed_dmsp,pred_all, s=.01, c='slategrey')
axs[1,1].plot([normed_dmsp.min(),normed_dmsp.max()], [normed_dmsp.min(),normed_dmsp.max()], 'k--',lw=1.5)
axs[1,1].set_title('all R\u00b2={:.5f}'.format(r2_value_a), fontsize=14, fontweight='bold')
axs[1,1].legend(['Output = Target', 'Data'], loc='upper left', prop={'size': 11})
axs[1,1].set_xlabel('Target', fontsize=13)
axs[1,1].set_xticks(ticks=[-2,0,2,4])
axs[1,1].set_yticks(ticks=[-2,0,2,4])
axs[1,1].xaxis.set_minor_locator(AutoMinorLocator(5))
axs[1,1].yaxis.set_minor_locator(AutoMinorLocator(5))
axs[1,1].tick_params(axis='both',direction='in', right = True, top = True, which='both')

print(corrcoef_a)

#plt.savefig('regression_plot_mag.png', dpi=300)
plt.tight_layout()
plt.show()

print(model.evaluate(normed_dataset_train, normed_dmsp_train_label))

# #Compile and train model using optimizer and loss function
# #Considering replacing optimizer function with improved Lavenberg-Marquardt Optimization method


# model.fit(training_images, training_labels, epochs=5)
# #test the model on the data it has yet to see
# model.evaluate(test_images,test_labels)
