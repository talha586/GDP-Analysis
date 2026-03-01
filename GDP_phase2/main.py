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


def bootstrap():
    config     = load_config()
    input_key  = config.get("input",  "excel").lower()
    output_key = config.get("output", "charts").lower()
    data_path  = config.get("data_path", "data/gdp_with_continent_filled.xlsx")

    if input_key not in INPUT_DRIVERS:
        print(f"Unknown input driver '{input_key}'. Available: {list(INPUT_DRIVERS.keys())}")
        sys.exit(1)

    if output_key not in OUTPUT_DRIVERS:
        print(f"Unknown output driver '{output_key}'. Available: {list(OUTPUT_DRIVERS.keys())}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  GDP Analysis System — Phase 2")
    print("=" * 60)
    print(f"  Continent    : {config.get('continent')}")
    print(f"  Year Range   : {config.get('start_year')} – {config.get('end_year')}")
    print(f"  Input Driver : {input_key}")
    print(f"  Output Driver: {output_key}")
    print(f"  Data File    : {data_path}")
    print("=" * 60 + "\n")

    sink   = OUTPUT_DRIVERS[output_key]()
    engine = TransformationEngine(sink=sink, config=config)
    reader = INPUT_DRIVERS[input_key](service=engine, filepath=data_path)

    reader.run()
    print("\nPipeline complete.")


if __name__ == "__main__":
    bootstrap()
