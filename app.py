import os
import pandas as pd
import streamlit as st


st.set_page_config(layout="wide", page_title="TFT Set 12 Dashboard", page_icon=":penguin:")

# LOAD DATA ONCE
@st.cache_resource
def load_data():
    path = "Set3Champions.csv"
    if not os.path.isfile(path):
        path = f"https://github.com/swooshoo/set3carousel/raw/main/{path}"

    data = pd.read_csv(
        path,
        nrows=52,  # 52 units in set 3
        names=[
            "unit",
            "cost",
            "health",
            "armor",
            "magic_resist",
            "attack",
            "attack_range",
            "attack_speed",
            "dps",
            "skill_name",
            "skill_cost",
            "origin",
            "class"
        ],  # specify names directly since they don't change
        skiprows=1,  # don't read header since names specified directly
        usecols=range(13),  # uses all columns
    )
    
    # Convert the 'class' column to a list of classes
    data['class'] = data['class'].str.split('/')
    
    return data
                
from streamlit_elements import elements, mui, html, dashboard

def create_dashboard(): #resizable, draggable dashboard
    with elements("dashboard"):
    # You can create a draggable and resizable dashboard using
    # any element available in Streamlit Elements

    # First, build a default layout for every element you want to include in your dashboard
        layout = [
            # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
            dashboard.Item("first_item", 0, 0, 4, 2),
            dashboard.Item("second_item", 4, 2, 4, 2, isDraggable=True, isResizable=True),
            dashboard.Item("third_item", 8, 2, 4, 2, isDraggable= True, isResizable=True),
        ]
        # Next, create a dashboard layout using the 'with' syntax. It takes the layout
        # as first parameter, plus additional properties you can find in the GitHub links below.

        # If you want to retrieve updated layout values as the user move or resize dashboard items,
        # you can pass a callback to the onLayoutChange event parameter.

        def handle_layout_change(updated_layout):
            # You can save the layout in a file, or do anything you want with it.
            # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
            print(updated_layout)

        with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
            mui.Typography("Selected Unit", key="first_item")
            mui.Paper("Traits ", key="second_item")
            mui.Paper("Ability", key="third_item")


def image_select_demo():
    from streamlit_image_select import image_select

    img = image_select(
        label="Select a unit",
        images=[
            "images/briar.png",
            "images/camille.jpg",
            "images/diana.png",
            "images/milio.webp",
            "images/morgana.png",
            "images/norra.png",
            "images/smolder.png",
            "images/xerath.png",
            "images/fiora.png",
            "images/gwen.png",
            "images/kalista.png",
            "images/karma.png",
            "images/nami.png",
            "images/nasus.png",
            "images/olaf.png",
            "images/rakan.png",
            "images/ryze.png",
            "images/tahmkench.png",
            "images/taric.png",
            "images/varus.png",
        ],

        captions=["Briar", "Camille","Diana","Milio","Morgana","Norra","Smolder","Xerath","Fiora","Gwen","Kalista","Karma","Nami","Nasus","Olaf","Rakan","Ryze","Tahm Kench","Taric","Varus",],
        use_container_width=False,
        return_value="index"
    )
    st.write(str(img)[:100])
    
    #need to implement a while statement. default value = 0. while img is a valid number, show a card fr
    

if __name__ == "__main__":
    #create_tft_grid()
    create_dashboard()
    image_select_demo()