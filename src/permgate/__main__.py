"""CLI:  python -m permgate gate [permission|prompt] | suite"""
import sys
from .gate import check

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "suite":
        from .btsuite import run_local
        sys.exit(run_local())
    mode = args[1] if len(args) > 1 and args[0] == "gate" else (args[0] if args else "permission")
    if mode == "gate":
        mode = "permission"
    sys.exit(check(mode))
