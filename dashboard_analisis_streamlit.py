import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Setup Dashboard
# -----------------------------
st.set_page_config(page_title="Dashboard E-Commerce", layout="wide")
st.title("📊 Dashboard E-Commerce - Penjualan dan Review")

# -----------------------------
# Load data dari file lokal
# -----------------------------
try:
    df = pd.read_csv("merged_all_data.csv", parse_dates=["order_purchase_timestamp"])
except Exception as e:
    st.error(f"❌ Gagal membaca file: {e}")
    st.stop()

# -----------------------------
# Data Processing
# -----------------------------
df["total_price"] = df["price"] + df["freight_value"]

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filter Data")

all_cities = df["customer_city"].dropna().unique()
all_categories = df["product_category_name_english"].dropna().unique()

selected_cities = st.sidebar.multiselect("Pilih Kota", options=all_cities, default=all_cities)
selected_categories = st.sidebar.multiselect("Pilih Kategori Produk", options=all_categories, default=all_categories)

filtered_df = df[
    (df["customer_city"].isin(selected_cities)) &
    (df["product_category_name_english"].isin(selected_categories))
]

# -----------------------------
# Ringkasan Data
# -----------------------------
st.subheader("📈 Ringkasan Data")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Order", filtered_df["order_id"].nunique())
with col2:
    st.metric("Total Pendapatan", f"Rp {filtered_df['total_price'].sum():,.0f}")
with col3:
    st.metric("Total Produk Terjual", int(filtered_df["order_item_id"].count()))
with col4:
    avg_score = filtered_df["review_score"].mean()
    st.metric("Rata-rata Skor Review", f"{avg_score:.2f} ⭐")

# -----------------------------
# Visualisasi Tambahan
# -----------------------------
st.subheader("🛍️ Kategori Produk Terlaris")
top_products = (
    filtered_df.groupby("product_category_name_english")["order_item_id"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_products.values, y=top_products.index, ax=ax1, palette="viridis")
ax1.set_xlabel("Jumlah Terjual")
ax1.set_ylabel("Kategori Produk")
st.pyplot(fig1)

st.subheader("📉 Produk Kurang Peminat")
least_products = (
    filtered_df.groupby("product_category_name_english")["order_item_id"]
    .count()
    .sort_values(ascending=True)
    .head(10)
)

fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.barplot(x=least_products.values, y=least_products.index, ax=ax3, palette="magma")
ax3.set_xlabel("Jumlah Produk Terjual")
ax3.set_ylabel("Kategori Produk")
ax3.set_title("Kategori Produk dengan Penjualan Terendah")
st.pyplot(fig3)


st.subheader("📍 Distribusi Kota Pelanggan")
top_cities = (
    filtered_df["customer_city"]
    .value_counts()
    .head(10)
)

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_cities.values, y=top_cities.index, ax=ax2, palette="coolwarm")
ax2.set_xlabel("Jumlah Pesanan")
ax2.set_ylabel("Kota")
st.pyplot(fig2)
