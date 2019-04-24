% use 
% $ wget -e robots=off -np -r https://cdaweb.sci.gsfc.nasa.gov/pub/data/dmsp/dmspf07/
% to download data

clear all,
close all

pwd_dir = pwd;
sc_name='dmspf18';
root = '/home/camporea/ISSI_2019/dmsp_rawdata/cdaweb.sci.gsfc.nasa.gov/pub/data/dmsp/'
dir_sc = [sc_name '/ssj/precipitating-electrons-ions/']

cd([root dir_sc])



dir_list = dir;

Time=[];
SC_AACGM_LAT = [];
SC_AACGM_LTIME = [];
ELE_TOTAL_ENERGY_FLUX = [];
ELE_TOTAL_ENERGY_FLUX_STD = [];
ELE_AVG_ENERGY = [];
ELE_AVG_ENERGY_STD = [];

for d=3:length(dir_list) % loop over years (1st is "."; 2nd is "..")
  if dir_list(d).isdir
   
   cd([root dir_sc dir_list(d).name])

   % in case there are some index.html files
   delete index.html*
   delete SHA1SUM
   
   list_file = dir;
   
   for l=3:length(list_file)
   
        disp(['Processing file ' list_file(l).name]) 
        Time = [Time ; cell2mat(cdfread(list_file(l).name,'Variable','Epoch','ConvertEpochToDatenum',true))];
        SC_AACGM_LAT = [SC_AACGM_LAT ; cell2mat(cdfread(list_file(l).name,'Variable','SC_AACGM_LAT'))];
        SC_AACGM_LTIME = [SC_AACGM_LTIME ; cell2mat(cdfread(list_file(l).name,'Variable','SC_AACGM_LTIME'))];
        ELE_TOTAL_ENERGY_FLUX = [ELE_TOTAL_ENERGY_FLUX ; cell2mat(cdfread(list_file(l).name,'Variable','ELE_TOTAL_ENERGY_FLUX'))];
        ELE_TOTAL_ENERGY_FLUX_STD = [ELE_TOTAL_ENERGY_FLUX_STD ; cell2mat(cdfread(list_file(l).name,'Variable','ELE_TOTAL_ENERGY_FLUX_STD'))];
        ELE_AVG_ENERGY = [ELE_AVG_ENERGY ; cell2mat(cdfread(list_file(l).name,'Variable','ELE_AVG_ENERGY'))];
        ELE_AVG_ENERGY_STD = [ELE_AVG_ENERGY_STD ; cell2mat(cdfread(list_file(l).name,'Variable','ELE_AVG_ENERGY_STD'))];
        
       
   
   end
 end
 
end
   
   
% dmsp data comes at 1-sec cadence
% here we average over 1-min

one_sec = datenum(0,0,0,0,0,1);
one_min = datenum(0,0,0,0,1,0);

current_index=1;
max_length = ceil(length(Time)/60)

Time_1min = zeros(max_length,1);
SC_AACGM_LAT_1min = zeros(max_length,1); 
SC_AACGM_LTIME_1min = zeros(max_length,1);
ELE_TOTAL_ENERGY_FLUX_1min = zeros(max_length,1);
ELE_TOTAL_ENERGY_FLUX_STD_1min = zeros(max_length,1);
ELE_AVG_ENERGY_1min = zeros(max_length,1);
ELE_AVG_ENERGY_STD_1min = zeros(max_length,1);

l_Time = length(Time)-60;
index_1min=1;

while current_index<l_Time
 
    if abs(Time(current_index + 60) - Time(current_index)-one_min)<1e-9
        
        Time_1min(index_1min) = mean(Time(current_index:current_index+60));
        SC_AACGM_LAT_1min(index_1min) = mean(SC_AACGM_LAT(current_index:current_index+60));
        SC_AACGM_LTIME_1min(index_1min) = mean(SC_AACGM_LTIME(current_index:current_index+60));
        ELE_TOTAL_ENERGY_FLUX_1min(index_1min) = mean(ELE_TOTAL_ENERGY_FLUX(current_index:current_index+60));
        ELE_TOTAL_ENERGY_FLUX_STD_1min(index_1min) = mean(ELE_TOTAL_ENERGY_FLUX_STD(current_index:current_index+60));
        ELE_AVG_ENERGY_1min(index_1min) = mean(ELE_AVG_ENERGY(current_index:current_index+60));
        ELE_AVG_ENERGY_STD_1min(index_1min) = mean(ELE_AVG_ENERGY_STD(current_index:current_index+60));
        
        index_1min = index_1min + 1;
        
        current_index  = current_index + 60;
 
    else

        current_index = current_index + 1;
   
    end

    if mod(current_index,100)==0
     disp(['Processing ' num2str(index_1min) '/' num2str(max_length)])     
    end
    
end

Time = Time_1min(1:index_1min-1);
SC_AACGM_LAT = SC_AACGM_LAT_1min(1:index_1min-1);
SC_AACGM_LTIME = SC_AACGM_LTIME_1min(1:index_1min-1);
ELE_TOTAL_ENERGY_FLUX = ELE_TOTAL_ENERGY_FLUX_1min(1:index_1min-1);
ELE_TOTAL_ENERGY_FLUX_STD = ELE_TOTAL_ENERGY_FLUX_STD_1min(1:index_1min-1);
ELE_AVG_ENERGY = ELE_AVG_ENERGY_1min(1:index_1min-1);
ELE_AVG_ENERGY_STD = ELE_AVG_ENERGY_STD_1min(1:index_1min-1);


ID_SC = str2num(sc_name(6:7)) * ones(length(Time),1); 

T = table(Time, SC_AACGM_LAT, SC_AACGM_LTIME, ELE_TOTAL_ENERGY_FLUX, ELE_TOTAL_ENERGY_FLUX_STD, ELE_AVG_ENERGY, ELE_AVG_ENERGY_STD, ID_SC);

cd(pwd_dir)
writetable(T,[sc_name '_1min.csv'])

