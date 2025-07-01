# TODO
# - Change multipage behaviour : https://discuss.streamlit.io/t/rename-the-home-page-in-a-multi-page-app/65533/3
import streamlit as st

st.set_page_config(page_title="Home", 
                   layout="centered",
                   initial_sidebar_state="collapsed")

st.title("Soccer Data Science")

st.markdown("Soccer data science demonstration streamlit application to understand how soccer data can be manipulated and visualized")
st.markdown("## Available content")
st.markdown(" * [Match Insights](/Match_Insights#match-insights) : Explore soccer games for a specific team.")