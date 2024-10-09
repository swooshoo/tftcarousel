import os
import pandas as pd
import streamlit as st
from streamlit_elements import elements, mui, html, dashboard
from streamlit_image_select import image_select

import streamlit.components.v1 as components


# Define the base directory where images are stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

# Modify load_data function to include the 'image_path' column
@st.cache_resource
def load_data():
    path = "Set12Champions.csv"
    data = pd.read_csv(path, nrows=60, skiprows=1, usecols=range(14),
                       names=["unit", "cost", "health", "armor", "magic_resist", "attack", 
                              "attack_range", "attack_speed", "dps", "skill_name", 
                              "skill_cost", "origin", "class", "image_path"])

    data['class'] = data['class'].str.split('/')
    data['image_path'] = "static/images/" + data['image_path'].fillna('')  # Prepend 'static/images/' to paths

    return data

# Modify create_dashboard to display the image using the path from the CSV
def create_dashboard(unit_info):
    with elements("dashboard"):
        layout = [
            dashboard.Item("first_item", 0, 0, 4, 2),
            dashboard.Item("second_item", 4, 2, 4, 2),
            dashboard.Item("third_item", 8, 2, 4, 2),
        ]

        def handle_layout_change(updated_layout):
            print(updated_layout)

        with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
            image_path = unit_info['image_path']
            st.write(f"Image Path: {image_path}")  # Debugging to confirm path is correct

            # Ensure that the image path is correctly served
            mui.Typography(f"{unit_info['unit'].title()}", key="first_item")
            st.image(image=image_path, width=160)
            
            # Display traits using mui.Card 
            traits = ", ".join(unit_info['class'] + [unit_info['origin']])
            mui.Card(
                mui.CardContent(mui.Typography(f"Traits: {traits}")), 
                key="second_item",
                outlined=True
            )

            # Display ability using mui.Card
            ability = f"Ability: {unit_info['skill_name']} (Cost: {unit_info['skill_cost']})"
            mui.Card(
                mui.CardContent(mui.Typography(ability)), 
                key="third_item",
                outlined=True
            )
            
# The image_select_demo function stays the same, it retrieves the selected unit and its info
def image_select_demo():
    # Load data to get images and captions from the CSV
    data = load_data()

    # Use the 'image_path' column for the image paths
    images = data['image_path'].tolist()  # Image paths from CSV
    
    # Use the 'unit' column for captions
    captions = data['unit'].str.title().tolist()  # Unit names from CSV

    # Image selector
    img = image_select(
        label="Select a unit",
        images=images,
        captions=captions,
        use_container_width=False,
        return_value="index"
    )
    
    if img is not None:
        # Load the corresponding unit data from CSV
        selected_unit_info = data.iloc[img]  # Get the data row for the selected unit
        
        # Return the selected unit info (image path and data)
        return selected_unit_info
    return None

# Main function
if __name__ == "__main__":
    # Display the image select demo and pass the selected unit info to the dashboard
    load_data()
    selected_unit_info = image_select_demo()

    if selected_unit_info is not None:
        create_dashboard(selected_unit_info)
    
        
