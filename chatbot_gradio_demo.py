from dotenv import load_dotenv
import os
from openai import OpenAI
import gradio as gr

# Load environment variables
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

# Initialize the DeepSeek API client
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def update_system_message(character_name, gender, species, description, scenario):
    system_description = "No system message :)." # default
    if not scenario:
        scenario = f"{character_name} just accidentally meet the user." # default

    if (species in ["Canines", "Felidae", "Dragon", "Bird", "Imaginary"]):
        species = f"furry {species}"
        system_description = "Hey! The user is a furry, and you are a real anthropomorphic furry being! We all love furries."

    if (gender == "other"):
        gender = ""

    system_message = (
        f"You are {character_name}, a {gender} {species}. This is {character_name}'s background: {description}. "
        f"Here is the current scenario: {scenario}"
        f"System message: {system_description}. "
    )

    new_chat_history = [
        {"role": "system", "content": system_message},
    ]

    try:
        # Make an API call to get the first assistant response
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=new_chat_history,
            max_tokens=1024,
            temperature=1.3,
            stream=False
        )
        assistant_message = response.choices[0].message.content

        # Add the assistant response to the new chat history
        new_chat_history.append({"role": "assistant", "content": assistant_message})

        # Return the new history to display in the chatbot and store in state
        return new_chat_history, new_chat_history

    except Exception as e:
        # If there is any error, return the error as a user-like message
        error_message = f"Error: {str(e)}"
        return [{"role": "assistant", "content": error_message}], []

def chat_with_deepseek_turns(user_input, chat_history):
    try:
        # If chat history is empty, initialize it
        if not chat_history:
            chat_history = [{"role": "system", "content": "You are a furry femboy"}] # default

        # Add the user's message to the chat history
        chat_history.append({"role": "user", "content": user_input})


        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=chat_history,
            max_tokens=1024,
            temperature=1.3,
            stream=False
        )

        assistant_message = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": assistant_message})


        return chat_history, chat_history

    except Exception as e:
        return f"Error: {e}", chat_history



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
            chat_state = gr.State([])

            send_btn = gr.Button("发送")
            send_btn.click(
                fn=chat_with_deepseek_turns,
                inputs=[user_input, chat_state],
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
            # On confirming character info, call update_system_message
            # which returns the first assistant response as new chat_history
            save_btn.click(
                fn=update_system_message,
                inputs=[character_name, gender, species, description, scenario],
                outputs=[chatbot, chat_state]
            )

if __name__ == "__main__":
    interface.launch()