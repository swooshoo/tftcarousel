import os
import pandas as pd
import streamlit as st
from streamlit_image_select import image_select

# Load data function
@st.cache_resource
def load_data(path):
    data = pd.read_csv(
        path, nrows=64, skiprows=1, usecols=range(14),
        names=["unit", "cost", "health", "armor", "magic_resist", "attack", 
               "attack_range", "attack_speed", "dps", "skill_name", 
               "skill_cost", "origin", "class", "image_path"]
    )
    
    # Handle 'class' if it is in string representation of a list
    def parse_class(value):
        if isinstance(value, str):
            # If the string looks like a list (e.g., "[Ravenous,Shapeshifter]")
            if value.startswith('[') and value.endswith(']'):
                return [v.strip() for v in value[1:-1].split(',')]
            return value.split('/')
        return []
    
    data['class'] = data['class'].apply(parse_class)
    data['origin'] = data['origin'].apply(parse_class)
    
    # Combine 'origin' and 'class' into a unified 'traits' list
    data['traits'] = data.apply(lambda row: row['origin'] + row['class'], axis=1)
    
    # Prepare image paths
    data['image_path'] = "static/images/" + data['image_path'].fillna('')
    return data

# Display dashboard function
def create_dashboard(unit_info):
    with st.container():
        st.image(unit_info['image_path'], use_container_width=True, output_format="png")
        st.text(f"{unit_info['unit'].title()}")
        st.text(f"{unit_info['origin']}")
        st.text(f"{unit_info['class']}")
        st.text(f"Ability: {unit_info['skill_name']}")
        
        column1, column2, column3 = st.columns(3)
        column1.metric(label="HP", value=unit_info['health'])
        column2.metric(label="ARMOR", value=unit_info['armor'])
        column3.metric(label="MR", value=unit_info['magic_resist'])
        column1.metric(label="AS", value=unit_info['attack_speed'])
        column2.metric(label="AD", value=unit_info['attack'])
        column3.metric(label="AP", value=unit_info['attack'])

def image_select_demo(data):
    images = data['image_path'].tolist()
    captions = data['unit'].str.title().tolist()
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

# Main function for this page
def main():
    st.header("Set 13 Units: First Glance", divider="gray")
    data = load_data("Set13Champions.csv")
    if data is None:   
        st.write("DATA NOT FOUND")
        exit
    
    col1, col2 = st.columns([2.7, 2.3])
    
    with col1:
        selected_unit_info = image_select_demo(data)
    
    with col2:
        if selected_unit_info is None:
            selected_unit_info = data.iloc[0]
        create_dashboard(selected_unit_info)

if __name__ == "__main__":
    main()