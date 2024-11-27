import pandas as pd
import streamlit as st
import os

st.set_page_config(
    page_title="Units",
    page_icon="static/tft_icon.png",
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

def load_traits(traits_path):
    trait_data = pd.read_csv(traits_path)
    # Create a dictionary mapping traits to descriptions
    trait_description_map = trait_data.set_index('trait')['description'].to_dict()
    return trait_description_map
    
# Display card for each unit
def render_unit(unit, cost, traits, ability, image_path, stats, trait_description_map):
    unit = unit.replace("_", " ")
    unit = unit.replace("Ranged", "")
    
    # Determine the color based on the unit cost
    color_map = {1: "gray", 2: "green", 3: "blue", 4: "violet", 5: "orange"}
    color = color_map.get(cost, "gray")
    # Display the header with the divider color
    st.subheader(unit.title(), divider=color)
   
    st.image(image_path, use_container_width=False)
    # Tabs for unit-specific details
    tab1, tab2, tab3, tab4 = st.tabs(["Traits", "Ability", "Stats", "Items"])
    
    # Tab 1: Display traits with images and names
    with tab1:
        for trait in traits:
            cleaned_trait = trait.lower().replace("'", "").replace("[", "").replace("]", "") #could optimize this somehow?
            trait_image_path = f"static/traits/{cleaned_trait}.webp"
            col1, col2 = st.columns(2,gap="small")
            with col1:
                if os.path.exists(trait_image_path):
                    st.image(trait_image_path,width=50,)
                else:
                    st.write(f"Trait image not found: {trait_image_path}")  
            with col2:
                st.write(f"{cleaned_trait.title()}")
            description = trait_description_map.get(cleaned_trait.replace(" ","_"), "No description available.")
            formatted_desc = description.replace("   ", "  \n")
            st.markdown(formatted_desc)    
  
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
            
    st.subheader(" ",divider=color) 
    
def main():
    # Load data
    data = load_data("./Set13Champions.csv")
    trait_description_map = load_traits("traits.csv")
    st.sidebar.header("How to Use This Page")
    col1, col2 = st.sidebar.columns(2,gap="small")
    with col1:
        st.markdown(''':red[AD] | Attack Damage''')
        st.markdown(''':blue[AP] | Ability Power''') 
        st.markdown(''':green[HP] | Health''')
        st.markdown(''':gray[DA] | Damage Amp''')         
    with col2:
        st.markdown(''':orange[AR] | Armor''')
        st.markdown(''':violet[MR] | Magic Resist''')
        st.markdown(''':orange[AS] | Attack Speed''')
        st.markdown(''':gray[DR] | Durability''')
        

    cols_per_row = 3  # Number of cards per row
    for i in range(0, len(data), cols_per_row):
        cols = st.columns(cols_per_row)  # Create columns for each row
        for j, col in enumerate(cols):
            if i + j < len(data):  # Ensure no out-of-bounds access
                row = data.iloc[i + j]
                with col:
                    render_unit(
                        unit=row['unit'],
                        cost=row['cost'],
                        traits=row['traits'],
                        ability=row['skill_name'],
                        image_path=row['image_path'],
                        stats=row[["health", "armor", "magic_resist", "attack_speed", "attack", "skill_cost"]].to_dict(),
                        trait_description_map=trait_description_map,
                    )
    

if __name__ == "__main__":
    main()
