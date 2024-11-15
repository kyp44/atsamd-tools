import pendulum as pend

f1 = 1_024
t1 = 1 / f1

f2 = 32_768
t2 = 1 / f2

dur = lambda t, n: pend.Duration(seconds=n*t)

dur1 = lambda n: dur(t1, n)
dur2 = lambda n: dur(t2, n)
