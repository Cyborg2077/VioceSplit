#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频分割工具
功能：
1. 自动检测音频中的有声和无声段落
2. 按照有声段落进行分割
3. 保存分割后的音频文件
"""

import os
import argparse
from pathlib import Path
from typing import List

from pydub import AudioSegment
from pydub.silence import split_on_silence


class VoiceSplitter:
    """音频分割器类"""
    
    def __init__(self, output_dir: str = "output"):
        """
        初始化音频分割器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"输出目录: {self.output_dir}")
    
    def load_audio(self, file_path: str) -> AudioSegment:
        """
        加载音频文件
        
        Args:
            file_path: 音频文件路径
            
        Returns:
            AudioSegment对象
        """
        print(f"正在加载音频文件: {file_path}")
        
        # 使用pydub加载音频，支持多种格式
        audio = AudioSegment.from_file(file_path)
        
        # 转换为单声道以简化处理
        if audio.channels > 1:
            audio = audio.set_channels(1)
            
        print(f"音频加载完成 - 时长: {len(audio)/1000:.2f}秒, 采样率: {audio.frame_rate}Hz")
        return audio
    
    def detect_voice_segments(self, audio: AudioSegment, 
                            min_silence_len: int = 500,
                            silence_thresh: int = -40,
                            keep_silence: int = 200) -> List[AudioSegment]:
        """
        检测音频中的有声段落
        
        Args:
            audio: 音频对象
            min_silence_len: 最小静音长度(毫秒)
            silence_thresh: 静音阈值(dBFS)
            keep_silence: 保留的静音长度(毫秒)
            
        Returns:
            分割后的音频段落列表
        """
        print("正在检测有声段落...")
        
        # 使用pydub的split_on_silence函数进行分割
        segments = split_on_silence(
            audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh,
            keep_silence=keep_silence
        )
        
        # 过滤掉过短的段落(小于1秒)
        min_segment_len = 1000  # 1秒
        segments = [seg for seg in segments if len(seg) >= min_segment_len]
        
        print(f"检测到 {len(segments)} 个有声段落")
        return segments
    

    
    def process_audio(self, input_file: str, 
                     min_silence_len: int = 500,
                     silence_thresh: int = -40,
                     keep_silence: int = 200) -> List[str]:
        """
        处理音频文件，进行分割和转录
        
        Args:
            input_file: 输入音频文件路径
            min_silence_len: 最小静音长度(毫秒)
            silence_thresh: 静音阈值(dBFS)
            keep_silence: 保留的静音长度(毫秒)
            
        Returns:
            输出文件路径列表
        """
        # 加载音频
        audio = self.load_audio(input_file)
        
        # 检测有声段落
        segments = self.detect_voice_segments(
            audio, min_silence_len, silence_thresh, keep_silence
        )
        
        if not segments:
            print("未检测到有声段落")
            return []
        
        output_files = []
        input_name = Path(input_file).stem
        
        print("开始处理各个段落...")
        
        for i, segment in enumerate(segments, 1):
            print(f"\n处理第 {i}/{len(segments)} 个段落 (时长: {len(segment)/1000:.2f}秒)")
            
            # 生成文件名
            filename = f"{input_name}_{i:03d}.wav"
            output_path = self.output_dir / filename
            
            # 保存音频段落
            segment.export(str(output_path), format="wav")
            output_files.append(str(output_path))
            
            print(f"已保存: {output_path}")
        
        print(f"\n处理完成！共生成 {len(output_files)} 个文件")
        return output_files


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="音频分割工具")
    parser.add_argument("input_file", help="输入音频/视频文件路径")
    parser.add_argument("-o", "--output", default="output", help="输出目录 (默认: output)")
    parser.add_argument("--min-silence", type=int, default=500,
                       help="最小静音长度(毫秒) (默认: 500)")
    parser.add_argument("--silence-thresh", type=int, default=-40,
                       help="静音阈值(dBFS) (默认: -40)")
    parser.add_argument("--keep-silence", type=int, default=200,
                       help="保留的静音长度(毫秒) (默认: 200)")
    
    args = parser.parse_args()
    
    # 检查输入文件是否存在
    if not os.path.exists(args.input_file):
        print(f"错误: 输入文件不存在: {args.input_file}")
        return
    
    # 创建分割器
    splitter = VoiceSplitter(output_dir=args.output)
    
    try:
        # 处理音频
        output_files = splitter.process_audio(
            input_file=args.input_file,
            min_silence_len=args.min_silence,
            silence_thresh=args.silence_thresh,
            keep_silence=args.keep_silence
        )
        
        print(f"\n=== 处理完成 ===")
        print(f"输入文件: {args.input_file}")
        print(f"输出目录: {args.output}")
        print(f"生成文件数: {len(output_files)}")
        
    except Exception as e:
        print(f"处理失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()