# SiliconFlow图片生成API设计文档

## 1. 项目概述

本项目旨在实现一个基于FastAPI的RESTful API服务，允许用户通过HTTP请求上传图片、输入提示文案，调用SiliconFlow模型API并返回生成结果。同时，系统将记录API调用的总次数和图片输出信息。

## 2. 技术栈

- **Web框架**：FastAPI（用于构建高性能RESTful API）
- **API调用**：requests库
- **图片处理**：Pillow库
- **配置管理**：内置配置类
- **数据验证**：Pydantic（FastAPI内置）
- **文件上传**：FastAPI内置的FileUpload功能
- **日志记录**：Python标准库logging + python-json-logger

## 3. 目录结构

```
qwen3-image-edit/
├── main.py                     # FastAPI应用入口
├── config.py                   # 配置管理
├── services/
│   └── image_generator.py      # 图片生成服务
├── models/
│   ├── image_request.py        # 请求模型定义
│   └── image_response.py       # 响应模型定义
├── utils/
│   ├── image_utils.py          # 图片处理工具
│   └── logger_utils.py         # 日志处理工具
├── logs/                       # 日志存储目录
│   └── image_generation.log    # 日志文件
├── requirements.txt            # 依赖声明
├── README.md                   # 项目说明
└── design_document.md          # 设计文档
```

## 4. 核心功能设计

### 4.1 配置管理

- 使用`config.py`文件存储所有配置项
- 包含API密钥、模型配置、日志配置等
- 支持多种模型配置和图片尺寸配置

### 4.2 图片处理

- 支持多种图片格式上传（PNG、JPG、JPEG等）
- 将图片转换为base64格式以便API传输
- 支持单张和多张图片上传
- 提供图片信息提取功能（用于日志记录）

### 4.3 API调用

- 实现SiliconFlow API的调用逻辑
- 支持多种模型选择
- 支持提示词和负面提示词输入
- 支持批量生成
- 完善的错误处理机制

### 4.4 日志记录

- 记录API调用的详细信息，包括API密钥、输入图片、输出图片和总耗时
- 支持增量更新，每次调用都追加到日志文件
- 日志格式为JSON，便于后续分析
- API密钥使用掩码处理，仅显示前4位和后4位
- 图片base64编码仅显示前100字符，保护数据安全

## 5. API文档

### 5.1 健康检查接口

- **URL**: `/health`
- **方法**: `GET`
- **描述**: 检查API服务是否正常运行

**响应示例**:

```json
{
  "status": "healthy",
  "service": "SiliconFlow Image Generation API",
  "available_models": [
    "Qwen/Qwen-Image-Edit-2509",
    "Qwen/Qwen-Image-Edit",
    "Kwai-Kolors/Kolors"
  ]
}
```

### 5.2 图片生成接口

- **URL**: `/generate-images`
- **方法**: `POST`
- **描述**: 生成图片的主接口
- **Content-Type**: `multipart/form-data`

**请求参数**:

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| files | file[] | 是 | 上传的图片文件列表 |
| model | string | 否 | 模型名称，默认：Qwen/Qwen-Image-Edit-2509 |
| prompt | string | 是 | 提示词 |
| negative_prompt | string | 否 | 负面提示词 |
| image_size | string | 否 | 图片尺寸 |
| batch_size | integer | 否 | 批量大小，1-4 |
| seed | integer | 否 | 生成种子，0-9999999999 |
| num_inference_steps | integer | 否 | 推理步数，1-100 |
| guidance_scale | float | 否 | 引导比例，0.0-20.0（仅Kolor模型） |
| cfg | float | 否 | CFG值，0.1-20.0（仅Qwen模型） |

**响应示例**:

```json
{
  "success": true,
  "message": "图片生成成功",
  "images": [
    {
      "base64": "iVBORw0KGgoAAAANSUhEUgAAA...",
      "index": 0
    }
  ],
  "seed": 123456,
  "timing": {
    "total": 1.234,
    "inference": 1.123
  }
}
```

## 6. 日志格式设计

### 6.1 日志内容

```json
{
  "call_id": "uuid",
  "timestamp": "2023-01-01T12:00:00.000000Z",
  "api_key": "your*********here",
  "model": "Qwen/Qwen-Image-Edit-2509",
  "prompt": "test prompt",
  "negative_prompt": "test negative prompt",
  "input_images": [
    {
      "index": 0,
      "width": 100,
      "height": 100,
      "format": "PNG",
      "base64_preview": "iVBORw0KGgoAAAANSUhE..."
    }
  ],
  "output_images": [
    {
      "index": 0,
      "width": 1024,
      "height": 1024,
      "format": "PNG",
      "base64_preview": "iVBORw0KGgoAAAANSUhE..."
    }
  ],
  "status": "success",
  "seed": 12345,
  "image_size": "1024x1024",
  "batch_size": 1,
  "num_inference_steps": 20,
  "guidance_scale": "7.5",
  "cfg": "4.0",
  "total_time_seconds": 1.234,
  "total_time_ms": 1234.0,
  "timing": {
    "inference": 1.0,
    "total": 1.234
  },
  "error_message": null
}
```

### 6.2 日志特点

- **增量更新**：每次调用都追加到日志文件，不覆盖原有日志
- **安全记录**：API密钥使用掩码处理，图片base64仅显示前100字符
- **详细信息**：包含完整的请求和响应信息
- **易于分析**：JSON格式便于后续数据处理和分析

## 7. 核心模块实现

### 7.1 config.py - 配置管理

定义了所有配置项，包括API密钥、模型配置、日志配置等。

### 7.2 image_utils.py - 图片处理工具

提供了图片转换、尺寸获取、信息提取等功能。

### 7.3 logger_utils.py - 日志处理工具

提供了日志初始化、API密钥掩码、API调用记录等功能。

### 7.4 image_generator.py - 图片生成服务

实现了SiliconFlow API的调用逻辑，支持多种模型和参数配置。

### 7.5 main.py - FastAPI应用入口

定义了API路由，处理HTTP请求，调用图片生成服务，并记录日志。

## 8. 部署说明

### 8.1 安装依赖

```bash
pip install -r requirements.txt
```

### 8.2 运行应用

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 8.3 访问API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 9. 安全性考虑

- API密钥直接存储在配置文件中，注意保护配置文件的访问权限
- 图片处理过程中注意内存使用，限制最大上传图片数量
- 输入参数验证，防止恶意输入
- 日志中API密钥和图片base64使用掩码处理，保护数据安全
- 建议在生产环境中使用HTTPS

## 10. 扩展性考虑

- 支持添加更多模型配置
- 支持添加API请求限流
- 支持图片URL输入（除了文件上传）
- 支持生成历史记录查询
- 支持图片压缩和格式转换

## 11. 测试说明

### 11.1 单元测试

- 工具类测试：测试image_utils.py和logger_utils.py中的函数
- 运行命令：`python test_utils.py`

### 11.2 API测试

- 健康检查接口：`curl -s http://localhost:8000/health | jq`
- 图片生成接口：使用curl或Postman上传图片并测试

### 11.3 日志验证

- 检查日志文件是否生成
- 验证日志格式和内容完整性
- 验证日志增量更新功能

## 12. 总结

本项目实现了一个功能完整的SiliconFlow图片生成API服务，包括图片上传、API调用、结果返回和日志记录等功能。系统设计清晰，模块划分合理，具有良好的扩展性和安全性。通过详细的API文档和部署说明，方便用户快速使用和部署。