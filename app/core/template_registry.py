from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .logger import setup_logger

logger = setup_logger(__name__)


class TemplateRegistry:
    ROOT_DIR = Path(__file__).resolve().parent.parent

    def __init__(
        self,
        templates_full_path: Optional[Path] = None,
        static_dir: Optional[Path] = None,
    ):
        if templates_full_path:
            self.TEMPLATES_DIR = templates_full_path
        else:
            self.TEMPLATES_DIR = Path(self.ROOT_DIR, "templates")

        if static_dir:
            self.STATIC_DIR = static_dir
        else:
            self.STATIC_DIR = Path(self.ROOT_DIR, "static")

    # Mount static folder
    def mount_static(self, app: FastAPI, path: Optional[str] = "/static", name: Optional[str] = "static"):
        if self.STATIC_DIR.exists():
            logger.info("Static files mounted at /static")
            app.mount(path=path, app=StaticFiles(directory=str(self.STATIC_DIR)), name=name)
            return

        logger.error("Error mounting static files.")
