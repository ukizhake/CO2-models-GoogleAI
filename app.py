import io
import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
import os
from dotenv import load_dotenv
import pathlib
import textwrap
# from IPython.display import display
from IPython.display import Markdown
import pandas as pd

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

load_dotenv()
genai.configure( api_key = os.environ["GOOGLE_API_KEY"] )
model = genai.GenerativeModel('gemini-pro')
df = pd.read_csv('indivCarbonEmission.csv')
response = model.generate_content("use the content in  the data frame generated above  to create a text summary for carbon footprints")
to_markdown(response.parts[0].text)

async def get_response(messages, model="gemini-pro"):
    model = genai.GenerativeModel(model)
    res = await model.generate_content(messages, stream=True,
                                safety_settings={'HARASSMENT':'block_none'})
    res.resolve()
    return res

if "messages" not in st.session_state:
    st.session_state["messages"] = []
messages = st.session_state["messages"]

# The vision model gemini-pro-vision is not optimized for multi-turn chat.
if messages :
    for item in messages:
        role, parts = item.values()
        if role == "user":
            st.chat_message("user").markdown(parts[0])
        elif role == "model":
            st.chat_message("assistant").markdown(parts[0])

chat_message = st.chat_input("Say something")

if chat_message:
    st.chat_message("user").markdown(chat_message)
    res_area = st.chat_message("assistant").empty()
    messages.append(
        {"role": "user", "parts":  [chat_message]},
    )
    res = get_response(messages)
    res_text=''
    for chunk in response:
        res_text += chunk.parts[0].text

    res_area.markdown(res_text)
    messages.append({"role": "model", "parts": [res_text]})