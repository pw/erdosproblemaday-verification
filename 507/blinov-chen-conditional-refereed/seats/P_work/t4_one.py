import sys, time
sys.path.insert(0, '/tmp/oaimath/191b/seats/P_work')
import t4_toy as T
t0 = time.time()
T.report('main toy single (a=3, adversarial zero row-3)', 5, (0, 1, 3), 8, 2, 11,
         [((2, 0, 4), (2, 0, 4), (2, 0, 1))], row3='zero')
print('seconds', round(time.time() - t0, 1))
