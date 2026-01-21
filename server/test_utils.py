import os
import sys
import tempfile
from PIL import Image
from io import BytesIO
import base64

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.image_utils import ImageUtils
from utils.logger_utils import LoggerUtils
from config import Config

# 测试image_utils.py
print("=== 测试image_utils.py ===")

# 创建一个简单的测试图片
print("1. 创建测试图片")
test_image = Image.new('RGB', (100, 100), color='red')
buffered = BytesIO()
test_image.save(buffered, format="PNG")
test_image_bytes = buffered.getvalue()
print("✅ 测试图片创建成功")

# 测试bytes_to_pil_image函数
print("2. 测试bytes_to_pil_image函数")
pil_image = ImageUtils.bytes_to_pil_image(test_image_bytes)
assert isinstance(pil_image, Image.Image)
print("✅ bytes_to_pil_image函数测试成功")

# 测试pil_image_to_base64函数
print("3. 测试pil_image_to_base64函数")
base64_str = ImageUtils.pil_image_to_base64(test_image)
assert isinstance(base64_str, str)
assert len(base64_str) > 0
print("✅ pil_image_to_base64函数测试成功")

# 测试bytes_to_base64函数
print("4. 测试bytes_to_base64函数")
base64_str_from_bytes = ImageUtils.bytes_to_base64(test_image_bytes)
assert isinstance(base64_str_from_bytes, str)
assert len(base64_str_from_bytes) > 0
print("✅ bytes_to_base64函数测试成功")

# 测试get_image_size函数
print("5. 测试get_image_size函数")
width, height = ImageUtils.get_image_size(test_image)
assert width == 100
assert height == 100
print("✅ get_image_size函数测试成功")

# 测试get_image_info函数
print("6. 测试get_image_info函数")
image_info = ImageUtils.get_image_info(test_image, base64_str, 0, 20)
assert "index" in image_info
assert "width" in image_info
assert "height" in image_info
assert "format" in image_info
assert "base64_preview" in image_info
assert len(image_info["base64_preview"]) <= 23  # 20 + "..."
print("✅ get_image_info函数测试成功")

# 测试base64_to_pil_image函数
print("7. 测试base64_to_pil_image函数")
pil_image_from_base64 = ImageUtils.base64_to_pil_image(base64_str)
assert isinstance(pil_image_from_base64, Image.Image)
print("✅ base64_to_pil_image函数测试成功")

# 测试logger_utils.py
print("\n=== 测试logger_utils.py ===")

# 测试setup_logger函数
print("1. 测试setup_logger函数")
logger = LoggerUtils.setup_logger("test_logger")
assert logger is not None
print("✅ setup_logger函数测试成功")

# 测试mask_api_key函数
print("2. 测试mask_api_key函数")
original_key = "test_api_key_1234567890"
masked_key = LoggerUtils.mask_api_key(original_key, 4)
# 计算预期结果
prefix = original_key[:4]
suffix = original_key[-4:]
mask_length = len(original_key) - 8
expected = prefix + '*' * mask_length + suffix
assert masked_key == expected
print(f"✅ mask_api_key函数测试成功: {masked_key}")

# 测试log_api_call函数
print("3. 测试log_api_call函数")
try:
    LoggerUtils.log_api_call(
        logger=logger,
        api_key=original_key,
        model="Qwen/Qwen-Image-Edit-2509",
        prompt="test prompt",
        negative_prompt="test negative prompt",
        input_images=[image_info],
        output_images=[image_info],
        status="success",
        seed=12345,
        image_size="1024x1024",
        batch_size=1,
        num_inference_steps=20,
        guidance_scale=7.5,
        cfg=4.0,
        total_time_seconds=1.234,
        timing={"inference": 1.0, "total": 1.234}
    )
    print("✅ log_api_call函数测试成功")
except Exception as e:
    print(f"❌ log_api_call函数测试失败: {e}")

# 验证日志文件生成
print("4. 验证日志文件生成")
log_file_path = Config.LOG_PATH
if os.path.exists(log_file_path):
    print(f"✅ 日志文件生成成功: {log_file_path}")
    # 查看日志文件内容
    with open(log_file_path, 'r') as f:
        log_content = f.read()
        if len(log_content) > 0:
            print("✅ 日志文件内容不为空")
        else:
            print("❌ 日志文件内容为空")
else:
    print(f"❌ 日志文件未生成: {log_file_path}")

print("\n=== 所有测试完成 ===")
