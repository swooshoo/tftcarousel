import os
import pandas as pd
import streamlit as st
from streamlit_elements import elements, mui, dashboard
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

# Custom image grid function for selecting images with clickable unit name buttons below
def custom_image_grid(data):
    images = data['image_path'].tolist()
    captions = data['unit'].str.title().tolist()

    # Manually set the number of columns (e.g., 4 columns per row)
    cols = st.columns(4)  # Creates a grid with 4 columns

    selected_idx = None
    for idx, (img, caption) in enumerate(zip(images, captions)):
        col_idx= idx % 4 # Rotate through the 4 columns
        with cols[col_idx]:
            # Display the image first
            st.image(img, caption=None, width=100)  # Image without caption
            # Place a button below each image with the unit's name as the label
            if st.button(caption, key=f"btn_{idx}"):
                selected_idx = idx  # Set selected index to current unit

    return selected_idx

# Modify create_dashboard to display the image using the path from the CSV
def create_dashboard(unit_info):
    st.subheader("Selected Unit Information")
    st.image(unit_info['image_path'], width=160)
    
    st.write(f"**Unit Name**: {unit_info['unit'].title()}")
    st.write(f"**Cost**: {unit_info['cost']}")
    st.write(f"**Health**: {unit_info['health']}")
    st.write(f"**Armor**: {unit_info['armor']}")
    st.write(f"**Magic Resist**: {unit_info['magic_resist']}")
    st.write(f"**Attack**: {unit_info['attack']}")
    st.write(f"**Attack Range**: {unit_info['attack_range']}")
    st.write(f"**Attack Speed**: {unit_info['attack_speed']}")
    st.write(f"**DPS**: {unit_info['dps']}")
    
    traits = ", ".join(unit_info['class'] + [unit_info['origin']])
    st.write(f"**Traits**: {traits}")
    
    ability = f"{unit_info['skill_name']} (Cost: {unit_info['skill_cost']})"
    st.write(f"**Ability**: {ability}")

# Main image_select_demo function that integrates the custom grid
def image_select_demo():
    # Load data to get images and captions from the CSV
    data = load_data()

    # Create custom grid for selecting images
    selected_idx = custom_image_grid(data)

    if selected_idx is not None:
        selected_unit_info = data.iloc[selected_idx]
        return selected_unit_info
    
    return None

# Main function
if __name__ == "__main__":
    # Load data once
    load_data()

    # Create two columns: left for image grid, right for selected unit details
    col1, col2 = st.columns([2, 1])  # Left column wider than right column

    # Display the image select demo and pass the selected unit info
    with col1:
        selected_unit_info = image_select_demo()

    # If a unit is selected, display its information in the right column
    if selected_unit_info is not None:
        with col2:
            create_dashboard(selected_unit_info)
    else:
        with col2:
            st.write("No unit selected yet.")
