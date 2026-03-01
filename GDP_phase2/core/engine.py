from typing import List, Any
from core.contracts import DataSink


def _to_float(val):
    try:
        v = float(val)
        return 0.0 if v != v else v
    except (TypeError, ValueError):
        return 0.0
