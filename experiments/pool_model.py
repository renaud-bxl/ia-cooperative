import json
from pathlib import Path
mix=[(100,8),(400,16),(300,32),(150,64),(50,128)]
physical=sum(n*g for n,g in mix)
out={'mix':[{'users':n,'RAM_GB':g,'quota20_GB':g*.2,'offered_GB':n*g*.2} for n,g in mix], 'raw_GB':physical*.2, 'sensitivity':[]}
for online in [.2,.4,.7]:
  for replicas in [1,2,3]:
    out['sensitivity'].append({'online':online,'replicas':replicas,'useful_GB':physical*.2*online*.8/replicas})
Path('tmp/pdfs/pool_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
