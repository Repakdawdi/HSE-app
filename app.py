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

# Custom CSS for styling & print optimization
st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    @media print {
        body { background-color: white; color: black; }
        .stSidebar { display: none; }
        .stButton { display: none; }
    }
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

  df_register = pd.DataFrame(
      {
          "No.": [1, 2, 3, 4, 5, 6],
          "Date": [
              "2026-10-18",
              "2026-10-18",
              "2026-10-18",
              "2026-10-19",
              "2026-10-26",
              "2026-10-27",
          ],
          "Description": [
              "Labors working at Height on Tower crane without Harness",
              "Labor working without any PPE on construction site",
              "Scaffolding without proper platform/harness",
              "Labor working at height without safety harness",
              "Wooden structure about to collapse",
              "Uncovered electrical panel in workshop area",
          ],
          "Observed By": [
              "Repak Dawdi",
              "Mawlod Osman",
              "Repak Dawdi",
              "Repak Dawdi",
              "Repak Dawdi",
              "Shad Ibrahim",
          ],
          "Location": ["B1", "BT1", "B2", "B2", "B1", "Workshop"],
          "Suggested / Action Taken": [
              "Informed supervisor to provide harness",
              "Stopped work, instructed to wear PPE",
              "Updated HSE management procedure",
              "Stopped work, provided harness",
              "Barricaded and removed hazard",
              "Notified electrical team to rectify",
          ],
          "Company Concerned": [
              "Aram Tower",
              "Formwork and Reinforcement",
              "Formwork and Reinforcement",
              "Formwork and Reinforcement",
              "Formwork and Reinforcement",
              "KNR",
          ],
          "Type": [
              "Intervention",
              "Intervention",
              "Observation",
              "Intervention",
              "Observation",
              "Intervention",
          ],
          "Discipline": ["Safety", "Safety", "Safety", "Safety", "Safety", "Safety"],
          "Submission Type": [
              "Unsafe Activity",
              "Unsafe Condition",
              "Unsafe Activity",
              "Unsafe Activity",
              "Unsafe Condition",
              "Unsafe Condition",
          ],
          "Observation Category": [
              "Working at Height",
              "PPE / Safety Equipment",
              "Working at Height",
              "Working at Height",
              "Bypassing Safety Controls",
              "Electrical Hazard",
          ],
          "Status": ["CLOSED", "CLOSED", "IN PROGRESS", "CLOSED", "OPEN", "OPEN"],
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
        "🖨️ Printable Daily HSE Report",
        "🔍 Category & Status Explorer",
        "📝 New HSE Observation (Form)",
        "📋 Observation Register",
    ],
)

# ----------------------------------------------------
# PAGE 1: HIGHER MANAGEMENT DASHBOARD
# ----------------------------------------------------
if page == "📊 Higher Management Dashboard":
  st.title("Executive HSE Performance Dashboard")
  st.markdown(
      "Real-time safety metrics, incident breakdowns, and contractor"
      " compliance for higher management."
  )

  col1, col2, col3, col4, col5 = st.columns(5)
  col1.metric("Total Observations", "303", "+12 this week")
  col2.metric("Safe Activities", "61", "20%")
  col3.metric("Unsafe Conditions", "150", "49%")
  col4.metric("Unsafe Activities", "92", "30%")
  col5.metric("Closure Rate", "95%", "288 Closed")

  st.markdown("---")

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
# PAGE 2: PRINTABLE DAILY HSE REPORT
# ----------------------------------------------------
elif page == "🖨️ Printable Daily HSE Report":
  st.title("📄 Daily HSE Report & Print Preview")
  st.markdown(
      "Formatted for daily management distribution and printing. Click your"
      " browser's print button (`Ctrl + P` / `Cmd + P`) to export as PDF or"
      " print."
  )

  # Report Date selector
  report_date = st.date_input("Select Report Date", datetime.date.today())

  st.markdown("---")
  st.markdown(
      f"### 🛡️ AT HSE Daily Safety Report — {report_date.strftime('%B %d, %Y')}"
  )

  # Manpower & Man-Hours Section
  col_mh1, col_mh2, col_mh3 = st.columns(3)
  total_manpower = col_mh1.number_input("Total Site Manpower", value=450, step=10)
  safe_man_hours = col_mh2.number_input(
      "Total Safe Man-Hours (Cumulative)", value=124500, step=500
  )
  lti_count = col_mh3.number_input(
      "Lost Time Injuries (LTI) Today", value=0, step=1
  )

  st.markdown("---")
  st.markdown("#### 📊 Daily HSE Key Performance Indicators (KPIs)")

  kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
  kpi1.metric("LTI", lti_count)
  kpi2.metric("Near Misses", "1")
  kpi3.metric("Unsafe Acts", "3")
  kpi4.metric("Unsafe Conditions", "2")
  kpi5.metric("Safe Conditions", "1")

  st.markdown("---")
  st.markdown("#### 📋 Daily Observation Log (OCR Summary)")
  st.dataframe(df_register, use_container_width=True)

  st.markdown("---")
  sig1, sig2 = st.columns(2)
  sig1.markdown("**Prepared By:** HSE Officer\n\nSignature: ______________________")
  sig2.markdown(
      "**Approved By:** Project Manager\n\nSignature:"
      " ______________________"
  )

# ----------------------------------------------------
# PAGE 3: CATEGORY & STATUS EXPLORER
# ----------------------------------------------------
elif page == "🔍 Category & Status Explorer":
  st.title("🔍 Category & Item Count Explorer")
  st.markdown(
      "Select any category, item, or status below to check total occurrences"
      " and view matching records."
  )

  if st.button("🚨 Show All OPEN Observations Directly"):
    st.session_state["quick_status"] = "OPEN"

  st.markdown("---")

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

  filtered_df = df_register.copy()
  if (
      "quick_status" in st.session_state
      and st.session_state["quick_status"] == "OPEN"
  ):
    filtered_df = filtered_df[filtered_df["Status"] == "OPEN"]
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

  st.markdown("---")
  m1, m2, m3 = st.columns(3)
  m1.metric("Total Matching Records", len(filtered_df))
  m2.metric(
      "Open Count", len(filtered_df[filtered_df["Status"] == "OPEN"])
  )
  m3.metric(
      "Closed Count", len(filtered_df[filtered_df["Status"] == "CLOSED"])
  )

  st.subheader("📋 Filtered Observations Table")
  st.dataframe(filtered_df, use_container_width=True)

# ----------------------------------------------------
# PAGE 4: NEW HSE OBSERVATION FORM
# ----------------------------------------------------
elif page == "📝 New HSE Observation (Form)":
  st.title("📝 HSE Observation & Intervention Form")
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
    submitted = st.form_submit_button("Submit Observation Record")
    if submitted:
      st.success("✅ HSE Observation successfully recorded!")
      st.balloons()

# ----------------------------------------------------
# PAGE 5: OBSERVATION REGISTER TABLE
# ----------------------------------------------------
elif page == "📋 Observation Register":
  st.title("📋 Live Observation Register")
  st.dataframe(df_register, use_container_width=True)
