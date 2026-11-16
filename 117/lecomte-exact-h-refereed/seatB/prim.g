# Primitive solvable affine groups Q = V : L with L nilpotent nonabelian (Section 6.6), plus checks of
# sum_{c in L\1} |U_c| <= 2|L|-1 for m=9 and the fixed-point structure; exports Q for omega/a.
Read("export2.g");
out := OpenOut("prim.dat");
AffineGroupFromMatrices := function(L, p, d)
  local gens, V, mats, G;
  # build V:L as a permutation group on F_p^d
  V := Elements(GF(p)^d);
  gens := Concatenation(List(GeneratorsOfGroup(L), g -> PermList(List(V, v -> Position(V, v*g)))),
           List(IdentityMat(d, GF(p)), b -> PermList(List(V, v -> Position(V, v + b)))));
  return Group(gens);
end;
for pd in [[3,2],[5,2],[7,2]] do
  p := pd[1]; d := pd[2];
  GL_ := GL(d, p);
  cls := List(ConjugacyClassesSubgroups(GL_), Representative);
  for L in cls do
    if IsNilpotentGroup(L) and not IsAbelian(L) and Gcd(Size(L), p) = 1 and
       MTX.IsIrreducible(GModuleByMats(GeneratorsOfGroup(L), GF(p))) then
      Q := AffineGroupFromMatrices(L, p, d);
      # sum over c in L\{1} of |U_c| = |ker(1-c)|
      s := Sum(Filtered(Elements(L), c -> not IsOne(c)), c -> p^(d - RankMat(c - One(c))));
      tag := Concatenation("m=", String(p^d), " |L|=", String(Size(L)), " L=", StructureDescription(L),
                           " sumUc=", String(s), " 2|L|-1=", String(2*Size(L)-1), " omegaL=?");
      Print(tag, "\n");
      if p^d <= 49 then ExportGroupTag(Q, Concatenation("prim_", String(p), "_", String(d), "_", String(Size(L))), ReplacedString(tag, " ", ";"), out); fi;
    fi;
  od;
od;
CloseStream(out);
QUIT;
