# Qwen/Qwen-Image-Edit-2509 API 文档

## 概述

Qwen/Qwen-Image-Edit-2509 是 SiliconFlow 提供的图片编辑和生成模型，支持单图和多图编辑功能，能够基于文本提示词对上传的图片进行编辑和生成。

## 基本信息

- **API 端点**: `POST https://api.siliconflow.cn/v1/images/generations`
- **模型名称**: `Qwen/Qwen-Image-Edit-2509`
- **认证方式**: Bearer Token
- **Content-Type**: `application/json`

## 请求参数

### Body 参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|:---|:---|:---|:---|:---|
| **model** | string | 是 | - | 固定值：`"Qwen/Qwen-Image-Edit-2509"` |
| **prompt** | string | 是 | - | 生成图片的文本提示词，描述你想要的图片效果 |
| **negative_prompt** | string | 否 | - | 负向提示词，描述不希望在图片中出现的内容 |
| **image** | enum\<string\> | 否 | - | 第一张图片，支持 base64 格式或 URL。格式：`data:image/png;base64, XXX` 或 `img_url` |
| **image2** | enum\<string\> | 否 | - | 第二张图片（同上），用于多图编辑场景 |
| **image3** | enum\<string\> | 否 | - | 第三张图片（同上），用于多图编辑场景 |
| **num_inference_steps** | integer | 否 | 20 | 推理步数，范围：1-100。值越高生成质量越好，但耗时越长 |
| **cfg** | number | 否 | - | CFG (Classifier-Free Guidance)，平衡精度和创造力，范围：0.1-20。文本生成场景需大于1 |

### 重要说明

- **image_size 参数**: `Qwen/Qwen-Image-Edit-2509` **不支持** `image_size` 参数，图片尺寸由模型自动处理
- **多图支持**: 该模型最多支持 3 张图片输入（image, image2, image3），用于复杂的多图编辑场景
- **图片格式**: 支持的图片格式包括 PNG、JPEG 等，建议使用高质量图片以获得最佳效果

## 响应格式

### 成功响应 (200 OK)

```json
{
  "images": [
    {
      "url": "https://生成的图片URL"
    }
  ],
  "timings": {
    "inference": 1234
  },
  "seed": 1234567890
}
```

### 响应字段说明

| 字段名 | 类型 | 说明 |
|:---|:---|:---|
| **images** | object[] | 生成的图片列表 |
| images[].url | string | 生成图片的 URL 链接 |
| **timings** | object | 时间统计信息 |
| timings.inference | integer | 推理耗时（毫秒） |
| **seed** | integer | 生成的随机种子值，可用于复现结果 |

### Response Headers

- `x-siliconcloud-trace-id`: 唯一请求追踪 ID，用于日志查询和问题排查

## 使用示例

### 示例 1：单图编辑

将上传的图片根据提示词进行编辑：

```bash
curl --request POST \
  --url https://api.siliconflow.cn/v1/images/generations \
  --header 'Authorization: Bearer YOUR-API-KEY' \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "Qwen/Qwen-Image-Edit-2509",
  "prompt": "将图片中的天空变成夕阳橙红色，增加云层",
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "num_inference_steps": 30,
  "cfg": 7.0
}'
```

### 示例 2：多图编辑（图片融合）

使用多张图片进行融合和编辑：

```bash
curl --request POST \
  --url https://api.siliconflow.cn/v1/images/generations \
  --header 'Authorization: Bearer YOUR-API-KEY' \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "Qwen/Qwen-Image-Edit-2509",
  "prompt": "将两张图片融合，创造一个梦幻的场景",
  "image": "https://example.com/image1.jpg",
  "image2": "https://example.com/image2.jpg",
  "num_inference_steps": 25,
  "cfg": 7.5
}'
```

### 示例 3：带负向提示词的编辑

```bash
curl --request POST \
  --url https://api.siliconflow.cn/v1/images/generations \
  --header 'Authorization: Bearer YOUR-API-KEY' \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "Qwen/Qwen-Image-Edit-2509",
  "prompt": "为图片添加现代简约风格",
  "negative_prompt": "模糊，低质量，噪点，失真",
  "image": "data:image/png;base64,iVBORw0KGgo...",
  "num_inference_steps": 40
}'
```

