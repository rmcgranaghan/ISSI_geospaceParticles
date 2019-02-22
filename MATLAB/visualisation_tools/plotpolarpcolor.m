function plotpolarpcolor(bins_L, bins_MLT, arr_occe, titleStr, cbarStr)

% Create a grid
[rho_2D, theta_2D] = meshgrid(90 - (bins_L(1 : end - 1)), bins_MLT(1 : end - 1) * pi / 12);
[X_2D, Y_2D] = pol2cart(theta_2D, rho_2D);

% Create a polar figure
figure;
pplot = polar(0, floor(max(max(rho_2D))));

% Polish it slightly
set(0, 'ShowhiddenHandles', 'on');
polarline = findobj(gca,'type', 'line');
polartext = findobj(gca, 'type', 'text');
set(0, 'ShowhiddenHandles', 'off');

% Plot the stuff
hold on
pc = pcolor(X_2D, Y_2D, (arr_occe)');
pc.LineStyle = 'None';
axis equal tight 
colormap jet

% Adjust lines and stuff on the polar plot
uistack(polarline, 'top');
uistack(polartext(13:17), 'top');

set(findall(gcf, 'String', '90'),'String', '');
% set(findall(gcf, 'String', '90'),'String', ' 6');
set(findall(gcf, 'String', '180'),'String', ' 12');
set(findall(gcf, 'String', '270'),'String', ' 18');
set(findall(gcf, 'String', '30'),'String', '');
set(findall(gcf, 'String', '60'),'String', '');
set(findall(gcf, 'String', '120'),'String', '');
set(findall(gcf, 'String', '150'),'String', '');
set(findall(gcf, 'String', '210'),'String', '');
set(findall(gcf, 'String', '240'),'String', '');
set(findall(gcf, 'String', '300'),'String', '');
set(findall(gcf, 'String', '330'),'String', '');
set(findall(gcf, 'String', '  100'),'String', '');

for i = 1 : length(polarline)
%     polarline(i)
    polarline(i).LineStyle = '-.';
    polarline(i).LineWidth = 0.25;
    polarline(i).Color = [0.9 0.9 0.9];
end

% Modify the labels to correspond to latitudes values
string_arr = {'', '50', '60', '70', '80'};
for i = 13 : 17
    polartext(i).String = string_arr{i - 12};
%     polartext(i).Color = [0.8 0.8 0.8];
end

% Change position
pos = pplot.Parent.Position;
pplot.Parent.Position = [pos(1) * 0.1 pos(2) * 0.6 pos(3) pos(4)];

% Add colobar
hC = colorbar;
posHc = hC.Position;
delete(hC);
hC = colorbar('location', 'eastoutside', 'position', [posHc(1) * 1.14 posHc(2) * 0.97 posHc(3) posHc(4)]);
xlabel(hC, cbarStr)

% Increase fonts
f = gcf;
set(findall(f, '-property', 'FontSize'), 'FontSize', 14)

title(titleStr)

