import csv
import time
import multiprocessing


# ── Type casting helper 

def _cast(value: str, data_type: str):
    """Casts a raw string value to the correct Python primitive based on schema."""
    try:
        if data_type == "integer":
            return int(float(value))
        elif data_type == "float":
            return float(value)
        else:
            return str(value).strip()
    except (ValueError, TypeError):
        return None
