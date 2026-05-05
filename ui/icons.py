from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageTk
import customtkinter as ctk


class AppIcons:
    """Centralized icon/image loader with cache."""

    def __init__(self, assets_dir: Path):
        self.assets_dir = assets_dir
        self._cache = {}

    def get(self, filename: str, size: Optional[Tuple[int, int]] = None, return_raw: bool = False):
        key = (filename, size, return_raw)
        if key in self._cache:
            return self._cache[key]

        image_path = self.assets_dir / filename
        if not image_path.exists():
            return None

        image = Image.open(image_path)
        
        if return_raw:
            if size:
                image = image.resize(size, Image.LANCZOS)
            final_image = ImageTk.PhotoImage(image)
        else:
            if size:
                final_image = ctk.CTkImage(light_image=image, dark_image=image, size=size)
            else:
                final_image = ctk.CTkImage(light_image=image, dark_image=image, size=image.size)
            
        self._cache[key] = final_image
        return final_image
