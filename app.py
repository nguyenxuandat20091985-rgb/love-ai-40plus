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
FREE_TRIAL_LIMIT = 5  # TĂNG LÊN 5 LƯỢT
PREMIUM_PRICE = "149.000đ"  # GIẢM GIÁ
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

# ==================== CSS PREMIUM ====================
def load_premium_css():
    st.markdown("""
    <style>
    /* ===== MÀU SẮC CHUẨN PREMIUM ===== */
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
        --shadow-medium: 0 10px 30px rgba(139, 92, 246, 0.15);
        --shadow-strong: 0 20px 50px rgba(139, 92, 246, 0.2);
        --radius-lg: 20px;
        --radius-md: 12px;
        --radius-sm: 8px;
    }
    
    /* ===== NỀN APP ===== */
    .stApp {
        background: var(--neutral-light);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* ===== HEADER PREMIUM ===== */
    .premium-header {
        background: linear-gradient(135deg, var(--primary-purple) 0%, var(--primary-pink) 100%);
        padding: 2rem 1rem;
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        text-align: center;
        box-shadow: var(--shadow-strong);
    }
    
    .premium-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 20%, rgba(255, 255, 255, 0.15) 0%, transparent 50%);
    }
    
    .header-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFFFFF 0%, #FFD6FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        max-width: 600px;
        margin: 0 auto;
        font-weight: 400;
        position: relative;
        z-index: 2;
    }
    
    /* ===== NAVIGATION BAR ===== */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-soft);
        margin-bottom: 2rem;
        position: sticky;
        top: 10px;
        z-index: 100;
        border: 1px solid rgba(139, 92, 246, 0.1);
    }
    
    .nav-left {
        display: flex;
        align-items: center;
        gap: 1rem;
        font-weight: 600;
        color: var(--primary-purple);
    }
    
    .nav-center {
        display: flex;
        align-items: center;
        gap: 1rem;
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .nav-button {
        background: linear-gradient(135deg, var(--primary-purple) 0%, var(--primary-pink) 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: var(--radius-md);
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
    }
    
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
    }
    
    /* ===== PREMIUM CARD ===== */
    .premium-card {
        background: white;
        border-radius: var(--radius-lg);
        padding: 2rem;
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(139, 92, 246, 0.08);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-medium);
    }
    
    .card-gradient {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(236, 72, 153, 0.05) 100%);
        border-left: 4px solid var(--primary-purple);
    }
    
    .card-gold {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.05) 0%, rgba(252, 211, 77, 0.05) 100%);
        border-left: 4px solid var(--accent-gold);
    }
    
    .card-emerald {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(52, 211, 153, 0.05) 100%);
        border-left: 4px solid var(--accent-emerald);
    }
    
    /* ===== INPUT STYLING ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        border-radius: var(--radius-md) !important;
        border: 2px solid rgba(139, 92, 246, 0.1) !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        background: white !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-purple) !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
        outline: none !important;
    }
    
    /* ===== PREMIUM BUTTONS ===== */
    .stButton > button {
        border-radius: var(--radius-md) !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        border: none !important;
        width: 100%;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, var(--accent-gold) 0%, #F59E0B 100%) !important;
        color: #1F2937 !important;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2) !important;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3) !important;
    }
    
    .btn-secondary {
        background: linear-gradient(135deg, var(--primary-purple) 0%, var(--primary-pink) 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2) !important;
    }
    
    .btn-secondary:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3) !important;
    }
    
    .btn-success {
        background: linear-gradient(135deg, var(--accent-emerald) 0%, #059669 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2) !important;
    }
    
    .btn-success:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3) !important;
    }
    
    /* ===== RADIO BUTTONS ===== */
    .stRadio > div {
        flex-direction: row;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    .stRadio > div > label {
        background: white;
        border: 2px solid rgba(139, 92, 246, 0.1);
        border-radius: var(--radius-md);
        padding: 0.8rem 1.2rem;
        transition: all 0.3s ease;
        flex: 1;
        min-width: 100px;
        text-align: center;
        font-weight: 500;
    }
    
    .stRadio > div > label:hover {
        border-color: var(--primary-purple);
        background: rgba(139, 92, 246, 0.05);
        transform: translateY(-2px);
    }
    
    /* ===== PROGRESS BAR ===== */
    .progress-container {
        width: 100%;
        background: rgba(139, 92, 246, 0.1);
        border-radius: 50px;
        overflow: hidden;
        height: 12px;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-purple), var(--primary-pink));
        border-radius: 50px;
        transition: width 0.6s ease;
    }
    
    /* ===== MESSAGE DISPLAY ===== */
    .message-display {
        background: linear-gradient(135deg, #FDF4FF 0%, #FCE7F3 100%);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin: 2rem 0;
        border: 2px solid rgba(236, 72, 153, 0.1);
        position: relative;
        box-shadow: var(--shadow-soft);
    }
    
    .message-display::before {
        content: '💌';
        position: absolute;
        top: -15px;
        left: 30px;
        font-size: 1.5rem;
        background: white;
        padding: 5px 15px;
        border-radius: 50px;
        border: 2px solid rgba(236, 72, 153, 0.2);
    }
    
    /* ===== BANK INFO DISPLAY ===== */
    .bank-info {
        background: linear-gradient(135deg, #1F2937 0%, #374151 100%);
        color: white;
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .bank-info::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
    }
    
    .bank-detail {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: var(--radius-md);
        margin: 1rem 0;
        border-left: 4px solid var(--accent-emerald);
    }
    
    /* ===== PRICE DISPLAY ===== */
    .price-display {
        text-align: center;
        padding: 2rem;
    }
    
    .old-price {
        font-size: 1.5rem;
        color: var(--neutral-gray);
        text-decoration: line-through;
        margin-bottom: 0.5rem;
    }
    
    .new-price {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, var(--accent-gold), #F59E0B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
        line-height: 1;
    }
    
    .saving-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--accent-emerald), #059669);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    /* ===== UTILITY CLASSES ===== */
    .text-center { text-align: center; }
    .text-right { text-align: right; }
    .mb-1 { margin-bottom: 0.5rem; }
    .mb-2 { margin-bottom: 1rem; }
    .mb-3 { margin-bottom: 1.5rem; }
    .mb-4 { margin-bottom: 2rem; }
    .mt-2 { margin-top: 1rem; }
    .mt-3 { margin-top: 1.5rem; }
    .mt-4 { margin-top: 2rem; }
    
    /* ===== HIDE DEFAULTS ===== */
    #MainMenu, footer, header { 
        visibility: hidden !important;
        height: 0 !important;
    }
    
    /* ===== MOBILE OPTIMIZATION ===== */
    @media (max-width: 768px) {
        .header-title { font-size: 2.2rem; }
        .header-subtitle { font-size: 1rem; }
        .nav-bar { flex-direction: column; gap: 1rem; padding: 1rem; }
        .nav-center { flex-wrap: wrap; justify-content: center; }
        .stRadio > div { flex-direction: column; }
        .stRadio > div > label { width: 100%; }
        .premium-card { padding: 1.5rem; }
        .new-price { font-size: 2.8rem; }
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* ===== BADGES ===== */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .badge-success {
        background: rgba(16, 185, 129, 0.1);
        color: var(--accent-emerald);
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .badge-warning {
        background: rgba(245, 158, 11, 0.1);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
    
    .badge-purple {
        background: rgba(139, 92, 246, 0.1);
        color: var(--primary-purple);
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

load_premium_css()

# ==================== AI ENGINE - NÂNG CẤP ====================
class EmotionalAI:
    def __init__(self):
        self.situations = {
            "Làm quen": {
                "Nam→Nữ": [
                    "Chào bạn, mình là {name} từ {context}. Mình thấy {detail} và muốn làm quen nếu không phiền. Hôm nay của bạn thế nào? ☕",
                    "Xin chào, hy vọng tin nhắn này không làm phiền. Mình ấn tượng với {impression} của bạn. Công việc của bạn dạo này ổn chứ? 💼",
                    "Chào bạn, mình vừa nghĩ đến cuộc trò chuyện của chúng ta. Hy vọng bạn có một ngày tốt lành. Có gì mới không? ✨"
                ],
                "Nữ→Nam": [
                    "Chào anh, em là {name} đây. Cảm ơn anh vì {reason}. Anh có vài phút trò chuyện không? 🌸",
                    "Xin chào, em thấy anh rất {trait}. Em muốn làm quen nếu anh không ngại. Anh đang bận gì không? 🤗",
                    "Chào anh, hy vọng anh có một ngày hiệu quả. Em có chút thắc mắc về {topic}, có thể hỏi ý kiến anh không? 💭"
                ]
            },
            
            "Hỏi thăm": {
                "Nam→Nữ": [
                    "Dạo này bạn thế nào? Công việc có ổn không? Nếu có gì cần chia sẻ, mình luôn sẵn sàng lắng nghe. 🌿",
                    "Chào bạn, mình nhớ đến bạn và muốn hỏi thăm. Mọi thứ ổn chứ? Có gì mình có thể giúp không? 🤝",
                    "Hy vọng bạn có một ngày nhẹ nhàng. Công việc tuần này thế nào rồi? Nếu có áp lực gì, đừng ngại chia sẻ nhé. 💪"
                ],
                "Nữ→Nam": [
                    "Anh ơi, dạo này anh có khoẻ không? Công việc nhiều không? Nhớ chăm sóc sức khoẻ nhé. 🫂",
                    "Chào anh, em muốn hỏi thăm anh một chút. Mọi thứ ổn chứ? Có gì anh muốn tâm sự không? 🌻",
                    "Em nghĩ đến anh và muốn gửi lời hỏi thăm. Hy vọng anh đang có một ngày tốt lành. 🌞"
                ]
            },
            
            "An ủi": {
                "Nam→Nữ": [
                    "Mình biết bạn đang không ổn. Hãy nhớ rằng bạn không đơn độc. Mọi khó khăn rồi sẽ qua thôi. 🫂",
                    "Những ngày này sẽ qua. Hãy cho phép bản thân được cảm thấy, được mệt mỏi. Mình ở đây nếu bạn cần. 🌧️→🌈",
                    "Đôi khi trái tim cần những ngày mưa. Mình tin bạn đủ mạnh mẽ. Có gì cứ chia sẻ với mình nhé. 🌱"
                ],
                "Nữ→Nam": [
                    "Em biết anh đang rất mệt mỏi. Hãy nhớ chăm sóc bản thân nhé. Sức khoẻ và tinh thần quan trọng lắm. 💖",
                    "Anh đừng ôm đồm một mình. Em ở đây để lắng nghe và ủng hộ anh. Mọi thứ rồi sẽ ổn thôi. 🤲",
                    "Em thấy anh mệt. Hãy nghỉ ngơi một chút. Đừng quá khắt khe với bản thân, anh nhé. 🕊️"
                ]
            },
            
            "Tỏ tình": {
                "Nam→Nữ": [
                    "Anh không giỏi nói những lời hoa mỹ. Chỉ biết rằng mỗi ngày có em bên cạnh là điều bình yên nhất với anh. Cảm ơn em. 💞",
                    "Có những điều đơn giản làm anh hạnh phúc: nụ cười của em, cách em quan tâm, và cả những im lặng bên nhau. 🍃",
                    "Tình cảm anh dành cho em không phải lời hứa xa xôi, mà là sự trân trọng từng ngày được bên em. 🏡"
                ],
                "Nữ→Nam": [
                    "Em không biết nói thế nào, chỉ biết rằng mỗi ngày có anh là một món quà. Cảm ơn anh vì tất cả. 🌸",
                    "Yêu anh là chọn nhau mỗi ngày, là thấu hiểu sau những bất đồng, là cùng nhau trưởng thành. Em biết ơn vì điều đó. 🌻",
                    "Với em, tình yêu không phải những lời lớn lao, mà là những điều nhỏ bé anh dành cho em mỗi ngày. 💝"
                ]
            },
            
            "Làm hoà": {
                "Nam→Nữ": [
                    "Anh xin lỗi vì đã làm em buồn. Dù có chuyện gì, tình cảm anh dành cho em không thay đổi. Chúng ta cùng tìm cách giải quyết nhé? 🕊️",
                    "Anh biết mình đã sai. Anh không muốn vì hiểu lầm mà làm tổn thương em. Em cho anh cơ hội được nói chuyện không? 🙏",
                    "Dù có bất đồng, anh vẫn yêu em. Chúng ta hãy cùng nhau vượt qua. Anh sẵn sàng lắng nghe và thay đổi. 💞"
                ],
                "Nữ→Nam": [
                    "Em xin lỗi vì đã để cảm xúc chi phối. Em không muốn chúng ta xa cách. Anh cho em cơ hội được giải thích nhé? 🌹",
                    "Em biết mình đã sai. Tình cảm của chúng ta quan trọng hơn bất kỳ tranh cãi nào. Chúng ta cùng tìm cách hoà giải nhé? 🤝",
                    "Dù có bất đồng, em vẫn trân trọng anh. Em không muốn mất anh vì những chuyện không đáng. Chúng ta nói chuyện được không? 💬"
                ]
            }
        }
    
    def generate(self, user_gender, target_gender, situation, context=""):
        """Tạo tin nhắn cảm xúc"""
        # Xác định key
        gender_key = f"{user_gender}→{target_gender}"
        
        # Lấy templates
        if situation in self.situations and gender_key in self.situations[situation]:
            templates = self.situations[situation][gender_key]
        else:
            # Fallback
            templates = ["Xin chào, hy vọng bạn có một ngày tốt lành. 💬"]
        
        # Chọn ngẫu nhiên
        template = random.choice(templates)
        
        # Cá nhân hoá
        if context:
            # Tách context thành các phần
            words = context.split()
            name = "mình" if len(words) < 2 else words[0]
            detail = context[:50] + "..." if len(context) > 50 else context
            
            replacements = {
                "{name}": name,
                "{context}": "đây" if len(context) < 10 else context[:30] + "...",
                "{detail}": detail,
                "{impression}": "sự chia sẻ",
                "{reason}": "sự giúp đỡ",
                "{trait}": "tử tế",
                "{topic}": "điều này"
            }
            
            for key, value in replacements.items():
                if key in template:
                    template = template.replace(key, value)
        
        return template

# ==================== QUẢN LÝ DỮ LIỆU ====================
def validate_phone(phone):
    """Xác thực số điện thoại Việt Nam"""
    phone = re.sub(r'\D', '', phone)
    if 9 <= len(phone) <= 11 and phone.startswith('0'):
        return phone
    return None

def get_usage_count(phone):
    """Lấy số lượt đã dùng"""
    try:
        df = pd.read_csv(USAGE_FILE)
        user_data = df[df["phone"] == phone]
        return 0 if user_data.empty else int(user_data.iloc[0]["count"])
    except:
        return 0

def update_usage(phone):
    """Cập nhật lượt dùng"""
    try:
        df = pd.read_csv(USAGE_FILE)
    except:
        df = pd.DataFrame(columns=["phone", "count", "last_used"])
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if phone in df["phone"].values:
        df.loc[df["phone"] == phone, "count"] += 1
        df.loc[df["phone"] == phone, "last_used"] = now
    else:
        new_row = pd.DataFrame({
            "phone": [phone],
            "count": [1],
            "last_used": [now]
        })
        df = pd.concat([df, new_row], ignore_index=True)
    
    df.to_csv(USAGE_FILE, index=False)

def load_paid_users():
    """Load danh sách đã thanh toán"""
    try:
        with open(PAID_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_paid_user(phone):
    """Lưu người dùng đã thanh toán"""
    paid_users = load_paid_users()
    paid_users[phone] = {
        "activated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "plan": "premium_lifetime"
    }
    with open(PAID_FILE, "w") as f:
        json.dump(paid_users, f, indent=2)

# ==================== TRÌNH BÀY GIAO DIỆN ====================
def render_header():
    """Render header premium"""
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
    """Render navigation bar"""
    if 'phone' in st.session_state and st.session_state.phone:
        phone_display = st.session_state.phone[:4] + "***" + st.session_state.phone[-3:]
        
        # Tính lượt còn lại
        if st.session_state.paid:
            usage_display = "Premium ✅"
        else:
            remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
            usage_display = f"Còn {remaining}/{FREE_TRIAL_LIMIT} lượt"
        
        st.markdown(f"""
        <div class="nav-bar">
            <div class="nav-left">
                <span>🏠</span>
                <span>EMOTICONN AI</span>
            </div>
            <div class="nav-center">
                <span>👤 {phone_display}</span>
                <span>📊 {usage_display}</span>
                <span class="badge badge-purple">5 lượt miễn phí</span>
            </div>
            <button class="nav-button" onclick="window.location.href='?upgrade=true'">
                💎 Nâng cấp
            </button>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="nav-bar">
            <div class="nav-left">
                <span>🏠</span>
                <span>EMOTICONN AI</span>
            </div>
            <div class="nav-center">
                <span>⭐ 4.9/5 từ 2,500+ người dùng</span>
                <span class="badge badge-success">5 lượt dùng thử</span>
            </div>
            <div></div>
        </div>
        """, unsafe_allow_html=True)

def render_progress_bar():
    """Render progress bar cho lượt dùng thử"""
    if not st.session_state.paid:
        remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
        percentage = (st.session_state.usage_count / FREE_TRIAL_LIMIT) * 100
        
        st.markdown(f"""
        <div class="premium-card card-gradient">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <div>
                    <h4 style="margin: 0; color: var(--primary-purple);">🎯 Bạn đang dùng thử miễn phí</h4>
                    <p style="color: var(--text-secondary); margin: 0.2rem 0;">Còn <b style="color: var(--primary-purple);">{remaining}/{FREE_TRIAL_LIMIT}</b> lượt sử dụng</p>
                </div>
                <div class="badge badge-warning">Ưu đãi 5 lượt</div>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {percentage}%;"></div>
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">
                Mỗi tin nhắn đều được AI tạo riêng cho tình huống của bạn
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_bank_info():
    """Render thông tin ngân hàng"""
    st.markdown(f"""
    <div class="bank-info">
        <h3 style="color: white; margin-bottom: 1.5rem;">🏦 Thông Tin Chuyển Khoản</h3>
        
        <div class="bank-detail">
            <div style="display: grid; grid-template-columns: 150px 1fr; gap: 1rem; align-items: center;">
                <strong style="color: rgba(255, 255, 255, 0.9);">Ngân hàng:</strong>
                <span style="color: white; font-weight: 500;">{BANK_INFO['bank']}</span>
                
                <strong style="color: rgba(255, 255, 255, 0.9);">Số tài khoản:</strong>
                <span style="color: white; font-weight: 500; font-size: 1.1rem;">{BANK_INFO['account']}</span>
                
                <strong style="color: rgba(255, 255, 255, 0.9);">Chủ tài khoản:</strong>
                <span style="color: white; font-weight: 500;">{BANK_INFO['name']}</span>
                
                <strong style="color: rgba(255, 255, 255, 0.9);">Số tiền:</strong>
                <span style="color: white; font-weight: 500;">149.000 VND</span>
                
                <strong style="color: rgba(255, 255, 255, 0.9);">Nội dung:</strong>
                <span style="color: white; font-weight: 500; background: rgba(255, 255, 255, 0.1); padding: 0.5rem; border-radius: var(--radius-sm);">
                    {BANK_INFO['note_format']}
                </span>
            </div>
        </div>
        
        <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: var(--radius-sm); margin-top: 1rem;">
            <p style="color: rgba(255, 255, 255, 0.9); margin: 0; font-size: 0.9rem;">
                <strong>📌 Ví dụ:</strong> Nếu SĐT của bạn là <strong>0912345678</strong><br>
                → Nội dung chuyển khoản: <code style="background: rgba(0,0,0,0.2); padding: 2px 6px; border-radius: 4px;">EMOTICONN 0912345678</code>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_payment_success():
    """Render thành công thanh toán"""
    st.markdown(f"""
    <div class="premium-card card-emerald" style="text-align: center;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
        <h2 style="color: var(--accent-emerald); margin-bottom: 1rem;">Chúc Mừng! Nâng Cấp Thành Công</h2>
        
        <div style="background: rgba(16, 185, 129, 0.1); padding: 1.5rem; border-radius: var(--radius-md); margin: 1.5rem 0;">
            <p style="margin: 0.5rem 0;"><strong>Số điện thoại:</strong> {st.session_state.phone}</p>
            <p style="margin: 0.5rem 0;"><strong>Thời gian kích hoạt:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            <p style="margin: 0.5rem 0;"><strong>Gói:</strong> Premium Trọn Đời ✅</p>
        </div>
        
        <h4 style="color: var(--text-primary); margin-bottom: 1rem;">🔥 Bây giờ bạn có thể:</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem;">∞</div>
                <p>Tin nhắn không giới hạn</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">📚</div>
                <p>7,000+ tình huống</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">🤗</div>
                <p>Hỗ trợ 24/7</p>
            </div>
        </div>
        
        <button onclick="window.location.href='?'" 
                style="background: linear-gradient(135deg, var(--accent-emerald) 0%, #059669 100%); 
                       color: white; border: none; padding: 1rem 3rem; 
                       border-radius: var(--radius-md); cursor: pointer; 
                       font-weight: 600; font-size: 1.1rem; margin-top: 1rem;">
            💬 Bắt đầu tạo tin nhắn
        </button>
    </div>
    """, unsafe_allow_html=True)

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
    
    # Kiểm tra query params
    query_params = st.query_params
    show_upgrade = query_params.get("upgrade") == "true"
    
    # Render header
    render_header()
    render_navigation()
    
    # ===== XỬ LÝ VERIFICATION =====
    if not st.session_state.verified and not show_upgrade:
        render_verification_section()
        return
    
    # ===== XỬ LÝ UPGRADE PAGE =====
    if show_upgrade:
        render_upgrade_page()
        return
    
    # ===== MAIN APP =====
    # Kiểm tra nếu đã hết lượt và chưa nâng cấp
    if not st.session_state.paid:
        remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
        if remaining <= 0:
            st.session_state.current_tab = "upgrade"
            st.query_params["upgrade"] = "true"
            st.rerun()
    
    # Hiển thị progress bar
    if not st.session_state.paid:
        render_progress_bar()
    
    # Hiển thị giao diện chính
    render_main_interface()

def render_verification_section():
    """Render trang đăng ký dùng thử"""
    st.markdown("""
    <div class="premium-card" style="text-align: center;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🔓</div>
        <h2 style="color: var(--primary-purple); margin-bottom: 0.5rem;">Bắt Đầu Dùng Thử Miễn Phí</h2>
        <p style="color: var(--text-secondary); margin-bottom: 2rem;">
            Nhận ngay <strong style="color: var(--primary-purple);">5 tin nhắn AI tinh tế</strong> hoàn toàn miễn phí
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input số điện thoại
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        phone_input = st.text_input(
            "**Số điện thoại của bạn**",
            placeholder="0912345678",
            help="Nhập số điện thoại Việt Nam để bắt đầu",
            key="verification_input"
        )
    
    # Nút xác nhận
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ **NHẬN 5 TIN MIỄN PHÍ**", key="verify_btn", use_container_width=True):
            if phone_input:
                valid_phone = validate_phone(phone_input)
                if valid_phone:
                    st.session_state.phone = valid_phone
                    st.session_state.verified = True
                    
                    # Kiểm tra đã thanh toán chưa
                    paid_users = load_paid_users()
                    if valid_phone in paid_users:
                        st.session_state.paid = True
                    else:
                        st.session_state.usage_count = get_usage_count(valid_phone)
                    
                    st.success("✅ **Kết nối thành công!** Bắt đầu tạo tin nhắn ngay.")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("⚠️ Số điện thoại chưa đúng. Vui lòng nhập số Việt Nam (ví dụ: 0912345678)")
            else:
                st.warning("📱 Hãy nhập số điện thoại để bắt đầu")
    
    # Hiển thị features
    st.markdown("""
    <div class="premium-card card-gradient">
        <h4 style="text-align: center; color: var(--primary-purple); margin-bottom: 2rem;">✨ Tại Sao Chọn EMOTICONN AI?</h4>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; color: var(--primary-purple); margin-bottom: 0.5rem;">🎯</div>
                <h5 style="margin-bottom: 0.5rem;">Dành cho người trưởng thành</h5>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">Ngôn từ tinh tế, sâu sắc, không sáo rỗng</p>
            </div>
            
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; color: var(--primary-pink); margin-bottom: 0.5rem;">💝</div>
                <h5 style="margin-bottom: 0.5rem;">7,000+ tình huống thực tế</h5>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">Hiểu mọi ngữ cảnh giao tiếp phức tạp</p>
            </div>
            
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; color: var(--accent-gold); margin-bottom: 0.5rem;">🔥</div>
                <h5 style="margin-bottom: 0.5rem;">5 lượt dùng thử miễn phí</h5>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">Trải nghiệm chất lượng trước khi quyết định</p>
            </div>
            
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; color: var(--accent-emerald); margin-bottom: 0.5rem;">💎</div>
                <h5 style="margin-bottom: 0.5rem;">Giá trị trọn đời</h5>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">Chỉ 149K - Dùng mãi mãi, cập nhật miễn phí</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_main_interface():
    """Render giao diện chính tạo tin nhắn"""
    st.markdown("""
    <div class="premium-card card-gradient">
        <h2 style="color: var(--primary-purple); margin-bottom: 0.5rem;">🎯 Tạo Tin Nhắn Tinh Tế</h2>
        <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
            Chia sẻ tình huống của bạn, để AI giúp bạn diễn đạt cảm xúc một cách chân thành
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Phần lựa chọn
    col1, col2 = st.columns(2)
    
    with col1:
        user_gender = st.radio(
            "**Bạn là:**",
            ["Nam", "Nữ"],
            horizontal=True,
            key="user_gender"
        )
    
    with col2:
        target_gender = st.radio(
            "**Gửi cho:**",
            ["Nam", "Nữ"],
            horizontal=True,
            key="target_gender"
        )
    
    # Chọn tình huống
    situation_options = ["Làm quen", "Hỏi thăm", "An ủi", "Tỏ tình", "Làm hoà"]
    situation = st.selectbox(
        "**Chọn tình huống:**",
        situation_options,
        key="situation"
    )
    
    # Thêm chi tiết
    context = st.text_area(
        "**Thêm chi tiết (tuỳ chọn):**",
        placeholder="Ví dụ: Chúng ta mới quen được 1 tuần, cô ấy là giáo viên 35 tuổi...\nHoặc: Anh ấy đang stress vì công việc, tôi muốn an ủi...",
        height=100,
        help="Càng chi tiết, tin nhắn càng cá nhân hoá",
        key="context"
    )
    
    # Nút tạo tin nhắn
    if st.button("✨ **TẠO TIN NHẮN TINH TẾ**", key="generate_btn", use_container_width=True):
        if not st.session_state.paid:
            # Cập nhật lượt dùng
            st.session_state.usage_count += 1
            update_usage(st.session_state.phone)
            remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
            
            if remaining < 0:
                st.error("🌸 Bạn đã hết lượt dùng thử miễn phí")
                st.query_params["upgrade"] = "true"
                st.rerun()
        
        # Tạo tin nhắn
        ai = EmotionalAI()
        with st.spinner("🤗 AI đang thấu hiểu cảm xúc và tạo tin nhắn chân thành cho bạn..."):
            time.sleep(1.5)
            result = ai.generate(user_gender, target_gender, situation, context)
            st.session_state.result = result
        
        # Scroll to result
        st.markdown("<div id='result'></div>", unsafe_allow_html=True)
    
    # Hiển thị kết quả
    if st.session_state.result:
        st.markdown("""
        <div class="message-display">
            <h4 style="color: var(--primary-purple); margin-bottom: 1.5rem;">💌 Tin Nhắn Gợi Ý</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Hiển thị tin nhắn
        st.markdown(f"""
        <div style="padding: 0 1rem 2rem 1rem;">
            <p style="font-size: 1.2rem; line-height: 1.8; color: var(--text-primary);">
                {st.session_state.result}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Nút hành động
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 **Copy tin nhắn**", use_container_width=True):
                st.success("✅ Đã copy tin nhắn vào clipboard!")
        
        with col2:
            if st.button("🔄 **Tạo tin khác**", use_container_width=True):
                st.session_state.result = ""
                st.rerun()
        
        with col3:
            if st.button("💾 **Lưu lại**", use_container_width=True):
                st.info("✨ Tin nhắn đã được lưu trong phiên làm việc")
        
        # Hiển thị lượt còn lại
        if not st.session_state.paid:
            remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
            if remaining <= 2:
                st.markdown(f"""
                <div class="premium-card card-gold" style="margin-top: 2rem;">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="font-size: 2rem;">🔥</div>
                        <div style="flex: 1;">
                            <h4 style="margin-bottom: 0.2rem; color: #D97706;">Chỉ còn {remaining} lượt dùng thử!</h4>
                            <p style="color: var(--text-secondary); margin-bottom: 0.5rem;">
                                Nâng cấp ngay để không giới hạn tin nhắn tinh tế
                            </p>
                            <button onclick="window.location.href='?upgrade=true'" 
                                    style="background: linear-gradient(135deg, var(--accent-gold) 0%, #F59E0B 100%); 
                                           color: #1F2937; border: none; padding: 0.5rem 1.5rem; 
                                           border-radius: var(--radius-md); cursor: pointer; 
                                           font-weight: 600;">
                                💎 Xem ưu đãi nâng cấp
                            </button>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def render_upgrade_page():
    """Render trang nâng cấp"""
    st.markdown("""
    <div class="premium-card" style="text-align: center;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">💎</div>
        <h2 style="color: var(--primary-purple); margin-bottom: 0.5rem;">Nâng Cấp Tài Khoản Premium</h2>
        <p style="color: var(--text-secondary); margin-bottom: 2rem;">
            Mở khóa toàn bộ tính năng cao cấp với mức giá cực kỳ ưu đãi
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hiển thị giá
    st.markdown("""
    <div class="price-display">
        <div class="old-price">~~199.000đ~~</div>
        <div class="new-price">149.000đ</div>
        <div class="saving-badge">Tiết kiệm 50.000đ (25%)</div>
        <p style="color: var(--text-secondary); margin-top: 1rem;">
            Thanh toán một lần - Dùng mãi mãi
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Lợi ích
    st.markdown("""
    <div class="premium-card card-gradient">
        <h4 style="text-align: center; color: var(--primary-purple); margin-bottom: 1.5rem;">🎁 Bạn Sẽ Nhận Được</h4>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
            <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                <div style="color: var(--accent-emerald); font-size: 1.5rem;">✓</div>
                <div>
                    <h5 style="margin-bottom: 0.25rem;">Không giới hạn tin nhắn</h5>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">Tạo bao nhiêu tin nhắn tùy thích</p>
                </div>
            </div>
            
            <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                <div style="color: var(--accent-emerald); font-size: 1.5rem;">✓</div>
                <div>
                    <h5 style="margin-bottom: 0.25rem;">7,000+ tình huống</h5>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">Mọi ngữ cảnh giao tiếp phức tạp</p>
                </div>
            </div>
            
            <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                <div style="color: var(--accent-emerald); font-size: 1.5rem;">✓</div>
                <div>
                    <h5 style="margin-bottom: 0.25rem;">Hỗ trợ tư vấn 24/7</h5>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">Đội ngũ chuyên gia tâm lý</p>
                </div>
            </div>
            
            <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                <div style="color: var(--accent-emerald); font-size: 1.5rem;">✓</div>
                <div>
                    <h5 style="margin-bottom: 0.25rem;">Cập nhật trọn đời</h5>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">Luôn có tính năng mới</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hiển thị thông tin ngân hàng
    render_bank_info()
    
    # Xác nhận thanh toán
    st.markdown("### ✅ Xác Nhận Thanh Toán")
    st.markdown("""
    <div class="premium-card" style="text-align: center;">
        <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
            Sau khi chuyển khoản, nhập số điện thoại của bạn để kích hoạt ngay
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input xác nhận
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        confirm_phone = st.text_input(
            "**Nhập số điện thoại của bạn:**",
            placeholder="0912345678",
            key="confirm_phone"
        )
    
    # Nút xác nhận
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔓 **TÔI ĐÃ CHUYỂN KHOẢN - MỞ KHÓA NGAY**", key="confirm_payment", use_container_width=True):
            if confirm_phone:
                valid_phone = validate_phone(confirm_phone)
                
                if valid_phone and valid_phone == st.session_state.phone:
                    # Lưu thông tin thanh toán
                    save_paid_user(valid_phone)
                    st.session_state.paid = True
                    
                    # Hiển thị thành công
                    render_payment_success()
                    
                    # Tự động chuyển trang sau 5 giây
                    time.sleep(5)
                    st.query_params.clear()
                    st.rerun()
                else:
                    st.error("⚠️ Số điện thoại không khớp. Vui lòng nhập đúng số đã đăng ký.")
            else:
                st.warning("📱 Vui lòng nhập số điện thoại để xác nhận")
    
    # Bảo đảm
    st.markdown("""
    <div class="premium-card" style="text-align: center; margin-top: 2rem;">
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div>
                <div style="font-size: 2rem;">🔒</div>
                <p style="font-weight: 500; margin: 0.25rem 0;">Hoàn tiền 7 ngày</p>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">Nếu không hài lòng</p>
            </div>
            <div>
                <div style="font-size: 2rem;">📞</div>
                <p style="font-weight: 500; margin: 0.25rem 0;">Hỗ trợ 24/7</p>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">090-xxx-xxxx</p>
            </div>
            <div>
                <div style="font-size: 2rem;">⭐</div>
                <p style="font-weight: 500; margin: 0.25rem 0;">4.9/5 đánh giá</p>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">2,500+ người dùng</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Nút quay lại
    if st.button("← Quay lại trang chính", key="back_home"):
        st.query_params.clear()
        st.rerun()

if __name__ == "__main__":
    main()
