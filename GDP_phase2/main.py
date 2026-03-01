import json
import sys
import os

from plugins.inputs  import ExcelReader, JSONReader
from plugins.outputs import ConsoleWriter, GraphicsChartWriter
from core.engine     import TransformationEngine

INPUT_DRIVERS = {
    "excel": ExcelReader,
    "json":  JSONReader,
}

OUTPUT_DRIVERS = {
    "console": ConsoleWriter,
    "charts":  GraphicsChartWriter,
}


def load_config(path="config.json"):
    if not os.path.exists(path):
        print(f"ERROR: config file '{path}' not found.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)
