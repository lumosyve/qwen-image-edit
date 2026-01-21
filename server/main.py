from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from typing import List, Optional
from fastapi.responses import JSONResponse
from PIL import Image
import io
import time

from config import Config
from models.image_request import ImageGenerationRequest
from models.image_response import ImageGenerationResponse, GeneratedImage
from services.image_generator import ImageGenerator
from utils.image_utils import ImageUtils
from utils.logger_utils import LoggerUtils

# 创建FastAPI应用
app = FastAPI(
    title="SiliconFlow Image Generation API",
    description="基于SiliconFlow API的图片生成服务",
    version="1.0.0"
)

# 初始化图片生成器
image_generator = ImageGenerator()

# 初始化日志记录器
logger = LoggerUtils.get_default_logger()

@app.get("/health", summary="健康检查")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "SiliconFlow Image Generation API",
        "available_models": Config.AVAILABLE_MODELS
    }

@app.get("/models", summary="获取可用模型列表")
async def get_models():
    """获取可用模型列表接口，返回所有支持的模型信息，包括模型名称和默认参数"""
    models_info = []
    
    for model in Config.AVAILABLE_MODELS:
        # 根据模型类型确定支持的图片尺寸
        if model.startswith("Kwai-Kolors/"):
            available_sizes = Config.AVAILABLE_IMAGE_SIZES.get("Kolor", [])
            model_type = "image_generation"
        elif model in ["Qwen/Qwen-Image-Edit-2509", "Qwen/Qwen-Image-Edit"]:
            available_sizes = []  # 编辑模型不支持自定义尺寸
            model_type = "image_edit"
        else:
            available_sizes = Config.AVAILABLE_IMAGE_SIZES.get("Qwen-Image", [])
            model_type = "image_generation"
        
        models_info.append({
            "model_name": model,
            "model_type": model_type,
            "available_sizes": available_sizes,
            "is_default": model == Config.DEFAULT_MODEL
        })
    
    return {
        "models": models_info,
        "total": len(models_info)
    }

@app.post("/generate-images", response_model=ImageGenerationResponse, summary="生成图片")
async def generate_images(
    # 文件上传参数
    files: List[UploadFile] = File(..., description="上传的图片文件列表"),
    
    # 文本参数
    model: str = Form(Config.DEFAULT_MODEL, description="模型名称"),
    prompt: str = Form(..., description="提示词"),
    negative_prompt: str = Form("", description="负面提示词"),
    image_size: Optional[str] = Form(None, description="图片尺寸"),
    batch_size: int = Form(1, description="批量大小"),
    seed: Optional[int] = Form(None, description="种子"),
    num_inference_steps: int = Form(20, description="推理步数"),
    guidance_scale: float = Form(7.5, description="引导比例"),
    cfg: float = Form(4.0, description="CFG值")
):
    """
    生成图片API
    
    - **files**: 上传的图片文件列表，支持PNG、JPG、JPEG格式
    - **model**: 模型名称，可选值：Qwen/Qwen-Image-Edit-2509, Qwen/Qwen-Image-Edit, Kwai-Kolors/Kolors
    - **prompt**: 提示词
    - **negative_prompt**: 负面提示词
    - **image_size**: 图片尺寸
    - **batch_size**: 批量大小，1-4
    - **seed**: 生成种子，0-9999999999
    - **num_inference_steps**: 推理步数，1-100
    - **guidance_scale**: 引导比例，0.0-20.0（仅Kolor模型）
    - **cfg**: CFG值，0.1-20.0（仅Qwen模型）
    """
    # 记录API调用开始时间
    start_time = time.time()
    
    # 初始化日志数据
    input_images_log = []
    output_images_log = []
    status = "success"
    error_message = None
    
    try:
        # 验证模型参数
        if model not in Config.AVAILABLE_MODELS:
            raise HTTPException(status_code=400, detail=f"模型必须是以下之一: {', '.join(Config.AVAILABLE_MODELS)}")
        
        # 读取上传的图片
        images = []
        for i, file in enumerate(files):
            if not file.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail=f"文件 {file.filename} 不是有效的图片格式")
            
            # 读取文件内容
            image_bytes = await file.read()
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)
            
            # 转换为base64
            base64_str = ImageUtils.bytes_to_base64(image_bytes)
            
            # 记录输入图片信息
            image_info = ImageUtils.get_image_info(image, base64_str, i, Config.IMAGE_BASE64_PREVIEW_LENGTH)
            input_images_log.append(image_info)
        
        # 调用图片生成服务
        result = image_generator.generate_images(
            model=model,
            prompt=prompt,
            images=images,
            negative_prompt=negative_prompt,
            image_size=image_size,
            batch_size=batch_size,
            seed=seed,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            cfg=cfg
        )
        
        # 构建响应
        generated_images = []
        for i, image_data in enumerate(result["images"]):
            # 提取base64编码（如果包含前缀则去除）
            base64_str = image_data
            if base64_str.startswith("data:image/"):
                base64_str = base64_str.split(",")[1]
            
            # 将base64转换为PIL Image对象（用于获取图片信息）
            pil_image = ImageUtils.base64_to_pil_image(base64_str)
            
            # 记录输出图片信息
            image_info = ImageUtils.get_image_info(pil_image, base64_str, i, Config.IMAGE_BASE64_PREVIEW_LENGTH)
            output_images_log.append(image_info)
            
            generated_images.append(GeneratedImage(
                base64=base64_str,
                index=i
            ))
        
        # 记录API调用结束时间
        end_time = time.time()
        total_time = end_time - start_time
        
        # 记录日志
        LoggerUtils.log_api_call(
            logger=logger,
            api_key=Config.API_KEY,
            model=model,
            prompt=prompt,
            negative_prompt=negative_prompt,
            input_images=input_images_log,
            output_images=output_images_log,
            status=status,
            seed=result.get("seed"),
            image_size=image_size,
            batch_size=batch_size,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            cfg=cfg,
            total_time_seconds=total_time,
            timing=result.get("timings")
        )
        
        return ImageGenerationResponse(
            success=True,
            message="图片生成成功",
            images=generated_images,
            seed=result.get("seed"),
            timing=result.get("timings")
        )
        
    except HTTPException as e:
        # 记录错误信息
        status = "failed"
        error_message = str(e.detail)
        raise
    except Exception as e:
        # 记录错误信息
        status = "failed"
        error_message = str(e)
        
        # 记录API调用结束时间
        end_time = time.time()
        total_time = end_time - start_time
        
        # 记录日志
        LoggerUtils.log_api_call(
            logger=logger,
            api_key=Config.API_KEY,
            model=model,
            prompt=prompt,
            negative_prompt=negative_prompt,
            input_images=input_images_log,
            output_images=output_images_log,
            status=status,
            error_message=error_message,
            seed=seed,
            image_size=image_size,
            batch_size=batch_size,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            cfg=cfg,
            total_time_seconds=total_time
        )
        
        return JSONResponse(
            status_code=500,
            content=ImageGenerationResponse(
                success=False,
                message=f"图片生成失败: {str(e)}",
                images=[]
            ).dict()
        )
