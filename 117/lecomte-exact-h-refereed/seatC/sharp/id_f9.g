Read("sharp/f9_table.txt");
G := GroupByMultiplicationTable(F9TABLE);
Print("F9 trace model group: order ", Size(G), " centre ", Size(Centre(G)), " exponent ", Exponent(G), " IdGroup ", IdGroup(G), " IsomorphicToExtraspecial243_3 ", IdGroup(G) = IdGroup(ExtraspecialGroup(243,3)), "\n");
QUIT;
