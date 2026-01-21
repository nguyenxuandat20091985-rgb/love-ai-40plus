import streamlit as st
import pandas as pd
import json
import time
import random
import re
from datetime import datetime
from pathlib import Path

# ==================== CẤU HÌNH ====================
st.set_page_config(
    page_title="EMOTICONN AI - Trợ Lý Giao Tiếp Cảm Xúc",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== CSS ====================
st.markdown("""<style>
#MainMenu, footer, .stDeployButton {display:none!important;}
</style>""", unsafe_allow_html=True)

# ==================== HẰNG SỐ ====================
FREE_TRIAL_LIMIT = 5

# ==================== DATA ====================
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USAGE_FILE = DATA_DIR / "usage.csv"
PAID_FILE = DATA_DIR / "paid.json"

def init_files():
    if not USAGE_FILE.exists():
        pd.DataFrame(columns=["phone", "count", "last_used"]).to_csv(USAGE_FILE, index=False)
    if not PAID_FILE.exists():
        with open(PAID_FILE, "w") as f:
            json.dump({}, f)

init_files()

# ==================== HELPERS ====================
def validate_phone(phone):
    phone = re.sub(r"\D", "", phone)
    if phone.startswith("0") and 9 <= len(phone) <= 11:
        return phone
    return None

def get_usage_count(phone):
    try:
        df = pd.read_csv(USAGE_FILE)
        row = df[df["phone"] == phone]
        return int(row.iloc[0]["count"]) if not row.empty else 0
    except:
        return 0

def update_usage(phone):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        df = pd.read_csv(USAGE_FILE)
    except:
        df = pd.DataFrame(columns=["phone", "count", "last_used"])

    if phone in df["phone"].values:
        df.loc[df["phone"] == phone, "count"] += 1
        df.loc[df["phone"] == phone, "last_used"] = now
    else:
        df = pd.concat([df, pd.DataFrame({
            "phone": [phone],
            "count": [1],
            "last_used": [now]
        })], ignore_index=True)

    df.to_csv(USAGE_FILE, index=False)

def load_paid_users():
    try:
        with open(PAID_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# ==================== AI ENGINE ====================
class EmotionalAI:
    def __init__(self):
        self.templates = {
            "Làm quen": {
                "Nam→Nữ": [
                    "Chào bạn, mình thấy {detail} và muốn làm quen nếu bạn không phiền. Hôm nay của bạn thế nào? ☕",
                    "Xin chào, hy vọng tin nhắn này không làm phiền. Mình muốn làm quen và trò chuyện với bạn. 😊",
                ],
                "Nữ→Nam": [
                    "Chào anh, em muốn làm quen nếu anh không ngại. Anh đang làm gì vậy? 🌸",
                    "Xin chào anh, em thấy anh khá thú vị và muốn trò chuyện thử. 🤍",
                ]
            },
            "Hỏi thăm": {
                "Nam→Nữ": [
                    "Dạo này bạn thế nào? Công việc có áp lực nhiều không? Nếu cần chia sẻ, mình luôn sẵn sàng lắng nghe. 🌿",
                ],
                "Nữ→Nam": [
                    "Anh dạo này ổn không? Công việc có mệt lắm không, nhớ giữ sức khỏe nhé. 🤗",
                ]
            },
            "An ủi": {
                "Nam→Nữ": [
                    "Mình biết lúc này không dễ dàng, nhưng bạn không hề đơn độc. Mình ở đây nếu bạn cần. 🌱",
                ],
                "Nữ→Nam": [
                    "Em biết anh đang áp lực, nhưng mọi chuyện rồi sẽ ổn thôi. Em tin anh. 💛",
                ]
            },
            "Tỏ tình": {
                "Nam→Nữ": [
                    "Mình đã suy nghĩ rất nhiều trước khi nói điều này… mình thực sự có cảm tình với bạn. ❤️",
                ],
                "Nữ→Nam": [
                    "Em không giỏi nói lời hoa mỹ, nhưng em thích anh – thật lòng. 💕",
                ]
            },
            "Làm hoà": {
                "Nam→Nữ": [
                    "Mình xin lỗi nếu đã làm bạn buồn. Mình thật sự trân trọng mối quan hệ này. 🌧️➡️🌤️",
                ],
                "Nữ→Nam": [
                    "Em không muốn chúng ta xa cách như thế này. Mong anh cho em cơ hội nói chuyện lại. 🤍",
                ]
            }
        }

    def generate(self, user_gender, target_gender, situation, context=""):
        key = f"{user_gender}→{target_gender}"
        templates = self.templates.get(situation, {}).get(key, [
            "Chào bạn, hy vọng bạn có một ngày thật dễ chịu. 🌼"
        ])
        msg = random.choice(templates)
        if context:
            detail = context[:60] + "..." if len(context) > 60 else context
            msg = msg.replace("{detail}", detail)
        else:
            msg = msg.replace("{detail}", "bạn")
        return msg

# ==================== APP ====================
def main():
    if "verified" not in st.session_state:
        st.session_state.verified = False
    if "phone" not in st.session_state:
        st.session_state.phone = ""
    if "usage_count" not in st.session_state:
        st.session_state.usage_count = 0
    if "result" not in st.session_state:
        st.session_state.result = ""

    st.title("💬 EMOTICONN AI")
    st.caption("Nói điều bạn muốn – theo cách họ muốn nghe")

    # ===== ĐĂNG KÝ =====
    if not st.session_state.verified:
        phone = st.text_input("📱 Nhập số điện thoại")
        if st.button("✨ Nhận 5 tin miễn phí"):
            valid = validate_phone(phone)
            if not valid:
                st.error("Số điện thoại không hợp lệ")
                return
            st.session_state.phone = valid
            st.session_state.usage_count = get_usage_count(valid)
            st.session_state.verified = True
            st.success("Đăng ký thành công!")
            st.rerun()
        return

    # ===== TRIAL =====
    used = st.session_state.usage_count
    remaining = FREE_TRIAL_LIMIT - used
    percent = (used / FREE_TRIAL_LIMIT) * 100

    st.info(f"🎯 Lượt còn lại: {remaining}/{FREE_TRIAL_LIMIT}")
    st.progress(percent / 100)

    if remaining <= 0:
        st.warning("🚫 Bạn đã hết lượt dùng thử")
        return

    # ===== INPUT =====
    user_gender = st.radio("Bạn là:", ["Nam", "Nữ"], horizontal=True)
    target_gender = st.radio("Gửi cho:", ["Nam", "Nữ"], horizontal=True)
    situation = st.selectbox("Tình huống", ["Làm quen", "Hỏi thăm", "An ủi", "Tỏ tình", "Làm hoà"])
    context = st.text_area("Chi tiết thêm (tuỳ chọn)")

    # ===== GENERATE =====
    if st.button("✨ AI Tạo tin nhắn"):
        if st.session_state.usage_count >= FREE_TRIAL_LIMIT:
            st.error("Hết lượt dùng thử")
            return

        st.session_state.usage_count += 1
        update_usage(st.session_state.phone)

        ai = EmotionalAI()
        with st.spinner("AI đang suy nghĩ..."):
            time.sleep(1)
            st.session_state.result = ai.generate(
                user_gender, target_gender, situation, context
            )

    # ===== RESULT =====
    if st.session_state.result:
        st.subheader("💌 Tin nhắn gợi ý")
        st.write(st.session_state.result)

        st.markdown(
            f"""
            <button onclick="navigator.clipboard.writeText(`{st.session_state.result}`)"
            style="padding:10px;border-radius:10px;width:100%;margin-top:10px;">
            📋 Copy tin nhắn
            </button>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
