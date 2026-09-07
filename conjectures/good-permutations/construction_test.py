import sys
def construction(p):
    a=[1]
    x=p-1
    while x>=2:
        a += [x, x+1]; x -= 2
    return a
def bad_blocks(a, maxreport=5):
    n=len(a); pre=[0]
    for x in a: pre.append(pre[-1]+x)
    bad=[]
    for L in range(2,n):
        for i in range(0,n-L+1):
            if (pre[i+L]-pre[i])%L==0:
                bad.append((i+1,L,(pre[i+L]-pre[i])//L))
                if len(bad)>=maxreport: return bad
    return bad
for p in [7,15,31,63,127,255,511,1023,2047,4095,8191]:
    a=construction(p); assert sorted(a)==list(range(1,p+1))
    b=bad_blocks(a)
    print(p, 'GOOD' if not b else 'BAD', b)
