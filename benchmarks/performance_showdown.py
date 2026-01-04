import pandas as pd
import time
import os
from multiprocessing import cpu_count
from rich.console import Console
from rich.table import Table
from packethunter.fusion import fusion_engine
from packethunter.config import DEFAULT_CSV, LABEL_COLUMN

console = Console()

def run_benchmarks():
    if not os.path.exists(DEFAULT_CSV):
        console.print(f"[bold red]Error:[/] Dataset not found at {DEFAULT_CSV}")
        return

    console.print("\n🏁 [bold cyan]STARTING PACKETHUNTER PERFORMANCE SHOWDOWN[/]\n")
    
    # --- SEQUENTIAL (BASE FORM) ---
    console.print("🐢 [bold yellow]Base Form (Sequential) active...[/]")
    start_seq = time.perf_counter()
    df = pd.read_csv(DEFAULT_CSV, low_memory=False, usecols=[LABEL_COLUMN])
    # Minimal logic for comparison
    df[LABEL_COLUMN].value_counts()
    end_seq = time.perf_counter()
    time_seq = end_seq - start_seq
    
    # --- PARALLEL (FUSION) ---
    console.print("🐉 [bold cyan]Fusion Mode (Parallel) active...[/]")
    start_par = time.perf_counter()
    results = fusion_engine(str(DEFAULT_CSV))
    end_par = time.perf_counter()
    time_par = end_par - start_par
    
    # Summary
    table = Table(title="🏆 Performance Summary")
    table.add_column("Mode", style="bold")
    table.add_column("Time", justify="right")
    table.add_column("Throughput", justify="right")
    table.add_column("Efficiency", style="green")
    
    speed_seq = results['total'] / time_seq
    speed_par = results['total'] / time_par
    boost = speed_par / speed_seq
    
    table.add_row("🐢 Sequential", f"{time_seq:.2f}s", f"{speed_seq:,.0f} r/s", "1.0x")
    table.add_row("🐉 Parallel", f"{time_par:.2f}s", f"{speed_par:,.0f} r/s", f"{boost:.1f}x boost")
    
    console.print(table)
    
    if boost > 1.2:
        console.print(f"\n✨ [bold green]FUSION SUCCESSFUL![/] Speed increased by [bold]{boost:.1f}x[/] using {cpu_count()} cores.\n")
    else:
        console.print("\nℹ️  Dataset size might be too small to see significant multiprocessing gains on this I/O bound task.\n")

if __name__ == "__main__":
    run_benchmarks()
