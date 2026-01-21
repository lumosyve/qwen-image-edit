import os

class Config:
    # API配置
    API_KEY = "your_api_key_here"  # 在此处直接配置API密钥
    API_BASE_URL = "https://api.siliconflow.cn/v1/images/generations"
    
    # 模型配置
    DEFAULT_MODEL = "Qwen/Qwen-Image-Edit-2509"
    AVAILABLE_MODELS = [
        "Qwen/Qwen-Image-Edit-2509",
        "Qwen/Qwen-Image-Edit",
        "Kwai-Kolors/Kolors"
    ]
    
    # 图片尺寸配置
    DEFAULT_IMAGE_SIZE = "1024x1024"
    AVAILABLE_IMAGE_SIZES = {
        "Kolor": ["1024x1024", "960x1280", "768x1024", "720x1440", "720x1280"],
        "Qwen-Image": ["1328x1328", "1664x928", "928x1664", "1472x1140", "1140x1472", "1584x1056", "1056x1584"]
    }
    
    # 其他配置
    MAX_IMAGES = 3  # 最大支持上传图片数量
    
    # 服务配置
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True
    
    # 日志配置
    LOG_PATH = os.path.join(os.getcwd(), "logs", "image_generation.log")
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 图片日志配置
    IMAGE_BASE64_PREVIEW_LENGTH = 100  # 图片base64预览长度
    
    # API密钥日志配置
    API_KEY_VISIBLE_CHARS = 4  # API密钥前后可见字符数