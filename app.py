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
df["extracted_skills"] = df["extracted_skills"].apply(ast.literal_eval)
skill_count = {}
for skills in df["extracted_skills"]:
      for skill in skills:
          if skill not in skill_count:
            skill_count[skill] = 1
          else:
            skill_count[skill] += 1

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
    company_counts = df["company"].value_counts().head(10)
    company_df = company_counts.reset_index()
    company_df.columns = ["Company", "Jobs"]
    fig_company, ax = plt.subplots(figsize=(6, 4))
    ax.barh(company_df["Company"], company_df["Jobs"])
    for i, value in enumerate(company_df["Jobs"]):
         ax.text( value + 1,i,f"{value}",va="center",fontsize=9)
       
    ax.set_title("Top 10 Hiring Companies")
    ax.set_xlabel("Number of Jobs")
    ax.set_ylabel("Company")
    ax.invert_yaxis()
    
    
    #Top 10 Hiring Locations
    location_counts = df["location"].value_counts().head(10)
    location_df = location_counts.reset_index()
    location_df.columns = ["Location", "Jobs"]
    fig_location, ax = plt.subplots(figsize=(6, 4))

    ax.barh(location_df["Location"], location_df["Jobs"])
    for i, value in enumerate(location_df["Jobs"]):
         ax.text( value + 1,i,f"{value}",va="center",fontsize=9)
    

    ax.set_title("Top 10 Hiring Locations")
    ax.set_xlabel("Number of Jobs")
    ax.set_ylabel("Location")
    ax.invert_yaxis()
   
    col1, col2 = st.columns(2)

    with col1:
      st.subheader("🏢 Top Hiring Companies")
      st.pyplot(fig_company)

    with col2:
      st.subheader("📍 Top Hiring Locations")
      st.pyplot(fig_location)

    #Top 10 In-Demand Skills
    skill_df = pd.DataFrame(
    skill_count.items(),
    columns=["Skill", "Jobs"]
    )

    skill_df = skill_df.sort_values(
    by="Jobs",
    ascending=False
    ).head(10)

    fig_skills, ax = plt.subplots(figsize=(7, 4.5))

    ax.barh(skill_df["Skill"], skill_df["Jobs"])

    for i, value in enumerate(skill_df["Jobs"]):
      ax.text(value + 5, i, str(value), va="center", fontsize=9)
      
      
    ax.tick_params(axis="y", labelsize=10)
    ax.set_title("Top 10 In Demand Skills")
    ax.set_xlabel("Number of Jobs")
    ax.set_ylabel("Skill")
    ax.invert_yaxis()
    fig_skills.tight_layout()
    
    col3, col4 = st.columns(2)

    with col3:
      st.subheader("🛠️ Top 10 In-Demand Skills")
      st.pyplot(fig_skills)

    #Role Distribution
    role_df = df["Role"].value_counts().reset_index()
    role_df.columns = ["Role", "Jobs"]
    role_df = role_df.sort_values(
    by="Jobs",
    ascending=False
    )
    
    fig_role, ax = plt.subplots(figsize=(6,4))

    ax.bar(
	    role_df["Role"],
	    role_df["Jobs"]
    )

    for i, value in enumerate(role_df["Jobs"]):
           ax.text(
		i,
		value + role_df["Jobs"].max() * 0.02,
		str(value),
		ha="center",
		fontsize=9
           )

    ax.set_title("Job Role Distribution")
    ax.set_xlabel("Role")
    ax.set_ylabel("Number of Jobs")
    with col4:
        st.subheader("💼 Job Role Distribution")
        st.pyplot(fig_role)
