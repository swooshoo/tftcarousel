import pandas as pd
import streamlit as st
from streamlit_image_select import image_select

st.set_page_config(
    page_title="Cards",
    page_icon="static/imagestft_icon.webp",
)

# Load data function
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

# Display card for each unit
def render_card(unit, traits, ability, image_path):
    st.markdown(f"### {unit}")
    st.image(image_path, use_container_width=True)
    st.markdown(f"""
        **Traits:** {', '.join(traits)}  
        **Ability:** {ability}
    """)

# Main function for this page
def main():
    # Load data each time the page is accessed
    data = load_data("./Set12Champions.csv")
    
    cols_per_row = 3  # Number of cards per row
    for i in range(0, len(data), cols_per_row):
        cols = st.columns(cols_per_row)  # Create columns for each row
        for j, col in enumerate(cols):
            if i + j < len(data):  # Ensure no out-of-bounds access
                row = data.iloc[i + j]
                with col:
                    render_card(
                        unit=row['unit'],
                        traits=row['class'],
                        ability=row['skill_name'],
                        image_path=row['image_path']
                    )

if __name__ == "__main__":
    main()

