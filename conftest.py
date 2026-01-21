import sys
from pathlib import Path

# Añade la raíz del proyecto al sys.path para que "import app" funcione en tests
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))