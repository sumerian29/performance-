import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
import base64
from fpdf import FPDF
import matplotlib.pyplot as plt
import io

# ====================================================
# Custom Background Style (Gradient Blue)
# ====================================================
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to bottom right, #e0f7ff, #b3e5fc);
        }
        .logo {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 150px;
        }
    </style>
""", unsafe_allow_html=True)

# ====================================================
# Add Company Logo
# ====================================================
st.markdown('<img src="data:image/png;base64,{}" class="logo">'.format(
    base64.b64encode(open("image.png", "rb").read()).decode()), unsafe_allow_html=True)

# ====================================================
# App Title and Introduction
# ====================================================
st.title("Crude Flow Monitoring & Performance Analysis System")
st.markdown("**Monitoring flow rates and analyzing performance for metering & custody transfer operations**")

# ====================================================
# Data Input: Upload Flow Data or Use Sample Data
# ====================================================
st.markdown("### Upload Flow Data (Excel)")
uploaded_file = st.file_uploader("Select an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")
        if "Tank_Level" in df.columns:
            df.drop(columns=["Tank_Level"], inplace=True)
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Error reading the file: {e}")
else:
    st.info("No file uploaded. Using sample data.")
    np.random.seed(42)
    sample_data = {
        "Meter_ID": np.random.choice(["M1", "M2", "M3", "M4"], size=100),
        "Flow_Rate": np.random.uniform(1000, 5000, size=100),
        "Pressure": np.random.uniform(50, 150, size=100),
        "Temperature": np.random.uniform(10, 80, size=100),
        "Timestamp": [datetime(2023, 1, 1, 0, 0) + timedelta(hours=i) for i in range(100)]
    }
    df = pd.DataFrame(sample_data)
    st.dataframe(df.head())

# ====================================================
# Date Range Selection for Analysis
# ====================================================
st.markdown("### Select Date Range for Analysis")

date_range = st.date_input("Select Date Range", [df["Timestamp"].min(), df["Timestamp"].max()])
if isinstance(date_range, list) and len(date_range) == 2:
    df = df[(df["Timestamp"] >= pd.to_datetime(date_range[0])) & (df["Timestamp"] <= pd.to_datetime(date_range[1]))]

compare_option = st.selectbox("Compare Performance Over:", ["3 Months", "4 Months", "Semi-Annual", "Annual"])

comparison_map = {
    "3 Months": "3M",
    "4 Months": "4M",
    "Semi-Annual": "6M",
    "Annual": "A"
}
selected_comparison = comparison_map.get(compare_option, "M")

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

if not df.empty:
    df_numeric = df.select_dtypes(include=["number"])
    df_resampled = df_numeric.set_index(df["Timestamp"]).resample(selected_comparison).mean().reset_index()
    df = df_resampled.merge(df["Timestamp"].drop_duplicates(), on="Timestamp", how="left")

# ====================================================
# Display Analysis Charts
# ====================================================
st.markdown("## Data Analysis Charts")
if "Flow_Rate" in df.columns:
    fig_flow = px.line(df, x="Timestamp", y="Flow_Rate", title="Crude Oil Flow Rate Over Time")
    st.plotly_chart(fig_flow)

if "Pressure" in df.columns:
    fig_pressure = px.line(df, x="Timestamp", y="Pressure", title="Pressure Over Time")
    st.plotly_chart(fig_pressure)

if "Temperature" in df.columns:
    fig_temp = px.line(df, x="Timestamp", y="Temperature", title="Temperature Over Time")
    st.plotly_chart(fig_temp)

# ====================================================
# Generate PDF Report with Charts and Recommendations
# ====================================================
def generate_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Crude Flow Monitoring Report", ln=True, align='C')
    pdf.ln(10)

    if "Flow_Rate" in df.columns:
        avg_flow = df["Flow_Rate"].mean()
        pdf.cell(200, 10, f"Average Flow Rate: {avg_flow:.2f} BPD", ln=True)

    if "Pressure" in df.columns:
        avg_pressure = df["Pressure"].mean()
        pdf.cell(200, 10, f"Average Pressure: {avg_pressure:.2f} bar", ln=True)

    if "Temperature" in df.columns:
        avg_temp = df["Temperature"].mean()
        pdf.cell(200, 10, f"Average Temperature: {avg_temp:.2f} °C", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, "Analysis Charts", ln=True, align='C')
    pdf.ln(10)

    plt.figure()
    plt.plot(df["Timestamp"], df["Flow_Rate"], marker='o', linestyle='-', label='Flow Rate')
    plt.xlabel("Timestamp")
    plt.ylabel("Flow Rate (BPD)")
    plt.title("Crude Oil Flow Rate Over Time")
    plt.xticks(rotation=45)
    plt.grid()
    img_path = "flow_chart.png"
    plt.savefig(img_path)
    plt.close()
    pdf.image(img_path, x=10, w=180)

    pdf.ln(10)
    pdf.cell(200, 10, "End of Report", ln=True, align='C')

    pdf_file = "flow_analysis_report.pdf"
    pdf.output(pdf_file)
    return pdf_file

st.markdown("### Download Report as PDF")
if st.button("Generate PDF Report"):
    pdf_path = generate_pdf()
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
    b64_pdf = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="flow_analysis_report.pdf">Download PDF Report</a>'
    st.markdown(href, unsafe_allow_html=True)
    st.success("PDF report generated successfully!")

# ====================================================
# Footer Message
# ====================================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center;'>Designed by Tareq Mageed / Dhiqar Oil Co. / Ministry of Oil</p>",
    unsafe_allow_html=True
)
