import pandas as pd
import time
from multiprocessing import Pool, cpu_count
from rich.console import Console
from rich.table import Table
import os

# Configuration
DATASET_PATH = r'DATASET/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv'
LABEL_COLUMN = ' Label'
DDOS_LABELS = {'DDoS', 'DoS slowloris', 'DoS Slowhttptest', 'DoS Hulk', 'DoS GoldenEye'}
CHUNK_SIZE = 50_000

console = Console()

def _chunk_processor(chunk):
    """Worker function to process a single CSV chunk."""
    label_counts = chunk[LABEL_COLUMN].value_counts().to_dict()
    ddos_count = sum(count for label, count in label_counts.items() 
                     if label.strip() in DDOS_LABELS)
    benign_count = label_counts.get('BENIGN', 0)
    return {
        'ddos': ddos_count,
        'benign': benign_count,
        'rows': len(chunk)
    }

def run_parallel_benchmark():
    if not os.path.exists(DATASET_PATH):
        console.print(f"[bold red]Error:[/] Dataset not found at {DATASET_PATH}")
        return

    n_workers = cpu_count()
    console.print(f"\n🐉 [bold cyan]Starting Parallel Benchmark (Fusion Technique)[/]")
    console.print(f"File: [cyan]{DATASET_PATH}[/]")
    console.print(f"Cores: [bold green]{n_workers}[/]")
    
    start_time = time.perf_counter()
    
    # Map Phase
    chunks = pd.read_csv(DATASET_PATH, chunksize=CHUNK_SIZE, low_memory=False, usecols=[LABEL_COLUMN])
    
    with Pool(processes=n_workers) as pool:
        partial_results = list(pool.imap_unordered(_chunk_processor, chunks))
    
    # Reduce Phase
    total_ddos = sum(r['ddos'] for r in partial_results)
    total_benign = sum(r['benign'] for r in partial_results)
    total_rows = sum(r['rows'] for r in partial_results)
    
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    
    # Results visualization
    table = Table(title="🐉 Parallel Benchmark Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("🔴 DDoS Attacks", f"{total_ddos:,}")
    table.add_row("🟢 Benign Traffic", f"{total_benign:,}")
    table.add_row("📊 Total Rows", f"{total_rows:,}")
    table.add_row("⏱️ Execution Time", f"{elapsed:.3f}s")
    table.add_row("🚀 Speed", f"{total_rows/elapsed:,.0f} rows/sec")
    
    console.print(table)

if __name__ == "__main__":
    run_parallel_benchmark()