if page == "Company Analysis":
    st.title("🏢 Company Analysis")
    st.write(
    "Explore hiring companies and analyze their recruitment trends."
    )
    company_df = (
    df["company"]
    .value_counts()
    .reset_index()
    )
    company_df.columns = ["Company", "Jobs"]
    top_company_df = company_df.head(20)
    fig_company, ax = plt.subplots(figsize=(10,6))

    ax.barh(
    top_company_df["Company"],
    top_company_df["Jobs"]
    )

    ax.invert_yaxis()

    for i, value in enumerate(top_company_df["Jobs"]):
          ax.text(
          value + 1,
          i,
          str(value),
          va="center"
          )
    ax.set_title("Top 20 Hiring Companies")
    ax.set_xlabel("Number of Jobs")

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
    role_df = (
    company_jobs["Role"]
    .value_counts()
    .reset_index()
    )

    role_df.columns = ["Role", "Jobs"]
    
    fig_role, ax = plt.subplots(figsize=(10,6))

    ax.bar(
    role_df["Role"],
    role_df["Jobs"]
    )

    for i, value in enumerate(role_df["Jobs"]):
       ax.text(i, value+1, str(value), ha="center")

    ax.set_title("Role Distribution")
    skill_count = {}

    for skills in company_jobs["extracted_skills"]:
      for skill in skills:

        if skill not in skill_count:
            skill_count[skill] = 1
        else:
            skill_count[skill] += 1

    skill_df = pd.DataFrame(
    skill_count.items(),
    columns=["Skill","Jobs"]
    )

    skill_df = (
    skill_df
    .sort_values(
        by="Jobs",
        ascending=False
    )
    .head(10)
    )
    fig_skill, ax = plt.subplots(figsize=(6,4))
 
    ax.barh(
    skill_df["Skill"],
    skill_df["Jobs"]
    )

    ax.invert_yaxis()

    for i,value in enumerate(skill_df["Jobs"]):
      ax.text(value+0.5,i,str(value),va="center")

    ax.set_title("Top Skills Required")
    col1, col2 = st.columns(2)
    if len(company_jobs) >= 3:
      with col1:
        st.pyplot(fig_role)

      with col2:
      
        st.pyplot(fig_skill) 
    else:
      st.info("Not enough data to generate meaningful visualizations.")
if page == "Location Analysis":
    st.title("📍Location Analysis")
    st.write(
    "Explore hiring Locations and analyze the dominant jobs."
    )
    location_df = (
    df["location"]
    .value_counts()
    .reset_index()
    )
    location_df.columns = ["Location", "Jobs"]
    top_locations_df = location_df.head(20)
    #Top 20 Hiring Locations
    fig_location, ax = plt.subplots(figsize=(10,6))

    ax.barh(
    top_locations_df["Location"],
    top_locations_df["Jobs"]
    )

    ax.invert_yaxis()

    for i, value in enumerate(top_locations_df["Jobs"]):
          ax.text(
          value + 1,
          i,
          str(value),
          va="center"
          )
    ax.set_title("Top 20 Hiring Locations")
    ax.set_xlabel("Number of Jobs")

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
    company_df = (
    location_jobs["company"]
    .value_counts()
    .head(10)
    .reset_index()
    )

    company_df.columns = ["Company", "Jobs"]
    
    fig_company, ax = plt.subplots(figsize=(10,6))

    ax.bar(
    company_df["Company"],
    company_df["Jobs"]
    )

    for i, value in enumerate(company_df["Jobs"]):
       ax.text(i, value+1, str(value), ha="center")

    ax.set_title("Top 10 Hiring Companies")
    st.write(location_jobs)
    
    skill_count = {}

    for skills in location_jobs["extracted_skills"]:
      for skill in skills:

        if skill not in skill_count:
            skill_count[skill] = 1
        else:
            skill_count[skill] += 1

    skill_df = pd.DataFrame(
    skill_count.items(),
    columns=["Skill","Jobs"]
    )

    skill_df = (
    skill_df
    .sort_values(
        by="Jobs",
        ascending=False
    )
    .head(10)
    )
    fig_skill, ax = plt.subplots(figsize=(6,4))
 
    ax.barh(
    skill_df["Skill"],
    skill_df["Jobs"]
    )

    ax.invert_yaxis()

    for i,value in enumerate(skill_df["Jobs"]):
      ax.text(value+0.5,i,str(value),va="center")

    ax.set_title("Top Skills Required")
    col1, col2 = st.columns(2)
    if company_df["Jobs"].max() <= 1:
      st.info(
        "Companies in this location have only one job posting each, "
        "so the chart is not very informative."
      )
    else:
      
        st.pyplot(fig_company)
      
    role_df = (
    location_jobs["Role"]
    .value_counts()
    .reset_index()
    )

    role_df.columns = ["Role", "Jobs"]
    fig_role, ax = plt.subplots(figsize=(6,4))

    ax.barh(role_df["Role"], role_df["Jobs"])

    for i, value in enumerate(role_df["Jobs"]):
      ax.text(value + 0.3, i, str(value), va="center")

    ax.set_title("Role Distribution")
    ax.set_xlabel("Number of Jobs")
    ax.invert_yaxis()

    
    col1, col2 = st.columns(2)

    col3, col4 = st.columns(2)

    with col3:
      st.subheader("🛠️ Top Skills")
      st.pyplot(fig_skill)

    with col4:
      st.subheader("💼 Role Distribution")
      st.pyplot(fig_role)
