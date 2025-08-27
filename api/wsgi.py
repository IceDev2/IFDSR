import os, sys
from pathlib import Path

# Tambahkan ROOT repo ke sys.path supaya 'kelasku' bisa diimport
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kelasku.settings')

application = get_asgi_application()
