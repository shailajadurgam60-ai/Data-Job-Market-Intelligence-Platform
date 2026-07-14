import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ast

st.set_page_config(
    page_title="Data Job Market Intelligence Platform",
    page_icon="📊",
    layout="wide"
)
st.title("📊 Data Job Market Intelligence Platform")
st.write(
    "Analyze hiring trends, in-demand skills, companies, and locations through an interactive dashboard."
)
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_jobs.csv")
    df["extracted_skills"] = df["extracted_skills"].apply(ast.literal_eval)
    return df

df = load_data()
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a Section",
    [
        "Dashboard",
        "Skill Analysis",
        "Company Analysis",
        "Location Analysis",
        "Role Comparision"
    ]
 )
#Skill df function
def get_skill_df(data):
    skill_count = {}

    for skills in data["extracted_skills"]:
        for skill in skills:
            skill_count[skill] = skill_count.get(skill, 0) + 1

    skill_df = (
        pd.DataFrame(
            skill_count.items(),
            columns=["Skill", "Jobs"]
        )
        .sort_values(by="Jobs", ascending=False)
    )

    return skill_df, skill_count
#company df function
def get_company_df(data, top_n=10):
    company_df = (
        data["company"]
        .value_counts()
        .reset_index()
    )

    company_df.columns = ["Company", "Jobs"]

    return company_df.head(top_n)
#Location df function
def get_location_df(data, top_n=10):

    location_df = (
        data["location"]
        .value_counts()
        .reset_index()
    )

    location_df.columns = ["Location", "Jobs"]

    return location_df.head(top_n)
#Role df function
def get_role_df(data):

    role_df = (
        data["Role"]
        .value_counts()
        .reset_index()
    )

    role_df.columns = ["Role", "Jobs"]

    return role_df
#Charts function for skill,location and company analysis
def plot_horizontal_bar(
    data,
    x_col,
    y_col,
    title,
    xlabel,
    figsize=(8,5)
):
    fig, ax = plt.subplots(figsize=figsize)

    ax.barh(data[x_col], data[y_col])

    ax.invert_yaxis()

    for i, value in enumerate(data[y_col]):
        ax.text(value + 0.3, i, str(value), va="center")

    ax.set_title(title)
    ax.set_xlabel(xlabel)

    return fig
#Chart for Role Distribution 
def plot_vertical_bar(
    data,
    x_col,
    y_col,
    title,
    xlabel,
    ylabel,
    figsize=(8,5)
):
    fig, ax = plt.subplots(figsize=figsize)

    ax.bar(data[x_col], data[y_col])

    for i, value in enumerate(data[y_col]):
        ax.text(i, value + 0.5, str(value), ha="center")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    plt.xticks(rotation=15)

    return fig
skill_df,skill_count=get_skill_df(df)
with st.expander("🔍 Debug Values"):
    st.write("Total Jobs:", len(df))
    st.write("Total Companies:", df["company"].nunique())
    st.write("Total Locations:", df["location"].nunique())
    st.write("SQL Count:", skill_count["sql"])
    st.write("Python Count:", skill_count["python"])
