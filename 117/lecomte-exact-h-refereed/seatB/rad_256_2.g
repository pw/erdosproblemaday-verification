OUTFILE := "rad_256_2.txt";
ORDERS := [256];
IDS := n -> Filtered([28047..42069], i -> Size(Centre(SmallGroup(256,i))) <= 4);
Read("radicals.g");
out := OutputTextFile(OUTFILE, false); SetPrintFormattingStatus(out, false);
for n in ORDERS do
  for i in IDS(n) do
    P := SmallGroup(n, i);
    if not IsAbelian(P) then
      rd := RadicalData(P);
      hyp := ForAll(rd, x -> x[2]) and ForAll(rd, x -> x[1] >= 4) and ForAny(rd, x -> not x[3]);
      WriteAll(out, Concatenation(String(n), "_", String(i), " z=", String(Index(P, Centre(P))),
        " hyp51=", String(hyp), " forms=", String(Length(rd)), " data=",
        ReplacedString(String(rd), " ", ""), "\n"));
    fi;
  od;
od;
CloseStream(out);
QUIT;
