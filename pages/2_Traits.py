import streamlit as st
import pandas as pd

st.set_page_config(
        page_title="Traits",
        page_icon="static/imagestft_icon.webp",
    )

def load_traits(path):
    data = pd.read_csv(
        path, nrows=28, skiprows=1, usecols=range(3),
        names=["name",""]
    )
    data['class'] = data['class'].str.split('/')
    data['image_path'] = "static/images/" + data['image_path'].fillna('')
    return data


# Main function for this page
def main():
    
    st.write("This page will display recommended team compositions and strategies.")

if __name__ == "__main__":
    main()
