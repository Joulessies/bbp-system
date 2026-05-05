from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageTk


class AppIcons:
    """Centralized icon/image loader with cache."""

    def __init__(self, assets_dir: Path):
        self.assets_dir = assets_dir
        self._cache = {}

    def get(self, filename: str, size: Optional[Tuple[int, int]] = None):
        key = (filename, size)
        if key in self._cache:
            return self._cache[key]

        image_path = self.assets_dir / filename
        if not image_path.exists():
            return None

        image = Image.open(image_path)
        if size:
            image = image.resize(size, Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(image)
        self._cache[key] = tk_image
        return tk_image
