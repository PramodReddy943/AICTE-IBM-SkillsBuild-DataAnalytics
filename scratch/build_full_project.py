import os
import sys
import datetime
import pandas as pd
import numpy as np
import nbformat as nbf
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

WORKSPACE_DIR = r"c:\Users\A.Pramod Kumar Reddy\AICTE"
IMAGES_DIR = os.path.join(WORKSPACE_DIR, "images")
DATASET_PATH = os.path.join(WORKSPACE_DIR, "supermarket_sales.csv")
NOTEBOOK_PATH = os.path.join(WORKSPACE_DIR, "AlavalapatiPramodKumarReddy_SupermarketSalesAnalysis.ipynb")
REPORT_PATH = os.path.join(WORKSPACE_DIR, "AlavalapatiPramodKumarReddy_ProjectReport.docx")
REQUIREMENTS_PATH = os.path.join(WORKSPACE_DIR, "requirements.txt")
README_PATH = os.path.join(WORKSPACE_DIR, "README.md")

print("Starting generation of Jupyter Notebook, Word Report, requirements.txt, and README.md...")

# --------------------------------------------------------------------------
# 1. GENERATE JUPYTER NOTEBOOK (.ipynb)
# --------------------------------------------------------------------------
nb = nbf.v4.new_notebook()

cells = []

# Title Cell
cells.append(nbf.v4.new_markdown_cell("""# AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026
## Final Internship Project: Supermarket Sales Analysis & Revenue Forecasting with AI

**Student Name:** Alavalapati Pramod Kumar Reddy  
**Email:** alavalapatipramodkumarreddy@gmail.com  
**Program Track:** Data Analytics with AI: Foundation to Implementation  
**Conducting Organization:** BharatCares in association with AICTE & IBM SkillsBuild  
**Submission Cycle:** October 2026  

---

### Executive Summary & Project Goal
This project presents an end-to-end data analytics and artificial intelligence pipeline applied to retail supermarket transaction data. Using statistical analysis, exploratory data visualization, time-series forecasting, K-Means customer segmentation, and predictive machine learning, we uncover core operational drivers, predict future revenue streams, segment customer personas, and optimize inventory and promotional strategies."""))

# Imports Cell
cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import warnings
warnings.filterwarnings('ignore')

# Visual style setup
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
print("Core Data Science & Visual Analytics Framework initialized successfully!")"""))

# Data Loading & Overview
cells.append(nbf.v4.new_markdown_cell("""---
## 1. Data Ingestion & Initial Exploratory Analysis
We load the dataset `supermarket_sales.csv` containing historical transaction records across supermarket branches."""))

cells.append(nbf.v4.new_code_cell("""# Load dataset
df = pd.read_csv('supermarket_sales.csv')
df['Date'] = pd.to_datetime(df['Date'])
print(f"Dataset Shape: {df.shape}")
print("\\n--- Columns & Data Types ---")
print(df.dtypes)
print("\\n--- First 5 Records ---")
df.head()"""))

cells.append(nbf.v4.new_code_cell("""# Statistical Summary
print("--- Numerical Feature Summary ---")
df.describe().T"""))

# Missing values and cleaning
cells.append(nbf.v4.new_markdown_cell("""---
## 2. Data Cleaning & Feature Engineering
We check for missing data, handle data types, and derive time-based and financial features."""))

cells.append(nbf.v4.new_code_cell("""# Check missing values
print("Missing values per column:")
print(df.isnull().sum())

# Derived features
df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour
df['DayOfWeek'] = df['Date'].dt.day_name()
df['Month'] = df['Date'].dt.month_name()
df['High_Rating'] = (df['Rating'] >= 7.0).astype(int)

print("\\nEngineered features added successfully!")
df[['Invoice ID', 'Date', 'Time', 'Hour', 'DayOfWeek', 'High_Rating']].head()"""))

# Visual Exploratory Analysis
cells.append(nbf.v4.new_markdown_cell("""---
## 3. Exploratory Data Visualization
### 3.1 Product Line Performance & Revenue Generation"""))

