import streamlit as st
import pandas as pd
import os

st.set_page_config(
        page_title="Traits",
        page_icon="static/imagestft_icon.webp",
    )

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
            st.image(trait_image_path,width=75,)
        else:
            st.write(f"Trait image not found: {trait_image_path}")
    with col2:
        st.subheader(f"{trait.title()}")
    formatted_description = format_description(description)
    st.markdown(formatted_description)

# Main function for this page
def main():
    traits = load_traits(".\traits.csv")

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
