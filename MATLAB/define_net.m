% define NN 
  
  net = feedforwardnet(50);
  net.numLayers=3;
  net.biasConnect=[1; 1;  1];
  net.inputConnect=[1;0; 0];
  net.layerConnect=[0 0 0 ;1 0 0 ;0 1 0 ];
  net.outputConnect=[0 0  1];
  net.layers{2}.dimensions=10;
  net.layers{3}.dimensions=1;
  net.layers{2}.name='Hidden';
  net.layers{3}.name='Hidden';
  net.layers{3}.initFcn = 'initnw';


% help nnstran  sfer
net.layers{1}.transferFcn='poslin';
net.layers{2}.transferFcn='poslin';

net.divideFcn='divideind';net.divideParam.trainInd=train_ind;net.divideParam.valInd=val_ind;net.divideParam.testInd=test_ind;
%net.trainFcn = 'trainbfg';
net.trainParam.epochs=100;
%net.performFcn = 'my_cost_function';
%net.trainParam.max_fail=10;
net.performParam.regularization=0.2;


%net.trainParam.min_grad=1e-8;
%net.trainParam.showWindow=false;
%net.trainParam.showCommandLine=true;
