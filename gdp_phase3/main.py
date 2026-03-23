import json
import sys
import os
import multiprocessing

from plugins.inputs     import CSVReader
from plugins.outputs    import LiveDashboard
from core.engine        import CoreWorker, Aggregator
from telemetry.monitor  import PipelineTelemetry


def load_config(path="config.json"):
    if not os.path.exists(path):
        print(f"ERROR: config file '{path}' not found.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)

