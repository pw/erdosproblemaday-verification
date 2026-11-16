Read("export2.g");
out := OpenOut("g256b.dat");
for i in [16350,55808,55812,55816,55820,55824,55828,55852,55856,55860,55864,55868,55872,55876] do
  G := SmallGroup(256, i);
  ExportGroupTag(G, Concatenation("256_", String(i)), Concatenation("cls=", String(NilpotencyClassOfGroup(G)), " dG=", String(Size(DerivedSubgroup(G)))), out);
od;
CloseStream(out); QUIT;
