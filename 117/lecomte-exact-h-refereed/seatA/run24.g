Read("/home/exedev/MathDyad/subs-1116/117/seatA/lemma24.g");
tot := [0,0]; allf := [];
for ord in [6, 8, 12, 16, 18, 24, 27, 32] do
  for id in [1..NrSmallGroups(ord)] do
    G := SmallGroup(ord, id);
    if IsAbelian(G) then continue; fi;
    r := TestGroup(G, [ord, id]);
    tot := tot + r{[1,2]};
    Append(allf, r[3]);
    Print([ord,id], " cosets ", r[1], " cliques ", r[2], " fails ", List(r[3], f -> f[1]), "\n");
  od;
  Print("order ", ord, " done; cosets tested ", tot[1], ", max cliques checked ", tot[2], ", failures ", Length(allf), "\n");
od;
QUIT;
