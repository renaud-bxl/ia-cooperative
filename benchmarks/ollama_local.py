"""Measure an existing local Ollama model. No download or installation.

Only synthetic public text is sent. Generated text is not saved.
Configure the Ollama SERVER with OLLAMA_NO_CLOUD=1 before running.
"""
import argparse, hashlib, json, platform, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE="http://127.0.0.1:11434"
PROMPT="Explique en français, en quatre phrases, pourquoi le réseau compte pour répartir un calcul entre plusieurs ordinateurs."
FIELDS=("total_duration","load_duration","prompt_eval_count","prompt_eval_cached_count","prompt_eval_duration","eval_count","eval_duration","done_reason")

def consume_stream(lines, clock=time.perf_counter, start=None):
    start=clock() if start is None else start
    ttft=None; first_activity=None; final=None
    for raw in lines:
        if not raw.strip(): continue
        item=json.loads(raw)
        if item.get("error"): raise RuntimeError(item["error"])
        if (item.get("thinking") or item.get("response")) and first_activity is None:
            first_activity=clock()-start
        if item.get("response") and ttft is None: ttft=clock()-start
        if item.get("done") is True:
            final=item;break
    if final is None:
        raise RuntimeError("Incomplete stream: no done=true received")
    result={k:final.get(k) for k in FIELDS}
    duration=result.get("eval_duration")
    count=result.get("eval_count")
    result.update(wall_seconds=clock()-start,first_visible_text_seconds=ttft,
                  first_activity_seconds=first_activity,
                  server_decode_tokens_per_s=(count/(duration/1e9) if isinstance(duration,(float,int)) and duration>0 and isinstance(count,(float,int)) else None))
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--model",required=True,help="Exact name of a model already installed locally")
    p.add_argument("--runs",type=int,default=3)
    p.add_argument("--out",type=Path,default=Path("measurements/ollama.json"))
    a=p.parse_args()
    if not 1<=a.runs<=100: p.error("runs must be between 1 and 100")
    if "cloud" in a.model.lower(): p.error("Cloud-tagged models are outside this benchmark")
    # Disable environment proxies and HTTP redirects, including for loopback.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*args,**kwargs): return None
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    with opener.open(BASE+"/api/tags",timeout=10) as response:
        tags=json.load(response)
    models=[m for m in tags.get("models",[]) if m.get("name")==a.model or m.get("model")==a.model]
    if not models: p.error("Model is not in the local /api/tags list; no automatic download")
    with opener.open(BASE+"/api/version",timeout=10) as response: version=json.load(response)
    payload={"model":a.model,"prompt":PROMPT,"stream":True,"keep_alive":"5m",
             "options":{"temperature":0,"seed":42,"num_predict":64,"num_ctx":2048}}
    rows=[]
    for i in range(a.runs+1):
        req=urllib.request.Request(BASE+"/api/generate",json.dumps(payload).encode(),{"Content-Type":"application/json"})
        start=time.perf_counter()
        with opener.open(req,timeout=120) as response:
            observation=consume_stream(response,start=start)
        observation["phase"]="warmup" if i==0 else "measurement"
        rows.append(observation)
    report=dict(status="local_runtime_observation",created_at=datetime.now(timezone.utc).isoformat(),
                model=a.model,model_digest=models[0].get("digest"),ollama_version=version.get("version"),
                platform=platform.platform(),prompt_sha256=hashlib.sha256(PROMPT.encode()).hexdigest(),
                options=payload["options"],rows=rows,
                note="No RAM/energy measurement; num_predict is a cap, not an exact output length. Server cloud must be disabled separately. Check output quality separately.")
    a.out.parent.mkdir(parents=True,exist_ok=True)
    # Refuse to overwrite a previous observation accidentally.
    with a.out.open("x",encoding="utf-8") as f: json.dump(report,f,indent=2,ensure_ascii=False)
    print(str(a.out))

if __name__=="__main__": main()
