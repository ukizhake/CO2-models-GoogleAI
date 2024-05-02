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
print("ushakiz 111111")

load_dotenv()
genai.configure( api_key = os.environ["GOOGLE_API_KEY"] )
model = genai.GenerativeModel('gemini-pro')
df = pd.read_csv('indivCarbonEmission.csv')
response = model.generate_content("use the content in  the data frame generated above  to create a text summary for carbon footprints")
to_markdown(response.parts[0].text)
print("ushakiz 222222")

async def get_response(messages, model="gemini-pro"):
    res = await model.generate_content(messages, stream=True,
                                safety_settings={'HARASSMENT':'block_none'})
    res.resolve()
    return res

if "messages" not in st.session_state:
    st.session_state["messages"] = []
messages = st.session_state["messages"]
if messages :
    for item in messages:
        role, parts = item.values()
        if role == "user":
            st.chat_message("user").markdown(parts[0])
        elif role == "model":
            st.chat_message("assistant").markdown(parts[0])
print("ushakiz ====")
body_type = st.text_input("Body Type", "overweight", key="btyp")
sex = st.text_input("Sex", "female", key="sx")
diet = st.text_input("Diet", "vegetarian", key="dt")
how_often_shower = st.text_input("How Often Shower", "daily", key="shwr")
heating_energy_source = st.text_input("Heating Energy Source", "solar", key="ensrc")
transport = st.text_input("Transport", "hybrid", key="trans")
vehicle_type = st.text_input("Vehicle Type", "sedan", key="vt")
social_activity = st.text_input("Social Activity", "sometimes", key="sa")
frequency_of_traveling_by_air = st.text_input("Frequency of Traveling by Air", "sometimes", key="at")
waste_bag_size = st.text_input("Waste Bag Size", "medium", key="wb")
energy_efficiency = st.text_input("Energy Efficiency", "yes", key="ef")
recycling = st.text_input("Recycling", "plastic and metal", key="re")
cooking_with = st.text_input("Cooking With", "stove", key="cw")
chat_message = st.chat_input("Given above info and the dataframe, calculate my carbon footprint. Also calculate my green score (on a scale of 1 to 10) giving highest weightage to transportation and energy used, moderate weightage to waste and food ")

# Construct the Prompt (Tailored for Carbon Footprint Estimation)
prompt = f"Given my following lifestyle:\n" \
        f"- Body Type: {body_type}\n" \
        f"- Sex: {sex}\n" \
        f"- Diet: {diet}\n" \
        f"- How Often Shower: {how_often_shower}\n" \
        f"- Heating Energy Source: {heating_energy_source}\n" \
        f"- Transport: {transport}\n" \
        f"- Vehicle Type: {vehicle_type}\n" \
        f"- Social Activity: {social_activity}\n" \
        f"- Frequency of Traveling by Air: {frequency_of_traveling_by_air}\n" \
        f"- Waste Bag Size: {waste_bag_size}\n" \
        f"- Energy Efficiency: {energy_efficiency}\n" \
        f"- Recycling: {recycling}\n" \
        f"- Cooking With: {cooking_with}\n" \
        f"Type yes and hit enter to estimate my carbon footprint and provide a green score (out of 10) considering factors like transportation, energy use, and consumption habits based on the information provided."


if chat_message:
    st.chat_message("user").markdown(chat_message)
    res_area = st.chat_message("assistant").empty()
    print("prompt", prompt)
    messages.append(
        {"role": "user", "parts":  [prompt]},
    )
    res = get_response(messages)
    res_text=''
    for chunk in response:
        res_text += chunk.parts[0].text

    res_area.markdown(res_text)
    messages.append({"role": "model", "parts": [res_text]})