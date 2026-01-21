import requests
from typing import List, Optional, Dict, Any
from PIL import Image
from config import Config
from utils.image_utils import ImageUtils

class ImageGenerator:
    def __init__(self):
        self.api_key = Config.API_KEY
        self.api_base_url = Config.API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_images(self, model: str, prompt: str, images: Optional[List[Image.Image]] = None, 
                       negative_prompt: str = "", image_size: Optional[str] = None, 
                       batch_size: int = 1, seed: Optional[int] = None, 
                       num_inference_steps: int = 20, guidance_scale: float = 7.5, cfg: float = 4.0) -> Dict[str, Any]:
        """调用SiliconFlow API生成图片"""
        payload = {
            "model": model,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        }
        
        # 根据模型添加特定参数
        if model.startswith("Kwai-Kolors/"):
            payload["image_size"] = image_size or Config.DEFAULT_IMAGE_SIZE
            payload["batch_size"] = batch_size
            payload["num_inference_steps"] = num_inference_steps
            payload["guidance_scale"] = guidance_scale
        elif model.startswith("Qwen/"):
            if model not in ["Qwen/Qwen-Image-Edit-2509", "Qwen/Qwen-Image-Edit"]:
                payload["image_size"] = image_size or Config.DEFAULT_IMAGE_SIZE
            payload["cfg"] = cfg
        
        if seed is not None:
            payload["seed"] = seed
        
        # 处理图片
        if images:
            for i, image in enumerate(images[:Config.MAX_IMAGES]):
                base64_str = ImageUtils.pil_image_to_base64(image)
                if i == 0:
                    payload["image"] = f"data:image/png;base64,{base64_str}"
                elif i == 1 and model == "Qwen/Qwen-Image-Edit-2509":
                    payload["image2"] = f"data:image/png;base64,{base64_str}"
                elif i == 2 and model == "Qwen/Qwen-Image-Edit-2509":
                    payload["image3"] = f"data:image/png;base64,{base64_str}"
        
        try:
            response = requests.post(self.api_base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API调用失败: {str(e)}")
