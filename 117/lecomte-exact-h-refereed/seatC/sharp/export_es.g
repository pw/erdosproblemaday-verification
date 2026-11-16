# export twin-reduced noncommuting graphs of extraspecial 2-groups 2^{1+2r}, r=2,3,4 (+ and -)
Read("export.g");
ExportGroupObj := function(G, label, out)
  local Z, z, reps, m, imgs, hom, rows, a, b, x, y, keys, cls, k, str, s, u, j;
  Z := Centre(G); z := Index(G, Z);
  reps := Filtered(List(RightTransversal(G, Z)), t -> not t in Z);
  m := Length(reps);
  hom := IsomorphismPermGroup(G);
  imgs := List(reps, t -> Image(hom, t));
  rows := List([1..m], a -> BlistList([1..m], []));
  for a in [1..m] do x := imgs[a];
    for b in [a+1..m] do y := imgs[b];
      if x*y <> y*x then rows[a][b] := true; rows[b][a] := true; fi;
    od;
  od;
  keys := Set(rows); cls := List(keys, key -> Position(rows, key)); k := Length(cls);
  str := Concatenation(label, " ", String(Size(G)), " ", String(z), " ", String(k));
  for j in cls do
    s := List([1..k], u -> 0);
    for u in [1..k] do if rows[j][cls[u]] then s[u] := 1; fi; od;
    Append(str, " "); Append(str, Concatenation(List(s, String)));
  od;
  Append(str, Concatenation(" # ", String(m), "\n"));
  WriteAll(out, str);
end;
out := OutputTextFile("sharp/es_graphs.txt", false);
SetPrintFormattingStatus(out, false);
for r in [2,3,4] do
  for t in ["+","-"] do
    G := ExtraspecialGroup(2^(2*r+1), t);
    Print("r=", r, " type ", t, " order ", Size(G), " centre ", Size(Centre(G)), "\n");
    ExportGroupObj(G, Concatenation("ES2^(1+", String(2*r), ")", t), out);
  od;
od;
G := ExtraspecialGroup(243, 3); ExportGroupObj(G, "ES3^(1+4)exp3", out);
G := ExtraspecialGroup(243, 9); ExportGroupObj(G, "ES3^(1+4)exp9", out);
CloseStream(out);
QUIT;
