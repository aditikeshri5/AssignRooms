import sys
import os

# Add backend folder to Python path
backend_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "backend"
)

sys.path.insert(0, backend_path)

from app import app