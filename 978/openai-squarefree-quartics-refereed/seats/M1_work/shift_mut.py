# Mutation for the shift check: does D(t)<=1 fail if the ratio window is widened?
for lo, hi in [(0.15, 5), (0.05, 5), (0.15, 20), (0.01, 100)]:
    worst = (0, None)
    for k in range(2, 7):
        for a, b in [(1,0),(0,1),(1,1)]:
            for h in range(2, k+3):
                for i in range(0, 20001):
                    t = lo + (hi-lo)*i/20000
                    f = t/((k+t)**(h-1)*(a+b*t))**(1/h)
                    fp = f*(1/t - (h-1)/h/(k+t) - (b/h)/(a+b*t))
                    D = f + (1-t)*fp
                    if D > worst[0]: worst = (D, (k, a, b, h, round(t,4)))
    print(f"ratio window [{lo},{hi}]: max D = {worst[0]:.5f} at (k,a,b,h,t)={worst[1]}  -> {'FAIL' if worst[0] > 1 else 'pass'}")