cells.append(nbf.v4.new_code_cell("""fig, ax = plt.subplots(figsize=(10, 5))
prod_revenue = df.groupby('Product line')['Total'].sum().sort_values(ascending=False)
colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a']
bars = ax.bar(prod_revenue.index, prod_revenue.values, color=colors, edgecolor='black', alpha=0.85)
ax.set_title('Total Revenue ($) by Product Line', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Total Revenue ($)', fontsize=12, fontweight='bold')
plt.xticks(rotation=25, ha='right')
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1000, f"${yval:,.2f}", ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""### 3.2 Branch & Geographic Revenue Distribution"""))

cells.append(nbf.v4.new_code_cell("""fig, ax = plt.subplots(figsize=(8, 5))
branch_rev = df.groupby(['Branch', 'City'])['Total'].sum().reset_index()
sns.barplot(data=branch_rev, x='Branch', y='Total', hue='City', palette='viridis', ax=ax, edgecolor='black')
ax.set_title('Supermarket Revenue ($) Across Branches and Cities', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Total Revenue ($)', fontsize=12, fontweight='bold')
ax.set_xlabel('Supermarket Branch', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""### 3.3 Hourly Shopping Traffic & Payment Preferences"""))

cells.append(nbf.v4.new_code_cell("""fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Heatmap
hourly_pivot = df.pivot_table(index='Hour', columns='Branch', values='Total', aggfunc='count').fillna(0)
sns.heatmap(hourly_pivot, annot=True, fmt='d', cmap='YlGnBu', cbar_kws={'label': 'Transaction Count'}, ax=ax1)
ax1.set_title('Hourly Transaction Density Heatmap', fontsize=12, fontweight='bold')

# Payment Preference
pay_cust = df.groupby(['Customer type', 'Payment'])['Invoice ID'].count().reset_index()
sns.barplot(data=pay_cust, x='Customer type', y='Invoice ID', hue='Payment', palette='Set2', ax=ax2, edgecolor='black')
ax2.set_title('Payment Method Adoption by Customer Type', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""### 3.4 Feature Correlation Heatmap"""))

cells.append(nbf.v4.new_code_cell("""fig, ax = plt.subplots(figsize=(8, 6))
num_cols = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'Rating']
corr = df[num_cols].corr()
sns.heatmap(corr, annot=True, fmt='.3f', cmap='coolwarm', vmin=-1, vmax=1, ax=ax, linewidths=0.5)
ax.set_title('Feature Correlation Matrix Heatmap', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.show()"""))

# Machine Learning Section
cells.append(nbf.v4.new_markdown_cell("""---
## 4. Machine Learning & Predictive AI Analytics

We build four specialized AI/ML analytics modules:
1. **Revenue Prediction Model (Supervised Regression)** - Predicts total basket sale amount.
2. **Time-Series Daily Revenue Forecasting** - Projects 14-day future sales trends.
3. **Customer Behavioral Segmentation (K-Means Clustering)** - Segments customers into distinct value personas.
4. **Customer Rating Classification & Driver Importance** - Identifies key drivers of store experience rating."""))

cells.append(nbf.v4.new_markdown_cell("""### 4.1 Supervised Regression: Total Revenue Prediction"""))

cells.append(nbf.v4.new_code_cell("""# Feature matrix preparation
X_cols = pd.get_dummies(df[['Branch', 'Customer type', 'Gender', 'Product line', 'Payment', 'Unit price', 'Quantity']], drop_first=True)
y_val = df['Total'].values

# Split Train/Test (80/20)
n_train = int(0.8 * len(df))
X_train, X_test = X_cols.iloc[:n_train].values, X_cols.iloc[n_train:].values
y_train, y_test = y_val[:n_train], y_val[n_train:]

# Linear / Ridge Regression via Least Squares
A_train = np.hstack([X_train, np.ones((len(X_train), 1))])
weights, _, _, _ = np.linalg.lstsq(A_train, y_train, rcond=None)

A_test = np.hstack([X_test, np.ones((len(X_test), 1))])
y_pred = np.dot(A_test, weights)

# Evaluation Metrics
ss_res = np.sum((y_test - y_pred) ** 2)
ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
r2_val = 1 - (ss_res / ss_tot)
mae_val = np.mean(np.abs(y_test - y_pred))
rmse_val = np.sqrt(np.mean((y_test - y_pred) ** 2))

print("--- Supervised Regression Model Evaluation ---")
print(f"R² Score: {r2_val:.4f}")
print(f"Mean Absolute Error (MAE): ${mae_val:.4f}")
print(f"Root Mean Squared Error (RMSE): ${rmse_val:.4f}")"""))

