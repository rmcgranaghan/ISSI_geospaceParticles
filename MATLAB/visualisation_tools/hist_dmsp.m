clc
clear
load dmsp_omni

%%
isSaveFig = 1; % 1 to save; 0 not to save

%% Plot histograms
figure('Position', [515 69 1194 713])
subplot(2, 2, 1)
hold on
box on
grid on
histogram(LAT, 50)
title('Lat')

subplot(2, 2, 2)
hold on
box on
grid on
histogram(LTIME, 50)
title('LT')

subplot(2, 2, 3)
hold on
box on
grid on
histogram(log10(el_total_flux), 50)
title('Total energy flux')

subplot(2, 2, 4)
hold on
box on
grid on
histogram(log10(el_avg_energy), 50)
title('Average energy')

%% Save figure
if isSaveFig 
    print('./figs/hists_all', '-dpng', '-r300')
end
