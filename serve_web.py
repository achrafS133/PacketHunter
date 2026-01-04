import os
import sys
from textual_serve.server import Server

if __name__ == "__main__":
    # Use the absolute path to main.py to be safe
    app_path = os.path.join(os.getcwd(), "main.py")
    cmd = f'"{sys.executable}" "{app_path}"'
    
    print(f"🚀 Initializing Textual-Serve for: {cmd}")
    print("🌐 Dashboard will be available at: http://127.0.0.1:8000")
    
    # textual-serve Server(command, host, port)
    server = Server(cmd, host="127.0.0.1", port=8000)
    server.serve()
