import Bridge986Main
-- must FAIL: the library does not reach s = 3 (PrimeConstruction 2); main_ge4 needs 4 ≤ s.
example : Bridge986.FC.Erdos986At 3 := Bridge986.erdos986At_of_mainBounds 3 (Bridge986.main_ge4 3 (by norm_num)).1
