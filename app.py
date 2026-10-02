import streamlit as st

st.title("Ứng dụng đầu tiên của tôi")

st.write("Xin chào! Đây là app Streamlit của tôi.")

name = st.text_input("Bạn tên gì?")

if name:
    st.write("Xin chào", name, "👋")
