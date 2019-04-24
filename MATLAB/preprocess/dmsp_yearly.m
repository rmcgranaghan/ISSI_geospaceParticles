% use 
% $ wget -e robots=off -np -r https://cdaweb.sci.gsfc.nasa.gov/pub/data/dmsp/dmspf07/
% to download data

clear all,
close all

pwd_dir = pwd;

dir_list = dir;

Time=[];
SC_AACGM_LAT = [];
SC_AACGM_LTIME = [];
ELE_TOTAL_ENERGY_FLUX = [];
ELE_TOTAL_ENERGY_FLUX_STD = [];
ELE_AVG_ENERGY = [];
ELE_AVG_ENERGY_STD = [];

for year=1987:2018
    
   disp(['Processing YEAR ' num2str(year)]) 

    Time=[];
    SC_AACGM_LAT = [];
    SC_AACGM_LTIME = [];
    ELE_TOTAL_ENERGY_FLUX = [];
    ELE_TOTAL_ENERGY_FLUX_STD = [];
    ELE_AVG_ENERGY = [];
    ELE_AVG_ENERGY_STD = [];
    ID_SC = [];

    for dmspf=[06:9 12:18]

        disp(['Processing dmsp ' num2str(dmspf)]) 

        namefile = ['dmspf' num2str(dmspf,'%02.f') '_1min.csv'];
        tmp = readtable(namefile);

        time_tmp=datevec(tmp.Time);

        f=find(time_tmp(:,1)==year);

        Time = [Time ; datetime(datevec(tmp.Time(f)))];
        SC_AACGM_LAT = [SC_AACGM_LAT; tmp.SC_AACGM_LAT(f)];
        SC_AACGM_LTIME = [SC_AACGM_LTIME; tmp.SC_AACGM_LTIME(f)];
        ELE_TOTAL_ENERGY_FLUX = [ELE_TOTAL_ENERGY_FLUX; tmp.ELE_TOTAL_ENERGY_FLUX(f)];
        ELE_TOTAL_ENERGY_FLUX_STD = [ELE_TOTAL_ENERGY_FLUX_STD; tmp.ELE_TOTAL_ENERGY_FLUX_STD(f)];
        ELE_AVG_ENERGY = [ELE_AVG_ENERGY; tmp.ELE_AVG_ENERGY(f)];
        ELE_AVG_ENERGY_STD = [ELE_AVG_ENERGY_STD; tmp.ELE_AVG_ENERGY_STD(f)];
        ID_SC = [ID_SC; tmp.ID_SC(f)];
        
    end

T = table(Time, SC_AACGM_LAT, SC_AACGM_LTIME, ELE_TOTAL_ENERGY_FLUX, ELE_TOTAL_ENERGY_FLUX_STD, ELE_AVG_ENERGY, ELE_AVG_ENERGY_STD, ID_SC);

f=find(isnan(T.ELE_TOTAL_ENERGY_FLUX));
T(f,:)=[];	
savename = ['dmsp_' num2str(year) '.csv'];
writetable(T,savename)
end


