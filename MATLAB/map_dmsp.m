% generate particle precipitation map 
% from trained NN
clear all
% pick your time !
year = 2010;
doy = 20;
hour=2;
minute=10;
my_time = datenum(year,0,doy,hour,minute,0);

load dmsp_omni.mat

f=find(my_time==T);
f=f(1);

vec_X = X(f,:);

Nl=50; % number of grid points
Nmlt=51;
d_angle=2*pi/(Nmlt-1);

l=linspace(45,90,Nl);
mlt = 0:d_angle:2*pi;

[L_grid MLT_grid]=meshgrid(l,mlt);

pp = zeros(Nmlt,Nl);


for i=1:Nl
    for j=1:Nmlt
    
       vec = [ vec_X(1:end-3) sin(MLT_grid(j,i)+pi) cos(MLT_grid(j,i)+pi) L_grid(j,i)];

%        vec = [L_grid(j,i); sin(MLT_grid(j,i)+pi); cos(MLT_grid(j,i)+pi); 0; M(:,time)];
       % el(j,i,time) = den2d_themis(vec);
         pp(j,i) = net_test_1(vec'); 
    end
end

X=L_grid.*cos(MLT_grid-pi/2);
Y=L_grid.*sin(MLT_grid-pi/2);

figure
%set(gcf,'position',[110 310 1450 700])
pcolor(X,Y,squeeze(pp)),axis equal,shading interp,colorbar
hold on
plot(X',Y','k')
 plot(X(:,1:5:end),Y(:,1:5:end),'k')
 %[cc,ss]=contour(X,Y,squeeze(s(:,:,1)),[0.1:0.1:0.6],'k');
set(gca,'fontsize',16),axis equal

