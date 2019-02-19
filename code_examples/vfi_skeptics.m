%% Value Function Iteration for Deterministic Optimal Growth Model

sigma = 1.50;
delta = 0.10;
beta  = 0.99;
alpha = 0.30;
ks		= ( (1 - beta * (1 - delta)) / (alpha * beta))^(1 / (alpha - 1) );
kmin	= 0.1*ks;
kmax	= 1.9*ks;

nbk	= 1000;
dk	= (kmax-kmin)/(nbk-1);
k		= linspace(kmin,kmax,nbk)';
v0	= zeros(nbk,1);
v		= zeros(nbk,1);
dr  = zeros(nbk,1);

tol	= 1e-6;
crit	= 1;
num_iter = 0;

storeV = [];
storeK = [];
storeC = [];

%% Beginning of VFI

while crit>tol
  % looping over capital grid
  for i = 1 : nbk
    c = k(i) ^ alpha + (1 - delta) * k(i) - k(:);
    neg = find( c < 0 );
    c(neg) = NaN;
    u = (c.^(1 - sigma) - 1) / (1 - sigma);
    [v(i), dr(i)] = max( u + beta * v0(:) );
  end
  
  crit	= max(abs(v-v0));
  
  tmp_v = v0;
  tmp_k = k(dr);
  tmp_c = tmp_k.^alpha + (1 - delta) * k - tmp_k;

  storeV = [storeV, tmp_v];
  storeK = [storeK, tmp_k];
  storeC = [storeC, tmp_c];

  v0 = v;
  num_iter = num_iter + 1;
end


% evaluating solutions
k1	= k(dr);
c	= k.^alpha+(1-delta)*k-k1;
u	= (c.^(1-sigma)-1)/(1-sigma);


%% Plotting solutions

L = size( storeV, 2 );

shades = 1 - logspace( log10(0.01), log10(0.2), L )';
greyShades = repmat( shades, [1, 3] );

f = figure('Name', 'Paths explored by VFI algorithm');

for l = 1 : 30 : L
  subplot( 2, 2, [1, 3] )
    hold on
      plot( k, storeV(:, l), ...
            'Color', greyShades(num_iter, :), ...
            'LineWidth', 1 )
    hold off
    box on; grid on
    title( 'Value Function' )
  subplot( 2, 2, 2 )
    hold on
      plot( k, storeK(:, l), ...
            'Color', greyShades(num_iter, :), ...
            'LineWidth', 1 )
    hold off
    box on; grid on
    title( 'PolFun - Capital' )
  subplot( 2, 2, 4 )
    hold on
      plot( k, storeC(:, l), ...
            'Color', greyShades(num_iter, :), ...
            'LineWidth', 1 )
    hold off
    box on; grid on
    title( 'PolFun - Consumption' )
    
  waitforbuttonpress
end

subplot( 2, 2, [1, 3] )
  hold on
    plot( k, v, 'Color', 'red', 'LineWidth', 3 )
    xline( ks, 'LineWidth', 1, 'LineStyle', '--', 'Color', 'black' );
  hold off
subplot( 2, 2, 2 )
  hold on
    plot( k, k1, 'Color', 'red', 'LineWidth', 3 )
    plot( k, k, 'Color', 'black', 'LineWidth', 1, 'LineStyle', '--' )
    xline( ks, 'LineWidth', 1, 'LineStyle', '--', 'Color', 'black' );
  hold off
subplot( 2, 2, 4 )
  hold on
    plot( k, c, 'Color', 'red', 'LineWidth', 3 )
    xline( ks, 'LineWidth', 1, 'LineStyle', '--', 'Color', 'black' );
  hold off

