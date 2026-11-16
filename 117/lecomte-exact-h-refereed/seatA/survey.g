# Seat A survey: for each group, central-coset commutation data + scalar commutator forms (p-groups).
# Usage: gap -q survey.g  with OUTFILE, ORDERS (list of [order, ids or "all"]) bound beforehand.
# Output lines (one per group):  GROUP <order> <id> <z> <isPgroup> <p>
#   ROWS <list of lists>  : for each central coset i (1-based, identity included), indices of cosets commuting with it
#   FORMS <list of records as lists> [j, Rab, Rcen, m, ZReqZP, fibreLabels, zrIdx]  per scalar form (p-groups)
#   END

WriteGroup := function(out, G, ord, id)
  local Z, hom, Q, elsQ, reps, rows, p, isp, K, L, N1, nat, E, pcE, e, gens, k, cm, i, jj, forms,
        xi, vecs, A, cs, imgs, h, R, rk, Rab, Rcen, ZR, m, ZReq, homR, labs, rcos, zr, v, s, ii, tmp;
  Z := Centre(G);
  hom := NaturalHomomorphismByNormalSubgroup(G, Z);
  Q := Image(hom);
  elsQ := AsSSortedList(Q);
  reps := List(elsQ, q -> PreImagesRepresentative(hom, q));
  rows := List(reps, x -> List(AsSSortedList(Image(hom, Centralizer(G, x))), q -> PositionSorted(elsQ, q)));
  isp := IsPGroup(G);
  if isp and Size(G) > 1 then p := PrimePGroup(G); else p := 0; fi;
  AppendTo(out, "GROUP ", ord, " ", id, " ", Size(Q), " ", isp, " ", p, "\n");
  AppendTo(out, "ROWS ", rows, "\n");
  forms := [];
  if isp and not IsAbelian(G) then
    K := DerivedSubgroup(G);
    L := CommutatorSubgroup(K, G);
    N1 := ClosureGroup(L, Agemo(K, p));
    nat := NaturalHomomorphismByNormalSubgroup(K, N1);
    E := Image(nat);
    pcE := Pcgs(E);
    e := Length(pcE);
    gens := AsList(Pcgs(G));
    k := Length(gens);
    cm := List(gens, x -> List(gens, y -> ExponentsOfPcElement(pcE, Image(nat, Comm(x, y)))));
    A := ElementaryAbelianGroup(p^k);
    cs := AsList(Pcgs(A));
    # normalized nonzero functionals xi on F_p^e
    vecs := Filtered(Tuples([0..p-1], e), t -> ForAny(t, x -> x <> 0) and First(t, x -> x <> 0) = 1);
    for xi in vecs do
      imgs := List([1..k], jj -> Product([1..k], i -> cs[i]^((xi * cm[jj][i]) mod p)));
      h := GroupHomomorphismByImages(G, A, gens, imgs);
      if h = fail then Error("not a homomorphism"); fi;
      R := Kernel(h);
      rk := LogInt(Index(G, R), p);
      Rab := IsAbelian(R);
      Rcen := Size(R) = Size(Z);
      ZR := Centre(R);
      m := LogInt(Index(R, ZR), p);
      ZReq := Size(ZR) = Size(Z);
      # label each central coset by its R-coset: position of image in G/R
      homR := NaturalHomomorphismByNormalSubgroup(G, R);
      tmp := AsSSortedList(Image(homR));
      labs := List(reps, x -> PositionSorted(tmp, Image(homR, x)));
      # for each R-coset label: log_p [Z(R) : C_{Z(R)}(g)]
      zr := List(tmp, t -> LogInt(Index(ZR, Centralizer(ZR, PreImagesRepresentative(homR, t))), p));
      Add(forms, [rk / 2, Rab, Rcen, m, ZReq, labs, zr, xi]);
    od;
  fi;
  AppendTo(out, "FORMS ", forms, "\n");
  AppendTo(out, "END\n");
end;

RunSurvey := function(outfile, ord, ids)
  local out, id, G, t;
  out := OutputTextFile(outfile, true);
  SetPrintFormattingStatus(out, false);
  if ids = "all" then ids := [1..NrSmallGroups(ord)]; fi;
  for id in ids do
    G := SmallGroup(ord, id);
    if IsPcGroup(G) = false then
      G := Image(IsomorphismPcGroup(G));
    fi;
    WriteGroup(out, G, ord, id);
  od;
  CloseStream(out);
end;

RunSurveyAny := function(outfile, ord, ids)
  # for non-solvable groups we cannot use pc groups; forms only for p-groups anyway
  local out, id, G;
  out := OutputTextFile(outfile, true);
  SetPrintFormattingStatus(out, false);
  if ids = "all" then ids := [1..NrSmallGroups(ord)]; fi;
  for id in ids do
    G := SmallGroup(ord, id);
    if IsSolvableGroup(G) then G := Image(IsomorphismPcGroup(G)); fi;
    WriteGroup(out, G, ord, id);
  od;
  CloseStream(out);
end;
