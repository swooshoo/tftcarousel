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
    data = pd.read_csv(path, nrows=52, skiprows=1, usecols=range(14),
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
            mui.Typography(f"Selected Unit: {unit_info['unit']}", key="first_item")
            #mui.Paper(html.img(src=f"/{image_path}", style={"width": "100%"}), key="unit_image")
            st.image(image=image_path)

            # Display traits and ability
            traits = ", ".join(unit_info['class'] + [unit_info['origin']])
            mui.Paper(f"Traits: {traits}", key="second_item")
            ability = f"Ability: {unit_info['skill_name']} (Cost: {unit_info['skill_cost']})"
            mui.Paper(ability, key="third_item")

# The image_select_demo function stays the same, it retrieves the selected unit and its info
def image_select_demo():
    images = [ #need to sort images from the csv itself later, hard-coded for now
        "static/images/briar.png", "static/images/camille.png", "static/images/diana.png", "static/images/milio.png",
        "static/images/morgana.png", "static/images/norra.png", "static/images/smolder.png", "static/images/xerath.png",
        "static/images/fiora.png", "static/images/gwen.png", "static/images/kalista.png", "static/images/karma.png",
        "static/images/nami.png", "static/images/nasus.png", "static/images/olaf.png", "static/images/rakan.png",
        "static/images/ryze.png", "static/images/tahmkench.png", "static/images/taric.png", "static/images/varus.png",
        "static/images/bard.png", "static/images/ezreal.png", "static/images/hecarim.png", "static/images/hwei.png",
        "static/images/jinx.png", "static/images/katarina.png", "static/images/mordekaiser.png", "static/images/neeko.png", 
        "static/images/shen.png", "static/images/swain.png", "static/images/veigar.png", "static/images/vex.png", "static/images/wukong.png",
        
    ]
    captions = ["Briar", "Camille", "Diana", "Milio", "Morgana", "Norra", "Smolder", "Xerath", "Fiora", 
                "Gwen", "Kalista", "Karma", "Nami", "Nasus", "Olaf", "Rakan", "Ryze", "Tahm Kench", 
                "Taric", "Varus", "Bard", "Ezreal", "Hecarim", "Hwei", "Jinx", "Katarina", "Mordekaiser", "Neeko", "Shen", "Swain",
                "Veigar", "Vex", "Wukong",]

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
    
        
