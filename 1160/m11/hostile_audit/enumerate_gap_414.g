Print("# GAP ", GAPInfo.Version, "\n");
Print("# SmallGrp ", PackageInfo("smallgrp")[1].Version, "\n");
for n in [1..2047] do
    if NumberSmallGroupsAvailable(n) then
        Print(n, " ", NumberSmallGroups(n), "\n");
    fi;
od;
QUIT;
