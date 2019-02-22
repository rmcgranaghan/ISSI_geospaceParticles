clc
clear
load dmsp_omni

%%
isSaveFig = 0; % 1 to save; 0 not to save

%% Polar plot of occurrence for each spacecraft separately
ID_unique = unique(sat_number);

for satNum = ID_unique'
    
    bins_Lat = [linspace(min(LAT), max(LAT), 6*4) max(LAT) * 1.1];
    bins_LT = [linspace(min(LTIME), max(LTIME), 24*2) max(LTIME) * 1.1];
    
    latSat = LAT(sat_number == satNum);
    ltimeSat = LTIME(sat_number == satNum);
    
    % Calculate occurrence map
    arr_occe_all = NaN(length(bins_Lat) - 1, length(bins_LT) - 1);
    for iLat = 1 : length(bins_Lat) - 1
        for iLT = 1 : length(bins_LT) - 1
            inds = latSat >= bins_Lat(iLat) & latSat < bins_Lat(iLat + 1)  &...
                ltimeSat >= bins_LT(iLT) & ltimeSat < bins_LT(iLT + 1);
            arr_occe_all(iLat, iLT) = sum(inds);
            if arr_occe_all(iLat, iLT) == 0
                arr_occe_all(iLat, iLT) = NaN;
            end
        end
    end
    
    % Polar plot of measurements occurences
    titleStr = ['2010 - F' num2str(satNum)];
    cbarStr = '# measurements';
    plotpolarpcolor(bins_Lat, bins_LT, arr_occe_all, titleStr, cbarStr);
    
    % Save figure
    if isSaveFig
        print(['./figs/polar_occe_F' num2str(satNum)], '-dpng', '-r300')
    end 
end


%% Polar plot of occurrence for all spacecraft
bins_Lat = [linspace(min(LAT), max(LAT), 6*4) max(LAT) * 1.1];
bins_LT = [linspace(min(LTIME), max(LTIME), 24*2) max(LTIME) * 1.1];

latSat = LAT;
ltimeSat = LTIME;

% Calculate occurrence map
arr_occe_all = NaN(length(bins_Lat) - 1, length(bins_LT) - 1);
for iLat = 1 : length(bins_Lat) - 1
    for iLT = 1 : length(bins_LT) - 1
        inds = latSat >= bins_Lat(iLat) & latSat < bins_Lat(iLat + 1)  &...
            ltimeSat >= bins_LT(iLT) & ltimeSat < bins_LT(iLT + 1);
        arr_occe_all(iLat, iLT) = sum(inds);
        if arr_occe_all(iLat, iLT) == 0
            arr_occe_all(iLat, iLT) = NaN;
        end
    end
end

% Polar plot of measurements occurences
titleStr = 'All satellites - 2010';
cbarStr = '# measurements';
plotpolarpcolor(bins_Lat, bins_LT, arr_occe_all, titleStr, cbarStr);

% Save figure
if isSaveFig
    print('./figs/polar_occe_all', '-dpng', '-r300')
end





