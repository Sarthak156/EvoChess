"""Root entry point for Render deployment.
This file enables `uvicorn main:app` from the project root."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))
from app.main import app