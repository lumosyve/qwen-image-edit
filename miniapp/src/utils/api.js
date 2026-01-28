// src/utils/api.js
// API工具函数，用于与Qwen/Qwen-Image-Edit-2509模型交互

/**
 * 将本地图片文件转换为base64格式
 * @param {string} filePath - 图片文件路径
 * @returns {Promise<string>} base64格式的图片数据
 */
export const convertImageToBase64 = (filePath) => {
  return new Promise((resolve, reject) => {
    // 获取文件信息
    uni.getFileSystemManager().readFile({
      filePath: filePath,
      encoding: 'base64',
      success: (res) => {
        // 获取文件扩展名
        const ext = filePath.split('.').pop().toLowerCase();
        let mimeType = 'jpeg';
        if (ext === 'png') {
          mimeType = 'png';
        } else if (ext === 'jpg' || ext === 'jpeg') {
          mimeType = 'jpeg';
        } else if (ext === 'webp') {
          mimeType = 'webp';
        }
        
        // 构造base64数据URL
        const base64Data = `data:image/${mimeType};base64,${res.data}`;
        resolve(base64Data);
      },
      fail: (error) => {
        reject(new Error(`图片转换失败: ${error.errMsg}`));
      }
    });
  });
};

/**
 * 调用图片编辑API
 * @param {Object} params - API参数
 * @param {string} params.prompt - 编辑指令
 * @param {string} params.image - 第一张图片(base64或URL)
 * @param {string} [params.image2] - 第二张图片(可选)
 * @param {string} [params.image3] - 第三张图片(可选)
 * @param {number} [params.cfg=7.0] - CFG值(0.1-20)
 * @param {number} [params.numInferenceSteps=20] - 推理步数(1-100)
 * @param {number} [params.seed] - 随机种子(0-9999999999)
 * @param {string} [params.negativePrompt] - 负向提示词
 * @returns {Promise} API响应Promise
 */
export const editImage = async (params) => {
  // 从环境变量或配置中获取API Key
  const apiKey = uni.getStorageSync('siliconFlowApiKey') || import.meta.env.VITE_SILICON_FLOW_API_KEY;
  
  if (!apiKey) {
    throw new Error('请配置SiliconFlow API Key');
  }
  
  // 构建请求数据
  const requestData = {
    model: 'Qwen/Qwen-Image-Edit-2509',
    prompt: params.prompt,
    image: params.image,
    ...(params.image2 && { image2: params.image2 }),
    ...(params.image3 && { image3: params.image3 }),
    ...(params.cfg && { cfg: params.cfg }),
    ...(params.numInferenceSteps && { num_inference_steps: params.numInferenceSteps }),
    ...(params.seed && { seed: params.seed }),
    ...(params.negativePrompt && { negative_prompt: params.negativePrompt })
  };
  
  // 发送请求
  try {
    const response = await uni.request({
      url: 'https://api.siliconflow.cn/v1/images/generations',
      method: 'POST',
      header: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      data: requestData
    });
    
    // 检查响应状态
    if (response.statusCode === 200) {
      return response.data;
    } else {
      throw new Error(`API请求失败: ${response.statusCode}, ${response.data?.error?.message || '未知错误'}`);
    }
  } catch (error) {
    throw new Error(`网络请求失败: ${error.message}`);
  }
};

/**
 * 保存图片到本地
 * @param {string} imageUrl - 图片URL
 * @returns {Promise} 保存结果Promise
 */
export const saveImage = async (imageUrl) => {
  try {
    // 下载图片到本地
    const downloadResult = await uni.downloadFile({
      url: imageUrl
    });
    
    if (downloadResult.statusCode === 200) {
      // 保存到相册
      const saveResult = await uni.saveImageToPhotosAlbum({
        filePath: downloadResult.tempFilePath
      });
      
      return saveResult;
    } else {
      throw new Error('图片下载失败');
    }
  } catch (error) {
    throw new Error(`保存图片失败: ${error.message}`);
  }
};

export default {
  editImage,
  saveImage
};