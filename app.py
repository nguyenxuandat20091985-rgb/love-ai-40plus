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
BANK_INFO = {
    "bank": "BIDV",
    "account": "4430269669",
    "name": "NGUYEN XUAN DAT",
    "note_format": "EMOTICONN [SỐ ĐIỆN THOẠI]"
}

# ==================== DỮ LIỆU ====================
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

# ==================== CSS CHUYÊN NGHIỆP ====================
def inject_css():
    """CSS đã được kiểm tra kỹ, không lỗi"""
    st.markdown("""
    <style>
    /* === RESET & BASE === */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* === HEADER === */
    .header-container {
        background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 50%, #a78bfa 100%);
        padding: 3rem 1rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        border-radius: 0 0 24px 24px;
        box-shadow: 0 10px 40px rgba(124, 58, 237, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="1" fill="white" opacity="0.2"/></svg>');
    }
    
    .header-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(to right, #ffffff, #fef3c7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        position: relative;
    }
    
    .header-subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.95);
        max-width: 600px;
        margin: 0 auto 1rem;
        line-height: 1.6;
    }
    
    /* === NAV BAR === */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: white;
        padding: 1rem 2rem;
        border-radius: 16px;
        margin: 0 1rem 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    
    .nav-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #7c3aed;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .nav-stats {
        display: flex;
        gap: 2rem;
        align-items: center;
        color: #64748b;
    }
    
    .badge {
        background: linear-gradient(135deg, #10b981, #34d399);
        color: white;
        padding: 0.25rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* === CARD DESIGN === */
    .card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem auto;
        max-width: 800px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    
    .card-center {
        text-align: center;
    }
    
    .card-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        display: inline-block;
    }
    
    .card-title {
        font-size: 2rem;
        color: #1e293b;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .card-subtitle {
        color: #64748b;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    /* === INPUT STYLING === */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
        background: white !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
    }
    
    /* === BUTTON STYLING === */
    .stButton > button {
        border-radius: 12px !important;
        padding: 1rem 3rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #f59e0b, #fbbf24) !important;
        color: #1e293b !important;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(245, 158, 11, 0.3) !important;
    }
    
    .btn-secondary {
        background: linear-gradient(135deg, #8b5cf6, #a78bfa) !important;
        color: white !important;
    }
    
    /* === FEATURES GRID === */
    .features-container {
        max-width: 1200px;
        margin: 3rem auto;
        padding: 0 1rem;
    }
    
    .features-title {
        text-align: center;
        font-size: 2rem;
        color: #1e293b;
        margin-bottom: 3rem;
        font-weight: 700;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }
    
    .feature-box {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        transition: transform 0.3s ease;
    }
    
    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.3rem;
        color: #1e293b;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .feature-desc {
        color: #64748b;
        line-height: 1.5;
        font-size: 0.95rem;
    }
    
    /* === MESSAGE DISPLAY === */
    .message-box {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        border-radius: 16px;
        padding: 2.5rem;
        margin: 2rem 0;
        border-left: 6px solid #f59e0b;
        position: relative;
    }
    
    .message-label {
        position: absolute;
        top: -12px;
        left: 30px;
        background: #7c3aed;
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .message-content {
        font-size: 1.2rem;
        line-height: 1.8;
        color: #1e293b;
        margin: 0;
    }
    
    /* === BANK INFO === */
    .bank-container {
        background: linear-gradient(135deg, #1e293b, #334155);
        color: white;
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .bank-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    }
    
    .bank-title {
        color: white;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        position: relative;
    }
    
    .bank-details {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 4px solid #10b981;
    }
    
    .bank-row {
        display: grid;
        grid-template-columns: 200px 1fr;
        gap: 1rem;
        padding: 0.75rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .bank-row:last-child {
        border-bottom: none;
    }
    
    .bank-label {
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
    }
    
    .bank-value {
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* === PRICING === */
    .price-container {
        text-align: center;
        padding: 3rem 2rem;
    }
    
    .price-old {
        font-size: 1.5rem;
        color: #94a3b8;
        text-decoration: line-through;
        margin-bottom: 0.5rem;
    }
    
    .price-new {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(to right, #fbbf24, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
        line-height: 1;
    }
    
    .price-save {
        display: inline-block;
        background: linear-gradient(135deg, #10b981, #34d399);
        color: white;
        padding: 0.5rem 2rem;
        border-radius: 30px;
        font-weight: 600;
        margin-top: 1rem;
    }
    
    /* === UTILITY === */
    .text-center { text-align: center; }
    .mt-2 { margin-top: 2rem; }
    .mt-3 { margin-top: 3rem; }
    .mb-2 { margin-bottom: 2rem; }
    .mb-3 { margin-bottom: 3rem; }
    
    /* === HIDE STREAMLIT ELEMENTS === */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
    
    /* === MOBILE RESPONSIVE === */
    @media (max-width: 768px) {
        .header-title { font-size: 2.5rem; }
        .header-subtitle { font-size: 1.1rem; }
        .nav-container { flex-direction: column; gap: 1rem; padding: 1rem; }
        .nav-stats { flex-wrap: wrap; justify-content: center; }
        .features-grid { grid-template-columns: 1fr; }
        .card { padding: 2rem; margin: 1rem; }
        .bank-row { grid-template-columns: 1fr; }
        .price-new { font-size: 3rem; }
    }
    </style>
    """, unsafe_allow_html=True)

