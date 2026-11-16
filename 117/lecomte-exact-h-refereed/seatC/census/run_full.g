EXPORT_FULL := true;
Read("export.g");
ExportOrders([1..64], "census/exportFULL_le64.txt");
QUIT;
