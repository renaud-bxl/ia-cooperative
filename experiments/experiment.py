import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np, json, platform
from pathlib import Path

def run_case(W, X, bits, center=False):
    m,d=W.shape
    qmax=2**(bits-1)-1
    anchor=W.mean(axis=0) if center else np.zeros(d)
    target=W-anchor
    scales=np.max(np.abs(target),axis=1)/qmax
    scales=np.where(scales==0,1.0,scales)
    coarse=np.rint(target/scales[:,None])*scales[:,None]
    radius=np.linalg.norm(target-coarse,axis=1)
    stats=[]
    for x in X:
        score=coarse@x
        bound=radius*np.linalg.norm(x)+1e-10
        upper=score+bound
        j=int(np.argmax(score)); best=float((W[j]-anchor)@x)
        exact_id=j; fetched=1
        for i in np.argsort(-upper,kind='stable'):
            if upper[i] < best: break
            if i==j: continue
            val=float((W[i]-anchor)@x); fetched+=1
            if val>best or (val==best and i<exact_id):
                best=val; exact_id=int(i)
        reference=int(np.argmax(W@x))
        logical_bytes=m*d*bits/8 + m*16 + (d*8 if center else 0) + fetched*d*4
        stats.append([fetched/m,logical_bytes/(m*d*4),int(exact_id!=reference),int(j!=reference)])
    return np.array(stats)

results=[]
for kind in ['independent','aligned','correlated','correlated_centered']:
    for bits in [2,3,4,8]:
        samples=[]
        for seed in [17,29,43,71]:
            rng=np.random.default_rng(seed)
            W=rng.normal(size=(512,256))/16
            if kind.startswith('correlated'): W=rng.normal(size=(1,256))/16+0.025*W
            W=W.astype(np.float32).astype(np.float64)
            X=rng.normal(size=(200,256))
            if kind=='aligned':
                ids=rng.integers(0,512,size=200)
                X=8*W[ids]+0.20*X
            samples.append(run_case(W,X,bits,center=kind.endswith("_centered")))
        a=np.concatenate(samples)
        results.append(dict(case=kind,bits=bits,n=len(a),refined_fraction=float(a[:,0].mean()),refined_p95=float(np.quantile(a[:,0],.95)),read_ratio=float(a[:,1].mean()),mismatches=int(a[:,2].sum()),coarse_mismatch_rate=float(a[:,3].mean())))
result=dict(description='Synthetic argmax only; numerical simulation, no LLM or physical memory benchmark',matrix=[512,256],queries_per_case_and_bits=800,seeds=[17,29,43,71],dtype_reference='FP32 weights, FP64 arithmetic',numpy=np.__version__,python=platform.python_version(),results=results)
Path('tmp/pdfs/results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
