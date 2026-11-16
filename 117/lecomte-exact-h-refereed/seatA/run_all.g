Read("/home/exedev/MathDyad/subs-1116/117/seatA/survey.g");
WriteGroupNoForms := function(out, G, ord, id)
  local Z, hom, Q, elsQ, reps, rows;
  Z := Centre(G);
  hom := NaturalHomomorphismByNormalSubgroup(G, Z);
  Q := Image(hom);
  elsQ := AsSSortedList(Q);
  reps := List(elsQ, q -> PreImagesRepresentative(hom, q));
  rows := List(reps, x -> List(AsSSortedList(Image(hom, Centralizer(G, x))), q -> PositionSorted(elsQ, q)));
  AppendTo(out, "GROUP ", ord, " ", id, " ", Size(Q), " false 0\n");
  AppendTo(out, "ROWS ", rows, "\n");
  AppendTo(out, "FORMS [ ]\nEND\n");
end;
out := OutputTextFile("/tmp/p117A/data/sall.txt", false); SetPrintFormattingStatus(out, false);
for ord in [2..255] do
  if ord in [16, 32, 64, 81, 128, 243] then continue; fi;
  for id in [1..NrSmallGroups(ord)] do
    G := SmallGroup(ord, id);
    if IsAbelian(G) then continue; fi;
    WriteGroupNoForms(out, G, ord, id);
  od;
od;
CloseStream(out);
Print("done all\n");
QUIT;
