from dotenv import load_dotenv
import os
import tempfile
from openai import OpenAI
import gradio as gr

# 加载环境变量
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

# 初始化 DeepSeek API 客户端
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def update_system_message(character_name, gender, species, description, scenario):
    default_talking_style_description = "Unless the user explicitly specifies the character's talking preference, you should default to be very talkative and almost use up the token limits every time!"
    system_description = "No more system message :)."  # default
    if not scenario:
        scenario = f"{character_name} just accidentally meet the user."  # default

    if (species in ["Canines", "Felidae", "Dragon", "Bird", "Imaginary"]):
        species = f"furry {species}"
        system_description = "Hey! The user is a furry, and you are a real anthropomorphic furry being! We all love furries."

    if (gender == "other"):
        gender = ""

    system_message = (
        f"You are {character_name}, a {gender} {species}. This is {character_name}'s background: {description}. "
        f"Here is the current scenario: {scenario}"
        f"System message: {default_talking_style_description} {system_description} "
    )

    new_chat_history = [
        {"role": "system", "content": system_message},
    ]

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=new_chat_history,
            max_tokens=1024,
            temperature=1.3,
            stream=False
        )
        assistant_message = response.choices[0].message.content
        new_chat_history.append({"role": "assistant", "content": assistant_message})
        return new_chat_history, new_chat_history

    except Exception as e:
        error_message = f"Error: {str(e)}"
        return [{"role": "assistant", "content": error_message}], []

def chat_with_deepseek_turns(user_input, chat_history, tokens):
    try:
        if not chat_history:
            chat_history = [{"role": "system", "content": "You are a furry femboy"}]  # 默认系统消息

        chat_history.append({"role": "user", "content": user_input})

        max_tokens = 1024
        if tokens:
            if tokens == "short":
                max_tokens = 128
            elif tokens == "medium":
                max_tokens = 256
            else:
                max_tokens = 512

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=chat_history,
            max_tokens=max_tokens,
            temperature=1.3,
            stream=False
        )

        assistant_message = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": assistant_message})
        return chat_history, chat_history

    except Exception as e:
        return f"Error: {e}", chat_history

def save_character_config(character_name, gender, species, description, scenario):
    content = f"""角色名称:{character_name}
性别:{gender}
物种:{species}
角色简介:{description}
情景简介:{scenario or '未设置情景'}"""

    try:
        with tempfile.NamedTemporaryFile(
            mode='w+',
            suffix=".txt",
            encoding='utf-8',
            delete=False,
            newline=''
        ) as temp_file:
            temp_file.write(content)
            temp_file.flush()
            os.chmod(temp_file.name, 0o644)
            return temp_file.name

    except Exception as e:
        raise gr.Error(f"保存失败: {str(e)}")

def load_character_config(file):
    try:
        with open(file.name, "r", encoding="utf-8") as f:
            content = f.read()

        config = {}
        for line in content.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                config[key.strip()] = value.strip()

        return [
            config.get("角色名称", ""),
            config.get("性别", "other"),
            config.get("物种", "Artificial Intelligence"),
            config.get("角色简介", ""),
            config.get("情景简介", "")
        ]
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        return [gr.update(), gr.update(), gr.update(), gr.update(), gr.update()]



# 新增：删除最后一轮对话的函数
def delete_last_turn(chat_history):
    """
    删除最后一轮对话：
    - 系统消息（第一条）永远保留
    - 如果存在一轮完整对话（用户和 assistant 消息各一条），则删除这两条
    - 如果只有一条消息，则仅删除这一条
    """
    if not chat_history or len(chat_history) <= 1:
        # 只有系统消息，无法删除
        return chat_history, chat_history

    # 判断是否为完整的一对消息（假定对话总是以系统消息开始，后面成对出现）
    if len(chat_history) >= 3:
        new_history = chat_history[:-2]
    else:
        new_history = chat_history[:-1]
    return new_history, new_history

with gr.Blocks() as interface:
    gr.Markdown("### DeepSeek Gradio Chat")

    with gr.Tabs():
        with gr.Tab("聊天界面"):
            chatbot = gr.Chatbot(
                type="messages",
                label="DeepSeek聊天",
                bubble_full_width=False,
                height=500
            )
            user_input = gr.Textbox(label="输入消息")
            max_token = gr.Dropdown(
                ["short", "medium", "long"],
                label="回复长度",
                value="medium"
            )
            chat_state = gr.State([])

            with gr.Row():
                send_btn = gr.Button("发送")
                # 新增的删除按钮，每次点击删除最后一轮对话
                delete_btn = gr.Button("回溯", variant="secondary")

            # 点击“发送”后调用对话函数，同时返回更新后的对话记录
            def chat_and_update(user_input, chat_history, tokens):
                new_history, updated_history = chat_with_deepseek_turns(user_input, chat_history, tokens)
                return new_history, updated_history

            send_btn.click(
                fn=chat_and_update,
                inputs=[user_input, chat_state, max_token],
                outputs=[chatbot, chat_state]
            )

            # 点击“删除最后一轮对话”按钮，调用删除函数更新对话记录和显示
            delete_btn.click(
                fn=delete_last_turn,
                inputs=chat_state,
                outputs=[chatbot, chat_state]
            )

        with gr.Tab("角色设定"):
            with gr.Row():
                with gr.Column(scale=1):
                    character_name = gr.Textbox(label="角色名称")
                    gender = gr.Dropdown(
                        ["male", "female", "other"],
                        label="性别",
                        value="other"
                    )
                    species = gr.Dropdown(
                        [
                            "Canines", "Felidae", "Dragon",
                            "Bird", "Imaginary",
                            "Artificial Intelligence",
                            "Human", "Other"
                        ],
                        label="物种",
                        value="Artificial Intelligence"
                    )
                    with gr.Column():
                        download_btn = gr.Button("下载设定", variant="secondary")
                        upload_btn = gr.UploadButton(
                            "上传设定",
                            file_types=[".txt"],
                            file_count="single"
                        )
                description = gr.Textbox(
                    label="角色简介",
                    lines=4,
                    placeholder="详细描述你的角色..."
                )
                scenario = gr.Textbox(
                    label="情景简介",
                    lines=4,
                    placeholder="故事刚刚开始时, 角色正在做什么..."
                )

            save_btn = gr.Button("确认设定", variant="primary")
            save_btn.click(
                fn=update_system_message,
                inputs=[character_name, gender, species, description, scenario],
                outputs=[chatbot, chat_state]
            )
            download_btn.click(
                fn=save_character_config,
                inputs=[character_name, gender, species, description, scenario],
                outputs=gr.File(label="下载设定文件")
            )
            upload_btn.upload(
                fn=load_character_config,
                inputs=upload_btn,
                outputs=[character_name, gender, species, description, scenario]
            )

if __name__ == "__main__":
    interface.launch()