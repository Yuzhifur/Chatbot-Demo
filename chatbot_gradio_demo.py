from dotenv import load_dotenv
import os
from openai import OpenAI
import gradio as gr

# Load environment variables
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

# Initialize the DeepSeek API client
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


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
        chat_display = chat_history
        #for i in range (1, len(chat_history)):
        #    chat_display.append(gr.ChatMessage(role=chat_history[i]["role"], content=chat_history[i]["content"]))


        return chat_display, chat_history

    except Exception as e:
        return f"Error: {e}", chat_history



with gr.Blocks() as interface:
    gr.Markdown("### DeepSeek Gradio Chat")
    chatbox = gr.Chatbot(type="messages", label="DeepSeek Chat")  # Chat display
    user_input = gr.Textbox(label="Enter your message")  # User input box
    state = gr.State([])  # State to store chat history


    submit_btn = gr.Button("Send")


    submit_btn.click(
        chat_with_deepseek_turns,
        inputs=[user_input, state],
        outputs=[chatbox, state],
    )


if __name__ == "__main__":
    interface.launch()