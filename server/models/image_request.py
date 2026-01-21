from pydantic import BaseModel, Field, validator
from typing import Optional
from config import Config

class ImageGenerationRequest(BaseModel):
    model: str = Field(default=Config.DEFAULT_MODEL, description="模型名称")
    prompt: str = Field(..., description="提示词")
    negative_prompt: str = Field(default="", description="负面提示词")
    image_size: Optional[str] = Field(default=None, description="图片尺寸")
    batch_size: Optional[int] = Field(default=1, ge=1, le=4, description="批量大小")
    seed: Optional[int] = Field(default=None, ge=0, le=9999999999, description="种子")
    num_inference_steps: Optional[int] = Field(default=20, ge=1, le=100, description="推理步数")
    guidance_scale: Optional[float] = Field(default=7.5, ge=0.0, le=20.0, description="引导比例")
    cfg: Optional[float] = Field(default=4.0, ge=0.1, le=20.0, description="CFG值")
    
    @validator('model')
    def validate_model(cls, v):
        if v not in Config.AVAILABLE_MODELS:
            raise ValueError(f"模型必须是以下之一: {', '.join(Config.AVAILABLE_MODELS)}")
        return v
    
    @validator('image_size')
    def validate_image_size(cls, v, values):
        if v is None:
            return v
        
        model = values.get('model')
        if model.startswith("Kwai-Kolors/"):
            if v not in Config.AVAILABLE_IMAGE_SIZES["Kolor"]:
                raise ValueError(f"对于Kolor模型，图片尺寸必须是以下之一: {', '.join(Config.AVAILABLE_IMAGE_SIZES['Kolor'])}")
        elif model.startswith("Qwen/") and model not in ["Qwen/Qwen-Image-Edit-2509", "Qwen/Qwen-Image-Edit"]:
            if v not in Config.AVAILABLE_IMAGE_SIZES["Qwen-Image"]:
                raise ValueError(f"对于Qwen-Image模型，图片尺寸必须是以下之一: {', '.join(Config.AVAILABLE_IMAGE_SIZES['Qwen-Image'])}")
        
        return v