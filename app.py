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

def green_score_calc(liv_type, house,diet,how_often_water,heating_energy_source,transport,buying_activity,
                               frequency_of_traveling_by_air,waste_bag_week,energy_efficiency,recycling, cooking_with):
    score=0
    #liv_type = st.text_input("Live with more than 2 people-yes/no (points- 6/12)", "yes", key="ltyp")
    if (liv_type == "yes") :
        score += 6
    else :
        score += 12

    #house = st.text_input("House-large, medium, small (points- 10/7/4)", "large", key="hs")
    if (house == "large") :
        score +=10
    elif (house=="medium"):
        score+=7
    elif (house=="small"):
        score+=4
    
    #diet = st.text_input("Diet-vegan/vegetarian/pescatarian/omnivore (points-2/4/8/10)", "vegetarian", key="dt")
    if (diet == "vegan") :
        score +=2
    elif (diet=="vegetarian"):
        score+=4
    elif (diet=="pescatarian"):
        score+=8
    elif (diet=="omnivore"):
        score+=10

    #how_often_water = st.text_input("How Often Do You Use Washing Machine/Dishwasher a week - 3/7  (points- 5/10)", "3", key="water")

    if (how_often_water == 3) :
        score +=5
    elif (how_often_water==7):
        score+=10

    #heating_energy_source = st.text_input("Heating Energy Source-Solar/gas/coal/electricity (points- -10/20/30/10)", "solar", key="ensrc")

    if (heating_energy_source == "solar") :
        score +=10
    elif (heating_energy_source=="gas"):
        score+=20
    elif (heating_energy_source=="coal"):
        score+=30
    elif (heating_energy_source=="electricity"):
        score+=10

    #transport = st.text_input("Transport", "public/electric/hybrid/gasoline/bikewalk (points- -20/-20/-15/20/-40)", key="trans")

    if (transport == "public") :
        score +=-20
    elif (transport=="electric"):
        score+=-20
    elif (transport=="hybrid"):
        score+=-15
    elif (transport=="gasoline"):
        score+=20
    elif (transport=="bikewalk"):
        score+=-40

    #buying_activity = st.text_input("Buying Activity-5/10/15 purchases a year (points-4/7/10)", "5", key="buy")

    if (int(buying_activity) > 15 ) :
        score += 10
    elif (int(buying_activity) > 10):
        score+=7
    elif (int(buying_activity) > 5):
        score+=4

    #frequency_of_traveling_by_air = st.text_input("Frequency of Traveling Long Distance-5/10/15 times a year (points-20/40/60)", "3", key="at")

    if (int(frequency_of_traveling_by_air) > 15 ) :
        score += 60
    elif (int(frequency_of_traveling_by_air) > 10):
        score+=40
    elif (int(frequency_of_traveling_by_air) > 5):
        score+=20

    #waste_bag_week = st.text_input("#1/2 gallon waste Bags a week - 8/4/2 (points-50/30/10)", "2", key="wb")

    if (int(waste_bag_week) > 8 ) :
        score += 50
    elif (int(waste_bag_week) > 4):
        score+=30
    elif (int(waste_bag_week) > 2):
        score+=10

    #energy_efficiency = st.text_input("Energy Efficiency Applianes - yes/no (points- minus 10 if energy efficient)", "yes", key="ef")

    if (energy_efficiency == "yes" ) :
        score += -10
    elif (energy_efficiency == "no"):
        score+=10

   #recycling = st.text_input("Recycling-Glass/Plastic/Paper/Aluminum/Steel/Food (points-minus 4 for each)", "Plastic,Food", key="re")

    if (recycling and recycling.find("Glass") > 0 ) :
        score += -4
    elif (recycling and recycling.find("Plastic") > 0 ) :
        score += -4    
    elif (recycling and recycling.find("Paper") > 0 ) :
        score += -4   
    elif (recycling and recycling.find("Aluminum") > 0 ) :
        score += -4    
    elif (recycling and recycling.find("Steel") > 0 ) :
        score += -4
    elif (recycling and recycling.find("Food") > 0 ) :
        score += -4    

    #cooking_with = st.text_input("Cooking With stove/coal/electric/microwave (points- 10/20/20/-10/-10)", "stove/coal/wood/electric/microwave", key="cw")


    if (cooking_with and cooking_with.find("stove") > 0 ) :
        score += 10
    elif (cooking_with and cooking_with.find("coal") > 0 ) :
        score += 20
    elif (cooking_with and cooking_with.find("wood") > 0 ) :
        score += 20
    elif (cooking_with and cooking_with.find("electric") > 0 ) :
        score += -10
    elif (cooking_with and cooking_with.find("microwave") > 0 ) :
        score += -10
    return score

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
liv_type = st.text_input("Live with more than 2 people-yes/no (points- 6/12)", "yes", key="ltyp")
house = st.text_input("House-large, medium, small (points- 10/7/4)", "large", key="hs")
diet = st.text_input("Diet-vegan/vegetarian/pescatarian/omnivore (points-2/4/8/10)", "vegetarian", key="dt")
how_often_water = st.text_input("How Often Do You Use Washing Machine/Dishwasher a week - 3/7  (points- 5/10)", "3", key="water")
heating_energy_source = st.text_input("Heating Energy Source-Solar/gas/coal/electricity (points- -10/20/30/10)", "solar", key="ensrc")
transport = st.text_input("Transport", "public/electric/hybrid/gasoline/bikewalk (points- -20/-20/-15/20/-40)", key="trans")
buying_activity = st.text_input("Buying Activity-5/10/15 purchases a year (points-4/7/10)", "5", key="buy")
frequency_of_traveling_by_air = st.text_input("Frequency of Traveling Long Distance-5/10/15 times a year (points-20/40/60)", "3", key="at")
waste_bag_week = st.text_input("#1/2 gallon waste Bags a week - 8/4/2 (points-50/30/10)", "2", key="wb")
energy_efficiency = st.text_input("Energy Efficiency Applianes - yes/no (points- minus 10 if energy efficient)", "yes", key="ef")
recycling = st.text_input("Recycling-Glass/Plastic/Paper/Aluminum/Steel/Food (points-minus 4 for each)", "Plastic,Food", key="re")
cooking_with = st.text_input("Cooking With stove/coal/electric/microwave (points- 10/20/20/-10/-10)", "stove/coal/wood/electric/microwave", key="cw")
chat_message = st.chat_input("Calculate my carbon footprint. Also calculate my green score and give me recommendations to reduce my carbon footprint")

