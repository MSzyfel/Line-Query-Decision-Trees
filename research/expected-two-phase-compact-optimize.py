import runpy
b=runpy.run_path('expected-two-phase-compact-explore.py');e=b['explore'];lo,hi=.156,.159
for _ in range(14):
 d1=lo+(hi-lo)*.3819660112501;d2=lo+(hi-lo)*.6180339887499
 if e(3512863/1e6,d1)<e(3512863/1e6,d2):hi=d2
 else:lo=d1
print('OPT',lo,hi);e(3512863/1e6,(lo+hi)/2)
