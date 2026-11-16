Read("sharp/f9_table.txt");
# right regular representation: g -> (x -> x*g)
gens := List([1..243], g -> PermList(List([1..243], x -> F9TABLE[x][g])));
G := Group(gens);
Print("F9 trace model group: order ", Size(G), " centre ", Size(Centre(G)), " exponent ", Exponent(G),
      " IdGroup ", IdGroup(G), " (ExtraspecialGroup(243,3) has IdGroup ", IdGroup(ExtraspecialGroup(243,3)), ")\n");
QUIT;
