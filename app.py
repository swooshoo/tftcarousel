import os
import pandas as pd
import streamlit as st
from streamlit_image_select import image_select

# Set the page configuration
st.set_page_config(page_title="Teamfight Tactics Dashboard", layout="wide")

# Define the base directory where images are stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

# Load data with image paths
@st.cache_data
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
    with st.container():
        st.image(unit_info['image_path'], use_column_width=True, output_format="PNG")
        st.markdown(f"### {unit_info['unit'].title()}")
        st.markdown(f"**Origin:** {', '.join(unit_info['origin'])}")
        st.markdown(f"**Class:** {', '.join(unit_info['class'])}")
        st.markdown(f"**Ability:** {unit_info['skill_name']}")
        column1, column2, column3 = st.columns(3)
        column1.metric(label="HP", value=unit_info['health'])
        column2.metric("ARMOR", value=unit_info['armor'])
        column3.metric("MR", value=unit_info['magic_resist'])
        column1.metric("AS", value=unit_info['attack_speed'])
        column2.metric("AD", value=unit_info['attack'])
        column3.metric("AP", value=unit_info['attack'])

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
        return_value="index", 
    )

    if img is not None:
        selected_unit_info = data.iloc[img]
        return selected_unit_info
    return None

# Units Page
def units_page():
    st.header("Set 12 Units: First Glance", anchor=None)

    # Load data once and pass it to other functions
    data = load_data("Set12Champions.csv")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["All", "5 Cost", "4 Cost", "3 Cost", "2 Cost", "1 Cost"])

    # Using "with" notation for sidebar content specific to Units page
    with st.sidebar:
        st.markdown("### Units Navigation")
        st.write("Explore the various units available in Set 12.")
        # You can add more sidebar elements specific to Units here

    # Create two columns: one for the image grid (left) and one for the dashboard (right)
    col1, col2 = st.columns([2.7, 2.3])  # Left column 3/5 width, right column 2/5 width
    
    # Left column for the image grid
    with col1.container():
        # Show image selection grid with reduced image size
        selected_unit_info = image_select_demo(data)
    
    # Right column for the dashboard
    with col2:
        if selected_unit_info is None:
            selected_unit_info = data.iloc[0]  # Default unit if no selection is made
        # Create the dashboard for either the selected unit or the default
        create_dashboard(selected_unit_info)

# Comps Page
def comps_page():
    st.header("Team Compositions", anchor=None)

    with st.sidebar:
        st.markdown("### Compositions Navigation")
        st.write("Build and analyze team compositions.")
        # You can add more sidebar elements specific to Comps here

    st.markdown("""
    ## Create Your Composition

    - **Select Units:** Choose units from your collection to form a team.
    - **Analyze Synergies:** View the synergies and traits of your selected team.
    - **Optimize Strategy:** Adjust your team composition for optimal performance.

    ### Example Composition

    *This section can display example team comps or allow users to create their own.*
    """)

    # Placeholder for composition features
    st.write("Composition features will be added here.")

# Main Function
def main():
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Units", "Comps"])

    if page == "Units":
        units_page()
    elif page == "Comps":
        comps_page()

if __name__ == "__main__":
    main()