if page=="Dashboard":
    st.header("📊 Job Market Overview")
    #Dashboard Metrics
    total_jobs = len(df)
    total_skills=len(skill_count)
    total_companies=df["company"].nunique()
    total_locations=df["location"].nunique()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
      st.metric("📊 Total Jobs", total_jobs)

    with col2:
      st.metric("🏢 Hiring Companies", total_companies)

    with col3:
      st.metric("📍 Hiring Locations", total_locations)

    with col4:
      st.metric("🛠️ Unique Skills", total_skills)
       #Top 10 Hiring Companies
    company_df = get_company_df(df)
    fig_company = plot_horizontal_bar(
    company_df,
    "Company",
    "Jobs",
    "Top Hiring Companies",
    "Number of Jobs"
     )

    
   
    #Top 10 Hiring Locations
    location_df = get_location_df(df)
    fig_location=plot_horizontal_bar(
    location_df,
    "Location",
    "Jobs",
    "Top Hiring Locations",
    "Number of Jobs"
     )
    
    col1, col2 = st.columns(2)
    with col1:
      st.subheader("🏢 Top Hiring Companies")
      st.pyplot(fig_company)
    with col2:
      st.subheader("📍 Top Hiring Locations")
      st.pyplot(fig_location)

    #Top 10 In-Demand Skills
    skill_df, skill_count = get_skill_df(df)
    
    fig_skills=plot_horizontal_bar(
     skill_df,
    "Skill",
    "Jobs",
    "Top In-Demand Skills",
    "Number of Jobs"
     )
    
    col3, col4 = st.columns(2)
    with col3:
      st.subheader("🛠️ Top 10 In-Demand Skills")
      st.pyplot(fig_skills)

    #Role Distribution
    
    role_df = get_role_df(df)
    fig_role=plot_vertical_bar(
     role_df,
    "Role",
    "Jobs",
    "Top In-Demand Roles",
    "Role",
    "Number of Jobs"
     )
    with col4:
        st.subheader("💼 Job Role Distribution")
        st.pyplot(fig_role)
    st.markdown("---")
    st.subheader("💡 Key Insights")
    top_skill = skill_df.iloc[0]["Skill"]
    top_skill_jobs = skill_df.iloc[0]["Jobs"]

    top_company = company_df.iloc[0]["Company"]
    top_company_jobs = company_df.iloc[0]["Jobs"]

    top_location = location_df.iloc[0]["Location"]
    top_location_jobs = location_df.iloc[0]["Jobs"]

    top_role = role_df.iloc[0]["Role"]
    top_role_jobs = role_df.iloc[0]["Jobs"]
    st.markdown(f"""
    ### 📈 Market Summary

    The current job market is primarily driven by **{top_role}** opportunities.
    Employers are actively seeking professionals with **{top_skill}** skills.
    Among all companies, **{top_company}** has the highest hiring activity,
    while **{top_location}** continues to be the leading hiring location.
    """)
    st.info(f"""
    📊 **Dataset Summary**

    • **{top_skill}** is the most in-demand skill with **{top_skill_jobs}** job postings.

    • **{top_company}** is the top hiring company with **{top_company_jobs}** openings.

    • **{top_location}** has the highest hiring activity with **{top_location_jobs}** jobs.

    • **{top_role}** is the most frequently advertised role with **{top_role_jobs}** postings.
    """)
if page == "Company Analysis":
    st.title("🏢 Company Analysis")
    st.write(
    "Explore hiring companies and analyze their recruitment trends."
    )
    company_df = get_company_df(df,top_n=20)
    top_company_df = company_df.head(20)
    fig_company=plot_horizontal_bar(
    top_company_df,
    "Company",
    "Jobs",
    "Top 20 Hiring Companies",
    "Number of Jobs",
    )
    st.pyplot(fig_company)
    #Select Desired Company
    selected_company = st.selectbox(
    "Select a Company",
    sorted(company_df["Company"])
    )
    #Filter Dataset
    company_jobs = df[
    df["company"] == selected_company
    ]
    col1, col2, col3 = st.columns(3)
    with col1:
      st.metric("Jobs Posted", len(company_jobs))

    with col2:
      st.metric(
        "Locations",
        company_jobs["location"].nunique()
      )

    with col3:
      st.metric(
        "Roles",
        company_jobs["Role"].nunique()
      )
    role_df = get_role_df(company_jobs)
    filtered_role_df = role_df[role_df["Role"] != "Other"]
    if not filtered_role_df.empty:
      role_df = filtered_role_df
    
    fig_role=plot_vertical_bar(
    role_df,
    "Role",
    "Jobs",
    "Role Distribution",
    "Role",
    "Number of Jobs"
    )
    skill_df,skill_count=get_skill_df(company_jobs)
    
    fig_skill=plot_horizontal_bar(
    skill_df,
    "Skill",
    "Jobs",
    "Top Skills Required",
    "Number of Jobs"
    )
    col1, col2 = st.columns(2)
    if len(company_jobs) >= 3:
      with col1:
        st.pyplot(fig_role)

      with col2:
      
        st.pyplot(fig_skill) 
    else:
      st.info("Not enough data to generate meaningful visualizations.")
    #Job Listings
    st.subheader("📋 Job Listings")

    st.dataframe(
    company_jobs[
        [
            "title",
            "company",
            "location",
            "Role"
        ]
    ],
    use_container_width=True
    )
    #Insights
    # -----------------------------
# Company Insights
# -----------------------------

# Company-specific location data
    company_location_df = get_location_df(company_jobs)

