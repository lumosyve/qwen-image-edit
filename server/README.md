# SiliconFlow图片生成API

## 项目简介

本项目实现了一个基于FastAPI的RESTful API服务，允许用户通过HTTP请求上传图片、输入提示文案，调用SiliconFlow模型API并返回生成结果。同时，系统会记录API调用的详细信息，包括API密钥、输入图片、输出图片和总耗时。

## 技术栈

- **Web框架**：FastAPI
- **API调用**：requests
- **图片处理**：Pillow
- **数据验证**：Pydantic
- **日志记录**：Python标准库logging + python-json-logger

## 目录结构

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

## 安装步骤

1. 克隆或下载项目代码

2. 安装依赖

```bash
pip install -r requirements.txt
```

## 运行方式

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API文档

### 访问地址

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 健康检查接口

```
GET /health
```

### 图片生成接口

```
POST /generate-images
```

**请求参数**:

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| files | file[] | 是 | 上传的图片文件列表，支持PNG、JPG、JPEG格式 |
| model | string | 否 | 模型名称，默认：Qwen/Qwen-Image-Edit-2509 |
| prompt | string | 是 | 提示词 |
| negative_prompt | string | 否 | 负面提示词 |
| image_size | string | 否 | 图片尺寸 |
| batch_size | integer | 否 | 批量大小，1-4 |
| seed | integer | 否 | 生成种子，0-9999999999 |
| num_inference_steps | integer | 否 | 推理步数，1-100 |
| guidance_scale | float | 否 | 引导比例，0.0-20.0（仅Kolor模型） |
| cfg | float | 否 | CFG值，0.1-20.0（仅Qwen模型） |

## 测试说明

### 单元测试

```bash
python test_utils.py
```

### API测试

使用curl或Postman测试API接口：

```bash
# 测试健康检查接口
curl -s http://localhost:8000/health | jq

# 测试图片生成接口
curl -X POST "http://localhost:8000/generate-images" -F "files=@test_image.png" -F "model=Qwen/Qwen-Image-Edit-2509" -F "prompt=test prompt"
```

## 配置说明

所有配置项都在`config.py`文件中定义，包括：

- API密钥
- 模型配置
- 图片尺寸配置
- 日志配置

## 日志说明

### 日志文件路径

`logs/image_generation.log`

### 日志内容

- 每次API调用都会记录详细信息，包括API密钥、输入图片、输出图片和总耗时
- 日志采用JSON格式，便于后续分析
- API密钥使用掩码处理，仅显示前4位和后4位
- 图片base64编码仅显示前100字符，保护数据安全
- 支持增量更新，每次调用都追加到日志文件

## 安全性考虑

- API密钥直接存储在配置文件中，注意保护配置文件的访问权限
- 日志中API密钥和图片base64使用掩码处理，保护数据安全
- 输入参数验证，防止恶意输入
- 建议在生产环境中使用HTTPS

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License
