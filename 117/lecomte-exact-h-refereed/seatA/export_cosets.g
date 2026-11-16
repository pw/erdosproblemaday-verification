# export, for a group U, all right cosets of all subgroups as sorted index lists (elements of AsSSortedList(U))
ExportCosets := function(U, fn)
  local els, out, H, x, cs;
  els := AsSSortedList(U);
  out := OutputTextFile(fn, false); SetPrintFormattingStatus(out, false);
  AppendTo(out, Size(U), " ", PrimePGroup(U), "\n");
  for H in AllSubgroups(U) do
    for x in RightTransversal(U, H) do
      cs := List(AsList(RightCoset(H, x)), y -> PositionSorted(els, y));
      AppendTo(out, Size(H), " ", Set(cs), "\n");
    od;
  od;
  CloseStream(out);
end;
for pr in [[8,"all"],[16,"all"],[27,"all"],[9,"all"],[25,"all"],[32,"all"],[81,"all"],[125,"all"]] do
  ids := pr[2]; if ids = "all" then ids := [1..NrSmallGroups(pr[1])]; fi;
  for id in ids do
    ExportCosets(SmallGroup(pr[1], id), Concatenation("/tmp/p117A/l44/c_", String(pr[1]), "_", String(id), ".txt"));
  od;
od;
QUIT;
