import time
import threading
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Container, Horizontal, Vertical

from .widgets.cpu_monitor import CPUMonitor
from .widgets.attack_counter import AttackCounter
from .widgets.traffic_panel import TrafficPanel
from .widgets.top_ports import TopPorts
from packethunter.fusion import fusion_engine, fusion_scan_directory
from packethunter.config import DEFAULT_CSV, DATASET_DIR

class ScouterApp(App):
    """Dragon Ball inspired DDoS Detection Dashboard."""
    
    TRAFFIC_LOG_ID = "traffic"
    COUNTER_ID = "counter"
    PORTS_ID = "ports"

    CSS = """
    #main-grid {
        layout: grid;
        grid-size: 3;
        grid-columns: 1fr 1fr 1fr;
        grid-rows: 1fr 2fr;
        padding: 1;
        grid-gutter: 1;
    }
    CPUMonitor {
    }
    AttackCounter {
    }
    TopPorts {
    }
    TrafficPanel {
        column-span: 3;
    }
    """

    TITLE = "🐉 PACKETHUNTER: SCOUTER DASHBOARD"
    SUB_TITLE = "FUSION MODE ACTIVATED"
    BINDINGS = [
        ("q", "quit", "Exit"), 
        ("s", "start", "Single Fusion"),
        ("f", "full_scan", "Full Planet Scan")
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            CPUMonitor(),
            AttackCounter(id=self.COUNTER_ID),
            TopPorts(id=self.PORTS_ID),
            TrafficPanel(id=self.TRAFFIC_LOG_ID),
            id="main-grid"
        )
        yield Footer()

    def action_start(self) -> None:
        """Starts the fusion analysis engine for the default file."""
        self.query_one(f"#{self.TRAFFIC_LOG_ID}").log_activity("Engaging Single Fusion Ops...", style="bold cyan")
        threading.Thread(target=self.run_engine, args=(False,), daemon=True).start()

    def action_full_scan(self) -> None:
        """Analyzes every CSV in the dataset directory."""
        self.query_one(f"#{self.TRAFFIC_LOG_ID}").log_activity("INITIALIZING FULL PLANET SCAN...", style="bold magenta")
        threading.Thread(target=self.run_engine, args=(True,), daemon=True).start()

    def run_engine(self, full_scan: bool = False) -> None:
        start_time = time.perf_counter()
        
        def update_ui(partial_result):
            # Check if it's a status message or data chunk
            if isinstance(partial_result, dict) and partial_result.get('type') == 'status':
                self.call_from_thread(self.query_one(f"#{self.TRAFFIC_LOG_ID}").log_activity, partial_result['msg'], "yellow")
            else:
                self.call_from_thread(self.update_callback, partial_result)

        if full_scan:
            results = fusion_scan_directory(str(DATASET_DIR), progress_callback=update_ui)
            total_rows = sum(r['total'] for r in results)
        else:
            results = fusion_engine(progress_callback=update_ui)
            total_rows = results['total']
        
        elapsed = time.perf_counter() - start_time
        mode = "FULL SCAN" if full_scan else "SINGLE FUSION"
        self.call_from_thread(
            self.query_one(f"#{self.TRAFFIC_LOG_ID}").log_activity, 
            f"{mode} COMPLETE in {elapsed:.2f}s! Total Rows: {total_rows:,}", 
            "bold green"
        )

    def update_callback(self, partial_result):
        counter = self.query_one(f"#{self.COUNTER_ID}")
        counter.update_stats(
            ddos=partial_result['ddos'],
            benign=partial_result['benign'],
            total=partial_result['total']
        )

        ports = self.query_one(f"#{self.PORTS_ID}")
        ports.update_ports(partial_result['top_ports'])
        
        traffic = self.query_one(f"#{self.TRAFFIC_LOG_ID}")
        if partial_result['ddos'] > 0:
            traffic.log_activity(f"DETECTED {partial_result['ddos']} DDoS packets in chunk!", style="red")
        else:
            traffic.log_activity(f"Chunk clear: {partial_result['benign']} benign packets.", style="green")

if __name__ == "__main__":
    app = ScouterApp()
    app.run()
