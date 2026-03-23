

import multiprocessing
import queue
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class LiveDashboard:
    """
    The 'Observer' in the Observer Pattern.
    Subscribes to PipelineTelemetry to visualize queue backpressure 
    and renders real-time data charts based on config.json.
    """

    def __init__(self, config: dict, output_queue: multiprocessing.Queue, telemetry):
        self._config       = config
        self._output_queue = output_queue
        self._telemetry    = telemetry

        # Step 1: Subscribe to the telemetry subject (Observer Pattern)
        self._telemetry.subscribe(self)

        self._charts   = config["visualizations"]["data_charts"]
        self._max_size = config["pipeline_dynamics"]["stream_queue_max_size"]

        # Data buffers
        self._x_values   = deque(maxlen=100)
        self._y_values   = deque(maxlen=100)
        self._y_averages = deque(maxlen=100)

        # Telemetry state
        self._raw_q_size       = 0
        self._processed_q_size = 0
