
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

    def on_update(self, telemetry_data: dict):
        """Called by PipelineTelemetry whenever notify() is triggered."""
        self._raw_q_size       = telemetry_data.get("raw_queue_size", 0)
        self._processed_q_size = telemetry_data.get("processed_queue_size", 0)

    def _get_status_color(self, size: int) -> str:
        """Logic for color-coded warnings (Green, Yellow, Red)."""
        ratio = size / max(self._max_size, 1)
        if ratio < 0.4:  return "#2ecc71" # Green (Flowing)
        if ratio < 0.75: return "#f1c40f" # Yellow (Filling)
        return "#e74c3c"                  # Red (Backpressure)

    def run(self):
        # Configuration setup
        plt.rcParams['figure.facecolor'] = 'white'
        val_cfg = next(c for c in self._charts if c["type"] == "real_time_line_graph_values")
        avg_cfg = next(c for c in self._charts if c["type"] == "real_time_line_graph_average")

        fig, (ax_tel, ax_val, ax_avg) = plt.subplots(3, 1, figsize=(11, 9))
        fig.suptitle("GENERIC CONCURRENT PIPELINE — TELEMETRY DASHBOARD", fontsize=12, fontweight="bold")

        def _animate(_frame):
            # Pull all available results from the Aggregator
            while True:
                try:
                    packet = self._output_queue.get_nowait()
                    if packet is None:
                        plt.close()
                        return
                    self._x_values.append(packet.get(val_cfg["x_axis"], 0))
                    self._y_values.append(packet.get(val_cfg["y_axis"], 0))
                    self._y_averages.append(packet.get(avg_cfg["y_axis"], 0))
                except queue.Empty:
                    break

            # Trigger the Subject to notify us of the latest queue sizes
            self._telemetry.notify()

            # --- Panel 1: Queue Telemetry (The Monitor) ---
            ax_tel.cla()
            ax_tel.set_title("System Backpressure Monitor", loc='left', fontsize=10, fontweight="bold")
            ax_tel.set_xlim(0, self._max_size)
            ax_tel.set_yticks([0, 1])
            ax_tel.set_yticklabels(["Processed Q", "Raw Q"])
            
            # Background bars
            ax_tel.barh([0, 1], [self._max_size, self._max_size], color="#f5f5f5", height=0.6)
            # Active telemetry bars
            ax_tel.barh(1, self._raw_q_size, color=self._get_status_color(self._raw_q_size), height=0.6)
            ax_tel.barh(0, self._processed_q_size, color=self._get_status_color(self._processed_q_size), height=0.6)
            ax_tel.set_xlabel(f"Queue Capacity (Max: {self._max_size})", fontsize=8)

            # --- Panel 2: Live Results (Line Graph) ---
            ax_val.cla()
            ax_val.set_title(val_cfg["title"], loc='left', fontsize=10, color="#2ecc71")
            if self._x_values:
                ax_val.plot(list(self._x_values), list(self._y_values), color="#2ecc71", linewidth=2)
                ax_val.fill_between(range(len(self._y_values)), list(self._y_values), alpha=0.1, color="#2ecc71")
            ax_val.grid(True, alpha=0.3)

            # --- Panel 3: Running Average (Line Graph) ---
            ax_avg.cla()
            ax_avg.set_title(avg_cfg["title"], loc='left', fontsize=10, color="#3498db")
            if self._x_values:
                ax_avg.plot(list(self._x_values), list(self._y_averages), color="#3498db", linewidth=2)
                ax_avg.fill_between(range(len(self._y_averages)), list(self._y_averages), alpha=0.1, color="#3498db")
            ax_avg.set_xlabel(avg_cfg["x_axis"], fontsize=8)
            ax_avg.grid(True, alpha=0.3)

            plt.tight_layout(rect=[0, 0, 1, 0.95])

        ani = animation.FuncAnimation(fig, _animate, interval=100, cache_frame_data=False)
        plt.show()

