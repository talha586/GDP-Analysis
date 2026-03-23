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


def bootstrap():
    config      = load_config()
    parallelism = config["pipeline_dynamics"]["core_parallelism"]
    max_size    = config["pipeline_dynamics"]["stream_queue_max_size"]

    print("\n" + "=" * 60)
    print("  Generic Concurrent Real-Time Pipeline — Phase 3")
    print("=" * 60)
    print(f"  Dataset       : {config['dataset_path']}")
    print(f"  Core Workers  : {parallelism}")
    print(f"  Queue Max Size: {max_size}")
    print(f"  Input Delay   : {config['pipeline_dynamics']['input_delay_seconds']}s")
    print("=" * 60 + "\n")

    # ── Step 1: Create bounded queues (the two data streams) 
    raw_queue       = multiprocessing.Queue(maxsize=max_size)   # Input  → Core
    processed_queue = multiprocessing.Queue(maxsize=max_size)   # Core   → Aggregator
    output_queue    = multiprocessing.Queue()                    # Aggregator → Dashboard

    # ── Step 2: Create telemetry subject (Observer pattern) 
    telemetry = PipelineTelemetry(raw_queue, processed_queue, max_size)

    # ── Step 3: Instantiate all modules (Dependency Injection) 
    reader     = CSVReader(config=config, raw_queue=raw_queue)
    workers    = [CoreWorker(config=config, raw_queue=raw_queue, processed_queue=processed_queue)
                  for _ in range(parallelism)]
    aggregator = Aggregator(config=config, processed_queue=processed_queue,
                            output_queue=output_queue, num_workers=parallelism)
    dashboard  = LiveDashboard(config=config, output_queue=output_queue, telemetry=telemetry)

    # ── Step 4: Wrap in processes 
    producer_process    = multiprocessing.Process(target=reader.run,     name="CSVReader")
    worker_processes    = [multiprocessing.Process(target=w.run,         name=f"CoreWorker-{i}")
                           for i, w in enumerate(workers)]
    aggregator_process  = multiprocessing.Process(target=aggregator.run, name="Aggregator")

    # ── Step 5: Start all background processes 
    producer_process.start()
    for wp in worker_processes:
        wp.start()
    aggregator_process.start()

    print("[main] All processes started. Launching dashboard...\n")

    # ── Step 6: Run dashboard on main process
    dashboard.run()

    # ── Step 7: Wait for all processes to finish
    producer_process.join()
    for wp in worker_processes:
        wp.join()
    aggregator_process.join()

    print("\n[main] Pipeline complete.")


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn", force=True)
    bootstrap()
