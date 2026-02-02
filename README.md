# 🚀 RK3588-HighPerf-Decoder

[![Platform](https://img.shields.io/badge/Platform-RK3588-blue.svg)](http://www.rock-chips.com/)
[![Python](https://img.shields.io/badge/Python-3.9-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Commercial%2FTrial-orange.svg)](#license)

**[English](#english) | [中文](#chinese)**

---

### 📖 简介
**RK3588-HighPerf-Decoder** 是一款专为 **瑞芯微 RK3588/RK3588S** 平台打造的高性能、工业级视频解码 SDK。

它深度整合了 **MPP**（媒体处理平台）和 **RGA**（光栅图形加速），实现了从解码到缩放、格式转换（NV12 -> BGR）的全流程硬件加速。通过 C++ 底层封装，它提供了极其简单的 **Python 接口**，在保持 Python 开发便捷性的同时，拥有 C++ 级别的极致性能。

本 SDK 非常适合 **边缘 AI 计算** 场景（如 YOLO 实时推理），能够在极低的 CPU 占用率下，稳定并发处理 **8-16 路** 1080P 视频流，将宝贵的 CPU 资源留给业务逻辑。

### ✨ 核心特性
* **硬解码:** 支持 H.264 (AVC) 和 H.265 (HEVC) 硬件解码 (VPU)。
* **硬加速:** 利用 RGA 硬件核心进行图像缩放和色彩空间转换，彻底释放 CPU。
* **零拷贝:** 优化的内存管理，极小化数据搬运开销。
* **高并发:** 实测支持 8~16 路 1080P RTSP 稳定拉流。
* **易使用:** 直接返回标准 NumPy 数组，无缝对接 OpenCV。
* **稳定性:** 内置断线重连、坏帧丢弃和错误恢复机制。

### ⚠️ 环境要求 
> 本 SDK 专为 **Python 3.9** 编译环境构建。
> **请勿** 在 Python 3.8、3.10 或 3.11 环境下运行，否则会导致 `Symbol not found` 或 段错误 (Core Dump)。

* **硬件:** Rockchip RK3588 / RK3588S (例如: 香橙派5, Rock 5B, 鲁班猫, 边缘计算盒子等)。
* **系统:** Linux (Ubuntu 22.04)。
* **Python:** **3.9.x** (必须严格匹配)。
* **网络:** 首次启动需要连接互联网（用于云端授权验证）。

### 🛠️ 安装与运行

1.  **下载包:**
    在页面下载相关代码。

2.  **解压并进入目录:**
    ```bash
    cd rk_demo
    ```

3.  **安装 Python 依赖:**
    ```bash
    pip3 install opencv-python numpy
    ```

4.  **运行演示程序:**
    **请务必使用 `run.sh` 脚本启动**，它会自动加载我们打包好的专用动态库，避免环境冲突。
    ```bash
    chmod +x run.sh
    ./run.sh
    ```

### 📝 Python 代码示例

```python
import rk_decoder_sy
import cv2
import time

# 初始化解码器 (支持 RTSP / RTMP / 本地文件)
# 请替换为您真实的流地址
rtsp_url = "rtsp://admin:123456@192.168.1.100/stream"
decoder = rk_decoder_sy.MppDecoder(rtsp_url)
decoder.start()

try:
    while True:
        # 读取一帧 (返回 BGR 格式的 numpy 数组)
        frame = decoder.read()
        
        if frame is not None and frame.size > 0:
            # 显示画面 (在无桌面环境请注释掉 imshow)
            cv2.imshow("RK3588 Stream", frame)
        else:
            time.sleep(0.01)
            
        if cv2.waitKey(1) == 27: # 按 ESC 退出
            break
finally:
    decoder.stop()
```
### 授权与试用模式
本 SDK 内置了自动授权管理系统：
第 1 - 4 路: 免费试用 (纯净模式)。画面无水印，性能无限制，供开发者测试评估。
第 5 路及以上: 演示模式。画面会出现 "TRIAL MODE" 水印和红叉。
商业授权: 如需解锁无限路数并去除水印，请联系作者获取商业授权。

📧 联系方式 (Contact)
如果您对 商业授权 感兴趣，或在集成过程中遇到问题，欢迎联系：
Email: 2250157715@qq.com
WeChat (微信扫码):
<img src="wechat.jpg" width="200" alt="WeChat QR Code">
Issues: 如遇 Bug 或有功能建议，请提交 GitHub Issues。
