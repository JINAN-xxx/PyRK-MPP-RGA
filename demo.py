import sys
import os
import time
import cv2
import numpy as np
import multiprocessing
import signal

# ==========================================
# 1. 路径设置
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(current_dir, "build")
sys.path.append(build_dir)

# ==========================================
# 2. 单个解码进程的工作函数
# ==========================================
def worker_process(cam_id, rtsp_url, stop_event):
    """
    stop_event: 用于接收主进程的停止信号
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    try:
        import rk_decoder_sy
    except ImportError as e:
        print(f"[CAM {cam_id}] 导入失败: {e}")
        return

    print(f"[CAM {cam_id}] 正在初始化... (PID: {os.getpid()})")
    
    decoder = None
    try:
        decoder = rk_decoder_sy.MppDecoder(rtsp_url)
        decoder.start()
        print(f"[CAM {cam_id}] 拉流启动成功！")
    except RuntimeError as e:
        print(f"[CAM {cam_id}] 启动失败: {e}")
        return

    frame_count = 0
    start_time = time.time()
    
    enable_save = True 
    last_save_time = time.time()

    try:
        while not stop_event.is_set():
            frame = decoder.read()

            if frame is None or frame.size == 0:
                time.sleep(0.01)
                continue

            frame_count += 1
            if frame_count % 100 == 0:
                elapsed = time.time() - start_time
                fps = 100 / (elapsed + 1e-6)
                print(f"[CAM {cam_id}] FPS: {fps:.2f} | {frame.shape[1]}x{frame.shape[0]}")
                start_time = time.time()

            # 每 5 秒保存一次截图
            if enable_save and (time.time() - last_save_time > 5.0):
                # 文件名带上 cam_id，互不冲突
                # 覆盖保存，始终看最新的画面
                filename = f"cam_{cam_id}_snapshot.jpg"
                cv2.imwrite(filename, frame)
                print(f"[CAM {cam_id}] 截图已保存 -> {filename}")
                last_save_time = time.time()

    except Exception as e:
        print(f"[CAM {cam_id}] 发生异常: {e}")
    
    finally:
        if decoder:
            print(f"[CAM {cam_id}] 正在释放资源...")
            decoder.stop()
        print(f"[CAM {cam_id}] 进程已退出")

# ==========================================
# 3. 主进程管理
# ==========================================
def main():
    base_url = "rtsp://192.168.31.151:8554/mystream1"
    
    # 开启 9 路
    rtsp_list = [base_url] * 9 
    
    processes = []
    stop_event = multiprocessing.Event()

    print(f"准备启动 {len(rtsp_list)} 路视频解码进程...")
    
    for i, url in enumerate(rtsp_list):
        cam_id = i + 1
        p = multiprocessing.Process(target=worker_process, args=(cam_id, url, stop_event))
        p.daemon = True 
        processes.append(p)
        p.start()
        time.sleep(0.5) 

    print("所有进程已启动！按 Ctrl+C 停止所有任务...")

    try:
        while True:
            time.sleep(1)
            if all(not p.is_alive() for p in processes):
                print("所有子进程都已结束，主进程退出。")
                break

    except KeyboardInterrupt:
        print("收到 Ctrl+C，正在通知子进程优雅退出...")
        stop_event.set()
        
        for p in processes:
            p.join(timeout=3)
        
        for i, p in processes:
            if p.is_alive():
                print(f"[CAM {i+1}] 响应超时，强制终止！")
                p.terminate()
        
        print("✅ 所有任务已清理完毕。")

if __name__ == "__main__":
    try:
        multiprocessing.set_start_method('fork')
    except RuntimeError:
        pass
    main()