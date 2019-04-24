% match the timing between
% mag data with dmsp

clear all, close all

pwd_dir = pwd;

load final_times.mat; % this contains a variable match_times with all the times that are present in all stations and in dmsp

%station_list={'blc','bou','brw','bsl','cbb','cigo','cmo','frn','gua','hon','iqa','mea','new' };
%station_list={'blc','bsl','cbb','cigo','frn','gua','hon','iqa','mea','new' };
%station_list={'blc','cbb','cigo','frn','hon','iqa','mea','new' };

X=[];

mag_dir=['/home/camporea/ISSI_2019/mag_rawdata/'];


i=1;

 cd([mag_dir char(station_list(i))])
 
 dir_list = dir([station_list{i} '_vs_dmsp*']);

 for k=1:length(dir_list)-1;
 
 name_file = dir_list(k).name;
 disp(['Processing ' name_file]) 
 Y = readtable(name_file);
 
 ID_unique=unique(Y.ID_SC)

   for ID = 1:length(ID_unique)
    f=find(Y.ID_SC==ID_unique(ID));
    Y_oneSC = Y(f,:);

    [dum,IA,IB]=intersect(Y_oneSC.Time,match_times.Time); % this finds intersection but with no repetitions
    X = [X; Y_oneSC(IA,:)];
 
   end
 
 end

X.Properties.VariableNames{7}=['BD_' station_list{1}];
X.Properties.VariableNames{8}=['BH_' station_list{1}];
X.Properties.VariableNames{9}=['BZ_' station_list{1}];


size(X)

for i=2:length(station_list);

 cd([mag_dir char(station_list(i))])
 
 dir_list = dir([station_list{i} '_vs_dmsp*']);

 for k=1:length(dir_list)-1;
 
 name_file = dir_list(k).name;
 disp(['Processing ' name_file]) 
 Y = readtable(name_file);
 
 [dum, IA, IB]=intersect(X(:,[1:4 6]),Y(:,[1:4 6]),'rows','stable');

 X(IA,9+3*(i-2)+1:9+3*(i-2)+3)=Y(IB,7:9);
 disp(['size of X = ' num2str(size(X,1))])
 
 end
 
 X.Properties.VariableNames{end-2}=['BD_' station_list{i}];
 X.Properties.VariableNames{end-1}=['BH_' station_list{i}];
 X.Properties.VariableNames{end}=['BZ_' station_list{i}];
end


