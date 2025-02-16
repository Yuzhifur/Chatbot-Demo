# Chatbot-Demo

A chatbot demo based on DeepSeek API, implemented with Gradio.

## 项目简介

这是一个基于 DeepSeek API 的聊天机器人演示项目，使用 Gradio 构建用户界面。用户可以通过该界面与 DeepSeek 模型进行交互，支持角色设定、对话生成、推理过程展示等功能。

## 快速开始

### 1. 安装依赖

在运行项目之前，请确保已安装所需的依赖项。您可以通过以下命令安装：

```bash
pip install -r requirements.txt
```

### 2. 配置 API 密钥

在项目根目录下创建一个 `.env` 文件，并添加您的 DeepSeek API 密钥：

```plaintext
DEEPSEEK_API_KEY=your_api_key_here
```

### 3. 运行项目

使用以下命令启动 Gradio 界面：

```bash
python chatbot_gradio_demo.py
```

运行后，您可以在浏览器中访问生成的链接，开始使用聊天机器人。

## 功能介绍

### 聊天界面
- **模型选择**：支持 `deepseek-chat` 和 `deepseek-reasoner` 两种模型。
- **回复长度**：可选择 `short`、`medium` 或 `long` 来控制回复的长度。
- **推理过程展示**：如果选择 `deepseek-reasoner` 模型，推理过程会显示在专门的文本框中。
- **回溯功能**：支持删除最后一轮对话，方便用户调整对话内容。

### 角色设定
- **角色信息**：支持设置角色的名称、年龄、性别、物种、背景、世界观等详细信息。
- **输出偏好**：可选择 `普通` 或 `激进` 模式，影响生成内容的风格。
- **保存与加载**：支持将角色设定保存为文件，或从文件中加载角色设定。

## 注意事项

- 如果选择 `deepseek-chat` 模型，点击“确认设定”后，模型会自动生成第一句对话。
- 如果选择 `deepseek-reasoner` 模型，点击“确认设定”后, 模型不会自动生成第一句对话。推理过程会显示在“R1深度思考”文本框中。

## 贡献与反馈

2025 github.com/Yuzhifur
2025 github.com/JasonHistoria
2025 github.com/ChangLiu-byte