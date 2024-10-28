import os
import pandas as pd
import streamlit as st
from streamlit_elements import elements, mui, dashboard
from streamlit_image_select import image_select

# Define the base directory where images are stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

# Load data with image paths
@st.cache_resource
def load_data(path):
    data = pd.read_csv(
        path, nrows=60, skiprows=1, usecols=range(14),
        names=["unit", "cost", "health", "armor", "magic_resist", "attack", 
               "attack_range", "attack_speed", "dps", "skill_name", 
               "skill_cost", "origin", "class", "image_path"]
    )
    data['class'] = data['class'].str.split('/')
    data['image_path'] = "static/images/" + data['image_path'].fillna('')
    return data

df = load_data("Set12Champions.csv")
# Create dashboard function to display selected unit's info
def create_dashboard(unit_info):
    with st.container(border=True):
            st.image(unit_info['image_path'], use_column_width=True,output_format="PNG")
            st.text(f"{unit_info['unit'].title()}")
            st.text(f"{unit_info['origin']}")
            st.text(f"{unit_info['class']}")
            

# Image selection demo with buttons
def image_select_demo(data):
    images = data['image_path'].tolist()
    captions = data['unit'].str.title().tolist()

    # Display images as buttons
    img = image_select(
        label="Select a unit",
        images=images,
        captions=captions,
        use_container_width=False,
        return_value="index", 
    )

    if img is not None:
        selected_unit_info = data.iloc[img]
        return selected_unit_info
    return None

# Main function
if __name__ == "__main__":
    st.title("TFT Carousel Dashboard")
    
    # Load data once and pass it to other functions
    data = load_data("Set12Champions.csv")
    
    tab1, tab2, tab3 = st.tabs(["All", "5 Costs", "4 Star"])
    
    # Create two columns: one for the image grid (left) and one for the dashboard (right)
    col1, col2 = st.columns([3, 2])  # Left column 3/5 width, right column 2/5 width
    
    # Left column for the image grid
    with col1.container(height=600):
        # Show image selection grid with reduced image size
        selected_unit_info = image_select_demo(data)
    
    # Right column for the dashboard
    with col2:
        if selected_unit_info is None:
            selected_unit_info = data.iloc[0]  # Default unit if no selection is made
        # Create the dashboard for either the selected unit or the default
        create_dashboard(selected_unit_info)
