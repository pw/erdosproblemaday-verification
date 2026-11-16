EXPORT_FULL := true;
Read("export.g");
out := OutputTextFile("census/exportFULL_sample.txt", false);
SetPrintFormattingStatus(out, false);
L := [];
cnt := 0;
for n in [65..255] do
  for i in [1..NrSmallGroups(n)] do
    cnt := cnt + 1;
    if cnt mod 25 = 0 or [n,i] in [[128,2326],[128,2327],[192,1333],[192,1334],[192,1337],[192,1338],[243,65],[243,66]] then
      ExportGroup(n, i, out);
      Add(L, [n,i]);
    fi;
  od;
od;
CloseStream(out);
Print("exported ", Length(L), " groups\n");
QUIT;
