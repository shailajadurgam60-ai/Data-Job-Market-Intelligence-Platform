import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ast

st.set_page_config(
    page_title="Data Job Market Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_jobs.csv")
    df["extracted_skills"] = df["extracted_skills"].apply(ast.literal_eval)
    return df

df = load_data()
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
skill_df,skill_count=get_skill_df(df)
page = st.sidebar.radio(
    "Choose a Section",
    [
        "Dashboard",
        "Skill Analysis",
        "Company Analysis",
        "Location Analysis",
        "Role Comparision",
        "About Project"
    ]
)
st.sidebar.markdown("---")

with st.sidebar.expander("📊 Dataset Information"):

    st.metric("Job Posts", len(df))
    st.metric("Companies", df["company"].nunique())
    st.metric("Locations", df["location"].nunique())
    st.metric("Roles", df["Role"].nunique())
    st.metric("Skills", len(skill_count))
with st.sidebar.expander("📑 Dataset Columns"):
    st.write(df.columns.tolist())
with st.sidebar.expander("🔍 View Dataset"):

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    st.caption("Showing first 10 rows")

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
    figsize=(6,4)
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
    figsize=(6,4)
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
def show_footer():
    st.markdown("---")

    st.markdown(
    """
    <div style="text-align:center; padding:18px;">

    <h4>❤️ Thank you for visiting!</h4>

    <p>
    Built with curiosity, consistency, and ❤️ for learning.
    </p>

    <p style="color:#9CA3AF;">
    Data Job Market Intelligence Platform • Powered by Python, Pandas, Matplotlib & Streamlit
    </p>

    </div>
    """,
    unsafe_allow_html=True
    )
skill_df,skill_count=get_skill_df(df)
if page=="Dashboard":
    st.title("📊 Data Job Market Intelligence Platform")
    st.write(
        "Analyze hiring trends, in-demand skills, companies, locations and roles through an interactive dashboard."
    )
    st.header("📈 Job Market Overview")
    st.caption(
    "A quick snapshot of the current data job market."
    )
    #Dashboard Metrics
    total_jobs = len(df)
    total_skills=len(skill_count)
    total_companies=df["company"].nunique()
    total_locations=df["location"].nunique()
    col1, col2, col3, col4 = st.columns(4)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
      with st.container(border=True):
        st.metric("📊 Total Jobs", total_jobs)

    with col2:
      with st.container(border=True):
        st.metric("🏢 Companies", total_companies)

    with col3:
      with st.container(border=True):
        st.metric("📍 Locations", total_locations)

    with col4:
      with st.container(border=True):
        st.metric("🛠 Skills", total_skills)
    st.info(
    "This dashboard summarizes hiring activity across companies, locations, job roles and technical  skills extracted from the dataset."
    )
    st.markdown("---")
    st.header("📈 Market Visualizations")
    st.caption("Explore hiring trends across companies, locations, skills, and job roles.")
     
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
      with st.container():
        st.subheader("🏢 Top Hiring Companies")
        st.caption("Companies posting the highest number of jobs.")
        st.pyplot(fig_company, use_container_width=True)
    with col2:
       with st.container():
         st.subheader("📍 Top Hiring Locations")
         st.caption("Top Hiring Locations for Data Professionals")
         st.pyplot(fig_location,use_container_width=True)

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
      with st.container():
      
       st.subheader("🛠️ Top 10 In-Demand Skills")
       st.caption("Most Frequently Required Skills Across Job Postings")
       st.pyplot(fig_skills,use_container_width=True)

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
       with st.container():
          
          st.subheader("💼 Job Role Distribution")
          st.caption("Distribution of Data Job Roles in the Dataset")
          st.pyplot(fig_role,use_container_width=True)
    st.markdown("---")
    st.header("💡 Dashboard Insights")
    st.header("📊 Dashboard Overview")
    st.caption("A quick summary of the current data job market.")
    top_skill = skill_df.iloc[0]["Skill"]
    top_skill_jobs = skill_df.iloc[0]["Jobs"]

    top_company = company_df.iloc[0]["Company"]
    top_company_jobs = company_df.iloc[0]["Jobs"]

    top_location = location_df.iloc[0]["Location"]
    top_location_jobs = location_df.iloc[0]["Jobs"]

    top_role = role_df.iloc[0]["Role"]
    top_role_jobs = role_df.iloc[0]["Jobs"]
    with st.container(border=True):
       st.subheader("📈 Market Overview")

       st.write(f"""
The current job market is primarily driven by **{top_role}** opportunities.

Employers are actively seeking professionals with **{top_skill}** skills.

Among all companies, **{top_company}** has the highest hiring activity, while **{top_location}** remains the leading hiring location.
        """)
    with st.container(border=True):

        st.subheader("🔥 Key Highlights")

        col1, col2 = st.columns(2)

    with col1:
        st.success(f"🏢 Top Recruiter\n\n**{top_company}**")

        st.success(f"🛠 Most In-Demand Skill\n\n**{top_skill}**")

    with col2:
        st.success(f"📍 Hiring Hub\n\n**{top_location}**")

        st.success(f"💼 Dominant Role\n\n**{top_role}**")
    with st.container(border=True):

        st.subheader("📊 Dataset Snapshot")

        st.info(f"""
• **{top_skill}** appears in **{top_skill_jobs}** job postings.

• **{top_company}** has **{top_company_jobs}** openings.

• **{top_location}** contributes **{top_location_jobs}** jobs.

• **{top_role}** appears in **{top_role_jobs}** job postings.
""")
    show_footer()
