# 音频分割工具 (VoiceSplit)

一个基于Python的智能音频分割工具，能够自动检测音频中的有声段落，进行分割，并使用AI语音识别技术为每个段落生成描述性的文件名。

## 功能特点

- 🎵 **智能音频分割**: 自动检测音频中的有声和无声段落
- 🤖 **AI语音识别**: 使用OpenAI Whisper模型进行高精度语音转文字
- 📁 **智能命名**: 根据语音内容自动生成描述性文件名
- 🎬 **多格式支持**: 支持音频和视频文件（MP3, WAV, MP4, AVI等）
- ⚙️ **参数可调**: 可自定义静音检测阈值和分割参数
- 🚀 **易于使用**: 简单的命令行界面

## 安装要求

### 系统要求
- Python 3.8 或更高版本
- FFmpeg（用于处理多种音频格式）

### 安装FFmpeg

**Windows:**
```bash
# 使用Chocolatey
choco install ffmpeg

# 或使用Scoop
scoop install ffmpeg

# 或手动下载: https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg
```

### 安装Python依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
python voice_splitter.py input_audio.mp3
```

### 高级用法

```bash
# 指定输出目录
python voice_splitter.py input_audio.mp3 -o my_output_folder

# 使用更大的Whisper模型以获得更好的识别精度
python voice_splitter.py input_audio.mp3 -m large

# 调整静音检测参数
python voice_splitter.py input_audio.mp3 --min-silence 1000 --silence-thresh -35
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input_file` | 输入音频/视频文件路径 | 必需 |
| `-o, --output` | 输出目录 | `output` |
| `-m, --model` | Whisper模型大小 | `base` |
| `--min-silence` | 最小静音长度(毫秒) | `500` |
| `--silence-thresh` | 静音阈值(dBFS) | `-40` |
| `--keep-silence` | 保留的静音长度(毫秒) | `200` |

### Whisper模型选择

| 模型 | 大小 | 内存需求 | 速度 | 精度 |
|------|------|----------|------|------|
| `tiny` | 39M | ~1GB | 最快 | 较低 |
| `base` | 74M | ~1GB | 快 | 中等 |
| `small` | 244M | ~2GB | 中等 | 良好 |
| `medium` | 769M | ~5GB | 慢 | 很好 |
| `large` | 1550M | ~10GB | 最慢 | 最佳 |

## 使用示例

### 示例1：处理播客音频

```bash
python voice_splitter.py podcast_episode.mp3 -o podcast_segments -m small
```

输出文件示例：
```
podcast_segments/
├── podcast_episode_001_欢迎收听今天的节目.wav
├── podcast_episode_002_今天我们要讨论的话题是.wav
├── podcast_episode_003_首先让我们来看看.wav
└── ...
```

### 示例2：处理会议录音

```bash
python voice_splitter.py meeting_record.mp4 -o meeting_clips --min-silence 1000 --silence-thresh -35
```

### 示例3：处理语音备忘录

```bash
python voice_splitter.py voice_memo.wav -o memo_clips -m tiny
```

## 工作原理

1. **音频加载**: 使用PyDub加载音频文件，支持多种格式
2. **静音检测**: 基于音量阈值检测静音段落
3. **音频分割**: 在静音处分割音频，生成独立的音频段落
4. **语音识别**: 使用Whisper模型将每个音频段落转换为文字
5. **文件命名**: 根据转录文字生成描述性文件名
6. **文件保存**: 将分割后的音频保存为WAV格式

## 技术栈

- **[OpenAI Whisper](https://github.com/openai/whisper)**: 语音识别 <mcreference link="https://github.com/openai/whisper" index="4">4</mcreference>
- **[PyDub](https://github.com/jiaaro/pydub)**: 音频处理 <mcreference link="https://blog.csdn.net/crazyjinks/article/details/148402968" index="2">2</mcreference>
- **[Librosa](https://librosa.org/)**: 音频分析 <mcreference link="https://blog.csdn.net/gitblog_00080/article/details/136799057" index="1">1</mcreference>
- **NumPy & SciPy**: 数值计算

## 注意事项

1. **首次运行**: 第一次使用时，Whisper会自动下载模型文件，可能需要一些时间
2. **内存使用**: 较大的模型需要更多内存，请根据系统配置选择合适的模型
3. **处理时间**: 语音识别需要时间，较长的音频文件可能需要等待
4. **文件格式**: 输出文件统一为WAV格式，确保兼容性
5. **中文支持**: 工具针对中文语音进行了优化

## 故障排除

### 常见问题

**Q: 提示找不到FFmpeg**
A: 请确保FFmpeg已正确安装并添加到系统PATH中

**Q: 内存不足错误**
A: 尝试使用更小的Whisper模型（如tiny或base）

**Q: 识别精度不高**
A: 尝试使用更大的模型（如medium或large），或调整静音检测参数

**Q: 分割效果不理想**
A: 调整`--min-silence`和`--silence-thresh`参数

### 参数调优建议

- **安静环境录音**: `--silence-thresh -45`
- **嘈杂环境录音**: `--silence-thresh -30`
- **快速语音**: `--min-silence 300`
- **慢速语音**: `--min-silence 800`

## 许可证

本项目基于MIT许可证开源。

## 贡献

欢迎提交Issue和Pull Request来改进这个工具！

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本的音频分割和语音识别功能
- 支持多种音频格式
- 智能文件命名功能