import argparse, json, sys
from pathlib import Path
from .policy import quota_bytes, gb
from .planner import plan

def main(argv=None):
    parser=argparse.ArgumentParser(description="Coopérative IA : outils de recherche hors ligne")
    sub=parser.add_subparsers(dest="command",required=True)
    q=sub.add_parser("quota",help="Budget théorique, sans allocation")
    q.add_argument("--installed-gb",required=True);q.add_argument("--available-gb",required=True)
    q.add_argument("--reserve-gb",default="2");q.add_argument("--percent",default="20")
    q.add_argument("--cap-gb")
    p=sub.add_parser("plan",help="Plan de couches estimées, sans exécution")
    p.add_argument("config",type=Path)
    args=parser.parse_args(argv)
    try:
        if args.command=="quota":
            b=quota_bytes(gb(args.installed_gb),gb(args.available_gb),gb(args.reserve_gb),args.percent,
                          gb(args.cap_gb) if args.cap_gb is not None else None)
            result={"status":"planning_estimate","quota_bytes":b,"quota_gb":b/1e9,"enforced":False}
        else:
            result=plan(json.loads(args.config.read_text(encoding="utf-8")))
        print(json.dumps(result,indent=2,ensure_ascii=False))
        return 0 if result.get("feasible",True) else 2
    except (ValueError,KeyError,TypeError,OSError) as exc:
        parser.error(str(exc))

if __name__=="__main__":
    sys.exit(main())
