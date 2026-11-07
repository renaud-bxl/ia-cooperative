"""Reproducible queue simulation; assumptions, NOT measurements of AI hardware.
Python standard library. One active conversation per group; no batching.
Units: seconds, bytes, bit/s. Arrival stream is Poisson, FCFS shared queue.
Weights are warm. Groups in each scenario have identical modeled service.
"""
import json, math, random, statistics, heapq
from pathlib import Path

SEEDS = list(range(100, 120))
REQUESTS = 1000
INPUT_TOKENS, OUTPUT_TOKENS = 512, 64
COMPUTE_TOKEN = 0.080
COMPUTE_PREFILL = 1.280
ACTIVATION_BYTES = 8192

SCENARIOS = [
    dict(id='local_1', name='1 machine locale', groups=1, nodes=1, mbps=0, one_way=0, rate=0.1, faults=False),
    dict(id='lan_4', name='4 machines, réseau local', groups=1, nodes=4, mbps=1000, one_way=.0005, rate=.1, faults=False),
    dict(id='wan_4', name='4 machines, Internet', groups=1, nodes=4, mbps=100, one_way=.020, rate=.1, faults=False),
    dict(id='wan_8', name='8 machines, Internet', groups=1, nodes=8, mbps=100, one_way=.020, rate=.1, faults=False),
    dict(id='wan_4_light', name='4 machines Internet, demande réduite', groups=1, nodes=4, mbps=100, one_way=.020, rate=.04, faults=False),
    dict(id='wan_8_light', name='8 machines Internet, demande réduite', groups=1, nodes=8, mbps=100, one_way=.020, rate=.04, faults=False),
    dict(id='lan_pool', name='8 groupes de 4, réseau local', groups=8, nodes=4, mbps=1000, one_way=.0005, rate=.8, faults=False),
    dict(id='lan_pool_faults', name='Même coopérative, incidents injectés', groups=8, nodes=4, mbps=1000, one_way=.0005, rate=.8, faults=True),
]

def quantile(values, p):
    a=sorted(values); pos=(len(a)-1)*p; i=int(pos)
    return a[i]+(a[min(i+1,len(a)-1)]-a[i])*(pos-i)

def durations(s, compute_factor=1, latency_factor=1):
    prefill=COMPUTE_PREFILL*compute_factor
    step=COMPUTE_TOKEN*compute_factor
    if s['nodes'] > 1:
        n=s['nodes']; bps=s['mbps']*1e6
        prefill += n*s['one_way']*latency_factor + ((n-1)*ACTIVATION_BYTES*INPUT_TOKENS+4)*8/bps
        step += n*s['one_way']*latency_factor + ((n-1)*ACTIVATION_BYTES+4)*8/bps
    return prefill, prefill+(OUTPUT_TOKENS-1)*step

