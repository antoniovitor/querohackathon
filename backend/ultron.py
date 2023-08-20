import gradio as gr
import json
import requests
from user import system_message
from openai_key import get_headers

def system_message(system_msg, inputs):
    initial_message = [{"role": "user", "content": f"{inputs}"},]
    if system_msg.strip():
        initial_message.insert(0, {"role": "system", "content": system_msg})
    multi_turn_message = [{"role": "system", "content": system_msg},] if system_msg.strip() else []
    return initial_message, multi_turn_message

def render_system_message():
    with gr.Accordion(label="Mensagem do sistema:", open=False):
        system_msg = gr.Textbox(label="Instrua o Assistente de IA a definir seu comportamento", info="A mensagem do sistema ajuda a definir o comportamento do Assistente de IA.", value="", placeholder="Digite aqui..")
    return system_msg

API_URL = "https://api.openai.com/v1/chat/completions"

# Função para criar a payload
def create_payload(chat_counter, system_msg, inputs, temperature, top_p, chatbot):
    initial_message, multi_turn_message = system_message(system_msg, inputs)
    messages = initial_message if chat_counter == 0 else multi_turn_message
    for data in chatbot:
        messages += [{"role": "user", "content": data[0]}, {"role": "assistant", "content": data[1]}]
    messages.append({"role": "user", "content": inputs})
    payload = {
        "model": "gpt-4",
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "n": 1,
        "stream": True,
        "presence_penalty": 0,
        "frequency_penalty": 0,
    }
    return payload

# Função para fazer a previsão
def predict(openai_gpt4_key, system_msg, inputs, top_p, temperature, chat_counter, chatbot=[], history=[]):
    headers = get_headers(openai_gpt4_key)
    payload = create_payload(chat_counter, system_msg, inputs, temperature, top_p, chatbot)
    chat_counter += 1
    history.append(inputs)
    response = requests.post(API_URL, headers=headers, json=payload, stream=True)
    partial_words = ""
    token_counter = 0

    for counter, chunk in enumerate(response.iter_lines()):
        if counter == 0 or not chunk.decode():
            continue
        chunk = chunk.decode()
        if len(chunk) > 12 and "content" in json.loads(chunk[6:])['choices'][0]['delta']:
            partial_words += json.loads(chunk[6:])['choices'][0]["delta"]["content"]
            if token_counter == 0:
                history.append(" " + partial_words)
            else:
                history[-1] = partial_words
            chat = [(history[i], history[i + 1]) for i in range(0, len(history) - 1, 2)]
            token_counter += 1
            yield chat, history, chat_counter, response
