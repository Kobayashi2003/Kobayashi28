Hz = [50 100 120 140 160 180 200 250 300 400 500 1000 2500 5000 10000 20000 50000 100000 150000 200000 300000 400000 500000 700000];
Uo = [2.8 4.867 5.267 5.867 6.267 6.937 7.067 7.667 8.067 8.60 8.86 9.467 9.600 9.733 9.800 9.733 9.733 9.600 9.533 8.933 8.400 7.600 6.00 5.067];

figure(1)

Hz = log10(Hz);
Uo = 20*log10(Uo*1000); 

plot(Hz, Uo, '-')

hold on

fL = 170; fH = 495000;

UL = interp1(Hz, Uo, log10(fL));
UH = interp1(Hz, Uo, log10(fH));

line([log10(fL) log10(fL)], [UL 0], 'Color', 'r', 'LineStyle', '--')
line([log10(fH) log10(fH)], [UH 0], 'Color', 'g', 'LineStyle', '--')
line([0 log10(fL)], [UL UL], 'Color', 'r', 'LineStyle', '--')
line([0 log10(fH)], [UH UH], 'Color', 'g', 'LineStyle', '--')

title('R_{L}=\infty')
xlabel('log10(f)')
ylabel('20*log10(U_{o})')

xlim([1.5 6])
ylim([65 82])

hold off



figure(2)

Uo = [1.867 4.467 5.200 5.733 6.333 6.667 7.000 7.600 8.067 8.60 8.93 9.400  9.607 9.733 9.733 9.733 9.700 9.467 9.400 9.133 8.333 7.267 6.867 5.733];

Uo = 20*log10(Uo*1000);

plot(Hz, Uo, '-')

hold on

fL = 180; fH = 537000;

UL = interp1(Hz, Uo, log10(fL));
UH = interp1(Hz, Uo, log10(fH));

line([log10(fL) log10(fL)], [UL 0], 'Color', 'r', 'LineStyle', '--')
line([log10(fH) log10(fH)], [UH 0], 'Color', 'g', 'LineStyle', '--')

line([0 log10(fL)], [UL UL], 'Color', 'r', 'LineStyle', '--')
line([0 log10(fH)], [UH UH], 'Color', 'g', 'LineStyle', '--')

title('R_{L}=3k')
xlabel('log10(f)')
ylabel('20*log10(U_{o})')

xlim([1.5 6])
ylim([65 82])

hold off

saveas(figure(1), 'RLinf.png')
saveas(figure(2), 'RL3k.png')