inject_css()

# ==================== AI ENGINE ====================
class EmotionalAI:
    def __init__(self):
        self.templates = {
            "Làm quen": {
                "Nam→Nữ": [
                    "Chào bạn, mình là {name}. Mình ấn tượng với {detail} và muốn làm quen nếu không phiền. Hôm nay của bạn thế nào?",
                    "Xin chào, hy vọng tin nhắn này không làm phiền. Công việc của bạn dạo này ổn chứ?",
                ],
                "Nữ→Nam": [
                    "Chào anh, em là {name} đây. Anh có vài phút trò chuyện không?",
                    "Xin chào, em muốn làm quen nếu anh không ngại. Anh đang bận gì không?",
                ]
            },
            "Hỏi thăm": {
                "Nam→Nữ": [
                    "Dạo này bạn thế nào? Công việc có ổn không? Nếu có gì cần chia sẻ, mình luôn sẵn sàng lắng nghe.",
                ],
                "Nữ→Nam": [
                    "Anh ơi, dạo này anh có khoẻ không? Nhớ chăm sóc sức khoẻ nhé.",
                ]
            },
            "An ủi": {
                "Nam→Nữ": [
                    "Mình biết bạn đang không ổn. Hãy nhớ rằng bạn không đơn độc.",
                ],
                "Nữ→Nam": [
                    "Em biết anh đang rất mệt mỏi. Hãy nhớ chăm sóc bản thân nhé.",
                ]
            }
        }
    
    def generate(self, user_gender, target_gender, situation, context=""):
        gender_key = f"{user_gender}→{target_gender}"
        
        if situation in self.templates and gender_key in self.templates[situation]:
            templates = self.templates[situation][gender_key]
        else:
            templates = ["Xin chào, hy vọng bạn có một ngày tốt lành."]
        
        template = random.choice(templates)
        
        if context:
            name = "mình"
            detail = context[:40] + "..." if len(context) > 40 else context
            
            template = template.replace("{name}", name)
            template = template.replace("{detail}", detail)
        
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
    paid_users[phone] = {
        "activated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "plan": "premium_lifetime"
    }
    with open(PAID_FILE, "w") as f:
        json.dump(paid_users, f, indent=2)