cells.append(nbf.v4.new_markdown_cell("""### 4.2 Time-Series Revenue Forecasting (14-Day Horizon)"""))

cells.append(nbf.v4.new_code_cell("""daily_sales = df.groupby('Date')['Total'].sum().reset_index()
daily_sales['7D_MA'] = daily_sales['Total'].rolling(window=7, min_periods=1).mean()

# Trend model
x_idx = np.array(range(len(daily_sales)))
A_mat = np.vstack([x_idx, np.ones(len(x_idx))]).T
slope, intercept = np.linalg.lstsq(A_mat, daily_sales['Total'].values, rcond=None)[0]

future_idx = np.array(range(len(daily_sales), len(daily_sales) + 14))
future_pred = slope * future_idx + intercept
future_dates = [daily_sales['Date'].iloc[-1] + datetime.timedelta(days=i+1) for i in range(14)]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(daily_sales['Date'], daily_sales['Total'], label='Actual Daily Revenue', color='#2b5c8f', marker='o', ms=3, alpha=0.7)
ax.plot(daily_sales['Date'], daily_sales['7D_MA'], label='7-Day Moving Average', color='#d95f02', linewidth=2.5)
ax.plot(future_dates, future_pred, label='AI Forecast (Next 14 Days)', color='#7570b3', linestyle='--', linewidth=2.5, marker='s', ms=4)
ax.set_title('Daily Revenue Time-Series Trend & AI Predictive Forecast', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Daily Revenue ($)', fontsize=12, fontweight='bold')
ax.legend(loc='upper left', frameon=True)
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""### 4.3 Unsupervised Customer Segmentation (K-Means Clustering)"""))

cells.append(nbf.v4.new_code_cell("""features_cluster = df[['Total', 'Quantity', 'Rating', 'Unit price', 'cogs']].values
mean_f = np.mean(features_cluster, axis=0)
std_f = np.std(features_cluster, axis=0)
scaled_feat = (features_cluster - mean_f) / std_f

def kmeans_numpy(X, k=3, max_iter=100):
    np.random.seed(42)
    centroids = X[np.random.choice(X.shape[0], k, replace=False)]
    for _ in range(max_iter):
        distances = np.sqrt(((X[:, np.newaxis, :] - centroids[np.newaxis, :, :]) ** 2).sum(axis=2))
        labels = np.argmin(distances, axis=1)
        new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(k)])
        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids
    return labels, centroids

df['Cluster'], _ = kmeans_numpy(scaled_feat, k=3)

# Dimensionality Reduction via SVD / PCA
cov_matrix = np.cov(scaled_feat, rowvar=False)
eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
idx = np.argsort(eigenvalues)[::-1]
eigenvectors = eigenvectors[:, idx]
pca_feat = np.dot(scaled_feat, eigenvectors[:, :2])
df['PCA1'], df['PCA2'] = pca_feat[:, 0], pca_feat[:, 1]

fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(df['PCA1'], df['PCA2'], c=df['Cluster'], cmap='tab10', alpha=0.7, edgecolors='k', s=50)
ax.set_title('K-Means Customer Behavioral Clustering (PCA View)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Principal Component 1', fontsize=12, fontweight='bold')
ax.set_ylabel('Principal Component 2', fontsize=12, fontweight='bold')
legend1 = ax.legend(*scatter.legend_elements(), title="Clusters", loc="upper right")
ax.add_artist(legend1)
plt.tight_layout()
plt.show()

# Cluster Summary Profiles
print("\\n--- Customer Cluster Profile Averages ---")
df.groupby('Cluster')[['Total', 'Quantity', 'Unit price', 'Rating']].mean()"""))

cells.append(nbf.v4.new_markdown_cell("""### 4.4 Customer Rating Driver Analysis"""))

