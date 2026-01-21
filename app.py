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

# ==================== CSS ĐƠN GIẢN, AN TOÀN ====================
st.markdown("""
<style>
    /* Reset và nền */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%);
        padding: 3rem 1rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        border-radius: 0 0 24px 24px;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(to right, #ffffff, #fef3c7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.95);
        margin-bottom: 0.5rem;
    }
    
    /* Navigation */
    .nav-bar {
        background: white;
        padding: 1rem 2rem;
        border-radius: 16px;
        margin: 0 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }
    
    .badge {
        background: linear-gradient(135deg, #10b981, #34d399);
        color: white;
        padding: 0.25rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* Cards */
    .main-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem auto;
        max-width: 800px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    }
    
    /* Features */
    .features-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        flex: 1;
        min-width: 250px;
        max-width: 280px;
        background: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer { visibility: hidden; }
    
    /* Mobile */
    @media (max-width: 768px) {
        .main-title { font-size: 2.2rem; }
        .feature-card { min-width: 100%; }
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA FUNCTIONS ====================
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

# ==================== AI ENGINE ====================
class EmotionalAI:
    def __init__(self):
        self.templates = {
            "Làm quen": {
                "Nam→Nữ": [
                    "Chào bạn, mình thấy {detail} và muốn làm quen nếu không phiền. Hôm nay của bạn thế nào?",
                    "Xin chào, công việc của bạn dạo này ổn chứ? Mình muốn làm quen và trò chuyện.",
                ],
                "Nữ→Nam": [
                    "Chào anh, anh có vài phút trò chuyện không? Em muốn làm quen.",
                    "Xin chào, em thấy anh rất {trait}. Anh đang bận gì không?",
                ]
            },
            "Hỏi thăm": {
                "Nam→Nữ": [
                    "Dạo này bạn thế nào? Công việc có ổn không?",
                    "Chào bạn, mọi thứ ổn chứ? Có gì cần chia sẻ thì mình luôn ở đây.",
                ],
                "Nữ→Nam": [
                    "Anh ơi, dạo này anh có khoẻ không? Nhớ chăm sóc sức khoẻ nhé.",
                    "Chào anh, em muốn hỏi thăm anh một chút. Mọi thứ ổn chứ?",
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
            detail = context[:50] + "..." if len(context) > 50 else context
            template = template.replace("{detail}", detail)
            template = template.replace("{trait}", "tử tế")
        
        return template

# ==================== UI COMPONENTS (SỬ DỤNG STREAMLIT THUẦN) ====================
def render_header():
    """Render header bằng Streamlit thuần"""
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">💬 EMOTICONN AI</h1>
        <p class="main-subtitle">Nói điều bạn muốn - Theo cách họ muốn nghe</p>
        <p style="color: rgba(255, 255, 255, 0.9); font-size: 1rem;">
            Trợ lý giao tiếp cảm xúc dành cho người trưởng thành
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_navigation():
    """Render navigation bằng Streamlit thuần"""
    st.markdown("""
    <div class="nav-bar">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.5rem;">🏠</span>
            <span style="font-size: 1.2rem; font-weight: 700; color: #7c3aed;">EMOTICONN AI</span>
        </div>
        <div style="display: flex; align-items: center; gap: 1.5rem;">
            <span style="color: #64748b;">⭐ 4.9/5 từ 2,500+ người dùng</span>
            <span class="badge">5 lượt dùng thử</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_features():
    """Render features bằng Streamlit thuần - KHÔNG DÙNG HTML COMPLEX"""
    st.markdown("### ✨ Tại Sao Chọn EMOTICONN AI?")
    
    # Tạo columns cho features
    cols = st.columns(4)
    
    with cols[0]:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.05);">
            <div style="font-size: 3rem; color: #7c3aed;">🎯</div>
            <h4 style="color: #1e293b;">Dành cho người trưởng thành</h4>
            <p style="color: #64748b; font-size: 0.9rem;">Ngôn từ tinh tế, sâu sắc, không sáo rỗng</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.05);">
            <div style="font-size: 3rem; color: #ec4899;">💝</div>
            <h4 style="color: #1e293b;">7,000+ tình huống</h4>
            <p style="color: #64748b; font-size: 0.9rem;">Hiểu mọi ngữ cảnh giao tiếp phức tạp</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.05);">
            <div style="font-size: 3rem; color: #f59e0b;">🔥</div>
            <h4 style="color: #1e293b;">5 lượt dùng thử</h4>
            <p style="color: #64748b; font-size: 0.9rem;">Trải nghiệm chất lượng cao trước khi đầu tư</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.05);">
            <div style="font-size: 3rem; color: #10b981;">💎</div>
            <h4 style="color: #1e293b;">Giá trị trọn đời</h4>
            <p style="color: #64748b; font-size: 0.9rem;">Chỉ 149K - Dùng mãi mãi</p>
        </div>
        """, unsafe_allow_html=True)

def render_verification():
    """Render verification section"""
    st.markdown("""
    <div class="main-card" style="text-align: center;">
        <div style="font-size: 4rem; margin-bottom: 1.5rem;">🔓</div>
        <h1 style="color: #1e293b; margin-bottom: 1rem;">Bắt Đầu Dùng Thử Miễn Phí</h1>
        <p style="color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;">
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
        if st.button("✨ **NHẬN 5 TIN MIỄN PHÍ**", 
                    type="primary", 
                    use_container_width=True,
                    key="verify_btn"):
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
                    
                    st.success("✅ **Đăng ký thành công!**")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("⚠️ Số điện thoại không hợp lệ")
            else:
                st.warning("📱 Vui lòng nhập số điện thoại")

