[If1,eps1]=newtoncotes(@(x)(2/sqrt(pi)*exp(-x.^2)),0,0.475,1);
disp(sprintf('%0.8f ',If1))
disp(sprintf('%0.8f ',eps1))
[If2,eps2]=newtoncotes(@(x)(2/sqrt(pi)*exp(-x.^2)),0,0.475,2);
disp(sprintf('%0.8f ',If2))
disp(sprintf('%0.8f ',eps2))
[If3,eps3]=newtoncotes(@(x)(2/sqrt(pi)*exp(-x.^2)),0,0.475,4);
disp(sprintf('%0.8f ',If3))
disp(sprintf('%0.8f ',eps3))