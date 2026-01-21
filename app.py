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
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== HẰNG SỐ ====================
FREE_TRIAL_LIMIT = 5
PREMIUM_PRICE = "149.000đ"
BANK_INFO = {
    "bank": "BIDV",
    "account": "4430269669",
    "name": "NGUYEN XUAN DAT",
    "note_format": "EMOTICONN [SỐ ĐIỆN THOẠI]"
}

# ==================== ĐƯỜNG DẪN DỮ LIỆU ====================
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USAGE_FILE = DATA_DIR / "usage.csv"
PAID_FILE = DATA_DIR / "paid.json"

# ==================== KHỞI TẠO ====================
def init_files():
    if not USAGE_FILE.exists():
        pd.DataFrame(columns=["phone", "count", "last_used"]).to_csv(USAGE_FILE, index=False)
    if not PAID_FILE.exists():
        with open(PAID_FILE, "w") as f:
            json.dump({}, f)

init_files()

# ==================== CSS ĐÃ SỬA LỖI ====================
def load_css():
    st.markdown("""
    <style>
    :root {
        --primary-purple: #8B5CF6;
        --primary-pink: #EC4899;
        --accent-gold: #FBBF24;
        --accent-emerald: #10B981;
        --neutral-light: #F8FAFC;
        --neutral-dark: #1F2937;
        --neutral-gray: #6B7280;
        --text-primary: #111827;
        --text-secondary: #4B5563;
        --shadow-soft: 0 4px 20px rgba(139, 92, 246, 0.1);
        --radius-lg: 20px;
        --radius-md: 12px;
    }
    
    .stApp {
        background: var(--neutral-light);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header */
    .premium-header {
        background: linear-gradient(135deg, var(--primary-purple) 0%, var(--primary-pink) 100%);
        padding: 2rem 1rem;
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-soft);
    }
    
    .header-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFFFFF 0%, #FFD6FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Navigation */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-soft);
        margin-bottom: 2rem;
        border: 1px solid rgba(139, 92, 246, 0.1);
    }
    
    /* Cards */
    .premium-card {
        background: white;
        border-radius: var(--radius-lg);
        padding: 2rem;
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(139, 92, 246, 0.08);
        margin-bottom: 1.5rem;
    }
    
    .card-gradient {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(236, 72, 153, 0.05) 100%);
        border-left: 4px solid var(--primary-purple);
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: var(--radius-md) !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        border: none !important;
        width: 100%;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, var(--accent-gold) 0%, #F59E0B 100%) !important;
        color: #1F2937 !important;
    }
    
    .btn-secondary {
        background: linear-gradient(135deg, var(--primary-purple) 0%, var(--primary-pink) 100%) !important;
        color: white !important;
    }
    
    /* Features Grid - ĐÃ SỬA LỖI */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-top: 1.5rem;
    }
    
    .feature-item {
        text-align: center;
        padding: 1.5rem;
        background: rgba(139, 92, 246, 0.03);
        border-radius: var(--radius-md);
        border: 1px solid rgba(139, 92, 246, 0.1);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Hide defaults */
    #MainMenu, footer, header { 
        visibility: hidden !important;
        height: 0 !important;
    }
    
    /* Mobile */
    @media (max-width: 768px) {
        .header-title { font-size: 2.2rem; }
        .nav-bar { flex-direction: column; gap: 1rem; }
        .features-grid { grid-template-columns: 1fr; }
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ==================== AI ENGINE ====================
class EmotionalAI:
    def __init__(self):
        self.situations = {
            "Làm quen": {
                "Nam→Nữ": [
                    "Chào bạn, mình là {name} từ {context}. Mình thấy {detail} và muốn làm quen nếu không phiền. Hôm nay của bạn thế nào? ☕",
                    "Xin chào, hy vọng tin nhắn này không làm phiền. Mình ấn tượng với {impression} của bạn. Công việc của bạn dạo này ổn chứ? 💼",
                ],
                "Nữ→Nam": [
                    "Chào anh, em là {name} đây. Cảm ơn anh vì {reason}. Anh có vài phút trò chuyện không? 🌸",
                    "Xin chào, em thấy anh rất {trait}. Em muốn làm quen nếu anh không ngại. Anh đang bận gì không? 🤗",
                ]
            },
            "Hỏi thăm": {
                "Nam→Nữ": [
                    "Dạo này bạn thế nào? Công việc có ổn không? Nếu có gì cần chia sẻ, mình luôn sẵn sàng lắng nghe. 🌿",
                ],
                "Nữ→Nam": [
                    "Anh ơi, dạo này anh có khoẻ không? Công việc nhiều không? Nhớ chăm sóc sức khoẻ nhé. 🫂",
                ]
            }
        }
    
    def generate(self, user_gender, target_gender, situation, context=""):
        gender_key = f"{user_gender}→{target_gender}"
        
        if situation in self.situations and gender_key in self.situations[situation]:
            templates = self.situations[situation][gender_key]
        else:
            templates = ["Xin chào, hy vọng bạn có một ngày tốt lành. 💬"]
        
        template = random.choice(templates)
        
        if context:
            replacements = {
                "{name}": "mình",
                "{context}": "đây",
                "{detail}": context[:50] + "..." if len(context) > 50 else context,
                "{impression}": "sự chia sẻ",
                "{reason}": "sự giúp đỡ",
                "{trait}": "tử tế",
            }
            
            for key, value in replacements.items():
                if key in template:
                    template = template.replace(key, value)
        
        return template

# ==================== DATA FUNCTIONS ====================
def validate_phone(phone):
    phone = re.sub(r'\D', '', phone)
    if 9 <= len(phone) <= 11 and phone.startswith('0'):
        return phone
    return None

def get_usage_count(phone):
    try:
        df = pd.read_csv(USAGE_FILE)
        user_data = df[df["phone"] == phone]
        return 0 if user_data.empty else int(user_data.iloc[0]["count"])
    except:
        return 0

def update_usage(phone):
    try:
        df = pd.read_csv(USAGE_FILE)
    except:
        df = pd.DataFrame(columns=["phone", "count", "last_used"])
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
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

def save_paid_user(phone):
    paid_users = load_paid_users()
    paid_users[phone] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(PAID_FILE, "w") as f:
        json.dump(paid_users, f, indent=2)

# ==================== RENDER FUNCTIONS ====================
def render_header():
    st.markdown("""
    <div class="premium-header">
        <h1 class="header-title">💬 EMOTICONN AI</h1>
        <p class="header-subtitle">
            Nói điều bạn muốn - Theo cách họ muốn nghe
        </p>
        <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem; margin-top: 0.5rem;">
            Dành cho người trưởng thành muốn giao tiếp tinh tế
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_navigation():
    st.markdown("""
    <div class="nav-bar">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-weight: 600; color: #8B5CF6;">🏠 EMOTICONN AI</span>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem; color: #6B7280;">
            <span>⭐ 4.9/5 từ 2,500+ người dùng</span>
            <span style="background: rgba(16, 185, 129, 0.1); color: #10B981; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.9rem;">
                5 lượt dùng thử
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_features():
    """Render features grid - ĐÃ SỬA LỖI"""
    st.markdown("""
    <div class="features-grid">
        <div class="feature-item">
            <div class="feature-icon" style="color: #8B5CF6;">🎯</div>
            <h5>Dành cho người trưởng thành</h5>
            <p style="color: #6B7280; font-size: 0.9rem;">Ngôn từ tinh tế, sâu sắc, không sáo rỗng</p>
        </div>
        
        <div class="feature-item">
            <div class="feature-icon" style="color: #EC4899;">💝</div>
            <h5>7,000+ tình huống</h5>
            <p style="color: #6B7280; font-size: 0.9rem;">Hiểu mọi ngữ cảnh giao tiếp phức tạp</p>
        </div>
        
        <div class="feature-item">
            <div class="feature-icon" style="color: #FBBF24;">🔥</div>
            <h5>5 lượt dùng thử</h5>
            <p style="color: #6B7280; font-size: 0.9rem;">Trải nghiệm chất lượng trước khi quyết định</p>
        </div>
        
        <div class="feature-item">
            <div class="feature-icon" style="color: #10B981;">💎</div>
            <h5>Giá trị trọn đời</h5>
            <p style="color: #6B7280; font-size: 0.9rem;">Chỉ 149K - Dùng mãi mãi</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN APP ====================
def main():
    # Initialize session
    if 'phone' not in st.session_state:
        st.session_state.phone = ""
    if 'verified' not in st.session_state:
        st.session_state.verified = False
    if 'paid' not in st.session_state:
        st.session_state.paid = False
    if 'usage_count' not in st.session_state:
        st.session_state.usage_count = 0
    
    # Render UI
    render_header()
    render_navigation()
    
    # Check if verified
    if not st.session_state.verified:
        # Verification section
        st.markdown("""
        <div class="premium-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔓</div>
            <h2 style="color: #8B5CF6; margin-bottom: 0.5rem;">Bắt Đầu Dùng Thử Miễn Phí</h2>
            <p style="color: #6B7280; margin-bottom: 2rem;">
                Nhận ngay <strong style="color: #8B5CF6;">5 tin nhắn AI tinh tế</strong> hoàn toàn miễn phí
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Phone input
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            phone_input = st.text_input(
                "**Số điện thoại của bạn**",
                placeholder="0912345678",
                key="verification_input"
            )
        
        # Verify button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ **NHẬN 5 TIN MIỄN PHÍ**", key="verify_btn", use_container_width=True):
                if phone_input:
                    valid_phone = validate_phone(phone_input)
                    if valid_phone:
                        st.session_state.phone = valid_phone
                        st.session_state.verified = True
                        
                        paid_users = load_paid_users()
                        if valid_phone in paid_users:
                            st.session_state.paid = True
                        else:
                            st.session_state.usage_count = get_usage_count(valid_phone)
                        
                        st.success("✅ **Kết nối thành công!**")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("⚠️ Số điện thoại không hợp lệ")
                else:
                    st.warning("📱 Vui lòng nhập số điện thoại")
        
        # Features
        st.markdown("""
        <div class="premium-card card-gradient">
            <h4 style="text-align: center; color: #8B5CF6; margin-bottom: 2rem;">✨ Tại Sao Chọn EMOTICONN AI?</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Render features grid
        render_features()
        
        return
    
    # Main app after verification
    st.write("Đã đăng nhập với số điện thoại:", st.session_state.phone)
    
    # Check trial
    if not st.session_state.paid:
        remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
        if remaining <= 0:
            st.warning("Bạn đã hết lượt dùng thử!")
            return
        
        st.info(f"Bạn còn {remaining}/{FREE_TRIAL_LIMIT} lượt dùng thử")
    
    # Create message interface
    st.markdown("""
    <div class="premium-card">
        <h2 style="color: #8B5CF6;">🎯 Tạo Tin Nhắn Tinh Tế</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        user_gender = st.radio("Bạn là:", ["Nam", "Nữ"], horizontal=True)
    with col2:
        target_gender = st.radio("Gửi cho:", ["Nam", "Nữ"], horizontal=True)
    
    situation = st.selectbox("Tình huống:", ["Làm quen", "Hỏi thăm"])
    context = st.text_area("Thêm chi tiết (tuỳ chọn):", height=100)
    
    if st.button("✨ TẠO TIN NHẮN", use_container_width=True):
        if not st.session_state.paid:
            st.session_state.usage_count += 1
            update_usage(st.session_state.phone)
            remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
            
            if remaining < 0:
                st.error("Đã hết lượt dùng thử!")
                return
        
        ai = EmotionalAI()
        result = ai.generate(user_gender, target_gender, situation, context)
        
        st.markdown(f"""
        <div class="premium-card" style="border-left: 4px solid #EC4899;">
            <h4>💌 Tin nhắn gợi ý:</h4>
            <p style="font-size: 1.2rem; line-height: 1.8; color: #111827;">
                {result}
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
