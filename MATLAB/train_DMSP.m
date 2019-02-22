% Training NN for predicting particle precipitation
% using DMSP data

clear all, close all
clc

load dmsp_omni.mat

% standardize
X_mean = mean(X);
X_std = std(X);

X = (X-X_mean)./X_std;

y = log10(el_total_flux);

y_mean = mean(y);
y_std = std(y);

y = (y-y_mean)./std(y);


s = size(X,1); % number of events

% define the ratio between training, val and test
train_ratio = 0.5;
val_ratio = 0.25;
test_ratio = 0.25;

train_ind = 1:round(train_ratio*s);
val_ind = train_ind(end) + 1 : round((train_ratio + val_ratio)*s);
    test_ind = val_ind(end)+1:s;

% define the net
define_net

net.trainParam.showWindow=false;
net.trainParam.showCommandLine=true;
net=init(net);

[net,tr] = train(net,X',y','useGPU','yes');
