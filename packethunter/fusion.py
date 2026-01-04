import pandas as pd
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Callable, Optional
from .config import CHUNK_SIZE, LABEL_COLUMN, DEFAULT_CSV
from .detector import analyze_chunk

def fusion_engine(
    filepath: str = str(DEFAULT_CSV), 
    n_workers: Optional[int] = None,
    progress_callback: Optional[Callable[[Dict], None]] = None
) -> Dict:
    """
    Multiprocessing engine to scan network logs.
    """
    n_workers = n_workers or cpu_count()
    
    # Detect actual column names (CIC-IDS2017 headers often have varying spaces)
    sample = pd.read_csv(filepath, nrows=1)
    
    label_col = [c for c in sample.columns if 'Label' in c][0]
    port_col = [c for c in sample.columns if 'Destination Port' in c][0]
    
    # Usecols to minimize memory footprint
    chunks = pd.read_csv(
        filepath, 
        chunksize=CHUNK_SIZE, 
        low_memory=False, 
        usecols=[label_col, port_col]
    )
    
    results = []
    
    with Pool(processes=n_workers) as pool:
        # We use imap_unordered for speed
        for partial_result in pool.imap_unordered(analyze_chunk, chunks):
            results.append(partial_result)
            if progress_callback:
                progress_callback(partial_result)
                
    # Final Reduction
    total_ddos = sum(r['ddos'] for r in results)
    total_benign = sum(r['benign'] for r in results)
    total_rows = sum(r['total'] for r in results)
    
    # Aggregate top ports
    all_ports = {}
    for r in results:
        for port, count in r['top_ports'].items():
            all_ports[port] = all_ports.get(port, 0) + count
            
    # Sort and take top 5
    top_ports = dict(sorted(all_ports.items(), key=lambda x: x[1], reverse=True)[:5])
    
    return {
        'ddos': total_ddos,
        'benign': total_benign,
        'total': total_rows,
        'top_ports': top_ports,
        'speed_rows_per_sec': 0
    }

from pathlib import Path

def fusion_scan_directory(
    directory_path: str, 
    n_workers: Optional[int] = None,
    progress_callback: Optional[Callable[[Dict], None]] = None
) -> List[Dict]:
    """
    🐉 Full Planet Scan — Analyzes every CSV in the directory.
    """
    path = Path(directory_path)
    csv_files = list(path.glob("*.csv"))
    
    all_results = []
    for csv_file in csv_files:
        if progress_callback:
            # Send status update
            progress_callback({'type': 'status', 'msg': f"Scanning {csv_file.name}..."})
        
        result = fusion_engine(str(csv_file), n_workers, progress_callback)
        result['filename'] = csv_file.name
        all_results.append(result)
        
    return all_results
