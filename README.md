# 音频视频分割工具 (VoiceSplit)

一个基于Python的音频视频分割工具，能够自动检测音频中的静音段落，进行分割。

## 🎯 功能特点

- 🎵 **音频分割**: 自动检测音频中的静音段落，按有声内容进行分割
- 🎬 **视频支持**: 支持从视频文件中提取音频进行处理
- 🎛️ **参数可调**: 支持自定义静音检测阈值、最小静音长度等参数
- 📁 **批量处理**: 支持指定输出目录，便于文件管理
- 🔧 **多格式支持**: 支持常见的音频和视频格式

## 📋 支持的文件格式

### 音频格式
- WAV, MP3, FLAC, AAC, OGG, M4A

### 视频格式
- MP4, AVI, MOV, MKV, WMV, FLV (提取音频轨道)

## 🛠️ 安装要求

### 系统要求
- Python 3.8+
- FFmpeg (必需，用于处理音频/视频格式)

### 安装FFmpeg

**Windows:**
```bash
# 方法1: 使用winget (推荐)
winget install ffmpeg

# 方法2: 使用Chocolatey
choco install ffmpeg

# 方法3: 使用Conda
conda install ffmpeg

# 方法4: 直接下载
# 从 https://ffmpeg.org/download.html 下载并添加到PATH
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg
```

**验证FFmpeg安装:**
```bash
ffmpeg -version
```

### 安装Python依赖
```bash
pip install -r requirements.txt
```

## 🚀 使用方法

### 基本用法

**处理音频文件:**
```bash
python voice_splitter.py audio.mp3
```

**处理视频文件:**
```bash
python voice_splitter.py video.mp4
```

### 指定输出目录
```bash
python voice_splitter.py input.mp4 -o output_folder
```

### 自定义参数
```bash
python voice_splitter.py input.mp4 \
    -o output_folder \
    --min-silence 1000 \
    --silence-thresh -50 \
    --keep-silence 300
```

### 📊 参数说明

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `input_file` | - | 必需 | 输入音频/视频文件路径 |
| `--output` | `-o` | output | 输出目录 |
| `--min-silence` | - | 500 | 最小静音长度(毫秒) |
| `--silence-thresh` | - | -40 | 静音阈值(dBFS) |
| `--keep-silence` | - | 200 | 保留的静音长度(毫秒) |

### 🧠 模型选择指南

| 模型 | 参数量 | VRAM需求 | 速度 | 准确度 | 适用场景 |
|------|--------|----------|------|--------|----------|
| tiny | 39M | ~1GB | 最快 | 较低 | 快速预览 |
| base | 74M | ~1GB | 快 | 良好 | 日常使用 |
| small | 244M | ~2GB | 中等 | 很好 | 平衡性能 |
| medium | 769M | ~5GB | 慢 | 优秀 | 高质量需求 |
| large | 1550M | ~10GB | 最慢 | 最佳 | 专业转录 |

## 💡 使用示例

### 示例1: 处理播客视频
```bash
python voice_splitter.py podcast.mp4 -o podcast_segments -m small
```
输出: `podcast_segments/podcast_001_[转录文字].wav`

### 示例2: 处理会议录音
```bash
python voice_splitter.py meeting.wav -o meeting_segments --min-silence 1000 --silence-thresh -45
```

### 示例3: 高质量视频转录
```bash
python voice_splitter.py interview.mp4 -o interview_segments -m large
```

### 示例4: 处理音乐视频
```bash
python voice_splitter.py music_video.mkv -o music_segments --min-silence 2000 --silence-thresh -30
```

### 示例5: 批量处理不同格式
```bash
# 处理MP4视频
python voice_splitter.py "C:\Videos\lecture.mp4" -o "C:\Output\lecture"

# 处理MP3音频
python voice_splitter.py "C:\Audio\podcast.mp3" -o "C:\Output\podcast"

# 处理AVI视频
python voice_splitter.py "C:\Videos\movie.avi" -o "C:\Output\movie"
```

## ⚙️ 工作原理

1. **文件加载**: 使用pydub和FFmpeg加载音频/视频文件
2. **音频提取**: 从视频文件中提取音频轨道(如果需要)
3. **静音检测**: 基于音量阈值检测静音段落
4. **音频分割**: 按静音段落分割音频
5. **文件保存**: 将分割后的音频片段保存为WAV格式

## 🔧 技术栈

- **Python 3.8+**: 主要编程语言
- **PyDub**: 音频处理和格式转换
- **FFmpeg**: 音视频编解码支持

## ⚠️ 注意事项

1. **首次运行**: Whisper会自动下载模型文件，可能需要一些时间
2. **内存需求**: 较大的模型(medium/large)需要更多内存和计算时间
3. **FFmpeg依赖**: 确保FFmpeg已正确安装并添加到系统PATH
4. **文件命名**: 输出文件名会自动清理特殊字符，确保文件系统兼容性
5. **视频处理**: 只提取音频轨道，不处理视频内容

## 🔍 故障排除

### 常见问题

**Q: 提示找不到FFmpeg**
```
A: 请确保FFmpeg已安装并添加到系统PATH环境变量
   验证命令: ffmpeg -version
```

**Q: 分割效果不理想**
```
A: 调整静音检测参数(`--min-silence`, `--silence-thresh`)
```

**Q: 处理大文件时速度慢**
```
A: 可以先转换为WAV格式再处理，或调整静音检测参数
```

**Q: 视频文件无法处理**
```
A: 1. 确保FFmpeg已正确安装
   2. 检查视频文件是否损坏
   3. 尝试转换为支持的格式
```

## ⚡ 性能优化建议

1. **文件格式**: 使用WAV格式可获得最佳处理速度

2. **参数调整**: 根据音频特点调整静音检测参数
   - 对于语音间隔较短的音频，减小`--min-silence`值
   - 对于背景噪音较大的音频，调整`--silence-thresh`值

3. **批量处理**: 处理多个文件时建议使用脚本批量调用

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📝 更新日志

### v2.0.0 (2024-01-15)
- ✨ 简化版本发布
- 🎵 支持基于静音检测的音频分割
- 🎬 支持音频和视频文件处理
- ⚙️ 可自定义静音检测参数
- 📚 简化的文档和使用示例
- 🚀 移除语音转文字功能，提升处理速度