def simulate(s):
    all_latency=[]; all_first=[]; all_wait=[]; all_service=[]
    replica_results=[]; fault_events=0; fault_requests=0
    for seed in SEEDS:
        # Separate RNG streams preserve identical arrivals across comparisons.
        arrivals=random.Random(seed); variation=random.Random(seed+10000)
        faults=random.Random(seed+20000)
        server_heap=[(0.,i) for i in range(s['groups'])]; heapq.heapify(server_heap)
        now=0.; first_arrival=None; latencies=[]; firsts=[]; waits=[]; service_sum=0.
        for _ in range(REQUESTS):
            now += arrivals.expovariate(s['rate'])
            if first_arrival is None: first_arrival=now
            available, server=heapq.heappop(server_heap)
            start=max(available,now); waiting=start-now
            cf=variation.uniform(.9,1.1)
            sigma=math.sqrt(math.log(1+.3**2))
            lf=variation.lognormvariate(-.5*sigma*sigma,sigma)
            first, base_service=durations(s,cf,lf)
            base_first=first
            service=base_service; added=0.; progress=0.; count=0
            if s['faults']:
                # Independent per-node failure hazard of 1/1800 s of ACTIVE work.
                # Failures are not sampled during recovery or while a group is idle.
                # A warm spare replaces the lost stage. Restore entire context as
                # a conservative aggregate proxy, without double output tokens.
                while True:
                    active_until_fault=faults.expovariate(s['nodes']/1800.)
                    progress += active_until_fault
                    if progress >= base_service: break
                    replay=base_first*(1+(OUTPUT_TOKENS/INPUT_TOKENS)*(progress/base_service))
                    recovery=2.+3.+replay
                    added+=recovery; count+=1
                    if progress < base_first: first+=recovery
                service += added
            if count: fault_requests+=1; fault_events+=count
            done=start+service
            heapq.heappush(server_heap,(done,server))
            latencies.append(done-now); firsts.append(waiting+first); waits.append(waiting)
            all_service.append(service); service_sum+=service
        horizon=max(v for v,_ in server_heap)-first_arrival
        replica_results.append(dict(seed=seed, latency_p95=quantile(latencies,.95),
            output_tokens_per_s=REQUESTS*OUTPUT_TOKENS/horizon,
            busy_fraction=service_sum/(s['groups']*horizon)))
        all_latency.extend(latencies); all_first.extend(firsts); all_wait.extend(waits)
    nominal_first,nominal_service=durations(s)
    # Utilization parameter offered load; >=1 means no stationary queue here.
    offered_load=s['rate']*statistics.mean(all_service)/s['groups']
    return dict(**s, requests_simulated=len(all_latency), nominal_first_s=nominal_first,
        nominal_service_s=nominal_service, nominal_isolated_tokens_per_s=OUTPUT_TOKENS/nominal_service,
        offered_load=offered_load, stable_under_assumptions=offered_load<1,
        latency_p50_s=quantile(all_latency,.5), latency_p95_s=quantile(all_latency,.95),
        ttft_p50_s=quantile(all_first,.5), ttft_p95_s=quantile(all_first,.95),
        wait_p50_s=quantile(all_wait,.5), wait_p95_s=quantile(all_wait,.95),
        over_30s_fraction=sum(v>30 for v in all_latency)/len(all_latency),
        output_tokens_per_s_mean=statistics.mean(r['output_tokens_per_s'] for r in replica_results),
        fault_requests=fault_requests, fault_events=fault_events,
        p95_across_replications_min=min(r['latency_p95'] for r in replica_results),
        p95_across_replications_max=max(r['latency_p95'] for r in replica_results),
        replicas=replica_results)

if __name__=='__main__':
    output=dict(status='simulation, not hardware benchmark',
        assumptions=dict(seeds=SEEDS, requests_per_replication=REQUESTS,
            input_tokens=INPUT_TOKENS, output_tokens=OUTPUT_TOKENS,
            total_compute_prefill_seconds=COMPUTE_PREFILL,
            total_compute_decode_seconds_per_token=COMPUTE_TOKEN,
            latency_jitter_cv=.30, compute_uniform_factor=[.9,1.1],
            conversations_per_group=1, batching=False, warm_weights=True,
            failure_mean_active_seconds_per_node=1800, detection_seconds=2,
            warm_replacement_seconds=3, correlated_failures=False,
            recovery_failures=False, shared_uplink_contention=False,
            cold_model_loading=False, stable_queue_warmup_discard=0),
        results=[simulate(s) for s in SCENARIOS])
    p=Path(__file__).with_name('service_results.json')
    p.write_text(json.dumps(output,indent=2,ensure_ascii=False))
    for r in output['results']:
        print(f"{r['id']:16s} isolated={r['nominal_service_s']:.3f}s p50={r['latency_p50_s']:.2f}s p95={r['latency_p95_s']:.2f}s first95={r['ttft_p95_s']:.2f}s load={r['offered_load']:.3f} tok/s={r['output_tokens_per_s_mean']:.2f} failures={r['fault_requests']}")
