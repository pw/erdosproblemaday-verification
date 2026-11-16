# Seat A: brute-force test of Lemma 2.4 (and 2.3, (3)) on small groups.
# For G, every subgroup U (up to conjugacy), every left coset gU, EVERY maximum clique X in gU:
#  (a) U cap C_G(X) = Z(U) cap C_U(g)
#  (b) the sets C_G(x) cap gU (x in X) cover gU irredundantly
#  (c) some x in X has [U : C_U(x)] <= |X|
#  (d) every x in gU has omega(C_U(x)) <= omega(gU)          (checked via clique number of C_U(x))
#  (e) U nonabelian p-group => omega(gU) >= p+1
#  (f) [U : Z(U) cap C_U(g)] <= omega(gU)!   (Tomkinson consequence (3))
#  (g) if x in gU centralizes an abelian A of index I in U then the cover of U costs <= I*omega(gU) (checked
#      as: for every coset uA, [A:C_A(u)] <= omega(gU))

AllMaxCliques := function(S, nc)
  # S: list of elements; nc(i,j) true iff S[i],S[j] do not commute.  Returns list of maximum cliques (index sets).
  local n, best, res, recur;
  n := Length(S); best := 0; res := [];
  recur := function(cl, cand)
    local i, c2;
    if Length(cl) + Length(cand) < best then return; fi;
    if Length(cand) = 0 then
      if Length(cl) > best then best := Length(cl); res := [ShallowCopy(cl)];
      elif Length(cl) = best then Add(res, ShallowCopy(cl)); fi;
      return;
    fi;
    for i in [1..Length(cand)] do
      if Length(cl) + Length(cand) - i + 1 < best then return; fi;
      c2 := Filtered(cand{[i+1..Length(cand)]}, j -> nc(cand[i], j));
      Add(cl, cand[i]);
      recur(cl, c2);
      Remove(cl);
    od;
  end;
  recur([], [1..n]);
  return res;
end;

CliqueNumber := function(S)
  local nc;
  if Length(S) = 0 then return 0; fi;
  nc := function(i, j) return not IsOne(Comm(S[i], S[j])); end;
  return Length(AllMaxCliques(S, nc)[1]);
end;

TestGroup := function(G, tag)
  local cls, U, p, ZU, cosreps, g, S, nc, cl, X, w, CX, target, ok, x, covered, parts, i, idx, A, I, fails, ntests, nclq,
        cand, Ab, u;
  fails := []; ntests := 0; nclq := 0;
  for cls in ConjugacyClassesSubgroups(G) do
    U := Representative(cls);
    ZU := Centre(U);
    cosreps := List(RightTransversal(G, U), x -> x^-1);   # left coset reps g of gU
    for g in cosreps do
      S := List(AsList(U), u -> g * u);
      nc := function(i, j) return not IsOne(Comm(S[i], S[j])); end;
      cl := AllMaxCliques(S, nc);
      w := Length(cl[1]);
      target := Intersection(ZU, Centralizer(U, g));
      ntests := ntests + 1;
      for X in cl do
        nclq := nclq + 1;
        CX := Filtered(AsList(U), u -> ForAll(X, i -> IsOne(Comm(u, S[i]))));
        if Set(CX) <> Set(AsList(target)) then Add(fails, ["a", tag, U, g, X]); fi;
        # (b) cover and irredundancy
        parts := List(X, i -> Filtered([1..Length(S)], k -> IsOne(Comm(S[k], S[i]))));
        if Union(parts) <> [1..Length(S)] then Add(fails, ["b-cover", tag, U, g]); fi;
        for i in [1..Length(X)] do
          if Union(parts{Difference([1..Length(X)], [i])}) = [1..Length(S)] then Add(fails, ["b-irred", tag, U, g]); fi;
        od;
        # (c)
        if not ForAny(X, i -> Index(U, Centralizer(U, S[i])) <= Length(X)) then Add(fails, ["c", tag, U, g]); fi;
      od;
      # (d) for every x in gU
      for x in S do
        if CliqueNumber(AsList(Centralizer(U, x))) > w then Add(fails, ["d", tag, U, g, x]); fi;
      od;
      if IsPGroup(U) and not IsAbelian(U) then
        p := PrimePGroup(U);
        if w < p + 1 then Add(fails, ["e", tag, U, g, w]); fi;
      fi;
      if Index(U, target) > Factorial(w) then Add(fails, ["f", tag, U, g, w]); fi;
      # (g): abelian subgroups A of U centralized by some x in gU
      for Ab in Filtered(List(ConjugacyClassesSubgroups(U), Representative), IsAbelian) do
        if ForAny(S, x -> ForAll(GeneratorsOfGroup(Ab), a -> IsOne(Comm(a, x)))) then
          for u in AsList(U) do
            if Index(Ab, Centralizer(Ab, u)) > w then Add(fails, ["g", tag, U, g, Ab, u]); fi;
          od;
        fi;
      od;
    od;
  od;
  return [ntests, nclq, fails];
end;
