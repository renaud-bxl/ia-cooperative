import json
from pathlib import Path
out=[]
for nodes in [1,2,4,8,16]:
  for label,oneway,rate in [('LAN',0.0005,1e9/8),('WAN',0.020,100e6/8)]:
    t=0.080
    if nodes>1: t += nodes*oneway + ((nodes-1)*8192+4)/rate
    out.append(dict(nodes=nodes,network=label,serial_compute_ms=80,modeled_tokens_per_second=1/t,modeled_ms_per_token=1000*t))
result=dict(note='Analytical scenarios, not measurements; serial batch=1, fixed total compute, no overlap/speculation',rows=out,model_4GB_transfer_at_100Mbps_s=4e9/(100e6/8),prefill_4096_tokens_4096_hidden_fp16_MiB=4096*4096*2/2**20,availability_8_nodes=.95**8,availability_8_redundant_pairs=(1-.05**2)**8,heat_kWh=.3*2,heat_reused_kWh=.3*2*.8)
Path('tmp/pdfs/network_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
