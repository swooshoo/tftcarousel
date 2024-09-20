import os
import pandas as pd
import streamlit as st


st.set_page_config(layout="wide", page_title="TFT Set 3 Dashboard", page_icon=":penguin:")

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

def create_tft_grid():
    st.title("Teamfight Tactics Set 3 Units Grid")

    # Load the data
    df = load_data()

    # Create a 52-cell grid (7x8 with some empty cells)
    cols = st.columns(8)
    for i in range(52):
        if i < len(df):
            unit = df.iloc[i]
            with cols[i % 8]:
                st.write(f"**{unit['unit']}**")
                st.write(f"Cost: {unit['cost']}")
                st.write(f"Origin: {unit['origin']}")
                st.write(f"Class: {', '.join(unit['class'])}")
        else:
            with cols[i % 8]:
                st.empty()
                
from streamlit_elements import elements, mui, html, dashboard

def create_dashboard(): #resizable, draggable dashboard
    with elements("dashboard"):
    # You can create a draggable and resizable dashboard using
    # any element available in Streamlit Elements

    # First, build a default layout for every element you want to include in your dashboard
        layout = [
            # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
            dashboard.Item("first_item", 0, 0, 2, 2),
            dashboard.Item("second_item", 2, 0, 2, 2, isDraggable=True, moved=True),
            dashboard.Item("third_item", 0, 2, 1, 1, isResizable=True),
        ]

        # Next, create a dashboard layout using the 'with' syntax. It takes the layout
        # as first parameter, plus additional properties you can find in the GitHub links below.

        with dashboard.Grid(layout):
            mui.Paper("First item", key="first_item")
            mui.Paper("Second item ", key="second_item")
            mui.Paper("Third item ", key="third_item")

        # If you want to retrieve updated layout values as the user move or resize dashboard items,
        # you can pass a callback to the onLayoutChange event parameter.

        def handle_layout_change(updated_layout):
            # You can save the layout in a file, or do anything you want with it.
            # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
            print(updated_layout)

        with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
            mui.Paper("First item", key="first_item")
            mui.Paper("Second item ", key="second_item")
            mui.Paper("Third item ", key="third_item")
            

def image_select_demo():
    from streamlit_image_select import image_select

    img = image_select(
        label="Select a unit",
        images=[
            "briar.png",
            "camille.jpg",
            "diana.png",
            "milio.webp",
            "morgana.png",
            "norra.png",
            "smolder.png",
            "xerath.png",
            "fiora.png",
            "gwen.png",
            "kalista.png",
            "karma.png",
            "nami.png",
            "nasus.png",
            "olaf.png",
            "rakan.png",
            "ryze.png",
            "tahmkench.png",
            "taric.png",
            "varus.png",
        ],

        captions=["Briar", "Camille","Diana","Milio","Morgana","Norra","Smolder","Xerath","Fiora","Gwen","Kalista","Karma","Nami","Nasus","Olaf","Rakan","Ryze","Tahm Kench","Taric","Varus",],
        use_container_width=False
    )
if __name__ == "__main__":
    #create_tft_grid()
    #create_dashboard()
    image_select_demo()