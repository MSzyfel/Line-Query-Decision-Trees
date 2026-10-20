import runpy,math
b=runpy.run_path('expected-two-phase-explore.py');e=b['explore']
lo,hi=.155,.16
for _ in range(16):
    d1=lo+(hi-lo)*.3819660112501;d2=lo+(hi-lo)*.6180339887499
    r1=e(3512863/1e6,d1);r2=e(3512863/1e6,d2)
    if r1<r2:hi=d2
    else:lo=d1
print('OPT_DELTA',lo,hi)
e(3512863/1e6,(lo+hi)/2)
