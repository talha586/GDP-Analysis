
import json
import sys
import os

from plugins.inputs  import ExcelReader, JSONReader
from plugins.outputs import ConsoleWriter, GraphicsChartWriter
from core.engine     import TransformationEngine

<<<<<<< HEAD
INPUT_DRIVERS: dict = {
=======
INPUT_DRIVERS = {
>>>>>>> fe075c743bb37d67cd427a33f9d7aed8f72573ef
    "excel": ExcelReader,
    "json":  JSONReader,
}

<<<<<<< HEAD
OUTPUT_DRIVERS: dict = {
=======
OUTPUT_DRIVERS = {
>>>>>>> fe075c743bb37d67cd427a33f9d7aed8f72573ef
    "console": ConsoleWriter,
    "charts":  GraphicsChartWriter,
}

<<<<<<< HEAD
def load_config(path: str = "config.json") -> dict:
    """Parse the configuration file."""
    if not os.path.exists(path):
        print(f"[main] ERROR: config file '{path}' not found.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def bootstrap() -> None:
    """
    Wire the system together using Dependency Injection and run it.

    Wiring order (DIP golden rules):
      Step 1. Instantiate the Sink  (Output)
      Step 2. Instantiate the Core  (inject Sink)
      Step 3. Instantiate the Input (inject Core as PipelineService)
      Step 4. Run the Input source
    """
    config = load_config()

    input_key  = config.get("input",  "excel").lower()
    output_key = config.get("output", "charts").lower()
    data_path  = config.get("data_path", "data/gdp_with_continent_filled.xlsx")

    if input_key not in INPUT_DRIVERS:
        print(f"[main] ERROR: Unknown input driver '{input_key}'. "
              f"Available: {list(INPUT_DRIVERS.keys())}")
        sys.exit(1)

    if output_key not in OUTPUT_DRIVERS:
        print(f"[main] ERROR: Unknown output driver '{output_key}'. "
              f"Available: {list(OUTPUT_DRIVERS.keys())}")
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

    SinkClass   = OUTPUT_DRIVERS[output_key]
    sink        = SinkClass()

    engine      = TransformationEngine(sink=sink, config=config)

    ReaderClass = INPUT_DRIVERS[input_key]
    reader      = ReaderClass(service=engine, filepath=data_path)

    reader.run()

    print("\n[main] Pipeline complete.")


if __name__ == "__main__":
    bootstrap()
=======

def load_config(path="config.json"):
    if not os.path.exists(path):
        print(f"ERROR: config file '{path}' not found.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)
>>>>>>> fe075c743bb37d67cd427a33f9d7aed8f72573ef
