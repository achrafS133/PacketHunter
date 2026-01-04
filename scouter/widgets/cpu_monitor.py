import psutil
from textual.widgets import Static
from textual.app import ComposeResult
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn

class CPUMonitor(Static):
    """A widget to display CPU core utilization."""

    def on_mount(self) -> None:
        self.set_interval(1.0, self.update_cpu)

    def update_cpu(self) -> None:
        cpu_percent = psutil.cpu_percent()
        cores = psutil.cpu_count()
        
        progress = Progress(
            TextColumn("[bold blue]CPU Load"),
            BarColumn(bar_width=None),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        task_id = progress.add_task("cpu", total=100)
        progress.update(task_id, completed=cpu_percent)
        
        self.update(Panel(progress, title=f"[bold]Processor ({cores} Cores)[/]"))

    def compose(self) -> ComposeResult:
        yield Static("Scanning CPU...")
