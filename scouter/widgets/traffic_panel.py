from textual.widgets import Static
from rich.panel import Panel
from rich.text import Text

class TrafficPanel(Static):
    """A widget to show processing logs."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages = [Text("Ready for inspection...", style="dim")]

    def log_activity(self, message: str, style: str = "white") -> None:
        self.messages.append(Text(f"> {message}", style=style))
        if len(self.messages) > 15:
            self.messages.pop(1) # Keep "Ready" or just pop first
        self.refresh_display()

    def on_mount(self) -> None:
        self.refresh_display()

    def refresh_display(self) -> None:
        content = Text.assemble(*(m + "\n" for m in self.messages))
        self.update(Panel(content, title="[bold]Live Traffic Log[/]"))