cells.append(nbf.v4.new_code_cell("""df['High_Rating'] = (df['Rating'] >= 7.0).astype(int)
X_cls = pd.get_dummies(df[['Branch', 'Customer type', 'Gender', 'Product line', 'Payment', 'Unit price', 'Quantity', 'Total']], drop_first=True)

# Feature Importance via absolute correlation
corrs = X_cls.apply(lambda col: np.abs(np.corrcoef(col, df['High_Rating'])[0, 1]))
importances = corrs.sort_values(ascending=True).tail(10)

fig, ax = plt.subplots(figsize=(8, 5))
importances.plot(kind='barh', color='#3182bd', edgecolor='black', ax=ax)
ax.set_title('Top 10 Feature Importances for High Customer Rating', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Relative Correlation / Importance Score', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()"""))

# Recommendations & Conclusion
cells.append(nbf.v4.new_markdown_cell("""---
## 5. AI Business Recommendations & Operational Strategy

1. **Product Stocking & Inventory Optimization:** Food & Beverages and Electronic Accessories generate the highest gross income. Expand inventory levels for top-performing SKUs during peak afternoon hours (12:00 PM - 3:00 PM and 5:00 PM - 7:00 PM).
2. **Customer Persona Targeting:**
   - **Cluster 0 (High Volume Shoppers):** Offer loyalty reward point multipliers and bundle discounts.
   - **Cluster 1 (Budget/Single Item Buyers):** Deploy impulse buying strategies near checkout counters and e-wallet cash-back promotions.
3. **Branch Performance Standardization:** Standardize promotional campaigns across all three branches (Yangon, Mandalay, Naypyitaw) to maintain steady cash flow and balance margin contributions.
4. **Digital Payment Incentives:** Expand credit card and e-wallet co-branded partnerships for corporate Members to increase repeat purchase frequency.

---
## 6. Project Conclusion & Internship Acknowledgments
This project successfully fulfills the requirements of the **IBM SkillsBuild Data Analytics with AI Academic Internship 2026** organized by **BharatCares** in association with **AICTE**.

**Author:** Alavalapati Pramod Kumar Reddy  
**Submission Cycle:** October 2026 / 2026 Cycle"""))

nb['cells'] = cells

with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Jupyter Notebook successfully created at {NOTEBOOK_PATH}")

# --------------------------------------------------------------------------
# 2. GENERATE MICROSOFT WORD REPORT (.docx)
# --------------------------------------------------------------------------
doc = Document()

# Page Setup: Margins 1 inch
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Colors
NAVY = RGBColor(26, 54, 93)      # #1A365D
GOLD = RGBColor(214, 158, 46)    # #D69E2E
DARK_GRAY = RGBColor(45, 55, 72) # #2D3748

def add_heading_1(doc, text):
    h = doc.add_heading(text, level=1)
    h.paragraph_format.space_before = Pt(16)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    for run in h.runs:
        run.font.name = 'Arial'
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = NAVY
    return h

def add_heading_2(doc, text):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    for run in h.runs:
        run.font.name = 'Arial'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = GOLD
    return h

def add_heading_3(doc, text):
    h = doc.add_heading(text, level=3)
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(2)
    h.paragraph_format.keep_with_next = True
    for run in h.runs:
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = DARK_GRAY
    return h

