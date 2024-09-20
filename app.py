import os
import pandas as pd
import streamlit as st
from streamlit_elements import elements, mui, html, dashboard
from streamlit_image_select import image_select

# Define the base directory where images are stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

# Modify load_data function to include the 'image_path' column
@st.cache_resource
def load_data():
    path = "Set12Champions.csv"
    if not os.path.isfile(path):
        path = f"https://docs.google.com/spreadsheets/d/1dBq9ZXdW10H_U_Zr84alFP4dQn71gRQOSwbJP344rrE/edit?gid=910518616#gid=910518616"

    data = pd.read_csv(
        path,
        nrows=52,
        names=[
            "unit", "cost", "health", "armor", "magic_resist", "attack", "attack_range",
            "attack_speed", "dps", "skill_name", "skill_cost", "origin", "class", "image_path"
        ],  # Now includes 'image_path'
        skiprows=1,
        usecols=range(14),
    )
    
    # Convert the 'class' column to a list of classes
    data['class'] = data['class'].str.split('/')
    
    # Prepend the base image directory to each 'image_path'
    data['image_path'] = data['image_path'].apply(lambda img: os.path.join(IMAGE_DIR, img))
    return data

# Modify create_dashboard to display the image using the path from the CSV
def create_dashboard(unit_info):  # No need to pass selected_unit separately
    with elements("dashboard"):
        layout = [
            dashboard.Item("first_item", 0, 0, 4, 2),
            dashboard.Item("second_item", 4, 2, 4, 2),
            dashboard.Item("third_item", 8, 2, 4, 2),
        ]

        def handle_layout_change(updated_layout):
            print(updated_layout)

        with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
            # Display the unit's image using 'image_path' from the CSV
            st.write(unit_info['image_path'])
            image_path = unit_info['image_path']
            mui.Typography(f"Selected Unit: {unit_info['unit']}", key="first_item")
            mui.Paper(html.img(src=image_path, style={"width": "100%"}), key="unit_image")

            # Display traits
            traits = ", ".join(unit_info['class'] + [unit_info['origin']])
            mui.Paper(f"Traits: {traits}", key="second_item")

            # Display ability
            ability = f"Ability: {unit_info['skill_name']} (Cost: {unit_info['skill_cost']})"
            mui.Paper(ability, key="third_item")

# The image_select_demo function stays the same, it retrieves the selected unit and its info
def image_select_demo():
    images = [
        "images/briar.png", "images/camille.jpg", "images/diana.png", "images/milio.webp",
        "images/morgana.png", "images/norra.png", "images/smolder.png", "images/xerath.png",
        "images/fiora.png", "images/gwen.png", "images/kalista.png", "images/karma.png",
        "images/nami.png", "images/nasus.png", "images/olaf.png", "images/rakan.png",
        "images/ryze.png", "images/tahmkench.png", "images/taric.png", "images/varus.png",
    ]
    captions = ["Briar", "Camille", "Diana", "Milio", "Morgana", "Norra", "Smolder", "Xerath", "Fiora", 
                "Gwen", "Kalista", "Karma", "Nami", "Nasus", "Olaf", "Rakan", "Ryze", "Tahm Kench", 
                "Taric", "Varus"]

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
        data = load_data()
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
        
