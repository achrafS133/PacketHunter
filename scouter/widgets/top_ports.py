from textual.widgets import Static
from rich.panel import Panel
from rich.table import Table

class TopPorts(Static):
    """A widget to display top targeted ports during DDoS."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ports = {}

    def update_ports(self, port_data: dict) -> None:
        # Merge dictionaries
        for port, count in port_data.items():
            self.ports[port] = self.ports.get(port, 0) + count
        self.refresh_display()

    def on_mount(self) -> None:
        self.refresh_display()

    def refresh_display(self) -> None:
        table = Table.grid(expand=True)
        table.add_column("Port", style="cyan")
        table.add_column("Hits", justify="right", style="bold magenta")
        
        # Sort and take top 5
        sorted_ports = sorted(self.ports.items(), key=lambda x: x[1], reverse=True)[:5]
        
        if not sorted_ports:
            table.add_row("Scanning...", "")
        else:
            for port, count in sorted_ports:
                table.add_row(f"Port {int(port)}", f"{count:,}")

        self.update(Panel(table, title="[bold]Top Target Ports[/]", border_style="blue"))
