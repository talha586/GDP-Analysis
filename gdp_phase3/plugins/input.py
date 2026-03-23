import csv
import time
import multiprocessing


def _cast(value: str, data_type: str):
    try:
        if data_type == "integer":
            return int(float(value))
        elif data_type == "float":
            return float(value)
        else:
            return str(value).strip()
    except (ValueError, TypeError):
        return None

class CSVReader:

    def __init__(self, config: dict, raw_queue: multiprocessing.Queue):
        self._config    = config
        self._raw_queue = raw_queue

    def run(self):
        dataset_path  = self._config["dataset_path"]
        delay         = self._config["pipeline_dynamics"]["input_delay_seconds"]
        schema        = self._config["schema_mapping"]["columns"]
        parallelism   = self._config["pipeline_dynamics"]["core_parallelism"]

        # Build mapping: source column name → (internal name, data type)
        column_map = {
            col["source_name"]: (col["internal_mapping"], col["data_type"])
            for col in schema
        }

        print(f"[CSVReader] Opening '{dataset_path}' with schema mapping:")
        for src, (internal, dtype) in column_map.items():
            print(f"  {src} → {internal} ({dtype})")

        with open(dataset_path, "r", encoding="utf-8") as fh:
            reader  = csv.DictReader(fh)
            count   = 0

            for row in reader:
                packet = {}

                # Map source columns to internal generic names
                for source_name, (internal_name, data_type) in column_map.items():
                    raw_val = row.get(source_name, "")
                    packet[internal_name] = _cast(raw_val, data_type)

                # Push packet into bounded queue (blocks if full = backpressure)
                self._raw_queue.put(packet)
                count += 1

                # Simulate real-time stream speed
                time.sleep(delay)

        # Send one sentinel per worker to shut them all down
        for _ in range(parallelism):
            self._raw_queue.put(None)

        print(f"[CSVReader] Done. Sent {count} packets.")
