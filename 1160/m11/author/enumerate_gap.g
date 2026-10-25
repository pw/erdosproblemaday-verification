for n in [1..2047] do
    if NumberSmallGroupsAvailable(n) then
        Print(n, " ", NumberSmallGroups(n), "\n");
    fi;
od;
QUIT;
