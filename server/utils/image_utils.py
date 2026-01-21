from PIL import Image
from io import BytesIO
import base64
from typing import Dict, Any, Tuple

class ImageUtils:
    @staticmethod
    def bytes_to_pil_image(image_bytes: bytes) -> Image.Image:
        """将字节数据转换为PIL Image对象"""
        return Image.open(BytesIO(image_bytes))
    
    @staticmethod
    def pil_image_to_base64(image: Image.Image, format: str = "PNG") -> str:
        """将PIL Image对象转换为base64字符串"""
        buffered = BytesIO()
        image.save(buffered, format=format)
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    @staticmethod
    def bytes_to_base64(image_bytes: bytes, format: str = "PNG") -> str:
        """将字节数据直接转换为base64字符串"""
        image = ImageUtils.bytes_to_pil_image(image_bytes)
        return ImageUtils.pil_image_to_base64(image, format)
    
    @staticmethod
    def get_image_size(image: Image.Image) -> Tuple[int, int]:
        """获取图片尺寸"""
        return image.size
    
    @staticmethod
    def get_image_info(image: Image.Image, base64_str: str, index: int, max_base64_len: int = 100) -> Dict[str, Any]:
        """获取图片信息（用于日志记录）"""
        width, height = ImageUtils.get_image_size(image)
        
        return {
            "index": index,
            "width": width,
            "height": height,
            "format": image.format or "PNG",
            "base64_preview": base64_str[:max_base64_len] + "..." if len(base64_str) > max_base64_len else base64_str
        }
    
    @staticmethod
    def base64_to_pil_image(base64_str: str) -> Image.Image:
        """将base64字符串转换为PIL Image对象"""
        if base64_str.startswith("data:image/"):
            base64_str = base64_str.split(",")[1]
        image_bytes = base64.b64decode(base64_str)
        return Image.open(BytesIO(image_bytes))