import streamlit as st
import random

def welcome():
    return 'welcome all'

def prediction(body_type, sex, diet, how_often_shower, heating_energy_source, transport, vehicle_type, 
               social_activity, frequency_of_traveling_by_air, waste_bag_size, energy_efficiency, recycling, cooking_with):
    num = random.uniform(0, 1)
    
    if num < 0.5:
        prediction_result = "Low carbon footprint detected"
        prediction_color = "green"  # Color for a positive result
    else:
        prediction_result = "Significant carbon footprint predicted - consider reducing your environmental impact"
        prediction_color = "red"  # Color for a negative result

    return prediction_result, prediction_color

def main():
    st.title("Carbon Footprint Predictor")

    # Add your logo image using Markdown with CSS for positioning and sizing
    logo_url = ''
    logo_html = f'<img src="{logo_url}" style="display: block; margin: 0 auto; width: 150px; height: 150px;"/>'
    st.markdown(logo_html, unsafe_allow_html=True)
    
    html_temp = """
    <div style ="background-color:lightblue;padding:13px">
    <h2 style ="color:black;text-align:center;"> Predict your carbon footprint and make more sustainable choices. </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    body_type = st.text_input("Body Type", "")
    sex = st.text_input("Sex", "")
    diet = st.text_input("Diet", "")
    how_often_shower = st.text_input("How Often Shower", "")
    heating_energy_source = st.text_input("Heating Energy Source", "")
    transport = st.text_input("Transport", "")
    vehicle_type = st.text_input("Vehicle Type", "")
    social_activity = st.text_input("Social Activity", "")
    frequency_of_traveling_by_air = st.text_input("Frequency of Traveling by Air", "")
    waste_bag_size = st.text_input("Waste Bag Size", "")
    energy_efficiency = st.text_input("Energy Efficiency", "")
    recycling = st.text_input("Recycling", "")
    cooking_with = st.text_input("Cooking With", "")

    result = ""

    if st.button("Predict"):
        prediction_result, prediction_color = prediction(body_type, sex, diet, how_often_shower, heating_energy_source, 
                                                         transport, vehicle_type, social_activity, frequency_of_traveling_by_air, 
                                                         waste_bag_size, energy_efficiency, recycling, cooking_with)
        st.markdown(
            f'<p style="color: {prediction_color}; font-size: 18px;">Prediction: {prediction_result}</p>',
            unsafe_allow_html=True
        )

if __name__ == '__main__':
    main()
