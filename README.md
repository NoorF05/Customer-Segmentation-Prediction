# Customer-Segmentation-Prediction

E-commerce customer segmentation and prediction enables personalized marketing, improved retention, optimized spending, and increased sales growth.

---

## Problem Statement
Develop a robust customer segmentation model and a predictive classifier to categorize customers based on their purchasing patterns. This will enable the company to tailor marketing strategies, improve customer retention, and optimize inventory management.

---

## Project Overview
This project applies machine learning to analyze customer purchasing patterns, segment customers into meaningful groups, and predict future buying behavior. The objective is to build a robust segmentation and classification model that helps the company personalize marketing strategies, improve customer retention, and optimize inventory management.

---

## Data Collection and Cleaning
- **Source:** E-commerce transactions dataset (~541,909 records)  
- **Key columns:** CustomerID, InvoiceNo, InvoiceDate, Quantity, UnitPrice  
- **Data cleaning:** removed null CustomerID, negative Quantity, and canceled orders  

<img width="1033" height="396" alt="image" src="https://github.com/user-attachments/assets/dcbb8dd4-3e00-409d-ad90-29e9ec8a4f81" />

---

## Feature Engineering
- Created **TotalPrice** column (Quantity × UnitPrice)  
- Set **snapshot date** (latest purchase in the data)  
- Created the **RFM** (Recency, Frequency, Monetary) dataset for the customers  
- Applied **log transformation and scaling** to reduce skewness  

<img width="355" height="232" alt="image" src="https://github.com/user-attachments/assets/48b41e33-7c85-49c8-a20a-d5fe4e2e9740" />

---

## Customer Segmentation
- Used **Elbow method** to determine optimal K for KMeans  
- Compared KMeans with Hierarchical and DBSCAN clustering  
- **KMeans (4 clusters)** selected as best  
- **Segments:**  
   - **0 – New Customers:** Recent, low frequency & monetary  
   - **1 – VIP Customers:** Very recent, very high frequency & monetary  
   - **2 – Loyal Customers:** Moderate recency, frequency & monetary  
   - **3 – At-Risk Customers:** Long recency, low frequency & monetary  

<img width="478" height="376" alt="image" src="https://github.com/user-attachments/assets/913f59f6-1e78-4788-a449-cef838811ee9" />  
<img width="625" height="427" alt="image" src="https://github.com/user-attachments/assets/f88b8268-2cdf-4b73-8d35-b75d1b5f17f6" />

---

## Prediction Models
- Trained the following models to predict the KMeans segments:  
  - Logistic Regression  
  - Decision Trees  
  - Random Forest  
  - SVM  

- **Random Forest** was chosen as the best model with 98% accuracy  

<img width="435" height="393" alt="image" src="https://github.com/user-attachments/assets/6b72da68-765b-46b3-b715-0a1d8151bdce" />

- **Feature importance:** Monetary > Frequency > Recency  

<img width="524" height="363" alt="image" src="https://github.com/user-attachments/assets/4432538b-180a-4ad4-ada4-f7016eb277ed" />

---

## Power BI Dashboard
Interactive dashboards provide insights into customer segments, revenue trends, and segment-wise contributions. The following screenshots illustrate key visuals:  

<img width="979" height="536" alt="Dashboard Screenshot 1" src="https://github.com/user-attachments/assets/12a89722-6745-41c9-9461-6e2859b77e69" />  
<img width="966" height="534" alt="Dashboard Screenshot 2" src="https://github.com/user-attachments/assets/d927e285-4f5f-486d-83c7-0c143cf08e56" />  

## Streamlit App
- Interactive app allows:  
  - Manual RFM input
    <img width="798" height="392" alt="image" src="https://github.com/user-attachments/assets/c742426a-05de-4fc1-a1a2-dba34ed19e84" />

  - Single customer upload (CSV/XLSX)
    <img width="742" height="540" alt="image" src="https://github.com/user-attachments/assets/a5a24535-cf88-4dbd-903b-42b3e62241a8" />

  - Batch upload for all customers
    <img width="739" height="552" alt="image" src="https://github.com/user-attachments/assets/66262e7f-f83a-4466-b803-859e6d2dcfec" />

- Displays predicted segment and model confidence.

## Live Demo
Try the interactive app here: [Customer Segmentation Prediction App](https://customer-segmentation-prediction-app.streamlit.app/)