# Top values
    top_role = role_df.iloc[0]["Role"]
    top_role_jobs = role_df.iloc[0]["Jobs"]

    top_skill = skill_df.iloc[0]["Skill"]
    top_skill_jobs = skill_df.iloc[0]["Jobs"]

    top_location = company_location_df.iloc[0]["Location"]
    top_location_jobs = company_location_df.iloc[0]["Jobs"]

    total_jobs = len(company_jobs)
    unique_roles = company_jobs["Role"].nunique()
    unique_locations = company_jobs["location"].nunique()
    unique_skills = len(skill_count)
    percentage = round((top_role_jobs / total_jobs) * 100, 1)
    overall_company_df = (
    df["company"]
    .value_counts()
    .reset_index()
    )

    overall_company_df.columns = ["Company", "Jobs"]

    company_rank = (
    overall_company_df[
        overall_company_df["Company"] == selected_company
    ].index[0] + 1
    )
    if company_rank <= 10:
      recruiter_status = "one of the Top 10 recruiters"

    elif company_rank <= 20:
      recruiter_status = "one of the Top 20 recruiters"

    else:
      recruiter_status = "an emerging recruiter"
    st.markdown("---")
    st.subheader("💡 Company Insights")

    st.markdown(f"""
    ### 📈 Company Summary

    **{selected_company}** is **{recruiter_status}** in the current job market,
    with **{total_jobs}** job openings.

    Approximately **{percentage}%** of its openings are for
    **{top_role}** positions, indicating its primary hiring focus.

    The company mainly seeks professionals skilled in
    **{top_skill}**, with **{top_location}** being its leading hiring location.
    """)

    st.success(f"""
    ### 🔍 Key Findings

    ✅ Ranked **#{company_rank}** among all hiring companies.

    ✅ **{selected_company}** currently has **{total_jobs}** job openings.

    ✅ **{top_role}** is the dominant role (**{top_role_jobs}** jobs).

    ✅ **{top_skill}** is the most requested skill (**{top_skill_jobs}** jobs).

    ✅ **{top_location}** is the primary hiring location (**{top_location_jobs}** jobs).
    """)

    st.info(f"""
    🎯 **Hiring Diversity**

    • Hiring spans **{unique_roles}** different roles.

    • Jobs are distributed across **{unique_locations}** locations.

    • Recruiters are looking for **{unique_skills}** unique skills.
     """)
if page == "Location Analysis":
    st.title("📍Location Analysis")
    st.write(
    "Explore hiring Locations and analyze the dominant jobs."
    )
    location_df =get_location_df(df)
    top_locations_df = location_df.head(20)
    #Top 20 Hiring Locations
    fig_location=plot_horizontal_bar(top_locations_df,
    "Location",
    "Jobs",
    "Top 10 Hiring Locations",
    "Number of Jobs"
    )
    st.pyplot(fig_location)
    location_options = (
    df["location"]
    .value_counts()
    .index
    .tolist()
    )
    selected_location = st.selectbox(
       "Select a Location",
    location_options
    )
    location_jobs = df[
    df["location"] == selected_location
    ]
    
    col1, col2, col3 = st.columns(3)
    with col1:
      st.metric("Jobs Posted", len(location_jobs))

    with col2:
      st.metric(
        "Companies",
        location_jobs["company"].nunique()
      )

    with col3:
      st.metric(
        "Roles",
        location_jobs["Role"].nunique()
      )
    company_df = get_company_df(location_jobs)
    fig_company=plot_horizontal_bar(company_df,
    "Company",
    "Jobs",
    "Top 10 Hiring Companies",
    "Number of Jobs"
    )
    st.write(location_jobs)
    skill_df,skill_count = get_skill_df(location_jobs)
    fig_skill=plot_horizontal_bar(skill_df,
    "Skill",
    "Jobs",
    "Top Skills Required",
    "Number of Jobs"
    )
    col1, col2 = st.columns(2)
    if company_df["Jobs"].max() <= 1:
      st.info(
        "Companies in this location have only one job posting each, "
        "so the chart is not very informative."
      )
    else:
      
        st.pyplot(fig_company)
      
    role_df = get_role_df(location_jobs)

    fig_role=plot_vertical_bar(role_df,
    "Role",
    "Jobs",
    "Role Distribution",
    "Number of Jobs",
    "Roles"
    )
    col1, col2 = st.columns(2)

    col3, col4 = st.columns(2)

    with col3:
      st.subheader("🛠️ Top Skills")
      st.pyplot(fig_skill)

    with col4:
      st.subheader("💼 Role Distribution")
      st.pyplot(fig_role)
    #Insights
    top_role = role_df.iloc[0]["Role"]
    top_role_jobs = role_df.iloc[0]["Jobs"]

    top_skill = skill_df.iloc[0]["Skill"]
    top_skill_jobs = skill_df.iloc[0]["Jobs"]

    top_company = company_df.iloc[0]["Company"]
    top_company_jobs = company_df.iloc[0]["Jobs"]

    total_jobs = len(location_jobs)

    unique_companies = location_jobs["company"].nunique()
    unique_roles = location_jobs["Role"].nunique()
    unique_skills = len(skill_count)
    percentage = round((top_role_jobs / total_jobs) * 100, 1)
    if total_jobs >= 40:
      market = "a major hiring hub"

    elif total_jobs >= 20:
      market = "an active hiring market"

    else:
      market = "an emerging hiring market"
    st.markdown(f"""
    ### 📈 Location Summary

    **{selected_location}** is {market}, offering **{total_jobs}** job opportunities.

    Nearly **{percentage}%** of the openings are for **{top_role}** positions.

    Employers primarily seek **{top_skill}** skills, while **{top_company}**
    is the most active recruiter in this location.
    """)
    st.success(f"""
    ### 🔍 Key Findings

    ✅ **{selected_location}** has **{total_jobs}** job openings.

    ✅ **{top_role}** is the dominant role (**{top_role_jobs}** jobs).

    ✅ **{top_skill}** is the most requested skill (**{top_skill_jobs}** jobs).

    ✅ **{top_company}** has the highest hiring activity (**{top_company_jobs}** jobs).
    """)
    st.info(f"""
    🎯 **Location Diversity**

    • **{unique_companies}** companies are hiring here.

    • Opportunities span **{unique_roles}** different job roles.

    • Recruiters are looking for **{unique_skills}** unique skills.
    """)
