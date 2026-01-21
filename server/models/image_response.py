from pydantic import BaseModel, Field
from typing import List, Optional

class GeneratedImage(BaseModel):
    base64: str = Field(..., description="生成图片的base64编码")
    index: int = Field(..., description="图片索引")

class ImageGenerationResponse(BaseModel):
    success: bool = Field(..., description="生成是否成功")
    message: str = Field(..., description="响应消息")
    images: List[GeneratedImage] = Field(default_factory=list, description="生成的图片列表")
    seed: Optional[int] = Field(default=None, description="生成种子")
    timing: Optional[dict] = Field(default=None, description="生成时间信息")
