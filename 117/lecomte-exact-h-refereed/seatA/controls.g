Read("/home/exedev/MathDyad/subs-1116/117/seatA/survey.g");
f := "/tmp/p117A/controls.txt";
PrintTo(f, "");
out := OutputTextFile(f, true); SetPrintFormattingStatus(out, false);
L := [ ["S3", SmallGroup(6,1)], ["A4", SmallGroup(12,3)], ["D8", SmallGroup(8,3)],
       ["E27", ExtraspecialGroup(27,3)], ["E125", ExtraspecialGroup(125,5)],
       ["E243", ExtraspecialGroup(243,3)], ["E243b", ExtraspecialGroup(243,9)],
       ["E32p", ExtraspecialGroup(32,"+")], ["E128p", ExtraspecialGroup(128,"+")],
       ["UT3F4", Image(IsomorphismPcGroup(Group(List([ [[1,Z(4),0],[0,1,0],[0,0,1]], [[1,Z(4)^2,0],[0,1,0],[0,0,1]], [[1,0,0],[0,1,Z(4)],[0,0,1]], [[1,0,0],[0,1,Z(4)^2],[0,0,1]] ], m -> m*One(GF(4))))))] ];
i := 0;
for pr in L do
  i := i + 1;
  G := pr[2];
  if not IsPcGroup(G) then G := Image(IsomorphismPcGroup(G)); fi;
  Print(pr[1], " order ", Size(G), " id ", IdGroup(G), "\n");
  WriteGroup(out, G, Size(G), i);
od;
CloseStream(out);
QUIT;
