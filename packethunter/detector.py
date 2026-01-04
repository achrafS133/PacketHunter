import pandas as pd
from typing import Dict
from .config import DDOS_LABELS, LABEL_COLUMN

def analyze_chunk(chunk: pd.DataFrame) -> Dict:
    """
    Analyzes a dataframe chunk for DDoS patterns.
    Returns a dictionary of counts and top destination ports.
    """
    # Detect columns
    label_col = [c for c in chunk.columns if 'Label' in c][0]
    port_col = [c for c in chunk.columns if 'Destination Port' in c][0]

    # Normalize labels (strip whitespace)
    chunk[label_col] = chunk[label_col].str.strip()
    
    # Filter for DDoS only
    ddos_mask = chunk[label_col].isin(DDOS_LABELS)
    ddos_chunk = chunk[ddos_mask]
    
    label_counts = chunk[label_col].value_counts().to_dict()
    
    ddos_count = ddos_chunk.shape[0]
    benign_count = label_counts.get('BENIGN', 0)
    
    # Track top destination ports for attacks
    top_ports = {}
    if not ddos_chunk.empty:
        top_ports = ddos_chunk[port_col].value_counts().head(5).to_dict()
    
    return {
        'ddos': ddos_count,
        'benign': benign_count,
        'total': len(chunk),
        'top_ports': top_ports
    }

