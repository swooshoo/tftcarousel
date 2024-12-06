import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Traits",
    page_icon="static/tft_icon.png",
)

def legend():
    st.sidebar.header("Legend")
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
    with st.sidebar.expander("What do these terms mean?"):
        st.markdown(':red[AD] is base physical damage dealt with normal attacks, and is a key stat for champions who rely on consistent basic attacks to deal damage.')
        st.markdown(':blue[AP] is base magic damage dealt with abilities, and is a key stat for champions who rely on ability casts to deal damage.')
        st.markdown(''':green[HP] is base health points, and determines how much damage a unit can take in flat numbers. HP is prioritized on tankier frontline units.''')
        st.markdown(''':gray[DA] is damage amplification, and increases the total output of a unit by a percent value. For instance, a unit with 12% :gray[DA] whose ability does 100 base damage will do 112 damage.''')  
        st.markdown(''':orange[AR] is armor, and is the physical defense stat that nullifies physical damage dealt against it. It is calculated by :orange[AR]/(100 + :orange[AR]).''')
        st.markdown(''':violet[MR] is magic resist, and is the magic defense stat that nullifies magic damage dealt against it. It is calculated by :violet[MR]/(100 + :violet[MR]).''')
        st.markdown(''':orange[AS] is attack speed, and represents the number of auto-attacks per second. This is capped at 5.00, or five attacks per second.''')
        st.markdown(''':gray[DR] is Durability, and represents a unit's percent reduction in damage taken after :orange[AR] and :violet[MR] calculations.''')

def load_traits(traits_path):
    traits = pd.read_csv(
        traits_path, nrows = 26, skiprows =1, usecols=range(2),
        names=["trait","description"]
    )
    return traits

def format_description(description):
    """
    Automatically add Markdown-compatible line breaks to the description.
    Break at semicolons and periods, followed by two spaces for Markdown line breaks.
    """
    # Split the text at logical delimiters, then rejoin with Markdown breaks
    formatted = description.replace("   ", "  \n") #add newlines
    return formatted

def render_trait(trait, description):
    st.divider() 
    trait = trait.replace("_", " ")
    trait_image_path = f"static/traits/{trait}.webp"
    col1, col2 = st.columns(2,gap="small")
    with col1:
        if os.path.exists(trait_image_path):
            st.image(trait_image_path,width=60,)
        else:
            st.write(f"Trait image not found: {trait_image_path}")
    with col2:
        st.subheader(f"{trait.title()}")
    formatted_description = format_description(description)
    st.markdown(formatted_description)

# Main function for this page
def main():
    traits = load_traits("traits.csv")
    legend()
    st.header("Set 13 Traits")
    cols_per_row = 2  # Number of cards per row
    for i in range(0, len(traits), cols_per_row):
        cols = st.columns(cols_per_row)  # Create columns for each row
        for j, col in enumerate(cols):
            if i + j < len(traits):  # Ensure no out-of-bounds access
                row = traits.iloc[i + j]
                with col:
                    formatted_description = format_description(row['description'])
                    render_trait(
                        trait=row['trait'],
                        description=formatted_description,
                    )

if __name__ == "__main__":
    main()
