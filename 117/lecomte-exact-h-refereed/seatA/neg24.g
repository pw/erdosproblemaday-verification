Read("/home/exedev/MathDyad/subs-1116/117/seatA/lemma24.g");
cntE := 0; cntA := 0; cntF := 0;
for pr in [[8,3],[8,4],[27,3],[6,1],[12,3],[16,3]] do
  G := SmallGroup(pr[1], pr[2]);
  for cls in ConjugacyClassesSubgroups(G) do
    U := Representative(cls); ZU := Centre(U);
    for g in List(RightTransversal(G, U), x -> x^-1) do
      S := List(AsList(U), u -> g*u);
      nc := function(i,j) return not IsOne(Comm(S[i],S[j])); end;
      cl := AllMaxCliques(S, nc); w := Length(cl[1]);
      if IsPGroup(U) and not IsAbelian(U) and w < PrimePGroup(U) + 2 then cntE := cntE + 1; fi;
      for XX in cl do
        CX := Filtered(AsList(U), u -> ForAll(XX, i -> IsOne(Comm(u, S[i]))));
        if Set(CX) <> Set(AsList(ZU)) then cntA := cntA + 1; fi;
      od;
      if Index(U, Intersection(ZU, Centralizer(U, g))) > Factorial(w - 1) then cntF := cntF + 1; fi;
    od;
  od;
  Print(pr, " ", [cntE, cntA, cntF], "\n");
od;
Print("tightened (e) width>=p+2 fails in ", cntE, " cosets; wrong formula U cap C(X)=Z(U) fails in ", cntA,
      " cliques; Tomkinson with (w-1)! fails in ", cntF, " cosets\n");
QUIT;
