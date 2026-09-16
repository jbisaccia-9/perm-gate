"""CLI:  python -m permgate gate [permission|prompt] | suite"""
import sys
from .gate import check

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "suite":
        from .btsuite import run_local
        sys.exit(run_local())
    if args and args[0] == "live":
        from .live import check_live
        try:
            sys.exit(check_live(model=args[1] if len(args) > 1 else None))
        except RuntimeError as exc:
            print(f"LIVE BASELINE: {exc}", file=sys.stderr)
            sys.exit(2)
    mode = args[1] if len(args) > 1 and args[0] == "gate" else (args[0] if args else "permission")
    if mode == "gate":
        mode = "permission"
    sys.exit(check(mode))
