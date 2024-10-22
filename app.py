import os
import pandas as pd
import streamlit as st
from streamlit_elements import elements, mui, html, dashboard
from streamlit_image_select import image_select
import streamlit.components.v1 as components

# Define the base directory where images are stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

# Load data with image paths
@st.cache_resource
def load_data():
    path = "Set12Champions.csv"
    data = pd.read_csv(
        path, nrows=60, skiprows=1, usecols=range(14),
        names=["unit", "cost", "health", "armor", "magic_resist", "attack", 
               "attack_range", "attack_speed", "dps", "skill_name", 
               "skill_cost", "origin", "class", "image_path"]
    )
    data['class'] = data['class'].str.split('/')
    data['image_path'] = "static/images/" + data['image_path'].fillna('')
    return data

# Create dashboard function to display selected unit's info
def create_dashboard(unit_info):
    with elements("dashboard"):
        
        with st.container():
            st.text(f"Selected Unit: {unit_info['unit'].title()}")
            st.text(f"Traits: {unit_info['origin'].title()} {unit_info['class']}")
            st.text('very stylish container')
        
        layout = [
            dashboard.Item("first_item", 0, 0, 4, 2),
            dashboard.Item("second_item", 4, 2, 4, 2),
            dashboard.Item("third_item", 8, 2, 4, 2),
        ]
        
        def handle_layout_change(updated_layout):
            print(updated_layout)

        with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
            image_path = unit_info['image_path']
            mui.Typography(f"Selected Unit: {unit_info['unit'].title()}", key="first_item")
            st.image(image=image_path, width=160)

            # Display traits
            traits = ", ".join(unit_info['class'] + [unit_info['origin']])
            mui.Card(
                mui.CardContent(mui.Typography(f"Traits: {traits}")), 
                key="second_item",
                outlined=True
            )

            # Display ability
            ability = f"Ability: {unit_info['skill_name']} (Cost: {unit_info['skill_cost']})"
            mui.Card(
                mui.CardContent(mui.Typography(ability)), 
                key="third_item",
                outlined=True
            )

# Image selection demo with buttons
def image_select_demo(data):
    images = data['image_path'].tolist()
    captions = data['unit'].str.title().tolist()

    # Display images as buttons
    img = image_select(
        label="Select a unit",
        images=images,
        captions=captions,
        use_container_width=True,
        return_value="index"
    )

    if img is not None:
        selected_unit_info = data.iloc[img]
        return selected_unit_info
    return None

# Main function
if __name__ == "__main__":
    st.title("TFT Carousel Dashboard")
    
    # Load data once and pass it to other functions
    data = load_data()
    
    tab1, tab2, tab3 = st.tabs(["All", "5 Costs", "4 Star"])
    
    # Show a default unit (first row) when the dashboard is first loaded
    default_unit_info = data.iloc[0]
    create_dashboard(default_unit_info)

    # Allow user to select a unit after the default dashboard is displayed
    selected_unit_info = image_select_demo(data)

    # If a new unit is selected, update the dashboard with the selected unit
    if selected_unit_info is not None:
        create_dashboard(selected_unit_info)
