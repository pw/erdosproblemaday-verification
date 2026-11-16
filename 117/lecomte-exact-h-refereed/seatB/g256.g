Read("export2.g");
out := OpenOut("g256.dat");
for i in [298,301,304,307,328,331,338,378,383,388,399,410,413,428,469,472,483,504,507,510,513,516,519,522,14764,14767,14770,14773,15274,15445,15448,16348,16349,16350,16862,16871,16880,16883,16886,16979,16984,16987,53376,53379,53389,53459,54095,54098] do
  G := SmallGroup(256, i);
  ExportGroupTag(G, Concatenation("256_", String(i)), Concatenation("nil=true dG=", String(Size(DerivedSubgroup(G)))), out);
od;
CloseStream(out); QUIT;