if page == "Company Analysis":
    with st.container(border=True):
       st.title("🏢 Company Analysis")

       st.markdown("""
### Discover Recruitment Trends of Leading Companies

Explore hiring patterns across organizations and analyze:

- 📄 Total job openings
- 📍 Hiring locations
- 💼 Role distribution
- 🛠️ Most demanded technical skills
- 📊 Company-wise recruitment insights
""")
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
    st.markdown("---")
    st.subheader("🔍 Explore Individual Companies")
    #Select Desired Company
    selected_company = st.selectbox(
    "Select a Company",
    sorted(company_df["Company"])
    )
    #Filter Dataset
    company_jobs = df[
    df["company"] == selected_company
    ]
    if len(company_jobs) < 3:
       st.warning(
        "⚠️ This company has very few job postings. Charts may not represent meaningful trends."
       )
    col1, col2, col3 = st.columns(3)

    with col1:
       with st.container(border=True):
        st.metric(
            "📄 Total Jobs",
            len(company_jobs)
        )

    with col2:
       with st.container(border=True):
        st.metric(
            "📍 Hiring Locations",
            company_jobs["location"].nunique()
        )

    with col3:
        with st.container(border=True):
          st.metric(
            "💼 Job Roles",
            company_jobs["Role"].nunique()
        )
    st.markdown("---")

    st.header("📊 Company Hiring Analytics")

    st.caption(
    "Visualize hiring trends, role distribution, and skill requirements for the selected company."
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
    with col1:
      with st.container(border=True):
        st.subheader("💼 Role Distribution")
        st.caption(
            "Hiring roles offered by the selected company."
        )

        if role_df.empty:
            st.info("No role distribution available.")
        else:
            st.pyplot(fig_role)
    with col2:
      with st.container(border=True):
        st.subheader("🛠️ Top Required Skills")
        st.caption(
            "Most requested technical skills."
        )

        if skill_df.empty:
            st.info(
                "No technical skills could be extracted."
            )
        else:
            st.pyplot(fig_skill)
    #Job Listings
    st.subheader("📋 Job Listings")
    if company_jobs.empty:
      st.info("No job listings available.")
    else:
      
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
    st.markdown("---")

    with st.container(border=True):
      st.header("💡 Company Insights")

      st.caption(
        "Executive summary and hiring patterns for the selected company."
      )
    
    if not company_jobs.empty:

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
       if skill_df.empty:
         top_skill = "Not Available"
         top_skill_jobs = 0
       else:
         top_skill = skill_df.iloc[0]["Skill"]
         top_skill_jobs = skill_df.iloc[0]["Jobs"]
       top_role = role_df.iloc[0]["Role"]
       top_role_jobs = role_df.iloc[0]["Jobs"]

       top_location = company_location_df.iloc[0]["Location"]
       top_location_jobs = company_location_df.iloc[0]["Jobs"]

       total_jobs = len(company_jobs)
       unique_roles = company_jobs["Role"].nunique()
       unique_locations = company_jobs["location"].nunique()
       unique_skills = len(skill_count)
       percentage = round((top_role_jobs / total_jobs) * 100, 1)
       st.markdown(f"""
    ### 📈 Executive Summary

    **{selected_company}** is **{recruiter_status}** in the current job market,
    with **{total_jobs}** job openings.

    Approximately **{percentage}%** of its openings are for
    **{top_role}** positions, indicating its primary hiring focus.

    The company mainly seeks professionals skilled in
    **{top_skill}**, with **{top_location}** being its leading hiring location.
    """)

       st.success(f"""
    ### 🎯 Hiring Highlights

    ✅ Ranked **#{company_rank}** among all hiring companies.

    ✅ **{selected_company}** currently has **{total_jobs}** job openings.

    ✅ **{top_role}** is the dominant role (**{top_role_jobs}** jobs).

    ✅ **{top_skill}** is the most requested skill (**{top_skill_jobs}** jobs).

    ✅ **{top_location}** is the primary hiring location (**{top_location_jobs}** jobs).
    """)

       st.info(f"""
    🌍 Recruitment Diversity

    • Hiring spans **{unique_roles}** different roles.

    • Jobs are distributed across **{unique_locations}** locations.

    • Recruiters are looking for **{unique_skills}** unique skills.
     """)
   
       st.markdown("---")

       st.caption(
    "These insights are generated automatically from the cleaned job market dataset."
       )
    else:
         st.info("No insights available for this company.")
    show_footer()
if page == "Location Analysis":
    with st.container(border=True):
      st.title("📍 Location Analysis")

      st.markdown("""
### Discover Hiring Trends Across Locations

Analyze recruitment activity in different cities and regions.

Explore:

- 📄 Total job openings
- 🏢 Hiring companies
- 💼 Role distribution
- 🛠️ Most demanded skills
- 📊 Regional hiring insights
""")
   
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
    st.markdown("---")
    st.subheader("🔍 Explore Individual Locations")
    selected_location = st.selectbox(
       "Select a Location",
    location_options
    )
    location_jobs = df[
    df["location"] == selected_location
    ]
    
    col1, col2, col3 = st.columns(3)

    with col1:
       with st.container(border=True):
        st.metric(
            "📄 Total Jobs",
            len(location_jobs)
        )

    with col2:
       with st.container(border=True):
        st.metric(
            "📍 Hiring Companies",
            location_jobs["company"].nunique()
        )

    with col3:
        with st.container(border=True):
          st.metric(
            "💼 Job Roles",
            location_jobs["Role"].nunique()
        )
    
    st.markdown("---")

    st.header("📊 Regional Hiring Analytics")

    st.caption(
    "Explore company presence, role distribution, and skill demand in the selected location."
    )
    company_df = get_company_df(location_jobs)
    fig_company=plot_horizontal_bar(company_df,
    "Company",
    "Jobs",
    "Top 10 Hiring Companies",
    "Number of Jobs"
    )
    
    skill_df,skill_count = get_skill_df(location_jobs)
    fig_skill=plot_horizontal_bar(skill_df,
    "Skill",
    "Jobs",
    "Top Skills Required",
    "Number of Jobs"
    )
    role_df = get_role_df(location_jobs)

    fig_role=plot_vertical_bar(role_df,
    "Role",
    "Jobs",
    "Role Distribution",
    "Number of Jobs",
    "Roles"
    )
    col1, col2 = st.columns(2)

    with col1:
      with st.container(border=True):
        st.subheader("🏢 Top Hiring Companies")
        st.caption(
            "Companies with the highest recruitment activity in this location."
        )

        if company_df.empty:
            st.info("No company data available.")
        elif company_df["Jobs"].max() <= 1:
            st.info(
                "Companies in this location have only one job posting each."
            )
        else:
            st.pyplot(fig_company,use_container_width=True)
    with col2:
      with st.container(border=True):
        st.subheader("🛠️ Top Required Skills")
        st.caption(
            "Most requested technical skills in this location."
        )

        if skill_df.empty:
            st.info("No skill information available.")
        else:
            st.pyplot(fig_skill,use_container_width=True)
    col1, col2 = st.columns([1,1])
    with col1:
      with st.container(border=True):
        st.subheader("💼 Role Distribution")

        st.caption(
            "Distribution of job roles across this location."
        )

        if role_df.empty:
            st.info("No role distribution available.")
        else:
            st.pyplot(fig_role, use_container_width=True)

    with col2:
      st.empty()

      #Job Listings
    st.subheader("📋 Job Listings")
    if location_jobs.empty:
      st.info("No job listings available.")
    else:
      
      st.dataframe(
      location_jobs[
        [
            "title",
            "location",
            "company",
            "Role"
        ]
    ],
    use_container_width=True
    )
    st.markdown("---")
    st.subheader("💡 Location Insights")
  
    #Insights
    top_role = role_df.iloc[0]["Role"]
    top_role_jobs = role_df.iloc[0]["Jobs"]

    top_skill = skill_df.iloc[0]["Skill"]
    top_skill_jobs = skill_df.iloc[0]["Jobs"]

    top_company = company_df.iloc[0]["Company"]
    top_company_jobs = company_df.iloc[0]["Jobs"]

    total_jobs = len(location_jobs)
    if total_jobs < 5:
      st.warning(f"""
⚠️ **Limited Data Available**

Only **{total_jobs}** job postings were found for **{selected_location}**.

The insights below are based on a small sample and may not fully represent hiring trends in this location.
""")
    unique_companies = location_jobs["company"].nunique()
    unique_roles = location_jobs["Role"].nunique()
    unique_skills = len(skill_count)
    percentage = round((top_role_jobs / total_jobs) * 100, 1)
    if total_jobs >= 40:
      market = "a major hiring hub"

    elif total_jobs >= 20:
      market = "an active hiring market"

    elif total_jobs >= 5:
      market = "an emerging hiring location"

    else:
      market = "currently has limited job postings"
    st.markdown(f"""
### 📈 Location Summary

**{selected_location}** is **{market}**, with **{total_jobs}** job postings available in the dataset.

The most frequently advertised role is **{top_role}**.

Employers most commonly request **{top_skill}** skills, while **{top_company}** currently has the highest hiring activity in this location.
""")
    st.success(f"""
### 🔍 Key Findings

✅ **Total Opportunities:** **{total_jobs}** job postings are available in **{selected_location}**.

✅ **Most Common Role:** **{top_role}** appears in **{top_role_jobs}** posting(s).

✅ **Most Requested Skill:** **{top_skill}** is required in **{top_skill_jobs}** posting(s).

✅ **Top Hiring Company:** **{top_company}** has **{top_company_jobs}** posting(s) in this location.
""")
    st.info(f"""
    🎯 **Location Diversity**

    • **{unique_companies}** companies are hiring here.

    • Opportunities span **{unique_roles}** different job roles.

    • Recruiters are looking for **{unique_skills}** unique skills.
    """)
    show_footer()
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
if page == "About Project":

    st.title("📖 About the Project")

    st.write("""
    The **Data Job Market Intelligence Platform** is an interactive analytics
    dashboard developed to explore hiring trends in the data industry using
    real-world job postings.

    The platform helps students, job seekers, and aspiring data professionals
    understand current market demands by analyzing hiring companies,
    locations, skills, and job roles.
    
    Project Scope: This dashboard focuses on three core data careers—Data Analyst, Data Scientist, and  Data Engineer—to analyze hiring trends, required skills, companies, and locations.
    """
    )
    
    st.markdown("---")
    st.subheader("🎯 Project Objectives")

    st.markdown("""
- Analyze hiring trends across the data industry.
- Identify the most in-demand technical skills.
- Discover top hiring companies and locations.
- Compare opportunities across different data roles.
- Provide an interactive dashboard for easy exploration.
""")
    st.markdown("---")
    st.subheader("⚙️ Project Workflow")

    st.markdown("""
<div style='text-align:center; font-size:22px;'>

📂 <b>Raw Job Dataset</b>

⬇️

🧹 <b>Data Cleaning & Preprocessing</b>

⬇️

🛠️ <b>Skill Extraction</b>

⬇️

🤖 <b>Role Classification</b>

⬇️

📊 <b>Exploratory Data Analysis</b>

⬇️

🌐 <b>Interactive Dashboard</b>

</div>
""", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("📊 Dataset Overview")

    col1, col2 = st.columns(2)

    with col1:
	    st.metric("Job Posts", len(df))
	    st.metric("Companies", df["company"].nunique())
	    st.metric("Locations", df["location"].nunique())

    with col2:
	    st.metric("Roles", df["Role"].nunique())
	    st.metric("Unique Skills", len(skill_count))
    st.markdown("---")
    st.subheader("🛠️ Technologies Used")

    col1, col2 = st.columns(2)

    with col1:

      st.markdown("""
### Programming

- Python

### Data Analysis

- Pandas
- AST

### Visualization

- Matplotlib
""")

    with col2:

      st.markdown("""
### Dashboard

- Streamlit

### Dataset Processing

- Skill Extraction
- Role Classification
- Data Cleaning
""")
    st.markdown("---")
    st.subheader("✨ Key Features")

    st.success("""
✅ Interactive Dashboard

✅ Company Analysis

✅ Location Analysis

✅ Skill Analysis

✅ Role Comparison

✅ Job Listings Explorer

✅ Intelligent Insights
    """)
    st.markdown("---")
    st.subheader("🚀 Future Improvements")

    st.info("""
• Deploy the application on Streamlit Cloud

• Add advanced filtering options

• Integrate live job APIs

• Include salary trend analysis

• Add ML-based job recommendation system

• Support multiple datasets
    """)
    st.markdown("---")

    

    st.markdown("""
<div style='text-align:center; padding:25px;'>

<h3>💙 Thank you for exploring my project!</h3>

<p>
The <b>Data Job Market Intelligence Platform</b> was built to help students,
job seekers, and aspiring data professionals better understand today's hiring trends
through interactive analytics and visualizations.
</p>

<p>
👩‍💻 <b>Developed by Shailaja Durgam</b><br>
Rajiv Gandhi University of Knowledge Technologies (RGUKT Basar)
</p>

<p style="color:gray;">
🐍 Python • 🐼 Pandas • 📊 Matplotlib • 🌐 Streamlit
</p>

<p style="color:#808080;">
Built with curiosity, consistency, and ❤️ for learning.
</p>

<p style="color:#808080;">
✨ Thank you for exploring my project! Your feedback is always appreciated. ❤️
</p>

</div>
""", unsafe_allow_html=True)
    
