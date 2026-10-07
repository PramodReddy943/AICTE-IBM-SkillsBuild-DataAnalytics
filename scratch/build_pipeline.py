import os
import sys
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define paths
WORKSPACE_DIR = r"c:\Users\A.Pramod Kumar Reddy\AICTE"
IMAGES_DIR = os.path.join(WORKSPACE_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

DATASET_PATH = os.path.join(WORKSPACE_DIR, "supermarket_sales.csv")

print("Initializing data generation with pure NumPy/Pandas analytics...")

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic benchmark supermarket dataset (1000 records)
n_samples = 1000

branches = ['A', 'B', 'C']
city_map = {'A': 'Yangon', 'B': 'Mandalay', 'C': 'Naypyitaw'}
customer_types = ['Member', 'Normal']
genders = ['Female', 'Male']
product_lines = [
    'Electronic accessories', 
    'Fashion accessories', 
    'Food and beverages', 
    'Health and beauty', 
    'Home and lifestyle', 
    'Sports and travel'
]
payment_methods = ['Ewallet', 'Cash', 'Credit card']

# Generate random features
invoice_ids = [f"INV-{100000 + i}" for i in range(n_samples)]
branch_choices = np.random.choice(branches, n_samples, p=[0.34, 0.33, 0.33])
cities = [city_map[b] for b in branch_choices]
cust_choices = np.random.choice(customer_types, n_samples, p=[0.50, 0.50])
gender_choices = np.random.choice(genders, n_samples, p=[0.51, 0.49])
product_choices = np.random.choice(product_lines, n_samples)
unit_prices = np.round(np.random.uniform(10.0, 99.9, n_samples), 2)
quantities = np.random.randint(1, 11, n_samples)
payment_choices = np.random.choice(payment_methods, n_samples, p=[0.35, 0.35, 0.30])
ratings = np.round(np.random.uniform(4.0, 10.0, n_samples), 1)

# Generate dates from Jan 1, 2026 to Mar 30, 2026
start_date = datetime.date(2026, 1, 1)
end_date = datetime.date(2026, 3, 30)
days_delta = (end_date - start_date).days
random_days = np.random.randint(0, days_delta, n_samples)
dates = [start_date + datetime.timedelta(days=int(d)) for d in random_days]

# Generate times (10:00 to 20:59)
hours = np.random.randint(10, 21, n_samples)
minutes = np.random.randint(0, 60, n_samples)
times = [f"{h:02d}:{m:02d}" for h, m in zip(hours, minutes)]

# Calculate financial fields
cogs = np.round(unit_prices * quantities, 2)
tax_5 = np.round(cogs * 0.05, 4)
total = np.round(cogs + tax_5, 4)
gross_margin_pct = np.full(n_samples, 4.761904762)
gross_income = tax_5

df = pd.DataFrame({
    'Invoice ID': invoice_ids,
    'Branch': branch_choices,
    'City': cities,
    'Customer type': cust_choices,
    'Gender': gender_choices,
    'Product line': product_choices,
    'Unit price': unit_prices,
    'Quantity': quantities,
    'Tax 5%': tax_5,
    'Total': total,
    'Date': dates,
    'Time': times,
    'Payment': payment_choices,
    'cogs': cogs,
    'gross margin percentage': gross_margin_pct,
    'gross income': gross_income,
    'Rating': ratings
})

# Sort by date
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)
df.to_csv(DATASET_PATH, index=False)
print(f"Dataset created successfully with {len(df)} rows at {DATASET_PATH}")

# Set style for plots
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

# -------------------------------------------------------------
# Generate Chart 1: Revenue & Income by Product Line
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
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
fig1_path = os.path.join(IMAGES_DIR, "fig1_sales_by_product_line.png")
plt.savefig(fig1_path, dpi=300)
plt.close()

