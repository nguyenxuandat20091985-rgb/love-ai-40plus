import streamlit as st

st.set_page_config(page_title="LOVE AI 40+", layout="centered")

st.title("💬 LOVE AI 40+")
st.caption("Gợi ý nhắn tin tinh tế cho đàn ông trưởng thành")

mode = st.selectbox(
    "Mối quan hệ",
    [
        "Người yêu – xấp xỉ tuổi",
        "Người yêu – kém tuổi",
        "Crush – xấp xỉ tuổi",
        "Crush – kém tuổi",
    ],
)

last_msg = st.text_area("Tin nhắn vừa nhận")

if st.button("AI gợi ý trả lời"):
    st.success("Anh trả lời thế này là vừa đủ tinh tế.")