### 示例 4：JavaScript/Node.js 调用

```javascript
const axios = require('axios');

const apiKey = 'YOUR-API-KEY';

const imageData = {
  model: 'Qwen/Qwen-Image-Edit-2509',
  prompt: '将照片背景改为蓝天白云',
  image: 'data:image/jpeg;base64,/9j/4AAQSkZJRg...',
  num_inference_steps: 30,
  cfg: 7.0
};

axios.post('https://api.siliconflow.cn/v1/images/generations', imageData, {
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  }
})
.then(response => {
  console.log('生成的图片URL:', response.data.images[0].url);
  console.log('推理耗时:', response.data.timings.inference, '毫秒');
})
.catch(error => {
  console.error('请求失败:', error.response?.data || error.message);
});
```

### 示例 5：Python 调用

```python
import requests
import base64

def edit_image(api_key, prompt, image_path, negative_prompt=None):
    # 读取图片并转换为 base64
    with open(image_path, 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode()

    # 构建请求数据
    data = {
        "model": "Qwen/Qwen-Image-Edit-2509",
        "prompt": prompt,
        "image": f"data:image/jpeg;base64,{image_base64}",
        "num_inference_steps": 30,
        "cfg": 7.0
    }

    if negative_prompt:
        data["negative_prompt"] = negative_prompt

    # 发送请求
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.siliconflow.cn/v1/images/generations",
        json=data,
        headers=headers
    )

    if response.status_code == 200:
        result = response.json()
        return {
            "image_url": result["images"][0]["url"],
            "inference_time": result["timings"]["inference"],
            "seed": result["seed"]
        }
    else:
        raise Exception(f"请求失败: {response.status_code}, {response.text}")

# 使用示例
api_key = "YOUR-API-KEY"
result = edit_image(
    api_key,
    prompt="将照片风格转换为油画风格",
    image_path="input.jpg",
    negative_prompt="模糊，低质量"
)
print(f"生成的图片: {result['image_url']}")
print(f"推理耗时: {result['inference_time']} 毫秒")
```

## 参数调优建议

### num_inference_steps（推理步数）

| 值范围 | 效果 | 推荐场景 |
|:---|:---|:---|
| 10-20 | 速度快，质量一般 | 快速预览、原型设计 |
| 20-30 | 速度适中，质量较好 | 日常使用（推荐值） |
| 30-50 | 速度较慢，质量优秀 | 精细编辑、商业用途 |
| 50-100 | 速度最慢，质量最佳 | 最终成品、高质量需求 |

### cfg（Classifier-Free Guidance）

| 值范围 | 效果 | 推荐场景 |
|:---|:---|:---|
| 3.0-5.0 | 更具创造性和多样性 | 艺术创作、探索性编辑 |
| 5.0-7.0 | 平衡精度和创造力（推荐）| 日常编辑、场景优化 |
| 7.0-10.0 | 更严格匹配文本提示 | 精确编辑、细节修改 |
| 10.0-20.0 | 极度严格匹配，可能降低多样性 | 特定需求、精确控制 |

## 常见应用场景

### 1. 图像风格转换
```json
{
  "model": "Qwen/Qwen-Image-Edit-2509",
  "prompt": "将照片转换为梵高星空风格",
  "image": "data:image/jpeg;base64,..."
}
```

### 2. 背景替换
```json
{
  "model": "Qwen/Qwen-Image-Edit-2509",
  "prompt": "将背景替换为海滩日落场景",
  "image": "data:image/jpeg;base64,..."
}
```

### 3. 物体添加/移除
```json
{
  "model": "Qwen/Qwen-Image-Edit-2509",
  "prompt": "在画面左上角添加一只飞鸟",
  "negative_prompt": "不需要添加其他元素",
  "image": "data:image/jpeg;base64,..."
}
```

### 4. 多图融合
```json
{
  "model": "Qwen/Qwen-Image-Edit-2509",
  "prompt": "将两张图片的自然景观完美融合",
  "image": "https://example.com/mountain.jpg",
  "image2": "https://example.com/lake.jpg"
}
```

