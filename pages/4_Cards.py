import pandas as pd
import streamlit as st
from streamlit_image_select import image_select
import os

st.set_page_config(
    page_title="Cards",
    page_icon="static/imagestft_icon.webp",
)

def load_data(path):
    data = pd.read_csv(
        path, nrows=64, skiprows=1, usecols=range(15),
        names=["unit", "cost", "health", "armor", "magic_resist", "attack", 
               "attack_range", "attack_speed", "dps", "skill_name", 
               "skill_cost", "origin", "class", "image_path", "traits"]
    )
    data['image_path'] = "static/images/" + data['image_path'].fillna('')
    # Split traits into lists, need to leave this line of code in, even though I tried to change the data
    data['traits'] = data['traits'].fillna('').apply(lambda x: [t.strip() for t in x.split(',')] if x else [])
    
    return data

# Display card for each unit
def render_card(unit, traits, ability, image_path, stats):
    st.markdown(f"## {unit.replace('_', ' ').title()}")
    st.image(image_path, use_container_width=False)
    # Tabs for unit-specific details
    tab1, tab2, tab3, tab4 = st.tabs(["Traits", "Ability", "Stats", "Items"])
    
    # Tab 1: Display traits with images and names
    with tab1:
        for trait in traits:
            trait_image_path = f"static/traits/{trait.lower()}.svg"
            if os.path.exists(trait_image_path):
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <img src="{trait_image_path}" alt="{trait}" style="width: 50px; height: auto; margin-right: 10px;">
                        <span style="font-size: 16px;">{trait.title()}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.write(f"Trait image not found: {trait.title()}")

    # Tab 2: Display unit ability
    with tab2:
        st.markdown(f"**Ability:** {ability}")

    # Tab 3: Display unit stats
    with tab3:
        with st.container():
            column1, column2 = st.columns(2)
            column1.metric(label="HP", value=stats['health'])
            column2.metric(label="Armor", value=stats['armor'])
            column1.metric(label="MR", value=stats['magic_resist'])
            column2.metric(label="AS", value=stats['attack_speed'])
            column1.metric(label="AD", value=stats['attack'])
            column2.metric(label="AP", value=stats['skill_cost'])
    with tab4:
        st.write("Items Go Here")

def main():
    # Load data
    data = load_data("./Set13Champions.csv")
    
    cols_per_row = 3  # Number of cards per row
    for i in range(0, len(data), cols_per_row):
        cols = st.columns(cols_per_row)  # Create columns for each row
        for j, col in enumerate(cols):
            if i + j < len(data):  # Ensure no out-of-bounds access
                row = data.iloc[i + j]
                with col:
                    render_card(
                        unit=row['unit'],
                        traits=row['traits'],
                        ability=row['skill_name'],
                        image_path=row['image_path'],
                        stats=row[["health", "armor", "magic_resist", "attack_speed", "attack", "skill_cost"]].to_dict()
                    )

if __name__ == "__main__":
    main()
