Read("export.g");
ExportGroupTag := function(G, label, tag, stream)
  local Z, hom, Q, els, reps, n, i, C, lst, idpos;
  Z := Centre(G);
  hom := NaturalHomomorphismByNormalSubgroupNC(G, Z);
  Q := Image(hom);
  els := AsSSortedList(Q);
  n := Length(els);
  reps := List(els, q -> PreImagesRepresentative(hom, q));
  WriteAll(stream, Concatenation("G ", label, " ", String(n), " ", String(Size(G)), " ", tag, "\n"));
  for i in [1..n] do
    C := Centralizer(G, reps[i]);
    lst := List(AsSSortedList(Image(hom, C)), q -> PositionSorted(els, q));
    WriteAll(stream, Concatenation(String(i), " ", JoinStringsWithSeparator(List(lst, String), " "), "\n"));
  od;
  idpos := PositionSorted(els, One(Q));
  WriteAll(stream, Concatenation("ID ", String(idpos), "\n"));
end;
