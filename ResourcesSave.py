import os
import base64
import folder_paths
import numpy as np
import node_helpers
import torch

from PIL import Image, ImageOps, PngImagePlugin
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
                "filename_counter": ("BOOLEAN", {"default": True}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "ResourcesSave"

    def save(self, anything=None, filename_counter=True, filename_prefix="ComfyUI"):
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, folder_paths.get_output_directory())
        if not filename_counter:
            file = f"{filename}.npy"
        else:
            file = f"{filename}_{counter:05}_.npy"
        np.save(os.path.join(full_output_folder, file), anything)
        # print(f"{anything}")
        return {}

class RsaveImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "anything": (any, {})
            },
            "hidden": {
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("image", )
    FUNCTION = "save"
    CATEGORY = "ResourcesSave"

    def save(self, anything, extra_pnginfo):
        PngImagePlugin.MAX_TEXT_MEMORY = 12800 * 1024 * 1024
        dim = "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"
        img = node_helpers.pillow(ImageOps.exif_transpose, Image.open(BytesIO(base64.b64decode(dim))))
        if img.mode == "I":
            img = img.point(lambda img: img * (1 / 255))
        im = torch.from_numpy(np.array(img.convert("RGB")).astype(np.float32) / 255.0)[None,]
        npy = BytesIO()
        np.save(npy, anything)
        extra_pnginfo["ResourcesSave"] = f"{base64.b64encode(npy.getvalue())}"
        npy.close()
        return (im, )
    def IS_CHANGED(anything, extra_pnginfo):
        timestamp = time.time()
        return (timestamp, )

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
    CATEGORY = "ResourcesSave"

    def imagecs(self, images, iformat):
        imageg = []
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            imgo = BytesIO()
            if iformat == "webp":
                # img.save(imgo, quality=100, format="webp", optimize=True)
                img.save(imgo, quality=100, format="webp")
            elif iformat == "jpg":
                img.save(imgo, quality=100, format="jpeg")
            elif iformat == "png":
                img.save(imgo, compress_level=6, format="png")
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
    CATEGORY = "ResourcesSave"

    def getdate(self, prefix="", format="%Y-%m-%d-%H-%M-%S"):
        timestamp = time.time()
        local_time = time.localtime(timestamp)
        formatted_time = time.strftime(format, local_time)
        date = prefix + formatted_time
        return (date, )
    def IS_CHANGED(prefix="", format="%Y-%m-%d-%H-%M-%S"):
        timestamp = time.time()
        return (timestamp, )

NODE_CLASS_MAPPINGS = {
    "Rsave": Rsave,
    "RsaveImage": RsaveImage,
    "RsaveImageC": RsaveImageC,
    "RsaveDate": RsaveDate,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Rsave": "RsaveNpy",
    "RsaveImage": "RsaveImage",
    "RsaveImageC": "RsaveImageC",
    "RsaveDate": "RsaveDate",
}
