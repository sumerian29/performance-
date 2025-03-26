# Crude Flow Monitoring & Performance Analysis System

A Streamlit-based interactive web application for uploading and analyzing crude oil flow data. It helps visualize trends, calculate performance metrics, and generate PDF reports for operational insights.

---

## 🔧 Features

- Upload Excel files with metering and custody transfer data
- Auto-load sample data if no file is uploaded
- Interactive charts using Plotly for:
  - Flow Rate
  - Pressure
  - Temperature
- Date range filtering
- Time-based performance comparison (3M, 4M, 6M, 12M)
- PDF report generation including:
  - Summary metrics
  - Time series chart for flow rate
- Custom UI styling and logo support

---

## 📂 File Requirements

### Uploaded Excel File

Your Excel sheet should include the following columns:

| Column       | Type     | Description                            |
|--------------|----------|----------------------------------------|
| `Meter_ID`   | string   | ID of the metering point               |
| `Flow_Rate`  | float    | Flow rate in barrels per day (BPD)     |
| `Pressure`   | float    | Pressure in bar                        |
| `Temperature`| float    | Temperature in °C                      |
| `Timestamp`  | datetime | Timestamp for each record              |


