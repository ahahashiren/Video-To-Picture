# -*- coding: utf-8 -*-

import cv2
import os
import time
from tqdm.rich import tqdm
import warnings
from tqdm.rich import TqdmExperimentalWarning

# 忽略 TqdmExperimentalWarning 警告
warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)


class VTP:
    def __init__(self, file, gen):
        self.file = file
        self.gen = gen

    def process(self):
        # 创建目标文件夹（如果不存在）
        if not os.path.exists(self.gen):
            os.makedirs(self.gen)

        # 打开视频文件
        cap = cv2.VideoCapture(self.file)
        if not cap.isOpened():
            print(f"无法打开视频文件: {self.file}")
            return

        # 获取视频总帧数
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # 记录开始时间
        start_time = time.time()

        # 使用 tqdm.rich 创建更丰富的进度条
        frame_count = 0
        with tqdm(total=total_frames, desc="处理进度", unit="帧", ncols=100, colour="green") as pbar:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # 生成帧文件名
                frame_filename = f"{self.file}_{frame_count}.jpg"
                frame_path = os.path.join(self.gen, frame_filename)

                # 保存帧
                cv2.imwrite(frame_path, frame)
                frame_count += 1

                # 更新进度条
                pbar.update(1)

        # 记录结束时间
        end_time = time.time()
        processing_time = end_time - start_time

        cap.release()
        print(f"处理完成，共提取 {frame_count} 帧到 {self.gen}")
        print(f"处理耗时: {processing_time:.2f} 秒")

# 使用示例
if __name__ == "__main__":
    file = input("视频路径：")
    gen = input("保存路径：")
    vtp = VTP(file, gen)
    vtp.process()
    print(vtp)
