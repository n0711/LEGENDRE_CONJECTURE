function legendre_visualization(csv_path)
% NUMERICAL: visualize exported proof-obligation diagnostics; not a proof.
% Generate data first: python scripts/research_diagnostics.py
if nargin < 1
    csv_path = fullfile('data', 'research_diagnostics.csv');
end
d = readtable(csv_path);
assert(height(d) > 0 && all(isfinite(d{:,:}), 'all'));
f = figure('Visible', 'off', 'Position', [100, 100, 1200, 440]);
cleanup = onCleanup(@() close(f));
tiledlayout(1, 2, 'Padding', 'compact', 'TileSpacing', 'compact');
nexttile;
plot(d.n, [d.survivors_per_n, d.bonferroni_1_per_n, ...
    d.bonferroni_3_per_n], 'LineWidth', 1.5);
yline(0, ':');
xlabel('n'); ylabel('Count or lower bound, divided by n');
title('NUMERICAL: fixed-depth sieve bounds');
legend('Exact survivors', 'Bonferroni degree 1', 'Bonferroni degree 3', ...
    'Location', 'southwest'); grid on;
nexttile;
semilogy(d.n, [d.tail_kappa_1_per_n, d.tail_kappa_10_per_n], 'LineWidth', 1.5);
xlabel('n'); ylabel('B(n,T) / n');
title('NUMERICAL: tail budget at T = kappa n log n');
legend('kappa = 1', 'kappa = 10', 'Location', 'northeast'); grid on;
output_dir = fileparts(csv_path);
exportgraphics(f, fullfile(output_dir, 'research_diagnostics.png'), 'Resolution', 180);
exportgraphics(f, fullfile(output_dir, 'research_diagnostics.pdf'), 'ContentType', 'vector');
end
