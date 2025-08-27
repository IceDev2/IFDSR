import os, sys
from pathlib import Path

# Tambahkan ROOT repo ke sys.path supaya 'kelasku' bisa diimport
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kelasku.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
app = application  # Vercel cari variabel 'app'
