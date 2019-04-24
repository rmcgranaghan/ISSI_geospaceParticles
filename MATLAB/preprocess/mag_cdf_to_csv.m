% use 
% $ wget -e robots=off -np -r http://themis.ssl.berkeley.edu/data/themis/thg/ascii_data/mag/
% to download data
% this script transforms cdf files of a given magnetometer station into csv files
% it also performs 1-minute average 



clear all,
close all

pwd_dir = pwd;
station='new';
mkdir(station)
time_variable = ['thg_mag_' station '_time'];
B_variable = ['thg_mag_' station];
root = ['/home/camporea/ISSI_2019/mag_rawdata/themis.ssl.berkeley.edu/data/themis/thg/l2/mag/' station '/'];

cd(root)

dir_list = dir;


for d=3:length(dir_list) % loop over years (1st is "."; 2nd is "..")

Time=[];
BD=[]; BH=[]; BZ=[];

   if dir_list(d).isdir
   
        cd([root dir_list(d).name '/'])

        % in case there are some index.html files
        delete index.html*
        delete CHECKSUMS
        list_file = dir;
        
        for l = 3:length(list_file)
 
        
        disp(['Processing file ' list_file(l).name]) 

        this_day = list_file(3).name(end-15:end-8);
        year = str2num(this_day(1:4));
        month = str2num(this_day(5:6));
        day = str2num(this_day(7:8));

        tmp = cell2mat(cdfread(list_file(l).name,'Variable',time_variable));
        tmp_time = [1970 1 1 0 0].*ones(length(tmp),1);
        Time = [Time ; datenum([tmp_time tmp]) ];
        
        B=cell2mat(cdfread(list_file(l).name,'Variable',B_variable));
        B=reshape(B,3,length(tmp))';
        BD = [BD; B(:,1)];
        BH = [BH; B(:,2)];
        BZ = [BZ; B(:,3)];
   
        end
  end
 
   
   
% dmsp data comes at 1-sec cadence
% here we average over 1-min

one_sec = datenum(0,0,0,0,0,1);
one_min = datenum(0,0,0,0,1,0);

current_index=1;
max_length = ceil(length(Time)/60);

Time_1min = zeros(max_length,1);
BD_1min = zeros(max_length,1); 
BH_1min = zeros(max_length,1);
BZ_1min = zeros(max_length,1);

l_Time = length(Time)-60;
index_1min=1;

while current_index<l_Time
 
    if abs(Time(current_index + 60) - Time(current_index)-one_min)<1e-9
        
        Time_1min(index_1min) = mean(Time(current_index:current_index+60));
        BD_1min(index_1min) = mean(BD(current_index:current_index+60));
        BH_1min(index_1min) = mean(BH(current_index:current_index+60));
        BZ_1min(index_1min) = mean(BZ(current_index:current_index+60));
        
        index_1min = index_1min + 1;
        
        current_index  = current_index + 60;
 
    else

        current_index = current_index + 1;
   
    end

    if mod(current_index,100)==0
     disp(['Processing ' num2str(index_1min) '/' num2str(max_length)])     
    end
    
end

Time = datetime(datevec(Time_1min(1:index_1min-1)));
BD = BD_1min(1:index_1min-1);
BH = BH_1min(1:index_1min-1);
BZ = BZ_1min(1:index_1min-1);

T = table(Time, BD, BH, BZ);

cd([pwd_dir '/' station])
writetable(T,[station '_' num2str(year) '_1min.csv'])
cd(root)
end

cd(pwd_dir)