D=[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,43,44,45,46,48,50,52,54,63,275,14143068,10457416992];
print("count ", #D, " distinct ", #Set(D)==#D, " min ", vecmin(D), " sorted ", D==vecsort(D));
s=sum(i=1,#D,1/D[i]); print("rational sum = ", s);
L=lcm(D); print("lcm = ", L, " eq claimed ", L==6209352774424800);
print("sum L/d = ", sum(i=1,#D,L/D[i]), " eq L ", sum(i=1,#D,L/D[i])==L);
old=[42,640,337280,1735650,68479214496]; new=[46,275,14143068,10457416992];
print("surgery equal: ", sum(i=1,5,1/old[i])==sum(i=1,4,1/new[i]), " value ", sum(i=1,4,1/new[i]));
print("factor 275 ",factor(275)," 14143068 ",factor(14143068)," 10457416992 ",factor(10457416992));

quit
