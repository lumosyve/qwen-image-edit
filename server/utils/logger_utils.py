import logging
import json
import uuid
from datetime import datetime
from pythonjsonlogger import jsonlogger
from config import Config
from typing import Dict, Any, List, Optional

class LoggerUtils:
    @staticmethod
    def setup_logger(name: str = "image_generation") -> logging.Logger:
        """初始化日志配置"""
        logger = logging.getLogger(name)
        logger.setLevel(Config.LOG_LEVEL)
        
        # 检查是否已存在处理器，避免重复添加
        if not logger.handlers:
            # 创建文件处理器，使用追加模式
            file_handler = logging.FileHandler(Config.LOG_PATH, mode='a', encoding='utf-8')
            
            # 创建JSON格式的日志格式化器
            formatter = jsonlogger.JsonFormatter(
                fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
                datefmt='%Y-%m-%dT%H:%M:%S.%fZ'
            )
            file_handler.setFormatter(formatter)
            
            # 添加处理器到logger
            logger.addHandler(file_handler)
        
        return logger
    
    @staticmethod
    def mask_api_key(api_key: str, visible_chars: int = 4) -> str:
        """隐藏API密钥中间部分"""
        if len(api_key) <= visible_chars * 2:
            return api_key
        
        prefix = api_key[:visible_chars]
        suffix = api_key[-visible_chars:]
        mask_length = len(api_key) - visible_chars * 2
        masked = prefix + '*' * mask_length + suffix
        
        return masked
    
    @staticmethod
    def log_api_call(
        logger: logging.Logger,
        api_key: str,
        model: str,
        prompt: str,
        negative_prompt: str,
        input_images: List[Dict[str, Any]],
        output_images: List[Dict[str, Any]],
        status: str,
        error_message: Optional[str] = None,
        seed: Optional[int] = None,
        image_size: Optional[str] = None,
        batch_size: Optional[int] = None,
        num_inference_steps: Optional[int] = None,
        guidance_scale: Optional[float] = None,
        cfg: Optional[float] = None,
        total_time_seconds: Optional[float] = None,
        timing: Optional[Dict[str, float]] = None
    ) -> None:
        """记录API调用日志"""
        # 生成唯一调用ID
        call_id = str(uuid.uuid4())
        
        # 构建日志记录
        log_record = {
            "call_id": call_id,
            "timestamp": datetime.now().isoformat() + "Z",
            "api_key": LoggerUtils.mask_api_key(api_key, Config.API_KEY_VISIBLE_CHARS),
            "model": model,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "input_images": input_images,
            "output_images": output_images,
            "status": status,
            "seed": seed,
            "image_size": image_size,
            "batch_size": batch_size,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": str(guidance_scale) if guidance_scale is not None else None,
            "cfg": str(cfg) if cfg is not None else None,
            "total_time_seconds": total_time_seconds,
            "total_time_ms": total_time_seconds * 1000 if total_time_seconds is not None else None,
            "timing": timing
        }
        
        # 添加错误信息（如果有）
        if error_message:
            log_record["error_message"] = error_message
        
        # 记录日志
        if status == "success":
            logger.info(json.dumps(log_record, ensure_ascii=False))
        else:
            logger.error(json.dumps(log_record, ensure_ascii=False))
    
    @staticmethod
    def get_default_logger() -> logging.Logger:
        """获取默认日志记录器"""
        return LoggerUtils.setup_logger()