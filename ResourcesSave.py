import os
import folder_paths
import numpy as np

from PIL import Image
from io import BytesIO

import time

class AnyType(str):
    def __eq__(self, _) -> bool:
        return True

    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")

class Rsave:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "anything": (any, {}),
                "filename_date": ("BOOLEAN", {"default": False}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "ResourcesSL"

    def save(self, anything=None, filename_date=False, filename_prefix="ComfyUI"):
        if filename_date:
            timestamp = time.time()
            local_time = time.localtime(timestamp)
            formatted_time = time.strftime('%Y-%m-%d-%H-%M-%S', local_time)
            filename_prefix += formatted_time
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
            filename_prefix,
            folder_paths.get_output_directory()
        )
        if filename_date:
            file = f"{filename}.npy"
        else:
            file = f"{filename}_{counter:05}_.npy"
        np.save(os.path.join(full_output_folder, file), anything)
        return {}

class RsaveImageC:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
                "iformat": (["webp", "jpg", "png"], )
            }
        }

    RETURN_TYPES = (any, )
    RETURN_NAMES = ("output", )
    FUNCTION = "imagecs"
    CATEGORY = "ResourcesSL"

    def imagecs(self, images, iformat):
        imageg = []
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            imgo = BytesIO()
            if iformat == "webp":
                img.save(imgo, quality=100, format="webp", optimize=True)
            elif iformat == "jpg":
                img.save(imgo, quality=100, format="jpeg", optimize=True)
            elif iformat == "png":
                img.save(imgo, compress_level=6, format="png", optimize=True)
            imgb = imgo.getvalue()
            imageg.append(BytesIO(imgb))
            imgo.close()
        return (imageg, )

class RsaveDate:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prefix": ("STRING", {"default": ""}),
                "format": ("STRING", {"default": "%Y-%m-%d-%H-%M-%S"})
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("date", )
    FUNCTION = "getdate"
    CATEGORY = "ResourcesSL"

    def IS_CHANGED(prefix="", format="%Y-%m-%d-%H-%M-%S"):
        timestamp = time.time()
        local_time = time.localtime(timestamp)
        formatted_time = time.strftime(format, local_time)
        date = prefix + formatted_time
        return (date, )
    def getdate(self, prefix="", format="%Y-%m-%d-%H-%M-%S"):
        timestamp = time.time()
        local_time = time.localtime(timestamp)
        formatted_time = time.strftime(format, local_time)
        date = prefix + formatted_time
        return (date, )

NODE_CLASS_MAPPINGS = {
    "Rsave": Rsave,
    "RsaveImageC": RsaveImageC,
    "RsaveDate": RsaveDate,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Rsave": "Rsave",
    "RsaveImageC": "RsaveImageC",
    "RsaveDate": "RsaveDate",
}
