import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Data Job Market Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Job Market Intelligence Platform")

st.write(
    "Analyze hiring trends, in-demand skills, companies, and locations through an interactive dashboard."
)
df = pd.read_csv("data/cleaned_jobs.csv")
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a Section",
    [
        "Dashboard",
        "Skill Analysis",
        "Company Analysis",
        "Location Analysis",
        "Role Comparison"
    ]
)
if page == "Dashboard":
    st.header("Dashboard")
st.write(page)