# Construct the Prompt (Tailored for Carbon Footprint Estimation)
prompt = f"Given my following lifestyle:\n" \
        f"- Live With More Than 2 People: {liv_type}\n" \
        f"- House: {house}\n" \
        f"- Diet: {diet}\n" \
        f"- How Often Water Used for Dish Washing, Washing Machine: {how_often_water}\n" \
        f"- Heating Energy Source: {heating_energy_source}\n" \
        f"- Transport Type: {transport}\n" \
        f"- Buying Activity(Extravagant Purchases every year): {buying_activity}\n" \
        f"- Frequency of Traveling by Air: {frequency_of_traveling_by_air}\n" \
        f"- Waste Bag Size: {waste_bag_week}\n" \
        f"- Energy Efficiency Appliances: {energy_efficiency}\n" \
        f"- Recycling Type: {recycling}\n" \
        f"- Cooking With: {cooking_with}\n" \
        f"Type yes and hit enter to estimate my carbon footprint and recommendations to reduce my carbon footprint"
green_score = green_score_calc(liv_type, house,diet,how_often_water,heating_energy_source,transport,buying_activity,
                               frequency_of_traveling_by_air,waste_bag_week,energy_efficiency,recycling,cooking_with)
green_score_message = "Oof! Your carbon footprint is high(> 60). Find ways to reduce your impact on the planet.\n"
if (green_score < 60):
    green_score_message = "Congratulations! You are doing a great job. Your score is less than 60."
if chat_message:
    st.chat_message("user").markdown(chat_message)
    res_area = st.chat_message("assistant").empty()
    print("prompt", prompt)
    messages.append(
        {"role": "user", "parts":  [prompt]},
    )
    res = get_response(messages)
    res_text='Your green score is '+str(green_score)+". "+green_score_message 
    for chunk in response:
        res_text += chunk.parts[0].text

    res_area.markdown(res_text)
    messages.append({"role": "model", "parts": [res_text]})