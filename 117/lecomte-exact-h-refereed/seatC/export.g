# export.g -- for each SmallGroup in ORDERS (set by the caller), write one line:
#   n i z k row_1 ... row_k
# z = [G:Z(G)].  If G is abelian, k = 0.
# Otherwise the noncommuting graph is reduced to its "centraliser classes":
# noncentral elements x,y are twins iff C(x) = C(y) (same open neighbourhood,
# nonadjacent), so omega and chi of the noncommuting graph equal those of the
# twin quotient.  Vertices = distinct centralisers; row_j is a 0/1 string of
# length k, bit l = 1 iff representatives j,l do NOT commute.
# Also written (comment field after '#'): number of nontrivial central cosets.
#
# Commutation is decided on a faithful permutation image for speed; the twin
# classes are computed from the full (z-1)x(z-1) commutation matrix of
# transversal representatives (elements of one Z-coset commute pairwise and have
# equal centralisers, so the coset graph has the same omega/chi).

ExportGroup := function(n, i, out)
  local G, Z, z, T, reps, hom, P, imgs, m, rows, a, b, x, y, keys, cls, k, s, j, l, str, u;
  G := SmallGroup(n, i);
  if IsAbelian(G) then
    WriteAll(out, Concatenation(String(n), " ", String(i), " 1 0 # 0\n"));
    return;
  fi;
  Z := Centre(G);
  z := Index(G, Z);
  T := RightTransversal(G, Z);
  reps := Filtered(List(T), t -> not t in Z);
  m := Length(reps);
  if IsPermGroup(G) then
    imgs := reps;
  else
    hom := IsomorphismPermGroup(G);
    imgs := List(reps, t -> Image(hom, t));
  fi;
  rows := List([1..m], a -> BlistList([1..m], []));
  for a in [1..m] do
    x := imgs[a];
    for b in [a+1..m] do
      y := imgs[b];
      if x*y <> y*x then
        rows[a][b] := true;
        rows[b][a] := true;
      fi;
    od;
  od;
  # twin classes: identical rows <=> identical centraliser
  if IsBound(EXPORT_FULL) and EXPORT_FULL = true then
    cls := [1..m];                                  # control mode: no twin reduction
  else
    keys := Set(rows);
    cls := List(keys, key -> Position(rows, key));   # one representative per class
  fi;
  k := Length(cls);
  str := Concatenation(String(n), " ", String(i), " ", String(z), " ", String(k));
  for j in cls do
    s := List(cls, l -> 0);
    for u in [1..k] do
      if rows[j][cls[u]] then s[u] := 1; fi;
    od;
    Append(str, " ");
    Append(str, Concatenation(List(s, String)));
  od;
  Append(str, Concatenation(" # ", String(m), "\n"));
  WriteAll(out, str);
end;

ExportOrders := function(orders, fname)
  local n, i, t0, out;
  out := OutputTextFile(fname, false);
  SetPrintFormattingStatus(out, false);
  for n in orders do
    t0 := Runtime();
    for i in [1..NrSmallGroups(n)] do
      ExportGroup(n, i, out);
    od;
    Print("order ", n, " groups ", NrSmallGroups(n), " ms ", Runtime()-t0, "\n");
  od;
  CloseStream(out);
end;

ExportRange := function(n, i0, i1, fname)
  local i, t0, out;
  out := OutputTextFile(fname, false);
  SetPrintFormattingStatus(out, false);
  t0 := Runtime();
  for i in [i0..i1] do
    ExportGroup(n, i, out);
    if i mod 2000 = 0 then Print("order ", n, " id ", i, " ms ", Runtime()-t0, "\n"); fi;
  od;
  Print("done order ", n, " ids ", i0, "..", i1, " ms ", Runtime()-t0, "\n");
  CloseStream(out);
end;
