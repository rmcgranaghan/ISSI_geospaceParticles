clear all
close all

dmsp=readtable('full2010_reducedDB.csv');

T=datenum(dmsp.datetime);
T_unique = unique(T);

SC_AACGM_LTIME = dmsp.SC_AACGM_LTIME;
SC_AACGM_LAT = dmsp.SC_AACGM_LAT;
ELE_TOTAL_ENERGY_FLUX = dmsp.ELE_TOTAL_ENERGY_FLUX;
ELE_AVG_ENERGY = dmsp.ELE_AVG_ENERGY;
ID_sc = dmsp.spacecraftNumber;

ID_unique = unique(ID_sc);

load omni_2010.mat

el_avg_energy = [];
el_total_flux = [];
sat_number = [];

% loop over spacecraftNumber

X=[]; % matrix with attributes

LTIME=[];
LAT = [];

for ID_ind = ID_unique'
 
 
 this_sc = find(ID_sc == ID_ind);

 clear omni_1min omni_5mins_ago omni_10mins_ago omni_30mins_ago omni_45mins_ago
 clear half_hour_avrg_1_hr_ago half_hour_avrg_3_hr_ago
 clear one_hour_average_5_hr_ago one_hour_average_6_hr_ago

  five_mins=datenum(0,0,0,0,5,0);
  ten_mins=datenum(0,0,0,0,10,0);
  thirty_mins=datenum(0,0,0,0,30,0);
  fortyfive_mins=datenum(0,0,0,0,45,0);
  one_hour = datenum(0,0,0,1,0,0);
  three_hours = datenum(0,0,0,3,0,0);
  five_hours = datenum(0,0,0,5,0,0);

  for ind=1:size(omni,2)
    omni_1min(:,ind) = interp1(T_omni,omni(:,ind),T(this_sc));
    omni_5mins_ago(:,ind) = interp1(T_omni,omni(:,ind),T(this_sc)-five_mins);
    omni_10mins_ago(:,ind) = interp1(T_omni,omni(:,ind),T(this_sc)-ten_mins);
    omni_30mins_ago(:,ind) = interp1(T_omni,omni(:,ind),T(this_sc)-thirty_mins);
    omni_45mins_ago(:,ind) = interp1(T_omni,omni(:,ind),T(this_sc)-fortyfive_mins);
    half_hour_avrg_1_hr_ago(:,ind) = interp1(T_omni,half_hour_average(:,ind),T(this_sc)-one_hour);
    half_hour_avrg_3_hr_ago(:,ind) = interp1(T_omni,half_hour_average(:,ind),T(this_sc)-three_hours);
    one_hour_average_5_hr_ago(:,ind)=interp1(T_omni,one_hour_average(:,ind),T(this_sc)-five_hours);
    one_hour_average_6_hr_ago(:,ind)=interp1(T_omni,one_hour_average(:,ind),T(this_sc)-five_hours-one_hour);
  end

   doy_omni_1min=interp1(T_omni,doy_omni,T(this_sc));

   Xtemp = [sin(doy_omni_1min*2*pi/365) cos(doy_omni_1min*2*pi/365) omni_1min];
 
   Xtemp = [Xtemp omni_5mins_ago omni_10mins_ago omni_30mins_ago omni_45mins_ago];

   Xtemp = [Xtemp half_hour_avrg_1_hr_ago half_hour_avrg_3_hr_ago];

   Xtemp = [Xtemp one_hour_average_5_hr_ago one_hour_average_6_hr_ago];

   tmp_1 = SC_AACGM_LTIME(this_sc);
   tmp_2 = SC_AACGM_LAT(this_sc);
   Xtemp = [Xtemp sin(pi*tmp_1/12) cos(pi*tmp_1/12) tmp_2];
   LTIME=[LTIME;tmp_1];
   LAT = [LAT;tmp_2];
   
   X=[X;Xtemp];

   tmp = ELE_AVG_ENERGY(this_sc);
   el_avg_energy = [el_avg_energy; tmp];
   
   tmp = ELE_TOTAL_ENERGY_FLUX(this_sc);
   el_total_flux = [el_total_flux; tmp];
   
   tmp = ID_sc(this_sc);
   sat_number = [sat_number; tmp];

%ELE_AVG_ENERGY = ELE_AVG_ENERGY(360:end);
%ELET_OTAL_ENERGY_FLUX = ELE_TOTAL_ENERGY_FLUX(360:end);

end

% delete NaNs

[I,J]=find(isnan(X));
X(I,:)=[];
el_avg_energy(I)=[];
el_total_flux(I)=[];
sat_number(I) = [];

f=find(isnan(el_avg_energy));
el_avg_energy(f)=[];
el_total_flux(f)=[];
sat_number(f) = [];
X(f,:)=[];

f=find(isnan(el_total_flux));
el_avg_energy(f)=[];
el_total_flux(f)=[];
sat_number(f) = [];
X(f,:)=[];

save dmsp_omni.mat X T el_avg_energy el_total_flux LAT LTIME doy_omni_1min sat_number



