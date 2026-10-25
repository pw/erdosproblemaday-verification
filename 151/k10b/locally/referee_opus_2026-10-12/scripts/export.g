out := OutputTextFile("/tmp/ref151/gap/tables.txt", false);;
SetPrintFormattingStatus(out, false);;
for n in [9..41] do
  for i in [1..NumberSmallGroups(n)] do
    G := SmallGroup(n,i);; el := AsSSortedList(G);;
    # identity first
    el := Concatenation([One(G)], Filtered(el, x -> x <> One(G)));;
    T := List(el, x -> List(el, y -> Position(el, x*y) - 1));;
    AppendTo(out, n, " ", i, " ", StructureDescription(G), "\n");
    for row in T do AppendTo(out, JoinStringsWithSeparator(List(row, String), " "), "\n"); od;
  od;
od;
CloseStream(out);
QUIT;
