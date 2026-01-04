from textual.widgets import Static
from rich.panel import Panel
from rich.table import Table

class AttackCounter(Static):
    """A widget to display real-time attack statistics."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ddos = 0
        self.benign = 0
        self.total = 0

    def on_mount(self) -> None:
        self.refresh_display()

    def update_stats(self, ddos: int, benign: int, total: int) -> None:
        self.ddos += ddos
        self.benign += benign
        self.total += total
        self.refresh_display()

    def refresh_display(self) -> None:
        table = Table.grid(expand=True)
        table.add_column(style="bold red")
        table.add_column(justify="right")
        
        table.add_row("🔴 DDoS Attacks", f"{self.ddos:,}")
        table.add_row("🟢 Benign Traffic", f"{self.benign:,}")
        table.add_row("📊 Total Packets", f"{self.total:,}")
        
        perc = (self.ddos / self.total * 100) if self.total > 0 else 0
        table.add_row("⚠️ Threat Level", f"[bold yellow]{perc:.1f}%[/]")

        self.update(Panel(table, title="[bold white]Scouter Analysis[/]", border_style="red" if perc > 10 else "green"))
