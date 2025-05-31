import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from zipfile import ZipFile
from io import BytesIO

# -----------------------------
# Setup Dashboard
# -----------------------------
st.set_page_config(page_title="Dashboard E-Commerce", layout="wide")
st.title("📊 Dashboard E-Commerce - Penjualan dan Review")

# -----------------------------
# Pilihan Sumber Data
# -----------------------------
data_source = st.sidebar.radio(
    "Pilih Sumber Data",
    ["📤 Upload File", "🌐 GitHub Repository"]
)

df = None

if data_source == "📤 Upload File":
    # -----------------------------
    # File Uploader
    # -----------------------------
    uploaded_file = st.sidebar.file_uploader(
        "Upload file merged_all_data.csv", 
        type="csv"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, parse_dates=["order_purchase_timestamp"])
        except Exception as e:
            st.error(f"❌ Error membaca file: {e}")
            st.stop()

else:  # GitHub Source
    # -----------------------------
    # Load from GitHub ZIP
    # -----------------------------
    ZIP_URL = "https://raw.githubusercontent.com/qailacasandra14/submission-e-commerce/main/Merged_all_data.zip"
    
    try:
        response = requests.get(ZIP_URL)
        with ZipFile(BytesIO(response.content)) as zip_file:
            file_list = zip_file.namelist()
            csv_file = next((f for f in file_list if f.endswith('.csv')), None)
            
            if csv_file:
                with zip_file.open(csv_file) as file:
                    df = pd.read_csv(file, parse_dates=["order_purchase_timestamp"])
            else:
                st.error("File CSV tidak ditemukan dalam ZIP")
                st.stop()
                
    except Exception as e:
        st.error(f"❌ Gagal memuat data dari GitHub: {e}")
        st.stop()

# Jika data tidak terbaca (baik dari upload atau GitHub)
if df is None:
    st.warning("Silakan pilih sumber data terlebih dahulu")
    st.stop()

# -----------------------------
# Data Processing (untuk semua sumber data)
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
# Visualisasi (sama untuk semua sumber data)
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