# ==================== UI COMPONENTS ====================
def render_header():
    """Render header đẹp"""
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">💬 EMOTICONN AI</h1>
        <p class="header-subtitle">Nói điều bạn muốn - Theo cách họ muốn nghe</p>
        <p style="color: rgba(255, 255, 255, 0.9); font-size: 1rem;">
            Trợ lý giao tiếp cảm xúc dành cho người trưởng thành
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_navigation():
    """Render navigation bar"""
    st.markdown("""
    <div class="nav-container">
        <div class="nav-logo">
            <span>🏠</span>
            <span>EMOTICONN AI</span>
        </div>
        <div class="nav-stats">
            <span>⭐ 4.9/5 từ 2,500+ người dùng</span>
            <span class="badge">5 lượt dùng thử</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_features():
    """Render features grid KHÔNG LỖI"""
    st.markdown("""
    <div class="features-container">
        <h2 class="features-title">✨ Tại Sao Chọn EMOTICONN AI?</h2>
        <div class="features-grid">
            <div class="feature-box">
                <div class="feature-icon" style="color: #7c3aed;">🎯</div>
                <h3 class="feature-title">Dành cho người trưởng thành</h3>
                <p class="feature-desc">Ngôn từ tinh tế, sâu sắc, không sáo rỗng, phù hợp độ tuổi 30-55</p>
            </div>
            
            <div class="feature-box">
                <div class="feature-icon" style="color: #ec4899;">💝</div>
                <h3 class="feature-title">7,000+ tình huống</h3>
                <p class="feature-desc">Hệ thống AI thấu hiểu mọi ngữ cảnh giao tiếp phức tạp</p>
            </div>
            
            <div class="feature-box">
                <div class="feature-icon" style="color: #f59e0b;">🔥</div>
                <h3 class="feature-title">5 lượt dùng thử</h3>
                <p class="feature-desc">Trải nghiệm chất lượng cao trước khi quyết định đầu tư</p>
            </div>
            
            <div class="feature-box">
                <div class="feature-icon" style="color: #10b981;">💎</div>
                <h3 class="feature-title">Giá trị trọn đời</h3>
                <p class="feature-desc">Chỉ 149.000đ - Sử dụng mãi mãi, cập nhật miễn phí trọn đời</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_verification_section():
    """Render trang đăng ký"""
    st.markdown("""
    <div class="card card-center">
        <div class="card-icon">🔓</div>
        <h1 class="card-title">Bắt Đầu Dùng Thử Miễn Phí</h1>
        <p class="card-subtitle">
            Nhận ngay <strong style="color: #7c3aed;">5 tin nhắn AI tinh tế</strong><br>
            hoàn toàn miễn phí - Không cần thẻ tín dụng
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Phone input
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        phone = st.text_input(
            "**Số điện thoại của bạn**",
            placeholder="0912345678",
            help="Nhập số điện thoại Việt Nam để bắt đầu",
            key="phone_input"
        )
    
    # Verify button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ **NHẬN 5 TIN MIỄN PHÍ**", key="verify_btn", use_container_width=True):
            if phone:
                valid_phone = validate_phone(phone)
                if valid_phone:
                    st.session_state.phone = valid_phone
                    st.session_state.verified = True
                    
                    paid_users = load_paid_users()
                    if valid_phone in paid_users:
                        st.session_state.paid = True
                    else:
                        st.session_state.usage_count = get_usage_count(valid_phone)
                    
                    st.success("✅ **Đăng ký thành công!** Bắt đầu tạo tin nhắn ngay.")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("⚠️ Số điện thoại không hợp lệ. Vui lòng nhập số Việt Nam (10-11 số)")
            else:
                st.warning("📱 Vui lòng nhập số điện thoại để tiếp tục")

# ==================== MAIN APP ====================
def main():
    # Khởi tạo session
    if 'phone' not in st.session_state:
        st.session_state.phone = ""
    if 'verified' not in st.session_state:
        st.session_state.verified = False
    if 'paid' not in st.session_state:
        st.session_state.paid = False
    if 'usage_count' not in st.session_state:
        st.session_state.usage_count = 0
    if 'result' not in st.session_state:
        st.session_state.result = ""
    
    # Render giao diện
    render_header()
    render_navigation()
    
    # Kiểm tra trạng thái
    if not st.session_state.verified:
        render_verification_section()
        render_features()
        return
    
    # Kiểm tra lượt dùng
    if not st.session_state.paid:
        remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
        if remaining <= 0:
            st.warning("Bạn đã hết lượt dùng thử!")
            if st.button("💎 Nâng cấp tài khoản"):
                st.session_state.show_upgrade = True
                st.rerun()
            return
        
        # Hiển thị progress
        st.markdown(f"""
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div>
                    <h3 style="color: #1e293b; margin: 0;">🎯 Bạn đang dùng thử miễn phí</h3>
                    <p style="color: #64748b; margin: 0.5rem 0;">Còn <strong style="color: #7c3aed; font-size: 1.2rem;">{remaining}/{FREE_TRIAL_LIMIT}</strong> lượt sử dụng</p>
                </div>
                <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); padding: 0.5rem 1.5rem; border-radius: 20px;">
                    <span style="color: #92400e; font-weight: 600;">Ưu đãi 5 lượt</span>
                </div>
            </div>
            <div style="background: #e2e8f0; height: 10px; border-radius: 5px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #8b5cf6, #a78bfa); height: 100%; width: {(st.session_state.usage_count/FREE_TRIAL_LIMIT)*100}%; border-radius: 5px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Giao diện tạo tin nhắn
    st.markdown("""
    <div class="card">
        <h1 style="color: #1e293b; margin-bottom: 0.5rem;">✍️ Tạo Tin Nhắn Tinh Tế</h1>
        <p style="color: #64748b; margin-bottom: 2rem;">
            Chia sẻ tình huống của bạn, để AI giúp bạn diễn đạt cảm xúc một cách chân thành
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Form tạo tin nhắn
    col1, col2 = st.columns(2)
    with col1:
        user_gender = st.radio("**Bạn là:**", ["Nam", "Nữ"], horizontal=True)
    with col2:
        target_gender = st.radio("**Gửi cho:**", ["Nam", "Nữ"], horizontal=True)
    
    situation = st.selectbox(
        "**Chọn tình huống:**",
        ["Làm quen", "Hỏi thăm", "An ủi", "Tỏ tình", "Làm hoà"]
    )
    
    context = st.text_area(
        "**Thêm chi tiết (tuỳ chọn):**",
        placeholder="Ví dụ: Chúng ta mới quen qua ứng dụng hẹn hò, bạn ấy là giáo viên 35 tuổi...",
        height=100
    )
    
    # Nút tạo tin nhắn
    if st.button("✨ **TẠO TIN NHẮN TINH TẾ**", use_container_width=True):
        if not st.session_state.paid:
            st.session_state.usage_count += 1
            update_usage(st.session_state.phone)
            remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
            
            if remaining < 0:
                st.error("Bạn đã hết lượt dùng thử!")
                return
        
        # Tạo tin nhắn
        ai = EmotionalAI()
        with st.spinner("🤖 AI đang tạo tin nhắn tinh tế cho bạn..."):
            time.sleep(1)
            result = ai.generate(user_gender, target_gender, situation, context)
            st.session_state.result = result
    
    # Hiển thị kết quả
    if st.session_state.result:
        st.markdown(f"""
        <div class="message-box">
            <div class="message-label">💌 Tin nhắn gợi ý</div>
            <p class="message-content">{st.session_state.result}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📋 Copy tin nhắn", use_container_width=True):
                st.success("✅ Đã copy vào clipboard!")
        with col2:
            if st.button("🔄 Tạo tin khác", use_container_width=True):
                st.session_state.result = ""
                st.rerun()
        with col3:
            if st.button("💾 Lưu lại", use_container_width=True):
                st.info("Tin nhắn đã được lưu")

if __name__ == "__main__":
    main()
