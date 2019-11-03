% sensitivity analysis through leave-one-out

clear all, close all

load dmsp_omni.mat
y = log10(el_total_flux)';

load net_test_1.mat  y_mean y_std

trained_net='net_test_1';

y_net=feval(trained_net,X')';

[r_base m b]=regression(y_net',y');

n_attributes = size(X,2);

r = zeros(n_attributes,1);

for i=1:n_attributes
    
    X_test = X;
    X(:,i) = 0;
    y_net=feval(trained_net,X')';

    [r(i) m b]=regression(y_net',y');
    
end

plot(1:n_attributes,r/r_base,'.')

[r_sort ind_sort]sort(r/r_base);
