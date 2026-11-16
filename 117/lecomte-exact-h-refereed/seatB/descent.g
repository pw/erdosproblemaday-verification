# Lemma 6.2 check data: for nonnilpotent G, r_min = min |x^G| over x notin F(G), and
# idx = min over x notin F(G) with |x^G| = r, y in x^G with <x,y> nonnilpotent, of [G : C_G(<x,y>)],
# restricted to the x of smallest class size (as in the proof).  Output: label rmin idx
out := OutputTextFile("descent.txt", false); SetPrintFormattingStatus(out, false);
for n in [6..255] do
  for i in [1..NrSmallGroups(n)] do
    G := SmallGroup(n, i);
    if not IsNilpotentGroup(G) then
      F := FittingSubgroup(G);
      cls := Filtered(ConjugacyClasses(G), c -> not Representative(c) in F);
      rmin := Minimum(List(cls, Size));
      best := infinity;
      for c in Filtered(cls, c -> Size(c) = rmin) do
        x := Representative(c);
        for y in AsList(c) do
          L := Subgroup(G, [x, y]);
          if not IsNilpotentGroup(L) then
            best := Minimum(best, Index(G, Centralizer(G, L)));
          fi;
        od;
      od;
      WriteAll(out, Concatenation(String(n), "_", String(i), " ", String(rmin), " ", String(best), "\n"));
    fi;
  od;
od;
CloseStream(out);
QUIT;