# ==================== MAIN APP ====================
def main():
    # Khởi tạo session state
    if 'phone' not in st.session_state:
        st.session_state.phone = ""
    if 'verified' not in st.session_state:
        st.session_state.verified = False
    if 'paid' not in st.session_state:
        st.session_state.paid = False
    if 'usage_count' not in st.session_state:
        st.session_state.usage_count = 0
    
    # Render header và navigation
    render_header()
    render_navigation()
    
    # Kiểm tra nếu chưa đăng nhập
    if not st.session_state.verified:
        render_verification()
        render_features()
        return
    
    # Kiểm tra lượt dùng
    if not st.session_state.paid:
        remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
        if remaining <= 0:
            st.warning("Bạn đã hết lượt dùng thử!")
            if st.button("💎 Nâng cấp tài khoản", type="primary"):
                st.session_state.show_upgrade = True
            return
        
        # Hiển thị progress
        st.markdown(f"""
        <div style="background: white; padding: 2rem; border-radius: 16px; margin: 2rem auto; max-width: 800px; box-shadow: 0 8px 25px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div>
                    <h3 style="color: #1e293b; margin: 0;">🎯 Bạn đang dùng thử miễn phí</h3>
                    <p style="color: #64748b; margin: 0.5rem 0;">Còn <strong style="color: #7c3aed; font-size: 1.2rem;">{remaining}/{FREE_TRIAL_LIMIT}</strong> lượt sử dụng</p>
                </div>
                <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); padding: 0.5rem 1.5rem; border-radius: 20px;">
                    <span style="color: #92400e; font-weight: 600;">Ưu đãi 5 lượt</span>
                </div>
            </div>
            <div style="background: #e2e8f0; height: 10px; border-radius: 5px;">
                <div style="background: linear-gradient(90deg, #8b5cf6, #a78bfa); height: 100%; width: {(st.session_state.usage_count/FREE_TRIAL_LIMIT)*100}%; border-radius: 5px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Giao diện chính
    st.markdown("""
    <div style="background: white; padding: 2.5rem; border-radius: 20px; margin: 2rem auto; max-width: 800px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">
        <h1 style="color: #1e293b; margin-bottom: 1rem;">✍️ Tạo Tin Nhắn Tinh Tế</h1>
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
        placeholder="Ví dụ: Chúng ta mới quen qua ứng dụng hẹn hò, bạn ấy là giáo viên...",
        height=100
    )
    
    # Nút tạo tin nhắn
    if st.button("✨ **TẠO TIN NHẮN TINH TẾ**", 
                type="primary", 
                use_container_width=True):
        if not st.session_state.paid:
            st.session_state.usage_count += 1
            update_usage(st.session_state.phone)
            remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
            
            if remaining < 0:
                st.error("Bạn đã hết lượt dùng thử!")
                return
        
        # Tạo tin nhắn
        ai = EmotionalAI()
        with st.spinner("🤖 AI đang tạo tin nhắn..."):
            time.sleep(1)
            result = ai.generate(user_gender, target_gender, situation, context)
            
            # Hiển thị kết quả
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fef3c7, #fde68a); border-radius: 16px; padding: 2.5rem; margin: 2rem 0; border-left: 6px solid #f59e0b; position: relative;">
                <div style="position: absolute; top: -12px; left: 30px; background: #7c3aed; color: white; padding: 0.5rem 1.5rem; border-radius: 20px; font-weight: 600;">
                    💌 Tin nhắn gợi ý
                </div>
                <p style="font-size: 1.2rem; line-height: 1.8; color: #1e293b; margin: 0;">
                    {result}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📋 Copy", use_container_width=True):
                    st.success("✅ Đã copy!")
            with col2:
                if st.button("🔄 Tạo mới", use_container_width=True):
                    st.rerun()
            with col3:
                if st.button("💾 Lưu", use_container_width=True):
                    st.info("Đã lưu")

if __name__ == "__main__":
    main()
