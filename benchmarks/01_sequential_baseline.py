import pandas as pd
import time
from rich.console import Console
from rich.table import Table
import os

# Configuration
DATASET_PATH = r'DATASET/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv'
LABEL_COLUMN = ' Label'
DDOS_LABELS = {'DDoS', 'DoS slowloris', 'DoS Slowhttptest', 'DoS Hulk', 'DoS GoldenEye'}

console = Console()

def run_sequential_benchmark():
    if not os.path.exists(DATASET_PATH):
        console.print(f"[bold red]Error:[/] Dataset not found at {DATASET_PATH}")
        return

    console.print(f"\n🐢 [bold yellow]Starting Sequential Benchmark (Base Form)[/]")
    console.print(f"File: [cyan]{DATASET_PATH}[/]")
    
    start_time = time.perf_counter()
    
    # Read entire file at once (Single core)
    df = pd.read_csv(DATASET_PATH, low_memory=False)
    
    # Filtering logic
    label_counts = df[LABEL_COLUMN].value_counts().to_dict()
    
    total_ddos = sum(count for label, count in label_counts.items() 
                     if label.strip() in DDOS_LABELS)
    total_benign = label_counts.get('BENIGN', 0)
    total_rows = len(df)
    
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    
    # Results visualization
    table = Table(title="🐢 Sequential Benchmark Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("🔴 DDoS Attacks", f"{total_ddos:,}")
    table.add_row("🟢 Benign Traffic", f"{total_benign:,}")
    table.add_row("📊 Total Rows", f"{total_rows:,}")
    table.add_row("⏱️ Execution Time", f"{elapsed:.3f}s")
    table.add_row("🚀 Speed", f"{total_rows/elapsed:,.0f} rows/sec")
    
    console.print(table)

if __name__ == "__main__":
    run_sequential_benchmark()
