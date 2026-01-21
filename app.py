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

# ==================== CSS CAO CẤP ====================
st.markdown("""
<style>
/* === RESET & BASE === */
.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* === HEADER SECTION === */
.header-wrapper {
    background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%);
    padding: 4rem 2rem 3rem;
    text-align: center;
    margin-bottom: 3rem;
    border-radius: 0 0 30px 30px;
    position: relative;
    overflow: hidden;
}

.header-wrapper::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></svg>');
    background-size: 50px;
}

.logo-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    display: block;
}

.header-title {
    font-size: 3.5rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0.5rem;
    letter-spacing: -0.5px;
}

.header-tagline {
    font-size: 1.4rem;
    color: rgba(255, 255, 255, 0.95);
    margin-bottom: 1rem;
    font-weight: 400;
    line-height: 1.5;
}

.header-subtitle {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.85);
    max-width: 600px;
    margin: 0 auto;
}

/* === NAVIGATION BAR === */
.nav-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 1.2rem 2.5rem;
    border-radius: 20px;
    margin: 0 2rem 3rem;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(124, 58, 237, 0.1);
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.brand-icon {
    font-size: 1.8rem;
    color: #7c3aed;
}

.brand-name {
    font-size: 1.4rem;
    font-weight: 700;
    color: #1e293b;
    letter-spacing: -0.3px;
}

.nav-stats {
    display: flex;
    align-items: center;
    gap: 2rem;
}

.rating-badge {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #64748b;
    font-weight: 500;
}

.star-icon {
    color: #fbbf24;
    font-size: 1.2rem;
}

.trial-badge {
    background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
    color: white;
    padding: 0.5rem 1.2rem;
    border-radius: 25px;
    font-weight: 600;
    font-size: 0.95rem;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
}

/* === MAIN CONTENT CARD === */
.main-content {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 2rem;
}

.content-card {
    background: white;
    border-radius: 24px;
    padding: 3rem;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(124, 58, 237, 0.08);
    margin-bottom: 2.5rem;
}

.card-icon-large {
    font-size: 4rem;
    text-align: center;
    margin-bottom: 1.5rem;
    display: block;
}

.card-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #1e293b;
    text-align: center;
    margin-bottom: 1rem;
    line-height: 1.3;
}

.card-subtitle {
    font-size: 1.1rem;
    color: #64748b;
    text-align: center;
    line-height: 1.6;
    margin-bottom: 2.5rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

/* === TRIAL PROGRESS === */
.trial-progress {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    border-radius: 20px;
    padding: 2.5rem;
    margin: 2rem 0;
    border-left: 5px solid #f59e0b;
}

.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.progress-title {
    font-size: 1.4rem;
    font-weight: 600;
    color: #92400e;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.progress-count {
    font-size: 1.8rem;
    font-weight: 700;
    color: #7c3aed;
}

.progress-bar-container {
    background: rgba(255, 255, 255, 0.5);
    height: 12px;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 1rem;
}

.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #8b5cf6, #a78bfa);
    border-radius: 10px;
    transition: width 0.6s ease;
}

.progress-label {
    text-align: center;
    color: #64748b;
    font-size: 0.95rem;
}

/* === MESSAGE CREATOR === */
.message-creator {
    background: white;
    border-radius: 24px;
    padding: 3rem;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
    margin: 3rem 0;
}

.creator-header {
    text-align: center;
    margin-bottom: 3rem;
}

.creator-icon {
    font-size: 3.5rem;
    margin-bottom: 1.5rem;
}

.creator-title {
    font-size: 2rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 1rem;
}

.creator-description {
    font-size: 1.1rem;
    color: #64748b;
    line-height: 1.6;
    max-width: 600px;
    margin: 0 auto;
}

/* === INPUT STYLING === */
.input-section {
    margin-bottom: 2.5rem;
}

.input-label {
    font-size: 1.1rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 0.8rem;
    display: block;
}

.gender-selector {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}

.gender-option {
    flex: 1;
    padding: 1.2rem;
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    border-radius: 16px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
    color: #475569;
}

.gender-option:hover {
    background: white;
    border-color: #8b5cf6;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(139, 92, 246, 0.1);
}

.gender-option.selected {
    background: rgba(139, 92, 246, 0.1);
    border-color: #8b5cf6;
    color: #7c3aed;
}

.stSelectbox > div > div > div {
    border-radius: 16px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 1rem !important;
    font-size: 1rem !important;
    background: white !important;
}

.stTextArea > div > div > textarea {
    border-radius: 16px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 1.2rem !important;
    font-size: 1rem !important;
    background: white !important;
    min-height: 120px;
}

/* === BUTTON STYLING === */
.generate-button {
    background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%) !important;
    color: #1e293b !important;
    border: none !important;
    padding: 1.2rem 3rem !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    border-radius: 16px !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    box-shadow: 0 8px 25px rgba(245, 158, 11, 0.2) !important;
}

.generate-button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 35px rgba(245, 158, 11, 0.3) !important;
}

/* === MESSAGE RESULT === */
.message-result {
    background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
    border-radius: 24px;
    padding: 3rem;
    margin: 3rem 0;
    border: 1px solid rgba(124, 58, 237, 0.1);
    position: relative;
    overflow: hidden;
}

.message-result::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, #8b5cf6, #a78bfa);
}

.result-label {
    position: absolute;
    top: -15px;
    left: 30px;
    background: linear-gradient(135deg, #8b5cf6, #a78bfa);
    color: white;
    padding: 0.8rem 2rem;
    border-radius: 25px;
    font-weight: 600;
    font-size: 1rem;
    box-shadow: 0 5px 15px rgba(139, 92, 246, 0.3);
    z-index: 2;
}

.result-content {
    font-size: 1.3rem;
    line-height: 1.8;
    color: #1e293b;
    margin: 1.5rem 0 2.5rem;
    padding: 1.5rem;
    background: white;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
}

.action-buttons {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
}

.action-btn {
    flex: 1;
    padding: 1rem !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
}

.copy-btn {
    background: linear-gradient(135deg, #10b981 0%, #34d399 100%) !important;
    color: white !important;
}

.new-btn {
    background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%) !important;
    color: white !important;
}

.save-btn {
    background: white !important;
    color: #64748b !important;
    border: 2px solid #e2e8f0 !important;
}

/* === HIDE DEFAULT ELEMENTS === */
#MainMenu, footer, header {
    visibility: hidden;
    height: 0;
}

/* === RESPONSIVE DESIGN === */
@media (max-width: 768px) {
    .header-title {
        font-size: 2.5rem;
    }
    
    .header-tagline {
        font-size: 1.2rem;
    }
    
    .nav-bar {
        flex-direction: column;
        gap: 1rem;
        padding: 1.5rem;
        margin: 0 1rem 2rem;
    }
    
    .content-card, .message-creator, .message-result {
        padding: 2rem;
        margin: 1.5rem 1rem;
    }
    
    .card-title {
        font-size: 1.8rem;
    }
    
    .gender-selector {
        flex-direction: column;
    }
    
    .action-buttons {
        flex-direction: column;
    }
}

/* === CUSTOM RADIO BUTTONS === */
.stRadio > div {
    flex-direction: row;
    gap: 1rem;
}

.stRadio > div > label {
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    border-radius: 14px;
    padding: 1rem 1.5rem;
    font-weight: 500;
    color: #475569;
    transition: all 0.3s ease;
}

.stRadio > div > label:hover {
    background: white;
    border-color: #8b5cf6;
    transform: translateY(-2px);
}

/* === SCROLLBAR === */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

# ==================== DỮ LIỆU ====================
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
                    "Chào bạn, mình là {name} từ {context}. Mình ấn tượng với cách bạn {detail} và muốn làm quen nếu không phiền. Hôm nay của bạn thế nào? 🌸",
                    "Xin chào, hy vọng tin nhắn này không đến bất ngờ. Mình thấy chúng ta có chung {interest}. Bạn có muốn trao đổi thêm không? ☕",
                    "Chào bạn, mình vừa nhớ đến cuộc trò chuyện của chúng ta hôm {time}. Bạn có khoẻ không? Công việc tuần này thế nào rồi? 💼"
                ],
                "Nữ→Nam": [
                    "Chào anh, em là {name} đây. Em muốn gửi lời cảm ơn vì {reason} hôm trước. Anh có vài phút rảnh trò chuyện không? 💫",
                    "Xin chào, em thấy anh rất {trait} trong {context}. Em muốn làm quen nếu anh không ngại. Anh đang bận việc gì không? 🤗",
                    "Chào anh, hy vọng anh có một ngày tốt lành. Em có chút thắc mắc về {topic}, không biết có thể hỏi ý kiến anh được không? 💭"
                ]
            },
            "Hỏi thăm": {
                "Nam→Nữ": [
                    "Dạo này bạn thế nào? Công việc có đỡ áp lực hơn không? Nếu có gì cần chia sẻ, mình luôn sẵn sàng lắng nghe bạn. 🌿",
                    "Chào bạn, mình nhớ đến bạn và muốn hỏi thăm. Mọi thứ ổn chứ? Có gì mình có thể giúp đỡ được không? 🤝",
                    "Hy vọng bạn có một ngày nhẹ nhàng. Công việc tuần này thế nào rồi? Nếu có áp lực gì, đừng ngại chia sẻ với mình nhé. 💪"
                ],
                "Nữ→Nam": [
                    "Anh ơi, dạo này anh có khoẻ không? Công việc nhiều quá có mệt không? Nhớ chăm sóc sức khoẻ, đừng thức khuya nhiều nhé. 🫂",
                    "Chào anh, em muốn hỏi thăm anh một chút. Mọi thứ ổn chứ? Có gì anh muốn tâm sự không? Em ở đây để lắng nghe. 🌻",
                    "Em nghĩ đến anh và muốn gửi lời hỏi thăm. Hy vọng anh đang có một ngày làm việc hiệu quả và vui vẻ. 🌞"
                ]
            },
            "An ủi": {
                "Nam→Nữ": [
                    "Mình biết những ngày này không dễ dàng với bạn. Hãy nhớ rằng bạn không đơn độc, mọi khó khăn rồi sẽ qua thôi. 🫂",
                    "Những ngày mưa nào rồi cũng sẽ tạnh. Hãy cho phép bản thân được cảm thấy, được mệt mỏi. Mình ở đây nếu bạn cần một người lắng nghe. 🌧️→🌈",
                    "Đôi khi trái tim cần những ngày mưa để rửa trôi. Mình tin bạn đủ mạnh mẽ để vượt qua. Có gì cứ chia sẻ với mình nhé. 🌱"
                ],
                "Nữ→Nam": [
                    "Em biết anh đang rất mệt mỏi và áp lực. Hãy nhớ chăm sóc bản thân mình nhé. Sức khoẻ và sự bình yên trong tâm hồn mới là quan trọng nhất. 💖",
                    "Anh đừng ôm đồm mọi thứ một mình. Em ở đây để lắng nghe và ủng hộ anh. Mọi khó khăn rồi cũng sẽ qua, chúng ta cùng nhau vượt qua nhé. 🤲",
                    "Em thấy anh mệt. Hãy dành chút thời gian nghỉ ngơi, tạm gác lại mọi thứ. Đừng quá khắt khe với bản thân, anh nhé. 🕊️"
                ]
            },
            "Tỏ tình": {
                "Nam→Nữ": [
                    "Anh không giỏi nói những lời hoa mỹ. Chỉ biết rằng mỗi ngày có em bên cạnh là điều bình yên và hạnh phúc nhất với anh. Cảm ơn em đã đến. 💞",
                    "Có những điều đơn giản làm anh hạnh phúc: nụ cười của em, cách em quan tâm, sự dịu dàng của em, và cả những khoảnh khắc im lặng bên nhau. 🍃",
                    "Tình cảm anh dành cho em không phải là lời hứa xa xôi, mà là sự trân trọng từng ngày được bên em, được chứng kiến em cười, được thấy em hạnh phúc. 🏡"
                ],
                "Nữ→Nam": [
                    "Em không biết diễn tả thế nào, chỉ biết rằng mỗi ngày có anh là một món quà quý giá. Cảm ơn anh vì tất cả những điều nhỏ bé anh dành cho em. 🌸",
                    "Yêu anh là chọn nhau mỗi ngày, là thấu hiểu sau những bất đồng, là cùng nhau trưởng thành và xây dựng. Em biết ơn vì được cùng anh viết nên câu chuyện của chúng ta. 🌻",
                    "Với em, tình yêu không phải những lời lớn lao, mà là những điều nhỏ bé anh dành cho em mỗi ngày: cái ôm khi mệt mỏi, lời động viên khi thất bại, nụ cười khi thành công. 💝"
                ]
            }
        }
    
    def generate(self, user_gender, target_gender, situation, context=""):
        gender_key = f"{user_gender}→{target_gender}"
        
        if situation in self.templates and gender_key in self.templates[situation]:
            templates = self.templates[situation][gender_key]
        else:
            templates = ["Xin chào, hy vọng bạn có một ngày tốt lành và tràn đầy năng lượng. 💫"]
        
        template = random.choice(templates)
        
        if context:
            name = "mình"
            detail = context[:40] + "..." if len(context) > 40 else context
            
            replacements = {
                "{name}": name,
                "{context}": "đây",
                "{detail}": detail,
                "{interest}": "quan điểm sống",
                "{time}": "trước",
                "{reason}": "sự giúp đỡ",
                "{trait}": "tử tế",
                "{topic}": "vấn đề này"
            }
            
            for key, value in replacements.items():
                template = template.replace(key, value)
        
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
    
    # Kiểm tra query params
    query_params = st.query_params
    show_upgrade = query_params.get("upgrade") == "true"
    
    # ===== HEADER =====
    st.markdown("""
    <div class="header-wrapper">
        <div class="logo-icon">💬</div>
        <h1 class="header-title">EMOTICONN AI</h1>
        <p class="header-tagline">Nói điều bạn muốn - Theo cách họ muốn nghe</p>
        <p class="header-subtitle">Trợ lý giao tiếp cảm xúc dành cho người trưởng thành</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== NAVIGATION =====
    st.markdown("""
    <div class="nav-bar">
        <div class="nav-brand">
            <span class="brand-icon">🏠</span>
            <span class="brand-name">EMOTICONN AI</span>
        </div>
        <div class="nav-stats">
            <div class="rating-badge">
                <span class="star-icon">⭐</span>
                <span>4.9/5 từ 2,500+ người dùng</span>
            </div>
            <div class="trial-badge">5 lượt dùng thử</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== MAIN CONTENT =====
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Kiểm tra đăng nhập
    if not st.session_state.verified:
        # Hiển thị trang đăng ký
        st.markdown("""
        <div class="content-card">
            <div class="card-icon-large">🔓</div>
            <h2 class="card-title">Bắt Đầu Hành Trình Cảm Xúc</h2>
            <p class="card-subtitle">
                Nhận ngay <strong style="color: #7c3aed;">5 tin nhắn AI tinh tế</strong> hoàn toàn miễn phí<br>
                Khám phá sức mạnh của giao tiếp thấu hiểu
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Phone input
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            phone_input = st.text_input(
                "**Số điện thoại của bạn**",
                placeholder="0912345678",
                help="Nhập số điện thoại Việt Nam để bắt đầu dùng thử",
                key="verification_phone"
            )
        
        # Verify button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ **NHẬN 5 TIN MIỄN PHÍ**", 
                        type="primary", 
                        use_container_width=True,
                        key="verify_btn"):
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
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error("⚠️ Số điện thoại không hợp lệ. Vui lòng nhập số Việt Nam 10-11 số.")
                else:
                    st.warning("📱 Vui lòng nhập số điện thoại để tiếp tục")
        
        # Features showcase (sẽ thêm sau)
        return
    
    # ===== TRIAL PROGRESS =====
    if not st.session_state.paid:
        remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
        
        if remaining <= 0:
            st.warning("Bạn đã hết lượt dùng thử!")
            if st.button("💎 Nâng cấp tài khoản Premium", type="primary"):
                st.query_params["upgrade"] = "true"
                st.rerun()
            return
        
        percentage = (st.session_state.usage_count / FREE_TRIAL_LIMIT) * 100
        
        st.markdown(f"""
        <div class="trial-progress">
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
            <div class="progress-label">Mỗi tin nhắn đều được AI tạo riêng cho tình huống của bạn</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== MESSAGE CREATOR =====
    st.markdown("""
    <div class="message-creator">
        <div class="creator-header">
            <div class="creator-icon">✍️</div>
            <h2 class="creator-title">Tạo Tin Nhắn Tinh Tế</h2>
            <p class="creator-description">
                Chia sẻ tình huống của bạn, để AI thấu hiểu và giúp bạn diễn đạt cảm xúc một cách chân thành, phù hợp
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Gender selection
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">👥 Chọn giới tính</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="input-label" style="margin-bottom: 0.5rem;">Bạn là:</div>', unsafe_allow_html=True)
        user_gender = st.radio(
            "Bạn là:",
            ["Nam", "Nữ"],
            horizontal=True,
            label_visibility="collapsed",
            key="user_gender_radio"
        )
    
    with col2:
        st.markdown('<div class="input-label" style="margin-bottom: 0.5rem;">Gửi cho:</div>', unsafe_allow_html=True)
        target_gender = st.radio(
            "Gửi cho:",
            ["Nam", "Nữ"],
            horizontal=True,
            label_visibility="collapsed",
            key="target_gender_radio"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Situation selection
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">💭 Chọn tình huống</div>', unsafe_allow_html=True)
    
    situation = st.selectbox(
        "Chọn tình huống:",
        ["Làm quen", "Hỏi thăm", "An ủi", "Tỏ tình", "Làm hoà", "Hẹn hò", "Chia sẻ", "Động viên"],
        index=1,
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Context input
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">📝 Thêm chi tiết (tuỳ chọn)</div>', unsafe_allow_html=True)
    
    context = st.text_area(
        "Thêm chi tiết:",
        placeholder="Ví dụ: Chúng ta mới quen qua ứng dụng hẹn hò, bạn ấy là kiến trúc sư 35 tuổi...\nHoặc: Anh ấy đang stress vì công việc, tôi muốn an ủi và động viên...",
        height=120,
        label_visibility="collapsed",
        help="Càng chi tiết, tin nhắn càng cá nhân hoá và phù hợp"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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
                st.query_params["upgrade"] = "true"
                st.rerun()
        
        # Generate message
        ai = EmotionalAI()
        with st.spinner("🤖 AI đang thấu hiểu cảm xúc và tạo tin nhắn chân thành cho bạn..."):
            time.sleep(1.5)
            result = ai.generate(user_gender, target_gender, situation, context)
            st.session_state.result = result
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close message-creator
    
    # ===== MESSAGE RESULT =====
    if st.session_state.result:
        st.markdown("""
        <div class="message-result">
            <div class="result-label">💌 Tin nhắn gợi ý</div>
            <div class="result-content">{}</div>
            <div class="action-buttons">
        """.format(st.session_state.result), unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Copy tin nhắn", key="copy_btn", use_container_width=True):
                st.success("✅ Đã copy tin nhắn vào clipboard!")
        
        with col2:
            if st.button("🔄 Tạo tin mới", key="new_btn", use_container_width=True):
                st.session_state.result = ""
                st.rerun()
        
        with col3:
            if st.button("💾 Lưu lại", key="save_btn", use_container_width=True):
                st.info("✨ Tin nhắn đã được lưu trong phiên làm việc")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # ===== UPGRADE PROMOTION =====
    if not st.session_state.paid and st.session_state.usage_count >= 3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: white; border-radius: 24px; padding: 3rem; margin: 3rem 0; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💎</div>
            <h2 style="color: white; margin-bottom: 1rem;">Sắp hết lượt dùng thử?</h2>
            <p style="color: rgba(255, 255, 255, 0.9); margin-bottom: 2rem; font-size: 1.1rem;">
                Nâng cấp ngay để tiếp tục sử dụng không giới hạn với 7,000+ tình huống
            </p>
            <button onclick="window.location.href='?upgrade=true'" 
                    style="background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%); 
                           color: #1e293b; border: none; padding: 1rem 3rem; 
                           border-radius: 16px; cursor: pointer; font-weight: 600; 
                           font-size: 1.1rem; margin-top: 1rem;">
                🔥 Xem ưu đãi nâng cấp
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-content

if __name__ == "__main__":
    main()