if page == "Skill Analysis":
    st.subheader("🛠️ Skill Analysis")
    all_skills = set()

    for skills in df["extracted_skills"]:
      for skill in skills:
        all_skills.add(skill)

    selected_skill = st.selectbox(
    "Select a Skill",
    sorted(all_skills)
    )
    skill_jobs = df[
    df["extracted_skills"].apply(
        lambda skills: selected_skill in skills
    )
    ]
    col1, col2, col3 = st.columns(3)

    with col1:
      st.metric("Jobs", len(skill_jobs))

    with col2:
      st.metric(
        "Companies",
        skill_jobs["company"].nunique()
      )

    with col3:
      st.metric(
        "Locations",
        skill_jobs["location"].nunique()
      )
    company_df = get_company_df(skill_jobs)
    fig_company=plot_horizontal_bar(company_df,
    "Company",
    "Jobs",
    "Top 10 Hiring Companies",
    "Number of Jobs"
    )
    location_df = get_location_df(skill_jobs)
    fig_location=plot_horizontal_bar(location_df,
    "Location",
    "Jobs",
    "Top 10 Hiring Locations",
    "Number of Jobs"
    )
    col1, col2 = st.columns(2)

    with col1:
      st.subheader("🏢 Top Hiring Companies")
      st.pyplot(fig_company)

    with col2:
      st.subheader("📍 Top Hiring Locations")
      st.pyplot(fig_location)
    role_df = get_role_df(skill_jobs)
    fig_role=plot_vertical_bar(role_df,
    "Role",
    "Jobs",
    "Role Distribution",
    "Number of Jobs",
    "Roles"
    )
    st.pyplot(fig_role)
    st.subheader("📋 Job Listings")
 
    skill_jobs_display = skill_jobs.copy()

    skill_jobs_display["Skill"] = selected_skill
    st.dataframe(
    skill_jobs_display[
        ["title", "company", "location", "Role", "Skill"]
    ]
    )
    total_jobs = len(skill_jobs)

    top_role = (
    skill_jobs["Role"]
    .value_counts()
    .idxmax()
    )

    top_role_jobs = (
    skill_jobs["Role"]
    .value_counts()
    .max()
    )

    top_company = (
    skill_jobs["company"]
    .value_counts()
    .idxmax()
    )

    top_company_jobs = (
    skill_jobs["company"]
    .value_counts()
    .max()
    )
   
    top_location = (
    skill_jobs["location"]
    .value_counts()
    .idxmax()
    )

    top_location_jobs = (
    skill_jobs["location"]
    .value_counts()
    .max()
    )
    unique_companies = skill_jobs["company"].nunique()
    unique_locations = skill_jobs["location"].nunique()
    #Insights
    st.markdown("---")
    st.subheader("💡 Skill Insights")

    st.markdown(f"""
    ### 📈 Skill Summary

    **{selected_skill.title()}** appears in **{total_jobs}** job postings across
    **{unique_companies}** companies and **{unique_locations}** locations.

    This skill is most frequently required for **{top_role}** positions.
    The highest demand comes from **{top_company}**, while **{top_location}**
    has the largest concentration of opportunities requiring this skill.
    """)
    st.success(f"""
    ### 🔍 Key Findings

    ✅ **{selected_skill.title()}** appears in **{total_jobs}** job postings.

    ✅ Most demand is for **{top_role}** (**{top_role_jobs}** jobs).

    ✅ **{top_company}** has the highest demand (**{top_company_jobs}** jobs).

    ✅ **{top_location}** has the most openings (**{top_location_jobs}** jobs).

    ✅ This skill is required by **{unique_companies}** companies across
    **{unique_locations}** hiring locations.
    """)
