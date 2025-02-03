from dotenv import load_dotenv
import os
from openai import OpenAI
import gradio as gr

# Load environment variables
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

# Initialize the DeepSeek API client
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def update_system_message(character_name, gender, species, description):
    system_description = "No system description :)."

    if (species in ["Canines", "Felidae", "Dragon", "Bird", "Imaginary"]):
        species = f"furry {species}"
        system_description = "Hey! The user is a furry, and you are a real anthropomorphic furry being! We all love furries."

    if (gender == "other"):
        gender = ""

    system_message = f"You are {character_name}, a {gender} {species}. System message: {system_description}. Character background: {description}."
    return [{"role": "system", "content": system_message}]

def chat_with_deepseek_turns(user_input, chat_history):
    try:
        # If chat history is empty, initialize it
        if not chat_history:
            chat_history = [{"role": "system", "content": "You are a furry femboy"}]

        # Add the user's message to the chat history
        chat_history.append({"role": "user", "content": user_input})
        #chat_display.append({"role": "user", "content": user_input})


        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=chat_history,
            max_tokens=1024,
            temperature=1.3,
            stream=False
        )


        assistant_message = response.choices[0].message.content

        chat_history.append({"role": "assistant", "content": assistant_message})

        # Prepare the chat history for display in Gradio
        #for i in range (1, len(chat_history)):
        #    chat_display.append(gr.ChatMessage(role=chat_history[i]["role"], content=chat_history[i]["content"]))


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
                chat_with_deepseek_turns,
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
            save_btn = gr.Button("确认设定", variant="primary")
            save_btn.click(
                update_system_message,
                inputs=[character_name, gender, species, description],
                outputs=[chat_state]
            )



if __name__ == "__main__":
    interface.launch()