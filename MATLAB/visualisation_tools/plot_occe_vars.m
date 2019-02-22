clc
clear
load dmsp_omni
load header_dmspX

%% Plot the figures
y = log10(el_total_flux);

titleStr = 'Normalized occurrence';
iter = 1;
k = 1;
cnt = 1;

nRows = 3;
nCols = 2;

isSaveFig = 1; % 1 to save; 0 not to save

figure('Position', [955 -2 1016 1324]);

for i = 1 : size(X, 2)
    if k > nRows * nCols
        if isSaveFig
            saveName = ['./figs/occe_tef_part' num2str(cnt) ' (' num2str(iter) ')'];
            print(saveName, '-dpng', '-r300');
        end
        figure('Position', [955 -2 1016 1324]);
        k = 1;
        cnt = cnt + 1;
    end
    subplot(nRows, nCols, k)
    ndhist(X(:,i), y, 'bins', 0.65, 'normx');%, 'normx')%, 'numpoints', 15);
    xlabel(header{i})
    ylabel('log10(total energy flux)')
    
    k = k + 1;
end

if mod(size(X, 2), nRows * nCols)
    if isSaveFig
        saveName = ['./figs/occe_tef_part' num2str(cnt) ' (' num2str(iter) ')'];
        print(saveName, '-dpng', '-r300');
    end
end
