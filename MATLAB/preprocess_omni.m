clear all, close all
omni = load('omni_5min2010.asc');

f=find(omni(:,15)==9.999990000000000e+03);
omni(f,15)=NaN;
f=find(omni(:,18)==9.999990000000000e+03);
omni(f,18)=NaN;
f=find(omni(:,19)==9.999990000000000e+03);
omni(f,19)=NaN;
f=find(omni(:,22)==9.999989999999999e+04);
omni(f,22)=NaN;
f=find(omni(:,26)==9.999900000000000e+02);
omni(f,26)=NaN;
f=find(omni(:,28)==99.989999999999995);
omni(f,28)=NaN;


omni = omni(:,[1:4 15 18 19 22 26 28 38]);


one_hour_average= movmean(omni,12,'omitnan');

half_hour_average= movmean(omni,6,'omitnan');

T_omni = datenum(omni(:,1),0,omni(:,2),omni(:,3),omni(:,4),0);

% take away the time and keep record of the doy
doy_omni = omni(:,2); %

omni=omni(:,5:end);
one_hour_average = one_hour_average(:,5:end);
half_hour_average = half_hour_average(:,5:end);

save omni_2010.mat