if page=="Role Comparision":
    st.subheader("Role Comparision")
    selected_role = st.selectbox(
    "Select a Role",
    sorted(df["Role"].unique())
    )   
    role_jobs = df[
    df["Role"] == selected_role
    ] 
    unique_skills = set()

    for skills in role_jobs["extracted_skills"]:
      for skill in skills:
        unique_skills.add(skill)

    total_skills = len(unique_skills)
    #Metrics
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
      st.metric("Jobs", len(role_jobs))

    with col2:
      st.metric("Companies", role_jobs["company"].nunique())

    with col3:
      st.metric("Locations", role_jobs["location"].nunique())

    with col4:
      st.metric("Skills", total_skills)
      

    skill_df,skill_count=get_skill_df(role_jobs)
    #Top Charts
    company_df = get_company_df(role_jobs)
    fig_company=plot_horizontal_bar(company_df,
    "Company",
    "Jobs",
    "Top 10 Hiring Companies",
    "Number of Jobs"
    )
    location_df = get_location_df(role_jobs)
    fig_location=plot_horizontal_bar(location_df,
    "Location",
    "Jobs",
    "Top 10 Hiring Locations",
    "Number of Jobs"
    )
    col1, col2 = st.columns(2)

    with col1:
      st.subheader("🏢 Top Hiring Companies")
      st.pyplot(fig_company)

    with col2:
      st.subheader("📍 Top Hiring Locations")
      st.pyplot(fig_location)
    role_df = get_role_df(role_jobs)
    fig_role=plot_vertical_bar(role_df,
    "Role",
    "Jobs",
    "Role Distribution",
    "Number of Jobs",
    "Roles"
    )
    st.pyplot(fig_role)
    st.subheader("📋 Job Listings")
 
    role_jobs_display = role_jobs.copy()

    role_jobs_display["Role"] = selected_role
    st.dataframe(
    role_jobs_display[
        ["title", "company", "location", "Role"]
    ]
    )
    #Insights
    total_jobs = len(role_jobs)

    top_skill = skill_df.iloc[0]["Skill"]
    top_skill_jobs = skill_df.iloc[0]["Jobs"]

    top_company = company_df.iloc[0]["Company"]
    top_company_jobs = company_df.iloc[0]["Jobs"]

    top_location = location_df.iloc[0]["Location"]
    top_location_jobs = location_df.iloc[0]["Jobs"]

    unique_companies = role_jobs["company"].nunique()
    unique_locations = role_jobs["location"].nunique()
    st.markdown("---")
    st.subheader("💡 Role Insights")

    st.markdown(f"""
    ### 📈 Role Summary

    There are **{total_jobs}** **{selected_role}** positions available in the dataset.

    These opportunities are spread across **{unique_companies}** companies and
    **{unique_locations}** hiring locations.

    The most demanded skill is **{top_skill}**, while **{top_company}**
    currently has the highest number of openings.
    """)
    st.success(f"""
    ### 🔍 Key Findings

    ✅ **{selected_role}** has **{total_jobs}** job postings.

    ✅ **{top_skill}** is the most requested skill (**{top_skill_jobs}** jobs).

    ✅ **{top_company}** has the highest demand (**{top_company_jobs}** jobs).
 
    ✅ **{top_location}** has the largest number of openings (**{top_location_jobs}** jobs).

    ✅ Opportunities are available across **{unique_companies}** companies and **{unique_locations}**   locations.
    """)
