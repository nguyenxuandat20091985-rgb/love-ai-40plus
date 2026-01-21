import streamlit as st
import random

st.set_page_config(page_title="Yêu AI 40+", layout="centered")

st.title("❤️ Yêu AI 40+")
st.subheader("Gợi ý nhắn tin tinh tế cho đàn ông trưởng thành")

# ---------------- DATA OFFLINE ---------------- #

DATA = {
    "mệt": [
        "Nghe em nói vậy là anh hiểu hôm nay không nhẹ nhàng rồi. Nghỉ sớm đi, để mai mình nói tiếp cũng được.",
        "Có những ngày chỉ cần yên tĩnh một chút là đủ. Em cứ nghỉ ngơi, anh ở đây.",
        "Ừ, mệt thì đừng cố. Chăm mình trước đã, mọi thứ khác để sau."
    ],
    "lạnh": [
        "Anh không biết em đang bận hay chỉ muốn yên tĩnh, nên anh để em thoải mái nhé.",
        "Có thể hôm nay em không có tâm trạng nói chuyện, anh hiểu.",
        "Không sao đâu, khi nào em muốn nói thì anh vẫn ở đây."
    ],
    "vui": [
        "Nghe em vui là tự nhiên anh cũng thấy nhẹ người theo.",
        "Những lúc thế này nói chuyện với em thấy dễ chịu thật.",
        "Vậy là hôm nay là một ngày ổn áp rồi."
    ],
    "tán": [
        "Anh không vội, chỉ muốn nói chuyện với em một cách thoải mái.",
        "Nói chuyện với em thấy dễ chịu, vậy là đủ cho một ngày rồi.",
        "Anh thích những cuộc trò chuyện không cần gượng ép như thế này."
    ]
}

# ---------------- LOGIC PHÂN TÍCH ---------------- #

def analyze_message(msg):
    msg = msg.lower()
    if any(x in msg for x in ["mệt", "buồn", "stress", "chán"]):
        return "mệt"
    if any(x in msg for x in ["ừ", "ok", "tùy", "sao cũng được"]):
        return "lạnh"
    if any(x in msg for x in ["vui", "haha", "thích", "vui ghê"]):
        return "vui"
    return "tán"

# ---------------- UI ---------------- #

relationship = st.selectbox(
    "Mối quan hệ hiện tại",
    ["Người yêu – xấp xỉ tuổi", "Bạn gái mới / đang tìm hiểu"]
)

last_message = st.text_area(
    "Tin nhắn cuối cùng cô ấy gửi",
    placeholder="Ví dụ: Hôm nay em mệt quá..."
)

if st.button("AI gợi ý trả lời"):
    if last_message.strip() == "":
        st.warning("Anh nhập tin nhắn của cô ấy trước nhé.")
    else:
        mood = analyze_message(last_message)
        reply = random.choice(DATA[mood])
        st.success(reply)