### 5. 季节变换
```json
{
  "model": "Qwen/Qwen-Image-Edit-2509",
  "prompt": "将春天的景色转换为秋天的金黄色调",
  "image": "data:image/jpeg;base64,..."
}
```

## 注意事项

### 1. URL 有效期
- 生成的图片 URL **仅有效一小时**
- 请务必及时下载并存储图片，避免链接过期导致无法访问
- 建议在获取 URL 后立即下载到本地存储

### 2. 图片格式要求
- 支持 PNG、JPEG 等常见图片格式
- 建议使用高质量、高分辨率的原始图片
- 图片大小建议在 10MB 以内

### 3. 提示词编写技巧
- **具体性**: 使用具体、明确的描述词
- **细节**: 添加细节描述可以获得更好的效果
- **顺序**: 重要元素放在提示词前面
- **语言**: 建议使用中文或英文，避免混合使用

**好的提示词示例**:
```
"将天空改为紫罗兰色渐变，增加星光点缀，营造梦幻氛围"
```

**不好的提示词示例**:
```
"改一下天空" （太模糊）
```

### 4. 负向提示词的使用
负向提示词可以帮助你避免不需要的效果：
```json
{
  "negative_prompt": "模糊，低质量，噪点，失真，水印，文字"
}
```

### 5. 模型限制
- 不支持 `image_size` 参数
- 不支持 `batch_size` 参数（每次只能生成一张图片）
- 不支持 `guidance_scale` 参数（请使用 `cfg` 替代）

### 6. 性能优化
- `num_inference_steps` 参数对性能影响最大，建议从 20 开始测试
- 如果不需要极高的精度，可以降低到 15-20 以提高速度
- 使用负向提示词可以减少重复尝试，提高成功率

## 错误处理

### 常见错误码

| HTTP 状态码 | 错误类型 | 说明 |
|:---|:---|:---|
| 400 | Bad Request | 请求参数错误，如缺少必填参数、参数格式错误 |
| 401 | Unauthorized | API Key 无效或过期 |
| 429 | Too Many Requests | 请求频率超限 |
| 500 | Internal Server Error | 服务器内部错误 |

### 错误响应示例

```json
{
  "error": {
    "message": "Invalid API key",
    "type": "invalid_request_error",
    "param": "Authorization"
  }
}
```

### 错误处理建议

```javascript
try {
  const response = await axios.post(apiUrl, data, config);
  // 处理成功响应
} catch (error) {
  if (error.response) {
    // 服务器返回了错误状态码
    console.error('错误状态码:', error.response.status);
    console.error('错误信息:', error.response.data);
  } else if (error.request) {
    // 请求已发送但没有收到响应
    console.error('网络错误，请检查连接');
  } else {
    // 其他错误
    console.error('请求配置错误:', error.message);
  }
}
```

## 最佳实践

### 1. 提示词工程

**使用修饰词增强效果**:
```
"高质量的" + "精致的" + "专业的" + 主要描述
```

**使用风格关键词**:
- 摄影风格：`摄影`、`写实`、`超高清`
- 艺术风格：`油画`、`水彩`、`素描`
- 光照：`柔和光线`、`戏剧性光照`、`自然光`
- 构图：`黄金分割`、`对称`、`三分法`

### 2. 迭代优化

1. 第一次调用使用基本提示词
2. 查看结果，调整提示词或参数
3. 使用负向提示词排除不需要的效果
4. 多次迭代直到满意

### 3. 批量处理

如果需要处理多张图片，建议：
- 使用异步请求并发处理
- 实现请求队列避免频率限制
- 添加重试机制处理失败请求

### 4. 图片存储

- 获取图片 URL 后立即下载
- 使用有意义的文件名命名
- 保留原始图片作为备份

## 计费说明

- 具体计费方式请参考 SiliconFlow 官方计费文档
- 不同的 `num_inference_steps` 值可能影响费用
- 建议在正式使用前先进行小规模测试

## 技术支持

- **官方文档**: https://docs.siliconflow.cn/
- **API Key 获取**: 登录 SiliconFlow 控制台获取
- **问题反馈**: 通过官方渠道提交工单

## 更新日志

- 2025-01: Qwen/Qwen-Image-Edit-2509 模型上线
- 支持多图编辑功能（最多3张图片）
- 优化推理速度和质量
