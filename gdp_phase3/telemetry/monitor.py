import multiprocessing


# base class for any observer, must implement on_update
class TelemetryObserver:
    def on_update(self, telemetry_data: dict) -> None:
        raise NotImplementedError


# subject - watches the queues and tells observers whats going on
class PipelineTelemetry:

    def __init__(self, raw_queue: multiprocessing.Queue, processed_queue: multiprocessing.Queue, max_size: int):
        self._raw_queue       = raw_queue
        self._processed_queue = processed_queue
        self._max_size        = max_size
        self._observers       = []  # everyone who wants updates

    def subscribe(self, observer: TelemetryObserver) -> None:
        self._observers.append(observer)  # add to list

    def notify(self) -> None:
        # check queue sizes and send to all observers
        telemetry_data = {
            "raw_queue_size":       self._raw_queue.qsize(),
            "processed_queue_size": self._processed_queue.qsize(),
            "max_size":             self._max_size,
        }
        for observer in self._observers:
            observer.on_update(telemetry_data)
