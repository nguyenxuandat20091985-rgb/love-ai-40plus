import streamlit as st
from datetime import datetime

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Yêu AI 40+",
    page_icon="❤️",
    layout="centered"
)

st.title("❤️ Yêu AI 40+")
st.subheader("Gợi ý nhắn tin tinh tế cho đàn ông trưởng thành")

# ================== CHỌN NGỮ CẢNH ==================
relationship = st.selectbox(
    "Mối quan hệ hiện tại",
    [
        "Người yêu – xấp xỉ tuổi",
        "Người yêu – kém tuổi",
        "Crush – hợp tuổi",
        "Crush – kém nhiều tuổi"
    ]
)

last_message = st.text_area(
    "Tin nhắn cuối cùng cô ấy gửi",
    placeholder="Ví dụ: Hôm nay em mệt quá..."
)

# ================== LOGIC AI 40+ ==================
def ai_reply(context, message):
    if not message.strip():
        return "Anh cần nội dung tin nhắn của cô ấy để gợi ý chính xác hơn."

    if "Người yêu" in context:
        return (
            "Nghe em nói vậy anh cũng thấy thương. "
            "Mệt thì nghỉ ngơi chút đi, tối anh gọi nghe giọng em cho đỡ mệt nhé."
        )

    if "Crush" in context:
        return (
            "Vậy à, nghe em nói anh cũng thấy lo. "
            "Nếu cần người nghe em chia sẻ thì anh sẵn sàng."
        )

    return "Anh đang suy nghĩ cách trả lời phù hợp nhất."

# ================== NÚT XỬ LÝ ==================
if st.button("AI gợi ý trả lời"):
    reply = ai_reply(relationship, last_message)

    st.success("💬 Gợi ý trả lời theo phong cách đàn ông 40+:")
    st.write(reply)

    st.caption(f"Tạo lúc: {datetime.now().strftime('%H:%M %d-%m-%Y')}")
