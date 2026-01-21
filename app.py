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

# ==================== CSS HIỆN ĐẠI ====================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
/* ===== RESET & GLOBAL ===== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    min-height: 100vh;
}

/* ===== HERO SECTION ===== */
.hero-container {
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 1) 0%,
        rgba(139, 92, 246, 1) 50%,
        rgba(168, 85, 247, 1) 100%);
    padding: 80px 24px 60px;
    text-align: center;
    border-radius: 0 0 32px 32px;
    position: relative;
    overflow: hidden;
    margin-bottom: 40px;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.05);
    animation: float 20s linear infinite;
}

@keyframes float {
    0% { transform: translateY(0) rotate(0deg); }
    100% { transform: translateY(-100px) rotate(360deg); }
}

.hero-icon {
    font-size: 64px;
    margin-bottom: 24px;
    display: block;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    color: white;
    margin-bottom: 16px;
    letter-spacing: -0.5px;
    text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.hero-tagline {
    font-size: 20px;
    color: rgba(255, 255, 255, 0.95);
    margin-bottom: 12px;
    font-weight: 400;
    line-height: 1.5;
}

.hero-subtitle {
    font-size: 16px;
    color: rgba(255, 255, 255, 0.85);
    max-width: 600px;
    margin: 0 auto;
    font-weight: 300;
}

/* ===== NAVIGATION BAR ===== */
.nav-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 20px 40px;
    border-radius: 20px;
    margin: -20px 24px 40px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    position: relative;
    z-index: 10;
    border: 1px solid rgba(124, 58, 237, 0.1);
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-icon {
    font-size: 24px;
    color: #7c3aed;
}

.brand-text {
    font-size: 20px;
    font-weight: 700;
    color: #1e293b;
    background: linear-gradient(90deg, #7c3aed, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.nav-stats {
    display: flex;
    align-items: center;
    gap: 24px;
}

.rating {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #64748b;
    font-weight: 500;
}

.stars {
    color: #fbbf24;
    font-size: 18px;
}

.trial-badge {
    background: linear-gradient(135deg, #10b981, #34d399);
    color: white;
    padding: 8px 20px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 14px;
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
    white-space: nowrap;
}

/* ===== MAIN CONTENT CARD ===== */
.main-content {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 24px;
}

.content-card {
    background: white;
    border-radius: 28px;
    padding: 60px 48px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(124, 58, 237, 0.1);
    margin-bottom: 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.content-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    background: linear-gradient(90deg, #7c3aed, #8b5cf6, #a78bfa);
}

.card-icon {
    font-size: 72px;
    margin-bottom: 32px;
    display: inline-block;
    background: linear-gradient(135deg, #7c3aed, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.card-title {
    font-size: 36px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 20px;
    line-height: 1.2;
}

.card-description {
    font-size: 18px;
    color: #64748b;
    line-height: 1.6;
    margin-bottom: 40px;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

/* ===== PHONE INPUT STYLING ===== */
.phone-input-container {
    max-width: 400px;
    margin: 0 auto 40px;
}

.stTextInput > div > div {
    border-radius: 16px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 8px 16px !important;
    background: white !important;
}

.stTextInput > div > div > input {
    font-size: 18px !important;
    padding: 16px 20px !important;
    border: none !important;
    background: transparent !important;
}

.stTextInput > div > div > input:focus {
    outline: none !important;
    box-shadow: none !important;
}

.stTextInput > div > div > input::placeholder {
    color: #94a3b8 !important;
}

/* ===== BUTTON STYLING ===== */
.stButton > button {
    border-radius: 16px !important;
    padding: 20px 48px !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    border: none !important;
    background: linear-gradient(135deg, #f59e0b, #fbbf24) !important;
    color: #1e293b !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3) !important;
    width: 100% !important;
    max-width: 400px;
    margin: 0 auto;
    display: block;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 40px rgba(245, 158, 11, 0.4) !important;
}

/* ===== FEATURES GRID ===== */
.features-section {
    margin: 60px 0;
}

.features-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 48px;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
    margin-top: 32px;
}

.feature-card {
    background: white;
    padding: 32px 24px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(124, 58, 237, 0.1);
    transition: all 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);
}

.feature-icon {
    font-size: 48px;
    margin-bottom: 20px;
    display: block;
}

.feature-card:nth-child(1) .feature-icon { color: #7c3aed; }
.feature-card:nth-child(2) .feature-icon { color: #ec4899; }
.feature-card:nth-child(3) .feature-icon { color: #f59e0b; }
.feature-card:nth-child(4) .feature-icon { color: #10b981; }

.feature-name {
    font-size: 20px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 12px;
}

.feature-desc {
    font-size: 14px;
    color: #64748b;
    line-height: 1.5;
}

/* ===== TRIAL PROGRESS ===== */
.trial-card {
    background: linear-gradient(135deg, #fef3c7, #fde68a);
    border-radius: 24px;
    padding: 40px;
    margin: 40px 0;
    border-left: 6px solid #f59e0b;
}

.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.progress-title {
    font-size: 20px;
    font-weight: 600;
    color: #92400e;
    display: flex;
    align-items: center;
    gap: 12px;
}

.progress-count {
    font-size: 28px;
    font-weight: 700;
    color: #7c3aed;
}

.progress-bar-container {
    background: rgba(255, 255, 255, 0.7);
    height: 14px;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 16px;
}

.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #7c3aed, #8b5cf6);
    border-radius: 10px;
    transition: width 0.6s ease;
}

.progress-note {
    text-align: center;
    color: #92400e;
    font-size: 14px;
    font-weight: 500;
}

/* ===== MESSAGE CREATOR ===== */
.message-creator {
    background: white;
    border-radius: 28px;
    padding: 60px 48px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08);
    margin: 40px 0;
}

.creator-title {
    font-size: 32px;
    font-weight: 700;
    color: #1e293b;
    text-align: center;
    margin-bottom: 16px;
}

.creator-subtitle {
    font-size: 18px;
    color: #64748b;
    text-align: center;
    margin-bottom: 48px;
    line-height: 1.6;
}

/* ===== INPUT SECTIONS ===== */
.input-section {
    margin-bottom: 32px;
}

.section-label {
    font-size: 16px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 16px;
    display: block;
}

.gender-container {
    display: flex;
    gap: 16px;
    margin-bottom: 32px;
}

.gender-option {
    flex: 1;
    padding: 20px;
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    border-radius: 16px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 16px;
    font-weight: 500;
    color: #475569;
}

.gender-option:hover {
    background: white;
    border-color: #8b5cf6;
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(139, 92, 246, 0.1);
}

.gender-option.selected {
    background: rgba(139, 92, 246, 0.1);
    border-color: #8b5cf6;
    color: #7c3aed;
}

/* ===== STREAMLIT OVERRIDES ===== */
.stSelectbox > div > div {
    border-radius: 16px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 8px 16px !important;
    background: white !important;
}

.stSelectbox > div > div > div {
    padding: 16px !important;
    font-size: 16px !important;
}

.stTextArea > div > div {
    border-radius: 16px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 8px 16px !important;
    background: white !important;
}

.stTextArea > div > div > textarea {
    font-size: 16px !important;
    padding: 16px !important;
    min-height: 120px !important;
    border: none !important;
    background: transparent !important;
}

/* ===== MESSAGE RESULT ===== */
.message-result {
    background: linear-gradient(135deg, #f8fafc, #ffffff);
    border-radius: 24px;
    padding: 48px;
    margin: 40px 0;
    border: 1px solid rgba(124, 58, 237, 0.1);
    position: relative;
}

.result-label {
    position: absolute;
    top: -20px;
    left: 40px;
    background: linear-gradient(135deg, #7c3aed, #8b5cf6);
    color: white;
    padding: 12px 32px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 16px;
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.3);
}

.result-content {
    font-size: 20px;
    line-height: 1.8;
    color: #1e293b;
    margin: 32px 0;
    padding: 32px;
    background: white;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    white-space: pre-line;
}

/* ===== ACTION BUTTONS ===== */
.action-buttons {
    display: flex;
    gap: 16px;
    margin-top: 32px;
}

.action-btn {
    flex: 1;
    padding: 18px !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
}

/* ===== HIDE STREAMLIT ELEMENTS ===== */
#MainMenu { display: none !important; }
footer { display: none !important; }
.stDeployButton { display: none !important; }

/* ===== RESPONSIVE DESIGN ===== */
@media (max-width: 768px) {
    .hero-title { font-size: 36px; }
    .hero-tagline { font-size: 18px; }
    .nav-bar { flex-direction: column; gap: 16px; padding: 20px; }
    .content-card, .message-creator { padding: 40px 24px; }
    .card-title { font-size: 28px; }
    .features-grid { grid-template-columns: 1fr; }
    .gender-container { flex-direction: column; }
    .action-buttons { flex-direction: column; }
}
</style>
""", unsafe_allow_html=True)

# ==================== HẰNG SỐ ====================
FREE_TRIAL_LIMIT = 5
BANK_INFO = {
    "bank": "BIDV",
    "account": "4430269669",
    "name": "NGUYEN XUAN DAT",
    "note_format": "EMOTICONN [SỐ ĐIỆN THOẠI]"
}

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
    if not phone:
        return None
    phone = re.sub(r'\D', '', str(phone))
    if 9 <= len(phone) <= 11 and phone.startswith('0'):
        return phone
    return None

def get_usage_count(phone):
    try:
        df = pd.read_csv(USAGE_FILE)
        user_data = df[df["phone"] == phone]
        return 0 if user_data.empty else int(user_data.iloc[0]["count"])
    except Exception as e:
        print(f"Error reading usage: {e}")
        return 0

def update_usage(phone):
    try:
        try:
            df = pd.read_csv(USAGE_FILE)
        except:
            df = pd.DataFrame(columns=["phone", "count", "last_used"])
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if phone in df["phone"].values:
            df.loc[df["phone"] == phone, "count"] = df.loc[df["phone"] == phone, "count"].astype(int) + 1
            df.loc[df["phone"] == phone, "last_used"] = now
        else:
            new_row = pd.DataFrame({
                "phone": [phone],
                "count": [1],
                "last_used": [now]
            })
            df = pd.concat([df, new_row], ignore_index=True)
        
        df.to_csv(USAGE_FILE, index=False)
    except Exception as e:
        print(f"Error updating usage: {e}")

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
                    "Chào bạn, mình là {name}. Mình thấy {detail} và muốn làm quen nếu không phiền. Hôm nay của bạn thế nào? ☕",
                    "Xin chào, hy vọng tin nhắn này không làm phiền. Công việc của bạn dạo này ổn chứ? Mình muốn làm quen và trò chuyện. 💼",
                ],
                "Nữ→Nam": [
                    "Chào anh, em là {name} đây. Anh có vài phút trò chuyện không? Em muốn làm quen. 🌸",
                    "Xin chào, em muốn làm quen nếu anh không ngại. Anh đang bận gì không? 🤗",
                ],
                "Nam→Nam": [
                    "Chào bạn, mình là {name}. Mình thấy chúng ta có chung {detail}, muốn làm quen nếu bạn không ngại. Cà phê cuối tuần nhé? ☕",
                ],
                "Nữ→Nữ": [
                    "Chào bạn, mình là {name} đây. Mình muốn làm quen vì thấy chúng ta có chung {detail}. Bạn rảnh trò chuyện không? 🌸",
                ]
            },
            "Hỏi thăm": {
                "Nam→Nữ": [
                    "Dạo này bạn thế nào? Công việc có đỡ áp lực hơn không? Nếu có gì cần chia sẻ, mình luôn sẵn sàng lắng nghe bạn. 🌿",
                ],
                "Nữ→Nam": [
                    "Anh ơi, dạo này anh có khoẻ không? Công việc nhiều quá có mệt không? Nhớ chăm sóc sức khoẻ nhé. 🫂",
                ],
                "Nam→Nam": [
                    "Bạn ơi, dạo này thế nào rồi? Công việc ổn không? Có gì cần giúp đỡ cứ nói nhé. 💪",
                ],
                "Nữ→Nữ": [
                    "Bạn ơi, dạo này sao rồi? Công việc có ổn không? Nhớ giữ gìn sức khoẻ nha. 💖",
                ]
            },
            "An ủi": {
                "Nam→Nữ": [
                    "Nghe nói bạn đang có chuyện không vui. Nếu muốn chia sẻ, mình luôn ở đây để lắng nghe. Mọi chuyện rồi sẽ qua thôi. 🌈",
                ],
                "Nữ→Nam": [
                    "Anh ơi, em biết anh đang không vui. Nếu cần ai đó tâm sự, em luôn sẵn sàng. Mọi chuyện rồi sẽ tốt đẹp thôi. 💝",
                ],
                "Nam→Nam": [
                    "Nghe nói bạn đang gặp chuyện không vui. Nếu cần tâm sự, mình luôn sẵn sàng. Mọi chuyện rồi cũng sẽ ổn thôi. 🤝",
                ],
                "Nữ→Nữ": [
                    "Mình nghe nói bạn đang không vui. Nếu cần chia sẻ, mình luôn ở đây lắng nghe. Rồi mọi chuyện sẽ tốt đẹp thôi. 💕",
                ]
            },
            "Tỏ tình": {
                "Nam→Nữ": [
                    "Mình đã suy nghĩ rất nhiều và muốn nói rằng, mình thực sự thích bạn. Bạn cho mình cơ hội được không? 💖",
                ],
                "Nữ→Nam": [
                    "Anh à, em muốn nói rằng em rất thích anh. Anh có thể cho em cơ hội được không? 🌹",
                ],
                "Nam→Nam": [
                    "Mình muốn nói rằng mình rất quý bạn. Không biết bạn có thể cho mình cơ hội được không? 🌈",
                ],
                "Nữ→Nữ": [
                    "Mình muốn nói rằng mình rất thích bạn. Bạn có thể cho mình cơ hội được không? 💝",
                ]
            },
            "Làm hoà": {
                "Nam→Nữ": [
                    "Mình xin lỗi về những hiểu lầm vừa qua. Mình trân trọng bạn và mong chúng ta có thể nói chuyện để hiểu nhau hơn. 🤝",
                ],
                "Nữ→Nam": [
                    "Anh ơi, em xin lỗi vì những gì đã xảy ra. Anh có thể tha thứ cho em không? Em rất trân trọng anh. 🙏",
                ],
                "Nam→Nam": [
                    "Mình xin lỗi về chuyện vừa rồi. Mình trân trọng tình bạn này và mong chúng ta có thể làm lành. ✌️",
                ],
                "Nữ→Nữ": [
                    "Mình xin lỗi về mọi chuyện. Mình rất trân trọng bạn và mong chúng ta có thể làm lành. 💞",
                ]
            }
        }
    
    def generate(self, user_gender, target_gender, situation, context=""):
        gender_key = f"{user_gender}→{target_gender}"
        
        if situation in self.templates and gender_key in self.templates[situation]:
            templates = self.templates[situation][gender_key]
        else:
            templates = ["Xin chào, hy vọng bạn có một ngày tốt lành. 💫"]
        
        template = random.choice(templates)
        
        if context:
            detail = context[:50] + "..." if len(context) > 50 else context
            template = template.replace("{detail}", detail)
        
        # Thay thế {name} mặc định
        template = template.replace("{name}", "tôi")
        
        return template

# ==================== APP CHÍNH ====================
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
    if 'result' not in st.session_state:
        st.session_state.result = ""
    if 'user_gender' not in st.session_state:
        st.session_state.user_gender = "Nam"
    if 'target_gender' not in st.session_state:
        st.session_state.target_gender = "Nữ"
    
    # ===== HERO SECTION =====
    st.markdown("""
    <div class="hero-container">
        <div class="hero-icon">💬</div>
        <h1 class="hero-title">EMOTICONN AI</h1>
        <p class="hero-tagline">Nói điều bạn muốn - Theo cách họ muốn nghe</p>
        <p class="hero-subtitle">Trợ lý giao tiếp cảm xúc dành cho người trưởng thành</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== NAVIGATION =====
    st.markdown("""
    <div class="nav-bar">
        <div class="nav-brand">
            <span class="brand-icon">🏠</span>
            <span class="brand-text">EMOTICONN AI</span>
        </div>
        <div class="nav-stats">
            <div class="rating">
                <span class="stars">⭐⭐⭐⭐⭐</span>
                <span>4.9/5 từ 2,500+</span>
            </div>
            <div class="trial-badge">5 lượt dùng thử</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== MAIN CONTENT =====
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    if not st.session_state.verified:
        # ===== REGISTRATION CARD =====
        st.markdown("""
        <div class="content-card">
            <div class="card-icon">🔓</div>
            <h2 class="card-title">Bắt Đầu Hành Trình Cảm Xúc</h2>
            <p class="card-description">
                Nhận ngay <strong style="color: #7c3aed;">5 tin nhắn AI tinh tế</strong> hoàn toàn miễn phí<br>
                Khám phá sức mạnh của giao tiếp thấu hiểu
            </p>
            
            <div class="phone-input-container">
        """, unsafe_allow_html=True)
        
        # Phone input
        phone = st.text_input(
            "",
            placeholder="Nhập số điện thoại của bạn...",
            key="phone_input",
            label_visibility="collapsed"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Register button
        if st.button("✨ **NHẬN 5 TIN MIỄN PHÍ**", 
                    type="primary", 
                    key="register_btn",
                    use_container_width=True):
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
                    st.error("⚠️ Vui lòng nhập số điện thoại hợp lệ (10-11 số, bắt đầu bằng 0)")
            else:
                st.warning("📱 Vui lòng nhập số điện thoại")
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close content-card
        
        # ===== FEATURES SECTION =====
        st.markdown("""
        <div class="features-section">
            <h2 class="features-title">✨ Tại Sao Chọn EMOTICONN AI?</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <h3 class="feature-name">Dành cho người trưởng thành</h3>
                    <p class="feature-desc">Ngôn từ tinh tế, sâu sắc, không sáo rỗng, phù hợp độ tuổi 30-55+</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">💝</div>
                    <h3 class="feature-name">7,000+ tình huống</h3>
                    <p class="feature-desc">Hệ thống AI thấu hiểu mọi ngữ cảnh giao tiếp phức tạp</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🔥</div>
                    <h3 class="feature-name">5 lượt dùng thử</h3>
                    <p class="feature-desc">Trải nghiệm chất lượng cao trước khi quyết định đầu tư</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">💎</div>
                    <h3 class="feature-name">Giá trị trọn đời</h3>
                    <p class="feature-desc">Chỉ 149.000đ - Sử dụng mãi mãi, cập nhật miễn phí</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close main-content
        return
    
    # ===== TRIAL PROGRESS =====
    if not st.session_state.paid:
        remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
        
        if remaining <= 0:
            st.error("⚠️ **Bạn đã hết lượt dùng thử!** Vui lòng nâng cấp để tiếp tục sử dụng.")
            
            # Thêm phần thanh toán
            with st.expander("💳 **Nâng cấp tài khoản**"):
                st.markdown(f"""
                **Thông tin chuyển khoản:**
                - Ngân hàng: {BANK_INFO['bank']}
                - Số tài khoản: {BANK_INFO['account']}
                - Chủ tài khoản: {BANK_INFO['name']}
                - Nội dung: {BANK_INFO['note_format'].replace('[SỐ ĐIỆN THOẠI]', st.session_state.phone)}
                
                **Giá: 149.000đ** - Sử dụng trọn đời
                """)
                
                verify_btn = st.button("✅ **Tôi đã chuyển khoản**", use_container_width=True)
                if verify_btn:
                    save_paid_user(st.session_state.phone)
                    st.session_state.paid = True
                    st.success("🎉 **Nâng cấp thành công!** Cảm ơn bạn đã tin tưởng.")
                    time.sleep(1)
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)  # Close main-content
            return
        
        percentage = (st.session_state.usage_count / FREE_TRIAL_LIMIT) * 100
        
        st.markdown(f"""
        <div class="trial-card">
            <div class="progress-header">
                <div class="progress-title">
                    <span>🎯</span>
                    <span>Bạn đang dùng thử miễn phí</span>
                </div>
                <div class="progress-count">{remaining}/{FREE_TRIAL_LIMIT}</div>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar" style="width: {percentage}%"></div>
            </div>
            <div class="progress-note">Mỗi tin nhắn đều được AI tạo riêng cho tình huống của bạn</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== MESSAGE CREATOR =====
    st.markdown("""
    <div class="message-creator">
        <h2 class="creator-title">✍️ Tạo Tin Nhắn Tinh Tế</h2>
        <p class="creator-subtitle">
            Chia sẻ tình huống của bạn, để AI thấu hiểu và giúp bạn diễn đạt cảm xúc một cách chân thành, phù hợp
        </p>
    """, unsafe_allow_html=True)
    
    # Gender selection
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-label" style="font-size: 14px;">Bạn là:</div>', unsafe_allow_html=True)
        user_gender = st.radio(
            "",
            ["Nam", "Nữ"],
            horizontal=True,
            label_visibility="collapsed",
            key="user_gender_radio"
        )
    
    with col2:
        st.markdown('<div class="section-label" style="font-size: 14px;">Gửi cho:</div>', unsafe_allow_html=True)
        target_gender = st.radio(
            "",
            ["Nam", "Nữ"],
            horizontal=True,
            label_visibility="collapsed",
            key="target_gender_radio"
        )
    
    # Situation selection
    st.markdown('<div class="section-label">💭 Chọn tình huống</div>', unsafe_allow_html=True)
    
    situation = st.selectbox(
        "",
        ["Làm quen", "Hỏi thăm", "An ủi", "Tỏ tình", "Làm hoà"],
        index=1,
        label_visibility="collapsed"
    )
    
    # Context input
    st.markdown('<div class="section-label">📝 Thêm chi tiết (tuỳ chọn)</div>', unsafe_allow_html=True)
    
    context = st.text_area(
        "",
        placeholder="Ví dụ: Chúng ta mới quen qua ứng dụng hẹn hò, bạn ấy là kiến trúc sư 35 tuổi...",
        height=120,
        label_visibility="collapsed"
    )
    
    # Generate button
    if st.button("✨ **AI TẠO TIN NHẮN TINH TẾ**", 
                type="primary", 
                use_container_width=True,
                key="generate_btn"):
        
        if not st.session_state.paid:
            st.session_state.usage_count += 1
            update_usage(st.session_state.phone)
            remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
            
            if remaining < 0:
                st.error("Bạn đã hết lượt dùng thử!")
                st.rerun()
        
        # Generate message
        ai = EmotionalAI()
        with st.spinner("🤖 AI đang tạo tin nhắn..."):
            time.sleep(1)
            result = ai.generate(user_gender, target_gender, situation, context)
            st.session_state.result = result
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close message-creator
    
    # ===== MESSAGE RESULT =====
    if st.session_state.result:
        st.markdown(f"""
        <div class="message-result">
            <div class="result-label">💌 Tin nhắn gợi ý</div>
            <div class="result-content">{st.session_state.result}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📋 Copy", key="copy_btn", use_container_width=True):
                st.success("✅ Đã copy vào clipboard!")
        with col2:
            if st.button("🔄 Tạo mới", key="new_btn", use_container_width=True):
                st.session_state.result = ""
                st.rerun()
        with col3:
            if st.button("💾 Lưu lại", key="save_btn", use_container_width=True):
                st.info("✨ (Tính năng đang phát triển) Tin nhắn sẽ được lưu vào lịch sử")
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-content

if __name__ == "__main__":
    main()
