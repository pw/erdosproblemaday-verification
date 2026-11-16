# Export commuting structure of G/Z(G). Writes to an OutputTextFile stream with formatting off.
# Each group: line "G <label> <n> <|G|>" then n lines: "<i> <indices of Q-elements whose lifts commute with lift of i>",
# then "ID <identity index>".
ExportGroup := function(G, label, stream)
  local Z, hom, Q, els, reps, n, i, C, lst, idpos;
  Z := Centre(G);
  hom := NaturalHomomorphismByNormalSubgroupNC(G, Z);
  Q := Image(hom);
  els := AsSSortedList(Q);
  n := Length(els);
  reps := List(els, q -> PreImagesRepresentative(hom, q));
  WriteAll(stream, Concatenation("G ", label, " ", String(n), " ", String(Size(G)), "\n"));
  for i in [1..n] do
    C := Centralizer(G, reps[i]);
    lst := List(AsSSortedList(Image(hom, C)), q -> PositionSorted(els, q));
    WriteAll(stream, Concatenation(String(i), " ", JoinStringsWithSeparator(List(lst, String), " "), "\n"));
  od;
  idpos := PositionSorted(els, One(Q));
  WriteAll(stream, Concatenation("ID ", String(idpos), "\n"));
end;
OpenOut := function(path) local s; s := OutputTextFile(path, false); SetPrintFormattingStatus(s, false); return s; end;
