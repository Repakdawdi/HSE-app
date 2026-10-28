import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AT HSE Management Dashboard", page_icon="🛡️", layout="wide"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
""",
    unsafe_allow_html=True,
)


# Mock / Initial Data & Register Data
@st.cache_data
def load_data():
  lists = {
      "observers": [
          "Ahmed Abdulla",
          "Anthony Bumford",
          "Anthony Quinn",
          "Bryan Charlton",
          "David Gallagher",
          "Gary Bolton",
          "Rabar Saeed",
          "Repak Dawdi",
          "Shad Ibrahim",
          "Sujeet Kumar ray",
      ],
      "locations": [
          "B1",
          "B2",
          "B3",
          "B4",
          "B5",
          "BT1",
          "BT2",
          "Contractor Camp",
          "Main Offices",
          "Workshop",
      ],
      "companies": [
          "Aram Tower",
          "ESF Post-tensioning",
          "Formwork and Reinforcement",
          "KNR",
          "PPCL",
          "White Water",
      ],
      "types": ["Intervention", "Observation", "Suggestion", "Near Miss"],
      "disciplines": ["Safety", "Health", "Environment", "Security"],
      "categories": [
          "Working at Height",
          "PPE / Safety Equipment",
          "Electrical Hazard",
          "Housekeeping",
          "LSR - Bypassing Safety Controls",
          "Scaffolding",
          "Slip/Trip/Fall",
          "Tools & Equipment",
          "Hot Work",
          "Excavation",
      ],
      "stats": ["OPEN", "CLOSED", "IN PROGRESS"],
  }

  # Expanded sample DataFrame representing the register
  df_register = pd.DataFrame(
      {
          "No.": [1, 2, 3, 4, 5, 6, 7, 8],
          "Date": [
              "2026-10-18",
              "2026-10-18",
              "2026-10-18",
              "2026-10-18",
              "2026-10-19",
              "2026-10-26",
              "2026-10-27",
              "2026-10-27",
          ],
          "Observed By": [
              "Repak Dawdi",
              "Mawlod Osman",
              "Repak Dawdi",
              "Repak Dawdi",
              "Repak Dawdi",
              "Repak Dawdi",
              "Shad Ibrahim",
              "David Gallagher",
          ],
          "Location": ["B1", "BT1", "B2", "B1", "B2", "B1", "Workshop", "Main Offices"],
          "Company Concerned": [
              "Aram Tower",
              "Formwork and Reinforcement",
              "Formwork and Reinforcement",
              "ESF Post-tensioning",
              "Formwork and Reinforcement",
              "Formwork and Reinforcement",
              "KNR",
              "PPCL",
          ],
          "Description": [
              "Labors working at Height on Tower crane without Harness",
              "Labor working without any PPE on construction site",
              "Scaffolding without proper platform/harness",
              "Post tensioning Staff safely performing work",
              "Labor working at height without safety harness",
              "Wooden structure about to collapse",
              "Uncovered electrical panel in workshop area",
              "Good housekeeping observed in main office",
          ],
          "Type": [
              "Intervention",
              "Intervention",
              "Observation",
              "Observation",
              "Intervention",
              "Observation",
              "Intervention",
              "Observation",
          ],
          "Discipline": [
              "Safety",
              "Safety",
              "Safety",
              "Safety",
              "Safety",
              "Safety",
              "Safety",
              "Health",
          ],
          "Observation Category": [
              "Working at Height",
              "PPE / Safety Equipment",
              "Scaffolding",
              "Positive",
              "Working at Height",
              "Bypassing Safety Controls",
              "Electrical Hazard",
              "Housekeeping",
          ],
          "Status": [
              "CLOSED",
              "CLOSED",
              "IN PROGRESS",
              "CLOSED",
              "CLOSED",
              "OPEN",
              "OPEN",
              "CLOSED",
          ],
      }
  )
  return lists, df_register


lists, df_register = load_data()

# Sidebar Navigation
st.sidebar.title("🛡️ AT HSE Portal")
page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Higher Management Dashboard",
        "🔍 Category & Status Explorer",
        "📝 New HSE Observation (Form)",
        "📋 Observation Register",
    ],
)

# ----------------------------------------------------
# PAGE 1: HIGHER MANAGEMENT DASHBOARD (CHARTS)
# ----------------------------------------------------
if page == "📊 Higher Management Dashboard":
  st.title("Executive HSE Performance Dashboard")
  st.markdown(
      "Real-time safety metrics, incident breakdowns, and contractor"
      " compliance for higher management."
  )

  # Top KPI Summary Cards
  col1, col2, col3, col4, col5 = st.columns(5)
  col1.metric("Total Observations", "303", "+12 this week")
  col2.metric("Safe Activities", "61", "20%")
  col3.metric("Unsafe Conditions", "150", "49%")
  col4.metric("Unsafe Activities", "92", "30%")
  col5.metric("Closure Rate", "95%", "288 Closed")

  st.markdown("---")

  # Row 1: Charts
  chart_col1, chart_col2 = st.columns(2)

  with chart_col1:
    st.subheader("⚠️ Top Observation Categories")
    cat_data = pd.DataFrame(
        {
            "Category": [
                "PPE / Safety Equipment",
                "Electrical Hazard",
                "Working at Height",
                "Housekeeping",
                "Tools & Equipment",
                "Slip/Trip/Fall",
            ],
            "Count": [29, 19, 18, 24, 21, 10],
        }
    )
    fig_cat = px.bar(cat_data, x="Count", y="Category", orientation="h")
    fig_cat.update_traces(marker_color="#e63946")
    fig_cat.update_layout(
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig_cat, use_container_width=True)

  with chart_col2:
    st.subheader("📊 Submission Type Breakdown")
    sub_data = pd.DataFrame(
        {
            "Type": ["Unsafe Condition", "Unsafe Activity", "Safe Activity"],
            "Count": [150, 92, 61],
        }
    )
    fig_sub = px.pie(
        sub_data,
        names="Type",
        values="Count",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Teal,
    )
    fig_sub.update_layout(margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_sub, use_container_width=True)

  # Row 2: Contractor & Status
  chart_col3, chart_col4 = st.columns(2)

  with chart_col3:
    st.subheader("🏢 Contractor Performance (Concerns)")
    con_data = pd.DataFrame(
        {
            "Contractor": [
                "KNR",
                "Astyari Re",
                "PPCL",
                "Aland Energy",
                "White Water",
            ],
            "Observations": [158, 57, 33, 5, 3],
        }
    )
    fig_con = px.bar(con_data, x="Contractor", y="Observations")
    fig_con.update_traces(marker_color="#1d3557")
    fig_con.update_layout(margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_con, use_container_width=True)

  with chart_col4:
    st.subheader("📌 Status Tracking")
    status_data = pd.DataFrame(
        {"Status": ["CLOSED", "OPEN", "IN PROGRESS"], "Count": [288, 13, 2]}
    )
    fig_status = px.funnel(status_data, x="Count", y="Status")
    fig_status.update_traces(marker_color="#2a9d8f")
    fig_status.update_layout(margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_status, use_container_width=True)

# ----------------------------------------------------
# PAGE 2: CATEGORY & STATUS EXPLORER (NEW SECTION)
# ----------------------------------------------------
elif page == "🔍 Category & Status Explorer":
  st.title("🔍 Category & Item Count Explorer")
  st.markdown(
      "Select any category, item, or status below to instantly check total"
      " occurrences until now and view matching records."
  )

  # Quick Filter Shortcut for OPEN observations
  col_shortcut, col_blank = st.columns([2, 2])
  with col_shortcut:
    if st.button("🚨 Show All OPEN Observations Directly"):
      st.session_state["quick_status"] = "OPEN"

  st.markdown("---")

  # Filter Controls
  f_col1, f_col2, f_col3 = st.columns(3)

  with f_col1:
    selected_status = st.selectbox(
        "Filter by Status",
        ["(All Statuses)"] + list(df_register["Status"].unique()),
    )
  with f_col2:
    selected_category = st.selectbox(
        "Filter by Observation Category",
        ["(All Categories)"]
        + list(df_register["Observation Category"].unique()),
    )
  with f_col3:
    selected_company = st.selectbox(
        "Filter by Company Concerned",
        ["(All Companies)"] + list(df_register["Company Concerned"].unique()),
    )

  f_col4, f_col5 = st.columns(2)
  with f_col4:
    selected_location = st.selectbox(
        "Filter by Location", ["(All Locations)"] + list(df_register["Location"].unique())
    )
  with f_col5:
    selected_observer = st.selectbox(
        "Filter by Observed By",
        ["(All Observers)"] + list(df_register["Observed By"].unique()),
    )

  # Apply filtering logic
  filtered_df = df_register.copy()

  if (
      "quick_status" in st.session_state
      and st.session_state["quick_status"] == "OPEN"
  ):
    filtered_df = filtered_df[filtered_df["Status"] == "OPEN"]
    st.info("📌 Showing 1-Click Quick Filter: **OPEN Observations**")
    # Reset quick status after applying so user can change filters freely
    del st.session_state["quick_status"]
  else:
    if selected_status != "(All Statuses)":
      filtered_df = filtered_df[filtered_df["Status"] == selected_status]
    if selected_category != "(All Categories)":
      filtered_df = filtered_df[
          filtered_df["Observation Category"] == selected_category
      ]
    if selected_company != "(All Companies)":
      filtered_df = filtered_df[
          filtered_df["Company Concerned"] == selected_company
      ]
    if selected_location != "(All Locations)":
      filtered_df = filtered_df[filtered_df["Location"] == selected_location]
    if selected_observer != "(All Observers)":
      filtered_df = filtered_df[filtered_df["Observed By"] == selected_observer]

  # Metric Display for Count
  st.markdown("---")
  m1, m2, m3 = st.columns(3)
  m1.metric("Total Matching Records", len(filtered_df))
  m2.metric(
      "Open Count in Selection",
      len(filtered_df[filtered_df["Status"] == "OPEN"]),
  )
  m3.metric(
      "Closed Count in Selection",
      len(filtered_df[filtered_df["Status"] == "CLOSED"]),
  )

  st.subheader("📋 Filtered Observations Table")
  st.dataframe(filtered_df, use_container_width=True)

# ----------------------------------------------------
# PAGE 3: NEW HSE OBSERVATION FORM
# ----------------------------------------------------
elif page == "📝 New HSE Observation (Form)":
  st.title("📝 HSE Observation & Intervention Form")
  st.markdown(
      "Fill out the inspection details below using the standardized dropdown"
      " lists from the site register."
  )

  with st.form("observation_form"):
    col1, col2 = st.columns(2)

    with col1:
      obs_date = st.date_input("Observation Date", datetime.date.today())
      observed_by = st.selectbox("Observed By (Observer)", lists["observers"])
      location = st.selectbox("Location / Area", lists["locations"])
      company = st.selectbox("Company Concerned", lists["companies"])

    with col2:
      obs_type = st.selectbox("Submission Type", lists["types"])
      discipline = st.selectbox("Discipline", lists["disciplines"])
      category = st.selectbox("Observation Category", lists["categories"])
      status = st.selectbox("Status", lists["stats"])

    description = st.text_area(
        "Observation Description / Details",
        placeholder="Describe what was observed...",
    )
    action_taken = st.text_area(
        "Suggested / Immediate Action Taken",
        placeholder="Action taken or recommendation...",
    )

    uploaded_photo = st.file_uploader(
        "Upload Visual Photograph", type=["jpg", "png", "jpeg"]
    )

    submitted = st.form_submit_button("Submit Observation Record")

    if submitted:
      st.success(
          "✅ HSE Observation successfully recorded and synced to the database!"
      )
      st.balloons()

# ----------------------------------------------------
# PAGE 4: OBSERVATION REGISTER TABLE
# ----------------------------------------------------
elif page == "📋 Observation Register":
  st.title("📋 Live Observation Register")
  st.markdown(
      "Filter and review all submitted safety observations across project"
      " zones."
  )
  st.dataframe(df_register, use_container_width=True)
