import hashlib
import multiprocessing
from collections import deque


# pure function
def _generate_signature(raw_value_str: str, key: str, iterations: int) -> str:
    password_bytes = key.encode('utf-8')
    salt_bytes     = raw_value_str.encode('utf-8')
    hash_bytes     = hashlib.pbkdf2_hmac(
        hash_name  = 'sha256',
        password   = password_bytes,
        salt       = salt_bytes,
        iterations = iterations
    )
    return hash_bytes.hex()


# checks if packet is real or fake, returns None if fake
def _verify_packet(packet: dict, secret_key: str, iterations: int) -> dict | None:
    raw_value = packet.get("metric_value", 0.0)

    if raw_value is None:
        return None

    try:
        raw_value_str = f"{float(raw_value):.2f}"
    except (TypeError, ValueError):
        return None

    expected_sig = _generate_signature(raw_value_str, secret_key, iterations)
    actual_sig   = packet.get("security_hash", "")

    if expected_sig == actual_sig:
        return packet
    return None  # drop it


# worker that runs in its own process
# pulls from raw_queue, checks signature, sends to processed_queue
class CoreWorker:

    def __init__(self, config: dict, raw_queue: multiprocessing.Queue, processed_queue: multiprocessing.Queue):
        self._config          = config
        self._raw_queue       = raw_queue
        self._processed_queue = processed_queue

    def run(self):
        secret_key = self._config["processing"]["stateless_tasks"]["secret_key"]
        iterations = self._config["processing"]["stateless_tasks"]["iterations"]

        while True:
            packet = self._raw_queue.get()

            if packet is None:  # None means no more data, shut down
                self._processed_queue.put(None)
                break

            verified = _verify_packet(packet, secret_key, iterations)

            if verified:
                self._processed_queue.put(verified)
            else:
                print(f"[CoreWorker] Dropped packet: {packet.get('entity_name')} @ {packet.get('time_period')}")


# pure function, just calculates average of whatever is in the window
def _compute_running_average(window: deque) -> float:
    if not window:
        return 0.0
    return sum(window) / len(window)


# collects verified packets and keeps a running average
# shell = manages the deque (stateful)
# core  = _compute_running_average (pure, no state)
class Aggregator:

    def __init__(self, config: dict, processed_queue: multiprocessing.Queue, output_queue: multiprocessing.Queue, num_workers: int):
        self._config          = config
        self._processed_queue = processed_queue
        self._output_queue    = output_queue
        self._num_workers     = num_workers

    def run(self):
        window_size    = self._config["processing"]["stateful_tasks"]["running_average_window_size"]
        window         = deque(maxlen=window_size)  # only keeps last N values
        sentinels_seen = 0

        while True:
            packet = self._processed_queue.get()

            if packet is None:
                sentinels_seen += 1
                if sentinels_seen >= self._num_workers:  # all workers done
                    self._output_queue.put(None)
                    break
                continue

            window.append(packet["metric_value"])  # imperative shell - update state

            avg = _compute_running_average(window)  # functional core - pure calc

            enriched = dict(packet)
            enriched["computed_metric"] = round(avg, 4)

            self._output_queue.put(enriched)
