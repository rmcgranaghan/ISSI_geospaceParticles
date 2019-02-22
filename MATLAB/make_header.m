% Create a header

vars = {'Bx', 'By', 'Bz', 'vsw', 'nProt', 'pDynam', 'AE'};

operations = {'now', 'lag5min', 'lag10min', 'lag30min', 'lag45min', ...
    'halfhravg1hrago', 'halfhravg3hrago', 'onehravg5hrago', 'onehravg6hrago'};

header = [{'sin 2pidoy365'} {'cos 2pidoy365'}];

for iOp = 1 : length(operations)
    for iVar = 1 : length(vars)
        header = [header {[vars{iVar} ' ' operations{iOp}]}];
    end
end

header = [header {'sin piLTIME12'} {'cos piLTIME12'} {'LAT'}];
header = header';

%%
% save('header_dmspX', 'header')

