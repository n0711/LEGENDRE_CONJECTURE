function legendre_visualization(n_max)
if nargin < 1
    n_max = 1000;
end
n = (1:n_max)';
failures = zeros(n_max, 1);
for i = 1:n_max
    failures(i) = ~isempty(primes(n(i)^2 + 1, (n(i) + 1)^2 - 1));
end
plot(n, cumsum(failures == 0));
xlabel('n');
ylabel('cumulative failures');
title('Legendre scan failures');
grid on;
saveas(gcf, 'data/legendre_failures.png');
end
