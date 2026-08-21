"""CLI:  python -m permgate gate [permission|prompt]"""
import sys
from .gate import check

if __name__ == "__main__":
    mode = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "gate" else \
           (sys.argv[1] if len(sys.argv) > 1 else "permission")
    if mode == "gate":
        mode = "permission"
    sys.exit(check(mode))
