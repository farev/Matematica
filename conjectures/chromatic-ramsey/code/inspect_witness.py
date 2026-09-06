import sys, collections, itertools
fn=sys.argv[1]; k=int(sys.argv[2])
verts=set(); col={}
for l in open(fn):
    parts=l.strip().rsplit(' ',1); c=int(parts[1]); a,b=parts[0].split(') (')
    a=eval(a+')'); b=eval('('+b); verts.add(a); verts.add(b); col[(a,b)]=c
vs=sorted(verts); print('vertices',len(vs))
for c in range(k):
    layers=collections.Counter(v[c] for v in vs); print(' coordinate',c,'layer sizes',dict(sorted(layers.items())))
deg=collections.Counter()
for (a,b),c in col.items(): deg[(a,c)]+=1; deg[(b,c)]+=1
for c in range(k): print(' color',c,'edges',sum(1 for v in col.values() if v==c),'degree multiset',sorted(collections.Counter(deg[(v,c)] for v in vs).items()))
first=sum(1 for (a,b),c in col.items() if c==min(i for i in range(k) if a[i]!=b[i])); last=sum(1 for (a,b),c in col.items() if c==max(i for i in range(k) if a[i]!=b[i]))
print(' first-diff colored',first,'last-diff colored',last,'of',len(col))
# lines: points per axis-parallel line
lines=collections.Counter()
for v in vs:
    for c in range(k):
        key=(c, v[:c]+v[c+1:]); lines[key]+=1
print(' points-per-line distribution', sorted(collections.Counter(lines.values()).items()), 'lines total', 3**(k-1)*k)
# planes
if k>=2:
    planes=collections.Counter()
    for v in vs:
        for c1,c2 in itertools.combinations(range(k),2):
            key=(c1,c2,tuple(v[i] for i in range(k) if i not in (c1,c2))); planes[key]+=1
    print(' points-per-plane distribution', sorted(collections.Counter(planes.values()).items()))
print(' missing', sorted(set(itertools.product(range(3),repeat=k))-verts)[:30])
