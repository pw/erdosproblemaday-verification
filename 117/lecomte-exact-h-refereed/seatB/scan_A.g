OUTFILE := "scan_A.dat";
ORDERS := [1..127];
Read("export2.g");
out := OpenOut(OUTFILE);
for n in ORDERS do
  for i in [1..NrSmallGroups(n)] do
    G := SmallGroup(n, i);
    if not IsAbelian(G) then
      # tag: nilpotent / solvable / |G'| / exponent of G/Z
      tag := Concatenation("nil=", String(IsNilpotentGroup(G)), " sol=", String(IsSolvableGroup(G)),
                          " dG=", String(Size(DerivedSubgroup(G))));
      ExportGroupTag(G, Concatenation(String(n), "_", String(i)), tag, out);
    fi;
  od;
od;
CloseStream(out);
QUIT;
