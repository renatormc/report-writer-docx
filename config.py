import os
from pathlib import Path


app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
models_folder = app_dir / "models"
TEMPFOLDER = app_dir / "temp"
if not TEMPFOLDER.exists():
    TEMPFOLDER.mkdir()
