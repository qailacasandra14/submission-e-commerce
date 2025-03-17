import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Setup Dashboard
st.set_page_config(page_title="Dashboard E-Commerce", layout="wide")
st.title("Penjualan dan Review")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("merged_all_data.csv", parse_dates=["order_purchase_timestamp"])
    df["total_price"] = df["price"] + df["freight_value"]
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Data")

all_cities = df["customer_city"].dropna().unique()
all_categories = df["product_category_name_english"].dropna().unique()

selected_cities = st.sidebar.multiselect("Pilih Kota", options=all_cities, default=all_cities)
selected_categories = st.sidebar.multiselect("Pilih Kategori Produk", options=all_categories, default=all_categories)

filtered_df = df[
    (df["customer_city"].isin(selected_cities)) &
    (df["product_category_name_english"].isin(selected_categories))
]

# Ringkasan Data
st.subheader("Ringkasan Data")

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

# Grafik: Jumlah Order per Kota
st.subheader("Jumlah Order per Kota")
order_per_city = filtered_df.groupby("customer_city")["order_id"].nunique().sort_values(ascending=False)

fig1, ax1 = plt.subplots()
order_per_city.head(10).plot(kind="bar", ax=ax1, color='skyblue')
plt.title("Top 10 Kota dengan Jumlah Order Terbanyak")
plt.ylabel("Jumlah Order")
st.pyplot(fig1)

# Grafik: Pendapatan per Kategori
st.subheader("Pendapatan per Kategori Produk")
revenue_per_cat = filtered_df.groupby("product_category_name_english")["total_price"].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots()
revenue_per_cat.head(10).plot(kind="barh", ax=ax2, color='orange')
plt.title("Top 10 Kategori Produk dengan Pendapatan Tertinggi")
plt.xlabel("Total Pendapatan")
st.pyplot(fig2)

# Grafik: Rata-rata Skor Review per Kategori
st.subheader("Review per Kategori Produk")
avg_review_per_cat = filtered_df.groupby("product_category_name_english")["review_score"].mean().sort_values(ascending=False)

fig3, ax3 = plt.subplots()
avg_review_per_cat.head(10).plot(kind="bar", ax=ax3, color='green')
plt.title("Top 10 Kategori Produk dengan Review Tertinggi")
plt.ylabel("Skor Review Rata-rata")
st.pyplot(fig3)
