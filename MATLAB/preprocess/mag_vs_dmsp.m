% match the timing between
% mag data with dmsp

clear all, close all

pwd_dir = pwd;

dmsp_dir='/home/camporea/ISSI_2019/dmsp_rawdata/cdaweb.sci.gsfc.nasa.gov/pub/data/dmsp';

station='new';

mag_dir=['/home/camporea/ISSI_2019/mag_rawdata/' station];

% load all dmsp
disp('...load dmsp...')
cd(dmsp_dir)

dmsp_data=[];

for year=2007:2018
    name_file=['dmsp_' num2str(year) '.csv'];
    dmsp_data=[dmsp_data; readtable(name_file)];
end

dmsp_time=dmsp_data.Time;

% load mag data from single station
disp('...load mag...')

cd(mag_dir)

mag_data=[];
for year=2007:2018
    name_file=[station '_' num2str(year) '_1min.csv'];
    mag_data=[mag_data; readtable(name_file)];
end

% check for NaN

f=find(isnan(mag_data.BD)); mag_data(f,:)=[];
f=find(isnan(mag_data.BH)); mag_data(f,:)=[];
f=find(isnan(mag_data.BZ)); mag_data(f,:)=[];

mag_time = mag_data.Time;

ID_unique=unique(dmsp_data.ID_SC)

dmsp_vs_mag=[];
disp('Look for matches')
% look for matches one S/C at the time because there are repeated times
for ID = 1:length(ID_unique)
 f=find(dmsp_data.ID_SC==ID_unique(ID));
 dmsp = dmsp_data(f,:);

 [C,IA,IB]=intersect(dmsp.Time,mag_time); % this finds intersection but with no repetitions

 if length(C)
 dmsp_vs_mag = [dmsp_vs_mag; dmsp(IA,[1:5 8]) mag_data(IB,2:end)];
 end
end 

Year_unique = unique(dmsp_vs_mag.Time.Year);

cd(mag_dir)

disp('Save files')

for i=1:length(Year_unique);
 f=find(dmsp_vs_mag.Time.Year==Year_unique(i));
 tmp = dmsp_vs_mag(f,:);
 writetable(tmp,[station '_vs_dmsp_' num2str(Year_unique(i)) '.csv'])
end

time_only = unique(dmsp_vs_mag(:,1));
writetable(time_only,[station '_vs_dmsp_times.csv'])

cd(pwd_dir)


