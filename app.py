import streamlit as st
import pandas as pd
import json
import time
import os
from datetime import datetime
import phonenumbers
from streamlit_lottie import st_lottie
import requests
from pathlib import Path

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="EMOTICONN AI - Giao Tiếp Cảm Xúc Thông Minh",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CONSTANTS ====================
FREE_TRIAL_LIMIT = 3
BANK_ACCOUNT = {
    "bank": "BIDV",
    "account_number": "4430269669",
    "account_name": "NGUYEN XUAN DAT",
    "note_format": "AI + [SỐ ĐIỆN THOẠI]"
}

# ==================== FILE PATHS ====================
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USAGE_FILE = DATA_DIR / "usage_log.csv"
PAID_FILE = DATA_DIR / "paid_users.json"

# ==================== INITIALIZE FILES ====================
def init_files():
    if not USAGE_FILE.exists():
        pd.DataFrame(columns=["phone", "timestamp", "used_count"]).to_csv(USAGE_FILE, index=False)
    
    if not PAID_FILE.exists():
        with open(PAID_FILE, "w") as f:
            json.dump({}, f)

init_files()

# ==================== CSS STYLING ====================
def load_css():
    st.markdown("""
    <style>
    /* Main Theme */
    :root {
        --primary: #2C3E50;
        --secondary: #F8F9FA;
        --accent: #1ABC9C;
        --text: #333333;
    }
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(90deg, var(--primary) 0%, #34495E 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
        background: linear-gradient(90deg, #FFFFFF 0%, #1ABC9C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.5rem !important;
        opacity: 0.9;
        margin-bottom: 2rem !important;
    }
    
    /* Cards */
    .custom-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border: 1px solid #E9ECEF;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, var(--accent) 0%, #16A085 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 20px rgba(26, 188, 156, 0.3);
    }
    
    /* Input Fields */
    .stTextArea > div > div > textarea {
        border-radius: 15px !important;
        border: 2px solid #E9ECEF !important;
        padding: 1rem !important;
        font-size: 16px !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent) !important;
    }
    
    /* Radio Buttons */
    .stRadio > div {
        flex-direction: row;
        gap: 2rem;
    }
    
    .stRadio > div > label {
        background: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        border: 2px solid #E9ECEF;
        transition: all 0.3s ease;
    }
    
    .stRadio > div > label:hover {
        border-color: var(--accent);
        transform: translateY(-2px);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background-color: var(--accent);
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Payment Section */
    .payment-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
    }
    
    /* Result Card */
    .result-card {
        background: #FFF9F0;
        border-left: 5px solid var(--accent);
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem 0;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ==================== DATA MANAGEMENT ====================
def load_usage_data():
    try:
        return pd.read_csv(USAGE_FILE)
    except:
        return pd.DataFrame(columns=["phone", "timestamp", "used_count"])

def save_usage_data(df):
    df.to_csv(USAGE_FILE, index=False)

def load_paid_users():
    try:
        with open(PAID_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_paid_user(phone):
    paid_users = load_paid_users()
    paid_users[phone] = datetime.now().isoformat()
    with open(PAID_FILE, "w") as f:
        json.dump(paid_users, f)

# ==================== VALIDATION FUNCTIONS ====================
def validate_phone_number(phone):
    try:
        parsed = phonenumbers.parse(phone, "VN")
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except:
        pass
    return None

def get_user_usage(phone):
    df = load_usage_data()
    user_data = df[df["phone"] == phone]
    
    if user_data.empty:
        return 0
    else:
        # Reset count if it's a new day (optional feature)
        return int(user_data.iloc[-1]["used_count"])

def update_usage(phone):
    df = load_usage_data()
    current_time = datetime.now().isoformat()
    
    if phone in df["phone"].values:
        df.loc[df["phone"] == phone, "used_count"] += 1
        df.loc[df["phone"] == phone, "timestamp"] = current_time
    else:
        new_row = pd.DataFrame({
            "phone": [phone],
            "timestamp": [current_time],
            "used_count": [1]
        })
        df = pd.concat([df, new_row], ignore_index=True)
    
    save_usage_data(df)

# ==================== AI MESSAGE GENERATOR ====================
class MessageGenerator:
    def __init__(self):
        self.templates = {
            "new_acquaintance": {
                "male": [
                    "Chào bạn, rất vui được làm quen. Mình thấy {context} rất thú vị, có thể chia sẻ thêm về điều này không?",
                    "Xin chào, hy vọng bạn có một ngày tốt lành. Mình muốn hỏi về {context} nếu không phiền.",
                    "Chào bạn, mình vừa nghĩ đến bạn và muốn gửi lời chào. Công việc/dự án {context} của bạn thế nào rồi?"
                ],
                "female": [
                    "Chào bạn, thật tuyệt khi được kết nối. Mình rất ấn tượng với {context}, bạn có thể kể thêm không?",
                    "Xin chào, chúc bạn một ngày tràn đầy năng lượng. Mình tình cờ thấy {context} và nghĩ ngay đến bạn.",
                    "Chào bạn, hy vọng tin nhắn này không làm phiền bạn. Mình muốn hỏi về {context} một chút."
                ]
            },
            "dating": {
                "male": [
                    "Em ơi, anh vừa đi ngang qua quán cafe chúng mình hôm trước, nhớ em nhiều lắm. {context}",
                    "Chúc em ngủ ngon nhé. Hy vọng em có những giấc mơ đẹp. {context}",
                    "Anh vừa thấy món này nghĩ ngay đến em. {context} Em có muốn thử cùng anh không?"
                ],
                "female": [
                    "Anh ơi, em vừa nấu món mới, nhớ đến anh liền. {context}",
                    "Chúc anh một ngày làm việc hiệu quả nhé. {context}",
                    "Em đang nghe bài hát này, thấy hợp với tâm trạng của mình hôm nay. {context}"
                ]
            },
            "long_term": {
                "male": [
                    "Cảm ơn em vì tất cả. Dù ngày hôm nay thế nào, anh vẫn luôn biết ơn vì có em bên cạnh. {context}",
                    "Anh yêu em nhiều hơn những gì anh có thể nói. {context}",
                    "Nhìn lại chặng đường đã qua, anh thực sự hạnh phúc vì đã chọn em."
                ],
                "female": [
                    "Cảm ơn anh đã luôn là điểm tựa vững chắc. {context}",
                    "Em không thể tưởng tượng cuộc sống sẽ thế nào nếu không có anh. {context}",
                    "Dù có chuyện gì xảy ra, em vẫn luôn tin tưởng và yêu anh."
                ]
            },
            "spouse": {
                "neutral": [
                    "Cảm ơn anh/em vì đã cùng nhau xây dựng tổ ấm này. {context}",
                    "Dù bận rộn thế nào, mình luôn nhớ đến nhau nhé. {context}",
                    "Gia đình mình thật hạnh phúc vì có nhau. {context}"
                ]
            },
            "reconcile": {
                "male": [
                    "Anh xin lỗi vì đã làm em buồn. Anh thực sự trân trọng em và muốn mọi thứ tốt đẹp trở lại. {context}",
                    "Anh nhận ra mình đã sai. Em cho anh cơ hội được nói chuyện và sửa sai nhé. {context}",
                    "Tình cảm của chúng ta quan trọng hơn bất kỳ mâu thuẫn nào. Mình cùng vượt qua nhé em."
                ],
                "female": [
                    "Em xin lỗi anh. Em không muốn vì hiểu lầm mà làm tổn thương tình cảm của mình. {context}",
                    "Em nhớ anh nhiều lắm. Mình làm lành nhé? {context}",
                    "Dù có bất đồng, em vẫn yêu anh. Mình cùng tìm cách giải quyết tốt nhất nhé."
                ]
            }
        }
    
    def generate(self, gender, situation, user_input):
        import random
        
        gender_key = "male" if gender == "Nam" else "female"
        
        if situation == "Vợ/chồng":
            template_key = "spouse"
            gender_key = "neutral"
        else:
            situation_map = {
                "Mới quen": "new_acquaintance",
                "Đang tìm hiểu": "dating",
                "Yêu lâu năm": "long_term",
                "Nhắn tin làm hoà": "reconcile"
            }
            template_key = situation_map.get(situation, "new_acquaintance")
        
        templates = self.templates.get(template_key, {}).get(gender_key, [])
        
        if not templates:
            templates = ["Xin chào, {context}"]
        
        template = random.choice(templates)
        
        # Smart context insertion
        if user_input.strip():
            if len(user_input) < 50:
                # Short input - insert directly
                message = template.format(context=user_input)
            else:
                # Long input - summarize
                summary = user_input[:100] + "..." if len(user_input) > 100 else user_input
                message = template.format(context=f"Về chuyện {summary.lower()}")
        else:
            message = template.format(context="")
        
        # Add appropriate emoji based on situation
        emoji_map = {
            "Mới quen": "👋",
            "Đang tìm hiểu": "💝",
            "Yêu lâu năm": "❤️",
            "Vợ/chồng": "🏡",
            "Nhắn tin làm hoà": "🕊️"
        }
        
        return f"{message} {emoji_map.get(situation, '💬')}"

# ==================== STREAMLIT APP ====================
def main():
    # Initialize session state
    if 'phone' not in st.session_state:
        st.session_state.phone = ""
    if 'verified' not in st.session_state:
        st.session_state.verified = False
    if 'paid' not in st.session_state:
        st.session_state.paid = False
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">EMOTICONN AI</h1>
        <h2 class="hero-subtitle">Giao Điệu Cảm Xúc - Tinh Tế Trong Từng Tin Nhắn</h2>
        <p style="font-size: 1.2rem; opacity: 0.8;">AI thông minh giúp bạn diễn đạt cảm xúc chân thành, lịch sự, đúng lúc</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Access Bar
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🏠 Trang chủ", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("✨ Dùng thử", use_container_width=True):
            st.session_state.phone = ""
            st.session_state.verified = False
            st.rerun()
    with col3:
        if st.button("💳 Nâng cấp", use_container_width=True):
            st.session_state.phone = ""
            st.rerun()
    with col4:
        if st.button("📞 Hỗ trợ", use_container_width=True):
            st.info("📧 Email: support@emoticonn.ai | 📱 Zalo: 090-123-4567")
    
    st.markdown("---")
    
    # Phone Verification Section
    if not st.session_state.verified:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("🔐 Xác Thực Số Điện Thoại")
        st.write("Nhập số điện thoại để bắt đầu dùng thử (3 tin nhắn miễn phí)")
        
        phone_input = st.text_input(
            "Số điện thoại của bạn (Việt Nam):",
            placeholder="0912345678",
            key="phone_input"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            verify_btn = st.button("✅ Xác Nhận & Bắt Đầu Dùng Thử", use_container_width=True)
        
        if verify_btn:
            valid_phone = validate_phone_number(phone_input)
            if valid_phone:
                st.session_state.phone = valid_phone
                st.session_state.verified = True
                
                # Check if user is paid
                paid_users = load_paid_users()
                if valid_phone in paid_users:
                    st.session_state.paid = True
                
                st.success(f"✅ Xác thực thành công! Số điện thoại: {valid_phone}")
                st.rerun()
            else:
                st.error("⚠️ Số điện thoại không hợp lệ. Vui lòng nhập số Việt Nam (ví dụ: 0912345678)")
        
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Main Application Section
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    
    # Check usage limit
    if not st.session_state.paid:
        used_count = get_user_usage(st.session_state.phone)
        remaining = FREE_TRIAL_LIMIT - used_count
        
        if remaining <= 0:
            st.warning(f"⚠️ Bạn đã dùng hết {FREE_TRIAL_LIMIT} lượt miễn phí")
            st.markdown("</div>", unsafe_allow_html=True)
            show_payment_section()
            return
        
        st.info(f"🎯 Bạn còn **{remaining}/{FREE_TRIAL_LIMIT}** lượt dùng thử")
        st.progress(used_count / FREE_TRIAL_LIMIT)
    
    # User Input Section
    st.subheader("🎯 Tạo Tin Nhắn Tinh Tế")
    
    # Gender Selection
    gender = st.radio(
        "Giới tính của bạn:",
        ["Nam", "Nữ"],
        horizontal=True,
        key="gender"
    )
    
    # Situation Selection
    situation_options = ["Mới quen", "Đang tìm hiểu", "Yêu lâu năm", "Vợ/chồng", "Nhắn tin làm hoà"]
    situation = st.selectbox(
        "Tình huống giao tiếp:",
        situation_options,
        key="situation"
    )
    
    # Message Input
    user_input = st.text_area(
        "Nội dung bạn muốn nhắn (hoặc để trống để AI gợi ý):",
        placeholder="Ví dụ: Mình vừa xem bộ phim rất hay, muốn chia sẻ với bạn...",
        height=150,
        key="user_input"
    )
    
    # Generate Button
    generate_btn = st.button(
        f"🎯 Tạo Tin Nhắn Tinh Tế",
        use_container_width=True,
        type="primary",
        key="generate"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Result Section
    if generate_btn:
        if not st.session_state.paid:
            update_usage(st.session_state.phone)
            used_count = get_user_usage(st.session_state.phone)
            remaining = FREE_TRIAL_LIMIT - used_count
            
            if remaining < 0:
                st.error("⚠️ Bạn đã dùng hết lượt miễn phí")
                show_payment_section()
                return
        
        # Generate message
        generator = MessageGenerator()
        with st.spinner("🔄 AI đang tạo tin nhắn tinh tế cho bạn..."):
            time.sleep(1)  # Simulate AI processing
            result = generator.generate(gender, situation, user_input)
        
        # Display result
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.subheader("💌 Tin Nhắn Gợi Ý:")
        st.write(result)
        
        # Copy button
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("📋 Copy Tin Nhắn", use_container_width=True):
                st.code(result, language="text")
                st.success("✅ Đã copy vào clipboard!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show remaining attempts
        if not st.session_state.paid:
            st.info(f"🎯 Bạn còn **{remaining-1}/{FREE_TRIAL_LIMIT}** lượt dùng thử")
            
            if remaining <= 1:
                st.warning("⚠️ Chỉ còn 1 lượt miễn phí cuối cùng!")
    
    # Upgrade prompt (subtle)
    if not st.session_state.paid and get_user_usage(st.session_state.phone) >= 1:
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption("💎 **Mở khóa vĩnh viễn để không giới hạn tin nhắn tinh tế**")
        with col2:
            if st.button("💳 Nâng Cấp Ngay", use_container_width=True):
                show_payment_section()

def show_payment_section():
    st.markdown("""
    <div class="payment-card">
        <h2 style="color: white;">🔓 MỞ KHÓA VĨNH VIỄN</h2>
        <p style="font-size: 1.2rem;">Chỉ một lần duy nhất - Dùng trọn đời</p>
        <h1 style="color: #FFD700; font-size: 3rem;">199.000đ</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-card">
        <h3>💳 Hướng Dẫn Thanh Toán</h3>
        
        1. **Chuyển khoản qua ngân hàng:**
        
        ```
        Ngân hàng: BIDV
        Số tài khoản: 4430269669
        Chủ tài khoản: NGUYEN XUAN DAT
        Số tiền: 199.000 VND
        Nội dung chuyển khoản: AI {SỐ ĐIỆN THOẠI CỦA BẠN}
        ```
        
        **Ví dụ:** Nếu số điện thoại của bạn là 0912345678, nội dung CK: `AI 0912345678`
        
        2. **Sau khi chuyển khoản, quay lại đây nhập mã xác nhận:**
    </div>
    """, unsafe_allow_html=True)
    
    # Verification input
    col1, col2 = st.columns([2, 1])
    with col1:
        verification_code = st.text_input(
            "Nhập mã xác nhận (chính là SỐ ĐIỆN THOẠI của bạn):",
            placeholder="0912345678"
        )
    
    with col2:
        verify_payment = st.button("✅ Xác Nhận Thanh Toán", use_container_width=True)
    
    if verify_payment:
        if verification_code == st.session_state.phone.replace("+84", "0"):
            save_paid_user(st.session_state.phone)
            st.session_state.paid = True
            st.balloons()
            st.success("🎉 Chúc mừng! Bạn đã mở khóa thành công! Tận hưởng trải nghiệm không giới hạn!")
            time.sleep(2)
            st.rerun()
        else:
            st.error("⚠️ Mã xác nhận không đúng. Vui lòng kiểm tra lại hoặc liên hệ hỗ trợ.")

if __name__ == "__main__":
    main()