# -------------------------------------------------------------
# Generate Chart 2: Revenue by Branch & City
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
branch_rev = df.groupby(['Branch', 'City'])['Total'].sum().reset_index()
sns.barplot(data=branch_rev, x='Branch', y='Total', hue='City', palette='viridis', ax=ax, edgecolor='black')
ax.set_title('Supermarket Revenue ($) Across Branches and Cities', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Total Revenue ($)', fontsize=12, fontweight='bold')
ax.set_xlabel('Supermarket Branch', fontsize=12, fontweight='bold')
for p in ax.patches:
    if p.get_height() > 0:
        ax.annotate(f"${p.get_height():,.0f}", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                    ha='center', va='center', fontsize=10, color='white', fontweight='bold', rotation=90)
plt.tight_layout()
fig2_path = os.path.join(IMAGES_DIR, "fig2_revenue_by_branch_city.png")
plt.savefig(fig2_path, dpi=300)
plt.close()

# -------------------------------------------------------------
# Generate Chart 3: Hourly Sales Heatmap
# -------------------------------------------------------------
df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour
hourly_pivot = df.pivot_table(index='Hour', columns='Branch', values='Total', aggfunc='count').fillna(0)
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(hourly_pivot, annot=True, fmt='d', cmap='YlGnBu', cbar_kws={'label': 'Transaction Count'}, ax=ax)
ax.set_title('Hourly Transaction Density Heatmap by Branch', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Branch', fontsize=12, fontweight='bold')
ax.set_ylabel('Hour of Day (24-Hour Format)', fontsize=12, fontweight='bold')
plt.tight_layout()
fig3_path = os.path.join(IMAGES_DIR, "fig3_hourly_sales_heatmap.png")
plt.savefig(fig3_path, dpi=300)
plt.close()

# -------------------------------------------------------------
# Generate Chart 4: Payment Method by Customer Type
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
pay_cust = df.groupby(['Customer type', 'Payment'])['Invoice ID'].count().reset_index()
sns.barplot(data=pay_cust, x='Customer type', y='Invoice ID', hue='Payment', palette='Set2', ax=ax, edgecolor='black')
ax.set_title('Payment Method Adoption by Customer Type', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Transaction Count', fontsize=12, fontweight='bold')
ax.set_xlabel('Customer Type', fontsize=12, fontweight='bold')
for p in ax.patches:
    if p.get_height() > 0:
        ax.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()
fig4_path = os.path.join(IMAGES_DIR, "fig4_payment_methods_by_customer_type.png")
plt.savefig(fig4_path, dpi=300)
plt.close()

# -------------------------------------------------------------
# Generate Chart 5: Correlation Matrix
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6))
num_cols = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'Rating']
corr = df[num_cols].corr()
sns.heatmap(corr, annot=True, fmt='.3f', cmap='coolwarm', vmin=-1, vmax=1, ax=ax, linewidths=0.5)
ax.set_title('Feature Correlation Matrix Heatmap', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
fig5_path = os.path.join(IMAGES_DIR, "fig5_correlation_matrix.png")
plt.savefig(fig5_path, dpi=300)
plt.close()

# -------------------------------------------------------------
# Generate Chart 6: Time-Series Daily Revenue & AI Trend Forecast
# -------------------------------------------------------------
daily_sales = df.groupby('Date')['Total'].sum().reset_index()
daily_sales['7D_MA'] = daily_sales['Total'].rolling(window=7, min_periods=1).mean()

# Pure numpy linear regression for trend
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
fig6_path = os.path.join(IMAGES_DIR, "fig6_sales_forecasting_trend.png")
plt.savefig(fig6_path, dpi=300)
plt.close()

# -------------------------------------------------------------
# Generate Chart 7: Pure NumPy K-Means Customer Clustering & PCA
# -------------------------------------------------------------
features_cluster = df[['Total', 'Quantity', 'Rating', 'Unit price', 'cogs']].values
mean_f = np.mean(features_cluster, axis=0)
std_f = np.std(features_cluster, axis=0)
scaled_feat = (features_cluster - mean_f) / std_f

# Pure numpy K-Means algorithm
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

cluster_labels, _ = kmeans_numpy(scaled_feat, k=3)
df['Cluster'] = cluster_labels

# Pure numpy PCA (top 2 components via SVD)
cov_matrix = np.cov(scaled_feat, rowvar=False)
eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
idx = np.argsort(eigenvalues)[::-1]
eigenvectors = eigenvectors[:, idx]
pca_feat = np.dot(scaled_feat, eigenvectors[:, :2])
df['PCA1'] = pca_feat[:, 0]
df['PCA2'] = pca_feat[:, 1]

fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(df['PCA1'], df['PCA2'], c=df['Cluster'], cmap='tab10', alpha=0.7, edgecolors='k', s=50)
ax.set_title('K-Means Customer Behavioral Clustering (PCA View)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Principal Component 1', fontsize=12, fontweight='bold')
ax.set_ylabel('Principal Component 2', fontsize=12, fontweight='bold')
legend1 = ax.legend(*scatter.legend_elements(), title="Clusters", loc="upper right")
ax.add_artist(legend1)
plt.tight_layout()
fig7_path = os.path.join(IMAGES_DIR, "fig7_customer_segmentation_pca.png")
plt.savefig(fig7_path, dpi=300)
plt.close()

# -------------------------------------------------------------
# Generate Chart 8: Feature Importance for Customer Satisfaction
# -------------------------------------------------------------
df['High_Rating'] = (df['Rating'] >= 7.0).astype(int)
X_cls = pd.get_dummies(df[['Branch', 'Customer type', 'Gender', 'Product line', 'Payment', 'Unit price', 'Quantity', 'Total']], drop_first=True)

# Compute feature correlation magnitude with High_Rating as proxy for feature importance
corrs = X_cls.apply(lambda col: np.abs(np.corrcoef(col, df['High_Rating'])[0, 1]))
importances = corrs.sort_values(ascending=True).tail(10)

fig, ax = plt.subplots(figsize=(8, 5))
importances.plot(kind='barh', color='#3182bd', edgecolor='black', ax=ax)
ax.set_title('Top 10 Feature Importances for High Customer Rating', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Relative Correlation / Importance Score', fontsize=12, fontweight='bold')
plt.tight_layout()
fig8_path = os.path.join(IMAGES_DIR, "fig8_feature_importance_rf.png")
plt.savefig(fig8_path, dpi=300)
plt.close()

print("All 8 high-resolution figures generated successfully via pure NumPy pipeline!")
