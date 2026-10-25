# same B&B core as bnb60.py, but takes (i,w) lumps directly so synthetic controls can be fed in
import json, sys, time
from math import gcd
from fractions import Fraction as F
import numpy as np
sys.path.insert(0,'/home/exedev/MathDyad/erdos203/lines'); import linelemma as LL
exec(open('/tmp/ref203lines/bnb_core.py').read())