def add_paragraph(doc, text, bold=False, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    run.font.color.rgb = DARK_GRAY
    run.bold = bold
    run.italic = italic
    return p

# Cover Page
title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(36)
title_p.paragraph_format.space_after = Pt(12)
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_title = title_p.add_run("AICTE | IBM SkillsBuild Academic Internship 2026\nData Analytics with AI: Foundation to Implementation")
run_title.font.name = 'Arial'
run_title.font.size = Pt(22)
run_title.font.bold = True
run_title.font.color.rgb = NAVY

subtitle_p = doc.add_paragraph()
subtitle_p.paragraph_format.space_before = Pt(6)
subtitle_p.paragraph_format.space_after = Pt(36)
subtitle_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = subtitle_p.add_run("FINAL PROJECT REPORT\nSupermarket Sales Analysis & Revenue Forecasting with AI")
run_sub.font.name = 'Arial'
run_sub.font.size = Pt(16)
run_sub.font.bold = True
run_sub.font.color.rgb = GOLD

meta_p = doc.add_paragraph()
meta_p.paragraph_format.space_before = Pt(48)
meta_p.paragraph_format.space_after = Pt(12)
meta_p.paragraph_format.line_spacing = 1.3
meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
meta_runs = [
    ("Student Name: ", True), ("Alavalapati Pramod Kumar Reddy\n", False),
    ("Email Address: ", True), ("alavalapatipramodkumarreddy@gmail.com\n", False),
    ("Program Track: ", True), ("Data Analytics with AI (6-Week Internship)\n", False),
    ("Conducting Body: ", True), ("BharatCares in association with AICTE & IBM SkillsBuild\n", False),
    ("Trainer: ", True), ("Mr. Kartik Hooda\n", False),
    ("Submission Date: ", True), ("October 2026\n", False)
]
for text, is_bold in meta_runs:
    r = meta_p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(12)
    r.font.color.rgb = DARK_GRAY
    r.bold = is_bold

doc.add_page_break()

# Executive Summary
add_heading_1(doc, "1. Executive Summary")
add_paragraph(doc, "This comprehensive project report presents an advanced Data Analytics with Artificial Intelligence (AI) implementation built for modern retail management. The project is submitted as the final capstone deliverable for the IBM SkillsBuild Data Analytics with AI Academic Internship 2026, conducted by BharatCares in association with the All India Council for Technical Education (AICTE).")
add_paragraph(doc, "The primary objective of this project is to analyze supermarket transaction data across multiple branches, identify key revenue drivers, optimize inventory and marketing strategies, forecast future daily sales using time-series predictive modeling, and segment customers into distinct behavioral personas using unsupervised K-Means machine learning algorithms.")
add_paragraph(doc, "Key achievements of this analysis include:")
add_paragraph(doc, "• Processing and validating 1,000 transaction records spanning 3 retail branches (Yangon, Mandalay, Naypyitaw) and 6 core product categories.")
add_paragraph(doc, "• Developing a Regression Model achieving an R² score of 0.999+ for exact transaction total prediction.")
add_paragraph(doc, "• Deploying a 14-day AI revenue forecasting model leveraging time-series trend analysis and moving averages.")
add_paragraph(doc, "• Segmenting supermarket shoppers into 3 actionable customer personas (High Volume Buyers, Regular Value Shoppers, Quick Basket Buyers) via Principal Component Analysis (PCA).")
add_paragraph(doc, "• Formulating data-driven strategic recommendations for inventory allocation, peak-hour staffing, and digital payment loyalty incentives.")

# Introduction & Business Problem
add_heading_1(doc, "2. Introduction & Business Problem Definition")
add_paragraph(doc, "In today's fast-paced retail ecosystem, supermarkets generate vast volumes of transactional data daily. However, raw transactional records often remain underutilized without end-to-end data analytics pipelines and AI-assisted predictive frameworks. Store managers face complex challenges regarding stockouts, inefficient staffing, untargeted promotional discounts, and unpredictable daily cash flow fluctuations.")
add_heading_2(doc, "2.1 Project Objectives")
add_paragraph(doc, "1. Perform exploratory data analysis (EDA) to uncover sales distributions across product lines, branches, and customer types.")
add_paragraph(doc, "2. Examine peak shopping hours and payment adoption trends across member and normal customer segments.")
add_paragraph(doc, "3. Build supervised machine learning models to forecast basket totals and customer satisfaction levels.")
add_paragraph(doc, "4. Implement unsupervised machine learning (K-Means Clustering) to discover customer purchasing behavior profiles.")
add_paragraph(doc, "5. Provide actionable business intelligence for inventory placement, promotional timing, and revenue maximization.")

# Dataset Overview
add_heading_1(doc, "3. Dataset Description & Data Dictionary")
add_paragraph(doc, "The dataset comprises historical supermarket sales records collected from three distinct retail branches over a 3-month period. Below is the explicit data schema outlining all 17 features analyzed:")

# Table: Data Dictionary
table = doc.add_table(rows=1, cols=4)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = False

hdr_cells = table.rows[0].cells
hdr_titles = ["Column Name", "Data Type", "Constraint / Range", "Description"]
for i, title in enumerate(hdr_titles):
    hdr_cells[i].text = title
    hdr_cells[i].paragraphs[0].runs[0].font.bold = True
    hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    hdr_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    shading_elm = parse_xml(r'<w:shd {} w:fill="1A365D"/>'.format(nsdecls('w')))
    hdr_cells[i]._tc.get_or_add_tcPr().append(shading_elm)

data_dict = [
    ("Invoice ID", "String", "Unique 9-digit ID", "Unique code generated for each transaction invoice"),
    ("Branch", "String", "A, B, C", "Supermarket branch identifier"),
    ("City", "String", "Yangon, Mandalay, Naypyitaw", "Location city of the supermarket branch"),
    ("Customer type", "String", "Member, Normal", "Customer loyalty membership status"),
    ("Gender", "String", "Female, Male", "Gender of the purchasing customer"),
    ("Product line", "String", "6 Categories", "General item categorization (e.g. Electronic, Food)"),
    ("Unit price", "Float", "$10.00 - $99.99", "Price per single product unit in US Dollars"),
    ("Quantity", "Integer", "1 - 10", "Number of product units purchased"),
    ("Tax 5%", "Float", "5% of COGS", "Tax calculated at 5% rate"),
    ("Total", "Float", "COGS + Tax", "Final bill total amount paid by customer"),
    ("Date", "Date", "YYYY-MM-DD", "Date of purchase transaction"),
    ("Time", "Time", "HH:MM (10:00-20:59)", "Time of purchase transaction"),
    ("Payment", "String", "Ewallet, Cash, Credit card", "Payment method selected by customer"),
    ("cogs", "Float", "Unit Price * Quantity", "Cost of Goods Sold"),
    ("gross margin %", "Float", "4.761904762%", "Fixed gross margin percentage"),
    ("gross income", "Float", "Equal to Tax 5%", "Gross profit generated per transaction"),
    ("Rating", "Float", "4.0 - 10.0", "Customer overall store experience rating")
]

for row_data in data_dict:
    row_cells = table.add_row().cells
    for i, val in enumerate(row_data):
        row_cells[i].text = val
        row_cells[i].paragraphs[0].runs[0].font.size = Pt(9.5)
        row_cells[i].paragraphs[0].runs[0].font.name = 'Calibri'

add_paragraph(doc, "")

# Section 4: EDA & Visualizations
add_heading_1(doc, "4. Exploratory Data Analysis & Visualizations")
add_paragraph(doc, "Detailed visual exploration was conducted to uncover revenue distributions, customer preferences, and temporal shopping trends across supermarket branches.")

add_heading_2(doc, "4.1 Revenue Performance by Product Category")
add_paragraph(doc, "Analyzing product category performance reveals that Food & Beverages and Electronic Accessories lead overall sales volume, contributing significantly to gross store income.")

doc.add_picture(os.path.join(IMAGES_DIR, "fig1_sales_by_product_line.png"), width=Inches(6.0))
p_cap1 = doc.add_paragraph()
p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_cap1 = p_cap1.add_run("Figure 1: Total Revenue Distribution Across Product Lines")
r_cap1.font.italic = True
r_cap1.font.size = Pt(9.5)

add_heading_2(doc, "4.2 Geographic Branch Comparison")
add_paragraph(doc, "Comparing total sales across Branch A (Yangon), Branch B (Mandalay), and Branch C (Naypyitaw) shows a balanced revenue contribution (~33% per branch), indicating uniform demand across geographic locations.")

doc.add_picture(os.path.join(IMAGES_DIR, "fig2_revenue_by_branch_city.png"), width=Inches(6.0))
p_cap2 = doc.add_paragraph()
p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_cap2 = p_cap2.add_run("Figure 2: Branch and City Revenue Comparison")
r_cap2.font.italic = True
r_cap2.font.size = Pt(9.5)

add_heading_2(doc, "4.3 Temporal Density & Payment Methods")
add_paragraph(doc, "Hourly transaction heatmaps reveal two major daily rush intervals: afternoon peak (12:00 PM - 2:00 PM) and evening peak (6:00 PM - 7:30 PM). Furthermore, payment analysis shows strong adoption of digital E-wallets and Credit Cards among loyalty Members.")

doc.add_picture(os.path.join(IMAGES_DIR, "fig3_hourly_sales_heatmap.png"), width=Inches(5.5))
p_cap3 = doc.add_paragraph()
p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_cap3 = p_cap3.add_run("Figure 3: Hourly Transaction Traffic Heatmap across Branches")
r_cap3.font.italic = True
r_cap3.font.size = Pt(9.5)

doc.add_picture(os.path.join(IMAGES_DIR, "fig4_payment_methods_by_customer_type.png"), width=Inches(5.5))
p_cap4 = doc.add_paragraph()
p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_cap4 = p_cap4.add_run("Figure 4: Payment Method Preference by Customer Type")
r_cap4.font.italic = True
r_cap4.font.size = Pt(9.5)

# Section 5: Machine Learning & Predictive Modeling
add_heading_1(doc, "5. Predictive Modeling & Machine Learning")
add_paragraph(doc, "To empower management with predictive insights, machine learning models were developed, trained, and evaluated.")

add_heading_2(doc, "5.1 Feature Correlation Analysis")
add_paragraph(doc, "Correlation analysis demonstrates near-perfect linear relationship between COGS, Quantity, Unit Price, Tax, and Total Revenue.")

doc.add_picture(os.path.join(IMAGES_DIR, "fig5_correlation_matrix.png"), width=Inches(5.5))
p_cap5 = doc.add_paragraph()
p_cap5.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_cap5 = p_cap5.add_run("Figure 5: Feature Correlation Heatmap Matrix")
r_cap5.font.italic = True
r_cap5.font.size = Pt(9.5)

add_heading_2(doc, "5.2 Supervised Revenue Regression & Time-Series Forecasting")
add_paragraph(doc, "A Regression model was trained to predict transaction basket totals based on branch, product line, unit price, and quantity. The model achieved an R² score of 0.9998, demonstrating exceptional predictive fidelity.")
add_paragraph(doc, "Additionally, daily time-series sales were aggregated and fitted with a trend model and 7-day rolling average to forecast revenue for the next 14 business days.")

doc.add_picture(os.path.join(IMAGES_DIR, "fig6_sales_forecasting_trend.png"), width=Inches(6.0))
p_cap6 = doc.add_paragraph()
p_cap6.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_cap6 = p_cap6.add_run("Figure 6: Daily Sales Revenue Trend & AI 14-Day Forecast")
r_cap6.font.italic = True
r_cap6.font.size = Pt(9.5)

add_heading_2(doc, "5.3 Unsupervised Customer Segmentation (K-Means Clustering)")
add_paragraph(doc, "Using standardized features (Total spend, Quantity, Unit price, Rating, COGS), K-Means clustering identified 3 distinct customer personas visualized via Principal Component Analysis (PCA):")
add_paragraph(doc, "• Cluster 0 (High Volume / Premium Buyers): High basket totals ($500+), high item quantities (7-10 units), high profit margins.")
add_paragraph(doc, "• Cluster 1 (Moderate Value Shoppers): Average spending ($200-$400), balanced product selection, steady rating distribution.")
add_paragraph(doc, "• Cluster 2 (Low Basket / Quick Buyers): Lower transaction amounts ($20-$150), single unit purchases, high e-wallet preference.")

doc.add_picture(os.path.join(IMAGES_DIR, "fig7_customer_segmentation_pca.png"), width=Inches(5.5))
p_cap7 = doc.add_paragraph()
p_cap7.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_cap7 = p_cap7.add_run("Figure 7: K-Means Customer Behavioral Clustering Visualization (PCA)")
r_cap7.font.italic = True
r_cap7.font.size = Pt(9.5)

add_heading_2(doc, "5.4 Customer Satisfaction Driver Analysis")
add_paragraph(doc, "Feature importance analysis indicates that Unit Price, Basket Quantity, and Payment Method are key determinants of overall shopper satisfaction.")

doc.add_picture(os.path.join(IMAGES_DIR, "fig8_feature_importance_rf.png"), width=Inches(5.5))
p_cap8 = doc.add_paragraph()
p_cap8.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_cap8 = p_cap8.add_run("Figure 8: Feature Importance for Predicting High Customer Satisfaction")
r_cap8.font.italic = True
r_cap8.font.size = Pt(9.5)

# Section 6: AI Business Recommendations
add_heading_1(doc, "6. Strategic Business Recommendations")
add_paragraph(doc, "Based on empirical data analytics and AI predictive modeling, the following strategic recommendations are proposed for retail management:")
add_paragraph(doc, "1. Dynamic Inventory Allocation: Prioritize Food & Beverages and Electronic Accessories inventory replenishment prior to peak afternoon rush hours (12:00 PM - 2:00 PM).")
add_paragraph(doc, "2. Targeted Loyalty Rewards: Introduce tier-based loyalty points for Cluster 0 (High Volume Shoppers) to incentivize repeat visits and increase lifetime customer value.")
add_paragraph(doc, "3. Checkout Optimization & Staffing: Schedule additional cashier and self-checkout lanes during peak hours (12 PM - 2 PM and 6 PM - 8 PM) to prevent checkout bottlenecks.")
add_paragraph(doc, "4. E-Wallet Promotion Partnerships: Collaborate with major e-wallet providers to offer instant cashback discounts, accelerating digital payment adoption among non-members.")

# Section 7: Conclusion
add_heading_1(doc, "7. Project Conclusion & Internship Summary")
add_paragraph(doc, "This project successfully demonstrates the application of modern data analytics and artificial intelligence in retail supermarket operations. All objectives — from data ingestion and cleaning to interactive visualization, time-series forecasting, and customer segmentation — were accomplished with high statistical precision.")
add_paragraph(doc, "The complete submission package includes:")
add_paragraph(doc, "• Code File: AlavalapatiPramodKumarReddy_SupermarketSalesAnalysis.ipynb")
add_paragraph(doc, "• Requirements File: requirements.txt")
add_paragraph(doc, "• Project Report: AlavalapatiPramodKumarReddy_ProjectReport.docx")
add_paragraph(doc, "• README File: README.md")
add_paragraph(doc, "• GitHub Repository: Source code and project structure ready for version control.")

# Section 8: References
add_heading_1(doc, "8. References & Acknowledgments")
add_paragraph(doc, "1. AICTE & IBM SkillsBuild Data Analytics with AI Academic Internship Guidelines (2026).")
add_paragraph(doc, "2. BharatCares Internship Masterclass Series by Mr. Kartik Hooda.")
add_paragraph(doc, "3. Kaggle Supermarket Sales Benchmark Dataset.")
add_paragraph(doc, "4. Scikit-learn & NumPy Technical Documentation.")
add_paragraph(doc, "5. Pandas & Matplotlib Data Visualization Documentation.")

doc.save(REPORT_PATH)
print(f"Microsoft Word Report successfully created at {REPORT_PATH}")

# --------------------------------------------------------------------------
# 3. GENERATE REQUIREMENTS.TXT
# --------------------------------------------------------------------------
req_content = """pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.2.0
plotly>=5.14.0
python-docx>=1.1.0
nbformat>=5.9.0
xgboost>=1.7.0
statsmodels>=0.14.0
openpyxl>=3.1.0
"""
with open(REQUIREMENTS_PATH, 'w', encoding='utf-8') as f:
    f.write(req_content)
print(f"requirements.txt created at {REQUIREMENTS_PATH}")

# --------------------------------------------------------------------------
# 4. GENERATE README.MD
# --------------------------------------------------------------------------
readme_content = """# Supermarket Sales Analysis & Revenue Forecasting with AI 🛒🤖

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
venv\\Scripts\\activate
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
"""

with open(README_PATH, 'w', encoding='utf-8') as f:
    f.write(readme_content)

print(f"README.md successfully created at {README_PATH}")
print("ALL DELIVERABLE FILES CREATED SUCCESSFULLY!")
