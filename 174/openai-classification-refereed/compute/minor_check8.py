from minor_check import verdict
for S in [(0, 1, 2, 4, 5, 6, 9, 11), (0, 1, 2, 4, 6, 7, 8, 10), (0, 1, 4, 7, 8, 9, 10, 11), (0, 1, 5, 6, 8, 9, 10, 11), (0, 2, 4, 6, 8, 9, 10, 11)]:
    verdict(S, f"k=8 census FAILS {S}")
