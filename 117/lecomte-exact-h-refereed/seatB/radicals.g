# For 2-groups P: enumerate scalar commutator forms via kernels K (index-2 subgroups of P' containing
# gamma3(P)); radical R_K = preimage of Z(P/K).  Report per group: list of (d=log2[P:R], abelian?, central?,
# max fibre width if R abelian) and flag the Lemma 5.1 hypothesis set:
#   all radicals abelian, all ranks >= 4, some radical noncentral.
RadicalData := function(P)
  local D, g3, Ks, res, K, hom, R, d, ab, cen, wmax, T, t, Z;
  D := DerivedSubgroup(P);
  if Size(D) = 1 then return fail; fi;
  g3 := CommutatorSubgroup(D, P);
  Z := Centre(P);
  hom := NaturalHomomorphismByNormalSubgroupNC(D, g3);
  Ks := List(MaximalSubgroups(Image(hom)), M -> PreImage(hom, M));
  Ks := Filtered(Ks, M -> Index(D, M) = 2);
  res := [];
  for K in Ks do
    hom := NaturalHomomorphismByNormalSubgroupNC(P, K);
    R := PreImage(hom, Centre(Image(hom)));
    d := LogInt(Index(P, R), 2);
    ab := IsAbelian(R);
    cen := (Size(R) = Size(Z));
    wmax := -1;
    if ab and not cen then
      T := RightTransversal(P, R);
      wmax := Maximum(List(T, t -> Index(R, Centralizer(R, t))));
    fi;
    Add(res, [d, ab, cen, wmax]);
  od;
  return res;
end;
