import streamlit as st
import json
import streamlit.components.v1 as com
import practise as p1
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="DATA GLIMPSE",
    page_icon=":globe_with_meridians:",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.markdown("""
<style>
.stDeployButton
{
    visibility:hidden;
}       
</style>
""",unsafe_allow_html=True)

with st.sidebar:
    with open("animation.json") as source:
        animation=json.load(source)
        temp=st_lottie(animation,width=200,height=158,quality="medium",)
st.sidebar.success("**Lets Take a Tour !!!**")
with st.sidebar:
    selected=option_menu(
        menu_title="Menu",
        options=["Home","Web_scraping","Visualization"],
        default_index=0,
        menu_icon="cast"
    )

if selected =="Home":
    st.markdown('''<h1 style="text-align:left; "> DATA GLIMPSE </h1>''', unsafe_allow_html=True)
    st.markdown("---")

elif selected =="Web_scraping":
    scraper=p1.WebScraper()
    
elif selected=="Visualization":
    st.title(f"dkekd")

