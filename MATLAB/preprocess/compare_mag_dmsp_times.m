% match the timing between
% mag data with dmsp

clear all, close all

pwd_dir = pwd;

%station_list={'blc','bou','brw','bsl','cbb','cigo','cmo','frn','gua','hon','iqa','mea','new' };
station_list={'blc','bsl','cbb','cigo','frn','gua','hon','iqa','mea','new' };
%station_list={'blc','cbb','cigo','frn','hon','iqa','mea','new' };

mag_dir=['/home/camporea/ISSI_2019/mag_rawdata/'];

for i=1:length(station_list);

 cd([mag_dir char(station_list(i))])
 T{i} = readtable([char(station_list(i)) '_vs_dmsp_times.csv']);
 len_t(i) = height(T{i});
 
 end

V=nchoosek(1:10,6);

s = length(V);
Cmax_h=0;

for i=1:s
 C=intersect(T{V(i,1)},T{V(i,2)});
 for k =3:6
 C = intersect(C,T{V(i,k)});
 end
 if height(C)>Cmax_h
  Cmax_h = height(C)
  Cmax = C;
  Vbest = V(i,:);
 end
end
  
 
return
cd(pwd_dir);


match_times = Cmax;
station_list = station_list(Vbest);

save final_times.mat match_times station_list