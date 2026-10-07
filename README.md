# Supermarket Sales Analysis & Revenue Forecasting with AI 🛒🤖

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/Library-Scikit--Learn-orange.svg)
![Pandas](https://img.shields.io/badge/Data-Pandas-green.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

## 📌 Project Overview
This repository contains the complete capstone project for the **AICTE | IBM SkillsBuild Data Analytics with AI Academic Internship 2026**, conducted by **BharatCares** in association with **AICTE**.

The project implements an end-to-end data processing, exploratory data visualization, predictive machine learning, and customer behavioral segmentation pipeline on retail supermarket transaction data across three branches (Yangon, Mandalay, Naypyitaw).

---

## 👨‍🎓 Author Information
- **Student Name:** Alavalapati Pramod Kumar Reddy
- **Email:** alavalapatipramodkumarreddy@gmail.com
- **Internship Track:** Data Analytics with AI: Foundation to Implementation
- **Trainer:** Mr. Kartik Hooda
- **Program Partners:** AICTE, IBM SkillsBuild, BharatCares

---

## 🔑 Key Features & AI Capabilities
1. **Exploratory Data Analysis (EDA):** Deep analysis of revenue, gross margin, product line performance, hourly traffic density, and customer payment choices.
2. **Supervised Regression Modeling:** Regression predicting transaction totals with **R² = 0.9998** and MAE < $1.00.
3. **Time-Series Revenue Forecasting:** 14-day daily revenue projection using trend modeling and 7-day moving averages.
4. **Customer Behavioral Clustering:** Unsupervised **K-Means Clustering** (3 Clusters) segmenting shoppers into *High Volume Buyers*, *Moderate Shoppers*, and *Quick Basket Buyers*.
5. **Customer Satisfaction Drivers:** Feature importance identifying key factors behind high store experience ratings.

---

## 📊 Dataset Information
- **Dataset File:** `supermarket_sales.csv`
- **Source Benchmark:** Kaggle Supermarket Sales Dataset
- **Records:** 1,000 transaction records
- **Attributes:** 17 columns including Invoice ID, Branch, City, Customer type, Gender, Product line, Unit price, Quantity, Tax, Total, Date, Time, Payment, COGS, Gross Margin %, Gross Income, Rating.

---

## 📁 Repository Directory Structure
```
AICTE/
│
├── AlavalapatiPramodKumarReddy_SupermarketSalesAnalysis.ipynb   # Complete Executable Jupyter Notebook
├── AlavalapatiPramodKumarReddy_ProjectReport.docx             # Formal Academic Project Report
├── supermarket_sales.csv                                        # Benchmark Supermarket Dataset
├── requirements.txt                                             # Python Dependencies
├── README.md                                                     # Project Documentation & Setup Guide
└── images/                                                      # Visualizations & High-Res Plots
    ├── fig1_sales_by_product_line.png
    ├── fig2_revenue_by_branch_city.png
    ├── fig3_hourly_sales_heatmap.png
    ├── fig4_payment_methods_by_customer_type.png
    ├── fig5_correlation_matrix.png
    ├── fig6_sales_forecasting_trend.png
    ├── fig7_customer_segmentation_pca.png
    └── fig8_feature_importance_rf.png
```

---

## 🚀 Installation & Run Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YourUsername/AICTE-IBM-SkillsBuild-DataAnalytics.git
cd AICTE-IBM-SkillsBuild-DataAnalytics
```

### 2. Create & Activate Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Jupyter Notebook
```bash
jupyter notebook AlavalapatiPramodKumarReddy_SupermarketSalesAnalysis.ipynb
```

---

## 📈 Summary of Key Results & Metrics

| Model Task | Algorithm Used | Key Performance Metric |
| :--- | :--- | :--- |
| Basket Revenue Prediction | Multiple Regression | **R² = 0.9998, MAE = $0.48** |
| 14-Day Sales Forecasting | Trend + 7D Moving Average | **Trend Accuracy = 94.2%** |
| Customer Segmentation | K-Means (k=3) | **Silhouette Score = 0.3541** |
| Rating Classification | Driver Correlation Matrix | **Top Driver: Unit Price & Quantity** |

---

## 💡 Strategic Recommendations for Management
1. **Stock Optimization:** Increase stock for Food & Beverages and Electronic Accessories ahead of afternoon traffic spikes (12 PM - 2 PM).
2. **Loyalty Incentives:** Target Cluster 0 (High Volume Shoppers) with tiered rewards to enhance customer retention.
3. **Digital Payments:** Expand e-wallet cashback schemes to transition Cash customers into digital loyalty Members.

---

## 📜 License & Acknowledgments
This project is submitted under the **MIT License**.  
Special thanks to **AICTE**, **IBM SkillsBuild**, and **BharatCares** for conducting this learning program.
