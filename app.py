
import pandas as pd

st.set_page_config(
    page_title="Dashboard Kinh Doanh",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Kinh Doanh")
st.caption("Phân tích dữ liệu bán hàng mẫu năm 2026")

# Đọc dữ liệu
df = pd.read_csv("du_lieu_dashboard_kinh_doanh_2026.csv")
df["Ngày"] = pd.to_datetime(df["Ngày"])
df["Lợi nhuận (VNĐ)"] = df["Doanh thu (VNĐ)"] - df["Chi phí (VNĐ)"]

# Bộ lọc
st.sidebar.header("🔎 Bộ lọc")

products = st.sidebar.multiselect(
    "Sản phẩm",
    options=sorted(df["Sản phẩm"].unique()),
    default=sorted(df["Sản phẩm"].unique())
)

regions = st.sidebar.multiselect(
    "Khu vực",
    options=sorted(df["Khu vực"].unique()),
    default=sorted(df["Khu vực"].unique())
)

channels = st.sidebar.multiselect(
    "Kênh bán",
    options=sorted(df["Kênh bán"].unique()),
    default=sorted(df["Kênh bán"].unique())
)

filtered = df[
    df["Sản phẩm"].isin(products)
    & df["Khu vực"].isin(regions)
    & df["Kênh bán"].isin(channels)
]

# Chỉ số tổng quan
revenue = filtered["Doanh thu (VNĐ)"].sum()
cost = filtered["Chi phí (VNĐ)"].sum()
profit = filtered["Lợi nhuận (VNĐ)"].sum()
quantity = filtered["Số lượng"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Doanh thu", f"{revenue:,.0f} VNĐ")
col2.metric("💸 Chi phí", f"{cost:,.0f} VNĐ")
col3.metric("📈 Lợi nhuận", f"{profit:,.0f} VNĐ")
col4.metric("📦 Số lượng bán", f"{quantity:,}")

st.divider()

if filtered.empty:
    st.warning("Không có dữ liệu phù hợp với bộ lọc.")
    st.stop()

# Chuẩn bị dữ liệu theo tháng
monthly = (
    filtered.assign(Tháng=filtered["Ngày"].dt.to_period("M").astype(str))
    .groupby("Tháng", as_index=False)["Doanh thu (VNĐ)"]
    .sum()
)

st.subheader("📈 Doanh thu theo tháng")
st.line_chart(monthly.set_index("Tháng"))

# Hai biểu đồ
col1, col2 = st.columns(2)

with col1:
    st.subheader("🛍️ Doanh thu theo sản phẩm")
    product_sales = (
        filtered.groupby("Sản phẩm", as_index=False)["Doanh thu (VNĐ)"]
        .sum()
        .set_index("Sản phẩm")
    )
    st.bar_chart(product_sales)

with col2:
    st.subheader("🌎 Doanh thu theo khu vực")
    region_sales = (
        filtered.groupby("Khu vực", as_index=False)["Doanh thu (VNĐ)"]
        .sum()
        .set_index("Khu vực")
    )
    st.bar_chart(region_sales)

st.subheader("📋 Dữ liệu chi tiết")
display_df = filtered.copy()
display_df["Ngày"] = display_df["Ngày"].dt.strftime("%d/%m/%Y")
st.dataframe(display_df, use_container_width=True)
