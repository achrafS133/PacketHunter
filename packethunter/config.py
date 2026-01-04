from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATASET_DIR = BASE_DIR / "DATASET"
DEFAULT_CSV = DATASET_DIR / "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"

# Detection Logic
LABEL_COLUMN = ' Label'
BENIGN_LABEL = 'BENIGN'
DDOS_LABELS = {
    'DDoS', 
    'DoS slowloris', 
    'DoS Slowhttptest', 
    'DoS Hulk', 
    'DoS GoldenEye'
}

# Performance
CHUNK_SIZE = 100_000
