import streamlit as st
import pandas as pd
import json
import time
import os
from datetime import datetime
import re
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
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .hero-title {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
        background: linear-gradient(90deg, #FFFFFF 0%, #1ABC9C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.3rem !important;
        opacity: 0.9;
        margin-bottom: 1.5rem !important;
    }
    
    /* Cards */
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border: 1px solid #E9ECEF;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, var(--accent) 0%, #16A085 100%);
        color: white;
        border: none;
        padding: 10px 24px;
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
        border-radius: 12px !important;
        border: 2px solid #E9ECEF !important;
        padding: 0.8rem !important;
        font-size: 16px !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent) !important;
    }
    
    /* Radio Buttons */
    .stRadio > div {
        flex-direction: row;
        gap: 1rem;
    }
    
    .stRadio > div > label {
        background: white;
        padding: 0.8rem 1.5rem;
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
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
    }
    
    /* Result Card */
    .result-card {
        background: #FFF9F0;
        border-left: 5px solid var(--accent);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Phone Input */
    .phone-input {
        font-size: 1.2rem !important;
        padding: 12px !important;
        text-align: center !important;
    }
    
    /* Success Message */
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #28a745;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Warning Message */
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #ffc107;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ==================== VALIDATION FUNCTIONS ====================
def validate_phone_number(phone):
    """Simple Vietnamese phone number validation"""
    # Remove all non-digit characters
    phone = re.sub(r'\D', '', phone)
    
    # Check length
    if len(phone) < 9 or len(phone) > 11:
        return None
    
    # Check if starts with common Vietnamese prefixes
    prefixes = ['84', '0']
    for prefix in prefixes:
        if phone.startswith(prefix):
            # Standardize to 0XXXXXXXXX format
            if phone.startswith('84'):
                phone = '0' + phone[2:]
            return phone
    
    # If starts with 0, it's already in correct format
    if phone.startswith('0'):
        return phone
    
    return None

def get_user_usage(phone):
    """Get usage count for a phone number"""
    try:
        df = pd.read_csv(USAGE_FILE)
        user_data = df[df["phone"] == phone]
        
        if user_data.empty:
            return 0
        else:
            return int(user_data.iloc[-1]["used_count"])
    except:
        return 0

def update_usage(phone):
    """Update usage count for a phone number"""
    try:
        df = pd.read_csv(USAGE_FILE)
    except:
        df = pd.DataFrame(columns=["phone", "timestamp", "used_count"])
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
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
    
    df.to_csv(USAGE_FILE, index=False)

def load_paid_users():
    """Load paid users from JSON file"""
    try:
        with open(PAID_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_paid_user(phone):
    """Save paid user to JSON file"""
    paid_users = load_paid_users()
    paid_users[phone] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(PAID_FILE, "w") as f:
        json.dump(paid_users, f, indent=2)

# ==================== AI MESSAGE GENERATOR ====================
class MessageGenerator:
    def __init__(self):
        self.templates = {
            "Mới quen": {
                "Nam": [
                    "Chào bạn, rất vui được làm quen. Mình thấy {context} rất thú vị, có thể chia sẻ thêm về điều này không? 💬",
                    "Xin chào, hy vọng bạn có một ngày tốt lành. Mình muốn hỏi về {context} nếu không phiền. ☕",
                    "Chào bạn, mình vừa nghĩ đến bạn và muốn gửi lời chào. Công việc/dự án {context} của bạn thế nào rồi? 💼"
                ],
                "Nữ": [
                    "Chào bạn, thật tuyệt khi được kết nối. Mình rất ấn tượng với {context}, bạn có thể kể thêm không? ✨",
                    "Xin chào, chúc bạn một ngày tràn đầy năng lượng. Mình tình cờ thấy {context} và nghĩ ngay đến bạn. 🌟",
                    "Chào bạn, hy vọng tin nhắn này không làm phiền bạn. Mình muốn hỏi về {context} một chút. 💭"
                ]
            },
            "Đang tìm hiểu": {
                "Nam": [
                    "Em ơi, anh vừa đi ngang qua quán cafe chúng mình hôm trước, nhớ em nhiều lắm. {context} ❤️",
                    "Chúc em ngủ ngon nhé. Hy vọng em có những giấc mơ đẹp. {context} 🌙",
                    "Anh vừa thấy món này nghĩ ngay đến em. {context} Em có muốn thử cùng anh không? 🍰"
                ],
                "Nữ": [
                    "Anh ơi, em vừa nấu món mới, nhớ đến anh liền. {context} 🍲",
                    "Chúc anh một ngày làm việc hiệu quả nhé. {context} 💪",
                    "Em đang nghe bài hát này, thấy hợp với tâm trạng của mình hôm nay. {context} 🎵"
                ]
            },
            "Yêu lâu năm": {
                "Nam": [
                    "Cảm ơn em vì tất cả. Dù ngày hôm nay thế nào, anh vẫn luôn biết ơn vì có em bên cạnh. {context} 🙏",
                    "Anh yêu em nhiều hơn những gì anh có thể nói. {context} 💖",
                    "Nhìn lại chặng đường đã qua, anh thực sự hạnh phúc vì đã chọn em. {context} 🌟"
                ],
                "Nữ": [
                    "Cảm ơn anh đã luôn là điểm tựa vững chắc. {context} 🤗",
                    "Em không thể tưởng tượng cuộc sống sẽ thế nào nếu không có anh. {context} 💕",
                    "Dù có chuyện gì xảy ra, em vẫn luôn tin tưởng và yêu anh. {context} 💝"
                ]
            },
            "Vợ/chồng": {
                "Nam": [
                    "Cảm ơn em vì đã cùng anh xây dựng tổ ấm này. {context} 🏡",
                    "Dù bận rộn thế nào, anh luôn nhớ đến em. {context} 💑",
                    "Gia đình mình thật hạnh phúc vì có nhau. {context} 👨‍👩‍👧‍👦"
                ],
                "Nữ": [
                    "Cảm ơn anh vì đã cùng em xây dựng tổ ấm này. {context} 🏡",
                    "Dù bận rộn thế nào, em luôn nhớ đến anh. {context} 💑",
                    "Gia đình mình thật hạnh phúc vì có nhau. {context} 👨‍👩‍👧‍👦"
                ]
            },
            "Nhắn tin làm hoà": {
                "Nam": [
                    "Anh xin lỗi vì đã làm em buồn. Anh thực sự trân trọng em và muốn mọi thứ tốt đẹp trở lại. {context} 🕊️",
                    "Anh nhận ra mình đã sai. Em cho anh cơ hội được nói chuyện và sửa sai nhé. {context} 🤝",
                    "Tình cảm của chúng ta quan trọng hơn bất kỳ mâu thuẫn nào. Mình cùng vượt qua nhé em. {context} 💞"
                ],
                "Nữ": [
                    "Em xin lỗi anh. Em không muốn vì hiểu lầm mà làm tổn thương tình cảm của mình. {context} 🕊️",
                    "Em nhớ anh nhiều lắm. Mình làm lành nhé? {context} 🤗",
                    "Dù có bất đồng, em vẫn yêu anh. Mình cùng tìm cách giải quyết tốt nhất nhé. {context} 💞"
                ]
            }
        }
    
    def generate(self, gender, situation, user_input):
        import random
        
        # Get templates for the situation and gender
        if situation in self.templates and gender in self.templates[situation]:
            templates = self.templates[situation][gender]
        else:
            # Default templates
            templates = ["Xin chào, {context} 💬"]
        
        # Select random template
        template = random.choice(templates)
        
        # Process user input
        context_text = user_input.strip()
        
        if context_text:
            if len(context_text) < 50:
                # Short input - insert directly
                message = template.format(context=context_text)
            else:
                # Long input - use first part
                summary = context_text[:80] + "..."
                message = template.format(context=f"Về chuyện {summary}")
        else:
            # No input provided
            if "{context}" in template:
                message = template.format(context="")
            else:
                message = template
        
        return message

# ==================== MAIN APP ====================
def main():
    # Initialize session state
    if 'phone' not in st.session_state:
        st.session_state.phone = ""
    if 'verified' not in st.session_state:
        st.session_state.verified = False
    if 'paid' not in st.session_state:
        st.session_state.paid = False
    if 'usage_count' not in st.session_state:
        st.session_state.usage_count = 0
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">💬 EMOTICONN AI</h1>
        <h2 class="hero-subtitle">Giao Tiếp Cảm Xúc - Tinh Tế Trong Từng Lời Nói</h2>
        <p style="font-size: 1.1rem; opacity: 0.8;">Dành cho người trưởng thành muốn giao tiếp chân thành, lịch sự và đúng cảm xúc</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Navigation
    st.markdown("---")
    
    # Phone Verification Section
    if not st.session_state.verified:
        st.markdown("""
        <div class="custom-card">
            <h3>🔐 Bắt Đầu Dùng Thử Miễn Phí</h3>
            <p>Nhập số điện thoại để nhận <b>3 tin nhắn AI miễn phí</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        phone_input = st.text_input(
            "**Số điện thoại của bạn:**",
            placeholder="0912345678",
            key="phone_input",
            help="Nhập số điện thoại Việt Nam (10-11 số)"
        )
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            verify_btn = st.button("✅ Xác Nhận & Bắt Đầu", type="primary", use_container_width=True)
        
        if verify_btn:
            if phone_input:
                valid_phone = validate_phone_number(phone_input)
                if valid_phone:
                    st.session_state.phone = valid_phone
                    st.session_state.verified = True
                    
                    # Check if user is paid
                    paid_users = load_paid_users()
                    if valid_phone in paid_users:
                        st.session_state.paid = True
                    
                    # Get current usage
                    st.session_state.usage_count = get_user_usage(valid_phone)
                    
                    st.markdown("""
                    <div class="success-box">
                        <h4>✅ Xác thực thành công!</h4>
                        <p>Số điện thoại: <b>{}</b></p>
                        <p>Bạn có <b>{}/3</b> lượt dùng thử miễn phí</p>
                    </div>
                    """.format(valid_phone, FREE_TRIAL_LIMIT - st.session_state.usage_count), unsafe_allow_html=True)
                    
                    # Auto refresh
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("⚠️ Số điện thoại không hợp lệ. Vui lòng nhập số Việt Nam (ví dụ: 0912345678)")
            else:
                st.warning("⚠️ Vui lòng nhập số điện thoại")
        
        # Features preview
        st.markdown("""
        <div class="custom-card">
            <h4>✨ Tính năng nổi bật:</h4>
            <ul>
            <li>💌 <b>3 tin nhắn miễn phí</b> đầy đủ tính năng</li>
            <li>🎯 <b>5 tình huống</b> giao tiếp thực tế</li>
            <li>👥 <b>Cá nhân hóa</b> theo giới tính</li>
            <li>💝 <b>Ngôn từ tinh tế</b>, lịch sự, chân thành</li>
            <li>🔓 <b>Mở khóa vĩnh viễn</b> chỉ 199.000đ</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        return
    
    # Main Application - User is verified
    st.markdown("""
    <div class="custom-card">
        <h3>🎯 Tạo Tin Nhắn Tinh Tế</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Show usage status
    if not st.session_state.paid:
        remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
        
        if remaining <= 0:
            st.markdown("""
            <div class="warning-box">
                <h4>⚠️ Bạn đã dùng hết lượt miễn phí</h4>
                <p>Nâng cấp ngay để tiếp tục sử dụng không giới hạn!</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show payment section
            show_payment_section()
            
            # Option to try with another phone
            if st.button("📱 Thử với số điện thoại khác"):
                st.session_state.phone = ""
                st.session_state.verified = False
                st.session_state.paid = False
                st.rerun()
            
            return
        
        # Show progress bar
        st.info(f"**Bạn còn {remaining}/{FREE_TRIAL_LIMIT} lượt dùng thử miễn phí**")
        st.progress(st.session_state.usage_count / FREE_TRIAL_LIMIT)
    
    # User Input Section
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.radio(
            "**Giới tính của bạn:**",
            ["Nam", "Nữ"],
            horizontal=True,
            key="gender"
        )
    
    with col2:
        situation = st.selectbox(
            "**Tình huống giao tiếp:**",
            ["Mới quen", "Đang tìm hiểu", "Yêu lâu năm", "Vợ/chồng", "Nhắn tin làm hoà"],
            key="situation"
        )
    
    # Message input
    user_input = st.text_area(
        "**Nội dung bạn muốn nhắn (hoặc để trống để AI gợi ý):**",
        placeholder="Ví dụ: Hôm nay mình có chuyện muốn chia sẻ...\nMình vừa xem bộ phim rất hay...\nNhớ đến bạn và muốn hỏi thăm...",
        height=120,
        key="user_input",
        help="Càng chi tiết, AI càng tạo tin nhắn phù hợp"
    )
    
    # Generate button
    generate_btn = st.button(
        f"✨ Tạo Tin Nhắn Tinh Tế",
        type="primary",
        use_container_width=True,
        key="generate"
    )
    
    # Result Section
    if generate_btn:
        if not st.session_state.paid:
            # Update usage count
            st.session_state.usage_count += 1
            update_usage(st.session_state.phone)
            remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
        
        # Generate message
        generator = MessageGenerator()
        
        with st.spinner("🔄 AI đang sáng tạo tin nhắn tinh tế cho bạn..."):
            time.sleep(0.8)  # Simulate processing
            result = generator.generate(gender, situation, user_input)
        
        # Display result
        st.markdown(f"""
        <div class="result-card">
            <h4>💌 Tin nhắn gợi ý:</h4>
            <p style="font-size: 1.2rem; line-height: 1.8;">{result}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Copy button
        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption("📋 Click nút bên cạnh để copy tin nhắn")
        with col2:
            if st.button("📋 Copy", use_container_width=True):
                st.success("✅ Đã copy tin nhắn vào clipboard!")
        
        # Usage reminder
        if not st.session_state.paid:
            st.markdown(f"""
            <div class="custom-card">
                <p>🎯 <b>Bạn còn {remaining}/{FREE_TRIAL_LIMIT} lượt dùng thử</b></p>
                {f'<p style="color: #e74c3c;">⚠️ Chỉ còn <b>{remaining}</b> lượt miễn phí cuối cùng!</p>' if remaining <= 1 else ''}
            </div>
            """, unsafe_allow_html=True)
            
            # Upgrade prompt
            if remaining <= 2:
                st.markdown("---")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown("💎 **Mở khóa vĩnh viễn để không giới hạn tin nhắn tinh tế**")
                with col2:
                    if st.button("💳 Nâng Cấp Ngay", use_container_width=True):
                        show_payment_section()

def show_payment_section():
    st.markdown("""
    <div class="payment-card">
        <h2 style="color: white;">🔓 MỞ KHÓA VĨNH VIỄN</h2>
        <p style="font-size: 1.2rem;">Chỉ thanh toán một lần - Dùng trọn đời</p>
        <h1 style="color: #FFD700; font-size: 2.5rem;">199.000đ</h1>
        <p style="font-size: 0.9rem; opacity: 0.9;">(Chưa đầy 1 bữa cafe mỗi tháng)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-card">
        <h3>💳 Hướng Dẫn Thanh Toán</h3>
        
        **1. Chuyển khoản qua ngân hàng:**
        
        ```bash
        Ngân hàng: BIDV
        Số tài khoản: 4430269669
        Chủ tài khoản: NGUYEN XUAN DAT
        Số tiền: 199.000 VND
        Nội dung chuyển khoản: AI [SỐ ĐIỆN THOẠI CỦA BẠN]
        ```
        
        **📌 Ví dụ:** 
        - Số điện thoại của bạn: **0912345678**
        - Nội dung chuyển khoản: **AI 0912345678**
        
        **2. Xác nhận thanh toán:**
        
        Sau khi chuyển khoản, nhập số điện thoại của bạn vào ô bên dưới để mở khóa ngay lập tức.
    </div>
    """, unsafe_allow_html=True)
    
    # Verification
    st.markdown("### ✅ Xác Nhận Thanh Toán")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        verification_input = st.text_input(
            "Nhập số điện thoại của bạn để xác nhận:",
            placeholder="0912345678",
            key="verify_payment"
        )
    
    with col2:
        verify_btn = st.button("🔓 Mở Khóa Ngay", type="primary", use_container_width=True)
    
    if verify_btn:
        if verification_input:
            valid_phone = validate_phone_number(verification_input)
            
            if valid_phone and valid_phone == st.session_state.phone:
                # Save as paid user
                save_paid_user(valid_phone)
                st.session_state.paid = True
                
                # Celebration
                st.balloons()
                st.markdown("""
                <div class="success-box">
                    <h3>🎉 Chúc mừng!</h3>
                    <p><b>Bạn đã mở khóa EMOTICONN AI thành công!</b></p>
                    <p>Từ giờ bạn có thể tạo tin nhắn không giới hạn.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Auto refresh after 3 seconds
                time.sleep(3)
                st.rerun()
            else:
                st.error("⚠️ Số điện thoại không khớp. Vui lòng nhập đúng số bạn đã dùng đăng ký.")
        else:
            st.warning("⚠️ Vui lòng nhập số điện thoại để xác nhận")
    
    # Support contact
    st.markdown("""
    <div class="custom-card">
        <h4>🆘 Cần hỗ trợ?</h4>
        <ul>
        <li>📧 Email: <code>support@emoticonn.ai</code></li>
        <li>📱 Zalo: <code>090-xxx-xxxx</code></li>
        <li>⏰ Thời gian hỗ trợ: 8:00 - 22:00 hàng ngày</li>
        </ul>
        <p><i>Chúng tôi sẽ phản hồi trong vòng 30 phút</i></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
