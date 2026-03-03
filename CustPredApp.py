# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 22:29:15 2026

@author: Noor
"""

import streamlit as st
import pandas as pd
import joblib

# ------------------------
# Page config - must be first
# ------------------------
st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="📊",
    layout="centered"
)

# ------------------------
# Load trained model
# ------------------------
model = joblib.load("final_random_forest_model.pkl")

# Labels for predictions
plain_segment_labels = {
    0: "New Customer",
    1: "VIP Customer",
    2: "Loyal Customer",
    3: "At-Risk Customer"
}

segment_labels_ui = {
    0: ("🟢 New Customer", "#2ecc71"),
    1: ("💎 VIP Customer", "#9b59b6"),
    2: ("🔵 Loyal Customer", "#3498db"),
    3: ("🔴 At-Risk Customer", "#e74c3c")
}

# ------------------------
# Helper function: compute RFM
# ------------------------
def compute_rfm(df):
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum'
    })
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    rfm = rfm.reset_index()
    return rfm

# ------------------------
# Title
# ------------------------
st.title("📊 Customer Segment Prediction App")

# ------------------------
# Tabs for input options
# ------------------------
tab1, tab2, tab3 = st.tabs([
    "Direct RFM Input",
    "Single Customer Upload",
    "Batch Upload (Full Dataset)"
])

# ------------------------
# Tab 1: Direct RFM Input
# ------------------------
with tab1:
    st.write("Manually enter RFM values for a single customer.")

    col1, col2, col3 = st.columns(3)
    with col1:
        recency = st.number_input("Recency (Days)", min_value=0, max_value=500, value=1)
    with col2:
        frequency = st.number_input("Frequency", min_value=1, max_value=500, value=1)
    with col3:
        monetary = st.number_input("Monetary Value", min_value=0.0, value=0.0)

    if st.button("🚀 Predict Segment (Manual RFM)", key="manual_rfm"):
        input_data = pd.DataFrame([[recency, frequency, monetary]], columns=["Recency", "Frequency", "Monetary"])
        prediction = model.predict(input_data)[0]
        proba = model.predict_proba(input_data)[0]
        confidence = max(proba) * 100

        label, color = segment_labels_ui[prediction]
        st.markdown(f"""
            <div style="padding:20px; border-radius:12px; background-color:#fff;
                        box-shadow:0 4px 12px rgba(0,0,0,0.1); text-align:center;">
                <h2 style="color:{color}; margin:0;">{label}</h2>
                <p>Model Confidence: <b>{confidence:.2f}%</b></p>
            </div>
        """, unsafe_allow_html=True)

# ------------------------
# Tab 2: Single Customer Upload
# ------------------------
with tab2:
    st.write("Upload a file with raw transactions for a single customer.")
    st.write("""
             **Please upload a CSV or Excel file with the following columns (case-sensitive):**  
             - `CustomerID` (unique customer identifier)  
             - `InvoiceNo` (transaction ID)  
             - `InvoiceDate` (date of transaction, YYYY-MM-DD format)  
             - `Quantity` (number of items purchased)  
             - `UnitPrice` (price per item)  
             """)
    
    uploaded_file = st.file_uploader("Upload single customer CSV/XLSX", type=["csv","xlsx"], key="single_upload")

    if uploaded_file:
        try:
            # Read CSV or Excel
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Failed to load file: {e}")
        else:
            # Check required columns
            required_columns = ['CustomerID','InvoiceNo','InvoiceDate','Quantity','UnitPrice']
            missing_cols = [col for col in required_columns if col not in df.columns]

            if missing_cols:
                st.error(f"The following required columns are missing: {missing_cols}")
            else:
                rfm = compute_rfm(df)

                if len(rfm) != 1:
                    st.warning(f"Please upload only one customer's transactions. Found {len(rfm)} customers.")
                else:
                    input_data = rfm[['Recency', 'Frequency', 'Monetary']]
                    prediction = model.predict(input_data)[0]
                    proba = model.predict_proba(input_data)[0]
                    confidence = max(proba) * 100

                    label, color = segment_labels_ui[prediction]
                    st.markdown(f"""
                        <div style="padding:20px; border-radius:12px; background-color:#fff;
                                    box-shadow:0 4px 12px rgba(0,0,0,0.1); text-align:center;">
                            <h2 style="color:{color}; margin:0;">{label}</h2>
                            <p>Model Confidence: <b>{confidence:.2f}%</b></p>
                        </div>
                    """, unsafe_allow_html=True)

# ------------------------
# Tab 3: Batch Upload (Full Dataset)
# ------------------------
with tab3:
    st.write("Upload full transactions dataset to predict segments for all customers.")
    st.write("""
             **Please upload a CSV or Excel file with the following columns (case-sensitive):**  
             - `CustomerID` (unique customer identifier)  
             - `InvoiceNo` (transaction ID)  
             - `InvoiceDate` (date of transaction, YYYY-MM-DD format)  
             - `Quantity` (number of items purchased)  
             - `UnitPrice` (price per item)  
             """)
    
    uploaded_file_batch = st.file_uploader("Upload CSV/XLSX", type=["csv","xlsx"], key="batch_upload")
    
    if uploaded_file_batch:
        try:
            if uploaded_file_batch.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file_batch)
            else:
                df = pd.read_excel(uploaded_file_batch)
        except Exception as e:
            st.error(f"Failed to load file: {e}")
        else:
            # Check required columns
            required_columns = ['CustomerID','InvoiceNo','InvoiceDate','Quantity','UnitPrice']
            missing_cols = [col for col in required_columns if col not in df.columns]

            if missing_cols:
                st.error(f"The following required columns are missing: {missing_cols}")
            else:
                rfm = compute_rfm(df)
                predictions = model.predict(rfm[['Recency', 'Frequency', 'Monetary']])
                proba = model.predict_proba(rfm[['Recency', 'Frequency', 'Monetary']])
                confidences = proba.max(axis=1) * 100

                rfm['Segment'] = [plain_segment_labels[p] for p in predictions]
                rfm['Confidence (%)'] = confidences.round(2)

                st.markdown("### Prediction Preview:")
                st.write(rfm[['CustomerID','Recency','Frequency','Monetary','Segment','Confidence (%)']])

                csv = rfm.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Predictions CSV",
                    data=csv,
                    file_name="customer_segment_predictions.csv",
                    mime="text/csv"
                )