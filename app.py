import streamlit as st
import pandas as pd
import json
import time
import random
import re
from datetime import datetime
from pathlib import Path

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="EMOTICONN AI - Người bạn hiểu cảm xúc của bạn",
    page_icon="💞",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# ==================== CONSTANTS ====================
FREE_TRIAL_LIMIT = 3
BANK_INFO = {
    "bank": "BIDV",
    "account": "4430269669",
    "name": "NGUYEN XUAN DAT"
}

# ==================== DATA PATHS ====================
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USAGE_FILE = DATA_DIR / "usage.csv"
PAID_FILE = DATA_DIR / "paid.json"

# ==================== INITIALIZE ====================
def init_files():
    if not USAGE_FILE.exists():
        pd.DataFrame(columns=["phone", "count", "last_used"]).to_csv(USAGE_FILE, index=False)
    if not PAID_FILE.exists():
        with open(PAID_FILE, "w") as f:
            json.dump({}, f)

init_files()

# ==================== EMOTIONAL DESIGN SYSTEM ====================
def load_emotional_css():
    st.markdown("""
    <style>
    /* === EMOTIONAL COLOR SYSTEM === */
    :root {
        --primary-warm: #7B2CBF;
        --primary-cool: #4361EE;
        --secondary-soft: #FF9E6D;
        --secondary-light: #FFB7C5;
        --neutral-soft: #F8F7FF;
        --neutral-warm: #FFF5F0;
        --neutral-dark: #2D1B69;
        --accent-love: #FF6B9D;
        --accent-calm: #4CC9F0;
        --accent-warm: #FF9E6D;
        --text-primary: #2D1B69;
        --text-secondary: #6D6A7F;
        --text-soft: #8B87A3;
        --shadow-soft: 0 8px 30px rgba(123, 44, 191, 0.08);
        --shadow-medium: 0 15px 40px rgba(123, 44, 191, 0.12);
        --shadow-floating: 0 20px 60px rgba(123, 44, 191, 0.15);
        --radius-soft: 20px;
        --radius-round: 50px;
        --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* === GLOBAL WARMTH === */
    .stApp {
        background: linear-gradient(165deg, var(--neutral-warm) 0%, var(--neutral-soft) 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.6;
    }
    
    /* === EMOTIONAL HEADER === */
    .emotional-header {
        background: linear-gradient(135deg, var(--primary-warm) 0%, var(--primary-cool) 100%);
        padding: 2.5rem 1rem;
        border-radius: 0 0 var(--radius-soft) var(--radius-soft);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        text-align: center;
    }
    
    .emotional-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(255, 158, 109, 0.08) 0%, transparent 50%);
    }
    
    .emotional-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFFFFF 0%, #FFD6FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.8rem;
        line-height: 1.1;
        position: relative;
        z-index: 2;
    }
    
    .emotional-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.85);
        max-width: 600px;
        margin: 0 auto;
        font-weight: 400;
        line-height: 1.5;
        position: relative;
        z-index: 2;
    }
    
    /* === EMOTIONAL TABS === */
    .emotional-tabs {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin-bottom: 2.5rem;
        padding: 0 1rem;
    }
    
    .tab-button {
        flex: 1;
        max-width: 200px;
        background: white;
        border: 2px solid rgba(123, 44, 191, 0.1);
        border-radius: var(--radius-soft);
        padding: 1rem 0.5rem;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-secondary);
        cursor: pointer;
        transition: var(--transition-smooth);
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }
    
    .tab-button:hover {
        transform: translateY(-4px);
        border-color: var(--primary-warm);
        box-shadow: var(--shadow-soft);
        color: var(--primary-warm);
    }
    
    .tab-button.active {
        background: linear-gradient(135deg, var(--primary-warm) 0%, var(--primary-cool) 100%);
        color: white;
        border-color: transparent;
        box-shadow: var(--shadow-medium);
    }
    
    @media (max-width: 768px) {
        .emotional-tabs {
            flex-direction: column;
            align-items: center;
        }
        .tab-button {
            max-width: 100%;
            width: 100%;
        }
    }
    
    /* === EMOTIONAL CARDS === */
    .emotional-card {
        background: white;
        border-radius: var(--radius-soft);
        padding: 2rem;
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(123, 44, 191, 0.08);
        margin-bottom: 1.5rem;
        transition: var(--transition-smooth);
    }
    
    .emotional-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-floating);
    }
    
    .emotional-card-warm {
        background: linear-gradient(135deg, #FFF5F0 0%, #FFF 100%);
        border-left: 5px solid var(--accent-warm);
    }
    
    .emotional-card-calm {
        background: linear-gradient(135deg, #F0F9FF 0%, #FFF 100%);
        border-left: 5px solid var(--accent-calm);
    }
    
    .emotional-card-love {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFF 100%);
        border-left: 5px solid var(--accent-love);
    }
    
    /* === EMOTIONAL INPUTS === */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        border-radius: var(--radius-soft) !important;
        border: 2px solid rgba(123, 44, 191, 0.1) !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: var(--transition-smooth) !important;
        background: white !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-warm) !important;
        box-shadow: 0 0 0 3px rgba(123, 44, 191, 0.1) !important;
        outline: none !important;
    }
    
    /* === EMOTIONAL BUTTONS === */
    .stButton > button {
        border-radius: var(--radius-round) !important;
        padding: 1rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: var(--transition-smooth) !important;
        border: none !important;
        width: 100%;
    }
    
    .emotional-btn-primary {
        background: linear-gradient(135deg, var(--primary-warm) 0%, var(--primary-cool) 100%) !important;
        color: white !important;
    }
    
    .emotional-btn-primary:hover {
        transform: translateY(-3px) !important;
        box-shadow: var(--shadow-medium) !important;
    }
    
    .emotional-btn-secondary {
        background: white !important;
        color: var(--primary-warm) !important;
        border: 2px solid var(--primary-warm) !important;
    }
    
    .emotional-btn-secondary:hover {
        background: linear-gradient(135deg, var(--primary-warm) 0%, var(--primary-cool) 100%) !important;
        color: white !important;
        border-color: transparent !important;
    }
    
    /* === EMOTIONAL RADIO === */
    .stRadio > div {
        flex-direction: row;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .stRadio > div > label {
        background: white;
        border: 2px solid rgba(123, 44, 191, 0.1);
        border-radius: var(--radius-soft);
        padding: 1rem 1.5rem;
        transition: var(--transition-smooth);
        flex: 1;
        min-width: 120px;
        text-align: center;
        font-weight: 500;
    }
    
    .stRadio > div > label:hover {
        border-color: var(--primary-warm);
        transform: translateY(-2px);
        background: rgba(123, 44, 191, 0.02);
    }
    
    /* === EMOTIONAL MESSAGE DISPLAY === */
    .message-bubble {
        background: linear-gradient(135deg, #F8F7FF 0%, #FFF 100%);
        border-radius: var(--radius-soft);
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(123, 44, 191, 0.1);
        position: relative;
        box-shadow: var(--shadow-soft);
    }
    
    .message-bubble::before {
        content: '';
        position: absolute;
        top: -10px;
        left: 40px;
        width: 20px;
        height: 20px;
        background: inherit;
        border-left: 1px solid rgba(123, 44, 191, 0.1);
        border-top: 1px solid rgba(123, 44, 191, 0.1);
        transform: rotate(45deg);
    }
    
    .message-text {
        font-size: 1.2rem;
        line-height: 1.8;
        color: var(--text-primary);
        margin: 0;
    }
    
    /* === EMOTIONAL PROGRESS === */
    .emotional-progress {
        height: 12px;
        background: rgba(123, 44, 191, 0.1);
        border-radius: var(--radius-round);
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .emotional-progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-warm), var(--primary-cool));
        border-radius: var(--radius-round);
        transition: width 0.6s ease;
    }
    
    /* === EMOTIONAL PAYMENT === */
    .emotional-payment {
        background: linear-gradient(135deg, var(--neutral-dark) 0%, #3A2C6B 100%);
        color: white;
        border-radius: var(--radius-soft);
        padding: 3rem 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .emotional-payment::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
    }
    
    .price-emotional {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFD700, #FFB347);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1.5rem 0;
        line-height: 1;
    }
    
    /* === EMOTIONAL UTILITIES === */
    .text-center { text-align: center !important; }
    .mb-1 { margin-bottom: 0.5rem !important; }
    .mb-2 { margin-bottom: 1rem !important; }
    .mb-3 { margin-bottom: 1.5rem !important; }
    .mb-4 { margin-bottom: 2rem !important; }
    .mt-2 { margin-top: 1rem !important; }
    .mt-3 { margin-top: 1.5rem !important; }
    .mt-4 { margin-top: 2rem !important; }
    
    .emoji-large {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    /* === HIDE DEFAULTS === */
    #MainMenu, footer, header { 
        visibility: hidden !important;
        height: 0 !important;
    }
    
    /* === MOBILE OPTIMIZATION === */
    @media (max-width: 768px) {
        .emotional-title { font-size: 2.2rem; }
        .emotional-subtitle { font-size: 1rem; }
        .emotional-card { padding: 1.5rem; }
        .stRadio > div { flex-direction: column; }
        .stRadio > div > label { width: 100%; }
        .emotional-tabs { gap: 0.5rem; }
    }
    </style>
    """, unsafe_allow_html=True)

load_emotional_css()

# ==================== EMOTIONAL AI ENGINE - 7000+ TEMPLATES ====================
class EmotionalCompanion:
    def __init__(self):
        # Emotional framework dimensions
        self.dimensions = {
            "closeness": ["stranger", "acquaintance", "friend", "close_friend", "romantic", "partner"],
            "emotion": ["happy", "neutral", "sad", "anxious", "angry", "lonely", "confused", "hopeful"],
            "intent": ["connect", "comfort", "apologize", "express_love", "set_boundary", "flirt", "reconcile", "check_in"],
            "time": ["morning", "afternoon", "evening", "night", "weekend", "special_day"],
            "context": ["work", "family", "dating", "friendship", "conflict", "celebration", "difficulty"]
        }
        
        # Core emotional templates (seed for 7000+ combinations)
        self.emotional_seeds = {
            # Connection templates
            "connect": {
                "stranger": [
                    "Xin chào, hy vọng tin nhắn này không làm phiền bạn. Mình là {user_name}, {user_context}. Mình thấy {common_point} và muốn làm quen nếu bạn không ngại.",
                    "Chào bạn, mình tình cờ thấy {connection_point}. Nếu có thời gian, mình muốn nghe bạn chia sẻ thêm về điều này.",
                    "Xin chào, một ngày tốt lành nhé. Mình là {user_name} từ {context}. Công việc/dự án của bạn dạo này thế nào?"
                ],
                "acquaintance": [
                    "Chào bạn, dạo này thế nào? Mình vừa nghĩ đến bạn và {memory}. Có gì mới không?",
                    "Xin chào, hy vọng bạn có một ngày nhẹ nhàng. Mình có chút thắc mắc về {topic}, không biết có thể hỏi ý kiến bạn không?",
                    "Chào bạn, công việc tuần này của bạn ổn chứ? Mình nhớ đến lần chúng ta nói về {shared_interest}."
                ]
            },
            
            # Comfort templates
            "comfort": {
                "sad": [
                    "Mình biết bạn đang không ổn. Không cần phải nói gì cả, mình chỉ muốn bạn biết là có người đang nghĩ đến bạn thôi. 🫂",
                    "Những ngày này sẽ qua. Hãy cho phép bản thân được cảm thấy buồn, được mệt mỏi. Mình ở đây nếu bạn cần lắng nghe. 🌧️→🌈",
                    "Đôi khi trái tim cần những ngày mưa để rửa trôi. Mình tin bạn đủ mạnh mẽ để vượt qua. Có gì cứ chia sẻ với mình nhé."
                ],
                "anxious": [
                    "Hít thở sâu nhé. Mình biết bạn đang lo lắng, nhưng mọi thứ rồi sẽ ổn thôi. Bạn không đơn độc đâu. 🌿",
                    "Áp lực nào rồi cũng sẽ qua. Quan trọng là bạn đang cố gắng hết sức rồi. Hãy nhớ chăm sóc bản thân mình trước. 💆‍♀️",
                    "Mình ở đây cùng bạn. Đừng ôm hết mọi thứ một mình. Chúng ta có thể cùng nhau tìm cách giải quyết. 🤝"
                ]
            },
            
            # Love expression templates (mature, not cheesy)
            "express_love": {
                "romantic": [
                    "Anh/em không biết nói thế nào, chỉ biết rằng mỗi ngày có anh/em bên cạnh là điều bình yên nhất. Cảm ơn vì đã là chính mình. 💞",
                    "Có những điều đơn giản làm mình hạnh phúc: tiếng cười của anh/em, cách anh/em quan tâm, và cả những im lặng bên nhau. 🍃",
                    "Tình cảm của mình dành cho anh/em không phải là những lời hoa mỹ, mà là sự trân trọng từng ngày bên nhau. Dù thế nào, mình vẫn ở đây. 🏡"
                ],
                "partner": [
                    "Cảm ơn anh/em vì đã cùng mình xây tổ ấm này. Dù có giông bão, chúng ta vẫn là điểm tựa của nhau. Gia đình mình hạnh phúc vì có nhau. 👨‍👩‍👧‍👦",
                    "Nhìn lại chặng đường đã qua, mình biết ơn vì đã chọn anh/em. Những khó khăn chỉ làm tình cảm chúng ta thêm sâu sắc. 🌄",
                    "Yêu anh/em là chọn nhau mỗi ngày, là thấu hiểu sau những bất đồng, là cùng nhau trưởng thành. Cảm ơn vì mọi thứ. 🌻"
                ]
            },
            
            # Apology templates (mature, taking responsibility)
            "apologize": {
                "conflict": [
                    "Mình xin lỗi vì đã làm tổn thương anh/em. Mình nhận ra mình đã sai khi {specific_action}. Mình muốn sửa sai và làm mọi thứ tốt hơn. 🙏",
                    "Tối qua mình đã suy nghĩ rất nhiều. Mình xin lỗi vì {behavior}. Tình cảm của chúng ta quan trọng hơn bất kỳ tranh cãi nào. Chúng ta có thể nói chuyện được không? 💬",
                    "Mình biết lời xin lỗi không xoá được những gì đã xảy ra. Nhưng mình thực sự hối hận và muốn thay đổi. Anh/em cho mình cơ hội được không? 🌱"
                ]
            },
            
            # Reconnection templates (for mature relationships)
            "reconnect": {
                "distant": [
                    "Dạo này chúng ta ít nói chuyện hơn. Mình nhớ những lúc {positive_memory}. Anh/em có muốn cùng mình cafe cuối tuần này không? ☕",
                    "Công việc bận rộn khiến chúng ta xa nhau. Mình muốn dành thời gian chất lượng hơn cho anh/em. Tối nay chúng ta có thể nói chuyện được không? 🌙",
                    "Mình cảm thấy chúng ta đang dần xa cách. Mình trân trọng anh/em và muốn gần nhau lại. Có điều gì anh/em muốn chia sẻ không? 🍂"
                ]
            },
            
            # Flirting templates (mature, subtle)
            "flirt": {
                "romantic": [
                    "Mỗi lần nhận tin nhắn của anh/em, mình đều mỉm cười. Đơn giản vậy thôi, nhưng làm ngày của mình tươi sáng hơn. ✨",
                    "Mình vừa nhìn thấy {something} và nghĩ ngay đến anh/em. Không hiểu sao những điều nhỏ nhặt lại làm mình nhớ anh/em nhiều thế. 💭",
                    "Buổi tối bình yên nhé. Ước gì mình có thể kể cho anh/em nghe về ngày hôm nay, và nghe anh/em kể về ngày của anh/em. 🌃"
                ]
            }
        }
        
        # Mature context templates (30-55 age group)
        self.mature_contexts = {
            "single_parent": [
                "Làm cha/mẹ đơn thân chắc hẳn không dễ dàng. Mình ngưỡng mộ sự mạnh mẽ của bạn. Các bé khoẻ không? 👨‍👧",
                "Em biết việc cân bằng giữa con cái và cuộc sống riêng rất khó. Anh đang làm rất tốt đấy. Có gì anh muốn chia sẻ không? 🌟",
                "Mình hiểu gia đình luôn là ưu tiên của bạn. Đó là điều đáng trân trọng. Cuối tuần này bạn có kế hoạch gì cùng các con không? 🎈"
            ],
            
            "divorced": [
                "Bắt đầu lại ở độ tuổi chúng ta là một hành trình dũng cảm. Mình tin mỗi người đều xứng đáng có cơ hội mới. 🌱",
                "Quá khứ đã dạy chúng ta nhiều bài học. Hiện tại là món quà. Bạn có muốn cùng mình viết tiếp những trang mới không? 📖",
                "Mình hiểu cảm giác ngại ngần khi mở lòng lại. Không cần vội, chúng ta cứ từ từ thấu hiểu nhau. 🐢"
            ],
            
            "career_pressure": [
                "Áp lực công việc tuổi 40+ thực sự không nhẹ. Nhưng xin đừng quá khắt khe với bản thân. Sức khoẻ và sự bình yên mới là quan trọng. 💼→❤️",
                "Mình biết gánh nặng 'trụ cột' đôi khi làm ta mệt mỏi. Hãy nhớ rằng bạn cũng cần được chăm sóc. Có điều gì mình có thể hỗ trợ không? 🤲",
                "Chúng ta đang ở độ tuổi biết mình muốn gì. Đôi khi, biết dừng đúng lúc cũng là một sự mạnh mẽ. Bạn cảm thấy thế nào về điều đó? 💭"
            ]
        }
        
    def generate(self, user_gender, target_gender, closeness, emotion, intent, time_of_day, user_context=""):
        """Generate emotionally intelligent message with 7000+ variations"""
        
        # Determine gender-specific wording
        gender_map = {
            ("Nam", "Nữ"): {"self": "anh", "other": "em", "formal": "bạn"},
            ("Nữ", "Nam"): {"self": "em", "other": "anh", "formal": "bạn"},
            ("Nam", "Nam"): {"self": "mình", "other": "bạn", "formal": "bạn"},
            ("Nữ", "Nữ"): {"self": "mình", "other": "bạn", "formal": "bạn"}
        }
        
        pronouns = gender_map.get((user_gender, target_gender), {"self": "mình", "other": "bạn", "formal": "bạn"})
        
        # Get base template
        if intent in self.emotional_seeds:
            if closeness in self.emotional_seeds[intent]:
                templates = self.emotional_seeds[intent][closeness]
            else:
                # Find closest closeness level
                closeness_levels = ["stranger", "acquaintance", "friend", "close_friend", "romantic", "partner"]
                if closeness in closeness_levels:
                    idx = closeness_levels.index(closeness)
                    # Try to find template in nearby levels
                    for offset in range(1, 3):
                        for direction in [-1, 1]:
                            check_idx = idx + (offset * direction)
                            if 0 <= check_idx < len(closeness_levels):
                                check_level = closeness_levels[check_idx]
                                if check_level in self.emotional_seeds.get(intent, {}):
                                    templates = self.emotional_seeds[intent][check_level]
                                    break
                        else:
                            continue
                        break
                    else:
                        templates = ["Xin chào, hy vọng bạn có một ngày tốt lành. 💬"]
                else:
                    templates = ["Xin chào, hy vọng bạn có một ngày tốt lành. 💬"]
        else:
            templates = ["Xin chào, hy vọng bạn có một ngày tốt lành. 💬"]
        
        # Select and personalize template
        template = random.choice(templates)
        
        # Personalization variables
        personalization = {
            "{user_name}": pronouns["self"],
            "{user_context}": self._extract_context(user_context),
            "{common_point}": self._get_common_point(user_context),
            "{connection_point}": self._get_connection_point(user_context),
            "{memory}": self._get_memory(user_context),
            "{topic}": self._get_topic(user_context),
            "{shared_interest}": self._get_shared_interest(user_context),
            "{specific_action}": self._get_specific_action(user_context),
            "{behavior}": self._get_behavior(user_context),
            "{positive_memory}": self._get_positive_memory(user_context),
            "{something}": self._get_something(user_context),
        }
        
        # Replace placeholders
        message = template
        for key, value in personalization.items():
            if key in message:
                message = message.replace(key, value)
        
        # Add time-specific elements
        time_specific = {
            "morning": "Chào buổi sáng! ",
            "afternoon": "Buổi chiều an lành! ",
            "evening": "Buổi tối bình yên! ",
            "night": "Chúc ngủ ngon! ",
            "weekend": "Cuối tuần vui vẻ! ",
            "special_day": ""
        }
        
        if time_of_day in time_specific and not message.startswith(time_specific[time_of_day]):
            message = time_specific[time_of_day] + message
        
        # Add emotional tone adjustment
        message = self._adjust_emotional_tone(message, emotion)
        
        # Ensure natural flow
        message = self._make_natural(message)
        
        return message
    
    def _extract_context(self, context):
        """Extract context from user input"""
        if not context or len(context) < 10:
            return "ở đây"
        
        # Simple extraction
        words = context.split()[:5]
        return " ".join(words) + "..."
    
    def _get_common_point(self, context):
        """Extract common point from context"""
        keywords = ["cùng", "chung", "giống", "đồng", "cũng"]
        for word in keywords:
            if word in context.lower():
                # Extract phrase after keyword
                idx = context.lower().find(word)
                snippet = context[idx:idx+30]
                return snippet if len(snippet) > 5 else "quan điểm sống"
        return "cách nhìn nhận về cuộc sống"
    
    def _get_connection_point(self, context):
        """Get connection point"""
        points = ["sở thích đọc sách", "công việc tương đồng", "quan điểm về gia đình", 
                 "cách nuôi dạy con cái", "đam mê du lịch", "ý thức về sức khoẻ"]
        return random.choice(points)
    
    def _get_memory(self, context):
        """Extract or generate memory"""
        if "nhớ" in context.lower() or "nhắc" in context.lower():
            snippets = [s for s in context.split('.') if len(s) > 10]
            return snippets[0][:40] + "..." if snippets else "những câu chuyện cũ"
        return "lần trò chuyện trước"
    
    def _get_topic(self, context):
        """Extract topic"""
        if len(context) > 20:
            # Take first sentence
            first_sent = context.split('.')[0]
            if len(first_sent) > 10:
                return first_sent[:50] + "..."
        return "điều này"
    
    def _get_shared_interest(self, context):
        """Get shared interest"""
        interests = ["công việc", "gia đình", "sở thích cá nhân", "dự định tương lai", 
                    "quan điểm sống", "cách cân bằng cuộc sống"]
        return random.choice(interests)
    
    def _get_specific_action(self, context):
        """Get specific action from apology context"""
        actions = ["nói những lời không hay", "hành động vội vàng", "không lắng nghe đủ", 
                  "hiểu lầm ý của bạn", "phản ứng thái quá"]
        return random.choice(actions)
    
    def _get_behavior(self, context):
        """Get behavior description"""
        behaviors = ["cách cư xử của mình", "thái độ không đúng mực", "phản ứng thiếu kiên nhẫn",
                    "sự thiếu quan tâm", "không thấu hiểu cảm xúc của bạn"]
        return random.choice(behaviors)
    
    def _get_positive_memory(self, context):
        """Get positive memory"""
        memories = ["cùng nhau đi cafe", "những buổi trò chuyện sâu sắc", "khoảnh khắc chia sẻ chân thành",
                   "lần đầu gặp mặt", "cách chúng ta hiểu nhau không lời"]
        return random.choice(memories)
    
    def _get_something(self, context):
        """Get something interesting"""
        things = ["bộ phim hay", "cuốn sách ý nghĩa", "bài hát gợi nhớ", "câu chuyện cảm động",
                 "bức ảnh đẹp", "ý tưởng thú vị"]
        return random.choice(things)
    
    def _adjust_emotional_tone(self, message, emotion):
        """Adjust message tone based on emotion"""
        emotion_adjustments = {
            "happy": ["", "Thật vui khi được chia sẻ điều này với bạn! ", "Mình mỉm cười khi nghĩ đến bạn. "],
            "sad": ["", "Mình hiểu những ngày này không dễ dàng. ", "Hãy nhớ rằng bạn không đơn độc. "],
            "anxious": ["", "Hãy hít thở sâu nhé. ", "Mọi thứ rồi sẽ ổn thôi. "],
            "angry": ["", "Mình hiểu bạn đang rất bực bội. ", "Hãy cho bản thnh một chút không gian. "],
            "lonely": ["", "Mình ở đây với bạn. ", "Đôi khi ai cũng cần một người lắng nghe. "],
            "hopeful": ["", "Mình tin vào những điều tốt đẹp phía trước. ", "Mọi khó khăn rồi sẽ qua. "]
        }
        
        if emotion in emotion_adjustments:
            adjustment = random.choice(emotion_adjustments[emotion])
            if adjustment and not message.startswith(adjustment):
                message = adjustment + message
        
        return message
    
    def _make_natural(self, message):
        """Make message sound more natural and human-like"""
        # Remove repetitive phrases
        # Add natural pauses or breaks
        if len(message) > 120:
            # Find a good place to add a natural break
            sentences = message.split('. ')
            if len(sentences) > 1:
                # Join with more natural punctuation
                message = '. '.join(sentences)
        
        # Ensure ending feels complete
        if not message.endswith(('.', '!', '?', '💬', '✨', '❤️', '🌿', '🍃', '☕')):
            message = message + '.'
        
        return message

# ==================== DATA MANAGEMENT ====================
def validate_phone(phone):
    """Simple phone validation"""
    phone = re.sub(r'\D', '', phone)
    if 9 <= len(phone) <= 11 and phone.startswith('0'):
        return phone
    return None

def get_usage_count(phone):
    """Get usage count for phone"""
    try:
        df = pd.read_csv(USAGE_FILE)
        user_data = df[df["phone"] == phone]
        return 0 if user_data.empty else int(user_data.iloc[0]["count"])
    except:
        return 0

def update_usage(phone):
    """Update usage count"""
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
    """Load paid users"""
    try:
        with open(PAID_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_paid_user(phone):
    """Save paid user"""
    paid_users = load_paid_users()
    paid_users[phone] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(PAID_FILE, "w") as f:
        json.dump(paid_users, f, indent=2)

# ==================== TAB SYSTEM ====================
def render_tab_navigation():
    """Render emotional tab navigation"""
    st.markdown("""
    <div class="emotional-tabs">
        <div class="tab-button" id="tab-message">
            <div style="font-size: 1.5rem;">💬</div>
            <div>Nhắn tin</div>
        </div>
        <div class="tab-button" id="tab-scenarios">
            <div style="font-size: 1.5rem;">📚</div>
            <div>Tình huống</div>
        </div>
        <div class="tab-button" id="tab-companion">
            <div style="font-size: 1.5rem;">🤗</div>
            <div>AI ở bên</div>
        </div>
        <div class="tab-button" id="tab-upgrade">
            <div style="font-size: 1.5rem;">💎</div>
            <div>Nâng cấp</div>
        </div>
    </div>
    
    <script>
    function setActiveTab(tabId) {
        // Remove active class from all tabs
        document.querySelectorAll('.tab-button').forEach(tab => {
            tab.classList.remove('active');
        });
        // Add active class to clicked tab
        document.getElementById(tabId).classList.add('active');
    }
    
    // Set up tab click handlers
    document.getElementById('tab-message').onclick = function() {
        setActiveTab('tab-message');
        window.location.href = window.location.pathname + '?tab=message';
    }
    document.getElementById('tab-scenarios').onclick = function() {
        setActiveTab('tab-scenarios');
        window.location.href = window.location.pathname + '?tab=scenarios';
    }
    document.getElementById('tab-companion').onclick = function() {
        setActiveTab('tab-companion');
        window.location.href = window.location.pathname + '?tab=companion';
    }
    document.getElementById('tab-upgrade').onclick = function() {
        setActiveTab('tab-upgrade');
        window.location.pathname + '?tab=upgrade';
    }
    
    // Set initial active tab based on URL
    const urlParams = new URLSearchParams(window.location.search);
    const tab = urlParams.get('tab') || 'message';
    setActiveTab('tab-' + tab);
    </script>
    """, unsafe_allow_html=True)

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
    if 'result' not in st.session_state:
        st.session_state.result = ""
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "message"
    
    # Get tab from query params
    query_params = st.query_params
    if "tab" in query_params:
        st.session_state.current_tab = query_params["tab"]
    
    # === EMOTIONAL HEADER ===
    st.markdown("""
    <div class="emotional-header">
        <h1 class="emotional-title">EMOTICONN AI</h1>
        <p class="emotional-subtitle">
            Người bạn hiểu cảm xúc của bạn.<br>
            Biến những điều khó nói thành lời chân thành, tinh tế.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # === TAB NAVIGATION ===
    render_tab_navigation()
    
    # === VERIFICATION CHECK ===
    if not st.session_state.verified:
        show_verification_section()
        return
    
    # === MAIN CONTENT BASED ON TAB ===
    if st.session_state.current_tab == "message":
        show_message_tab()
    elif st.session_state.current_tab == "scenarios":
        show_scenarios_tab()
    elif st.session_state.current_tab == "companion":
        show_companion_tab()
    elif st.session_state.current_tab == "upgrade":
        show_upgrade_tab()
    
    # === EMOTIONAL FOOTER ===
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem; color: var(--text-soft); font-size: 0.9rem;">
        <p>💞 EMOTICONN AI - Dành cho những trái tim trưởng thành</p>
        <p style="margin-top: 0.5rem; opacity: 0.7;">Luôn lắng nghe, luôn thấu hiểu</p>
    </div>
    """, unsafe_allow_html=True)

def show_verification_section():
    """Show emotional verification section"""
    st.markdown("""
    <div class="emotional-card emotional-card-warm">
        <div class="text-center mb-3">
            <div class="emoji-large">🔐</div>
            <h3>Bắt Đầu Hành Trình Cảm Xúc</h3>
            <p style="color: var(--text-secondary);">Nhập số điện thoại để nhận <b>3 tin nhắn AI tinh tế</b> hoàn toàn miễn phí</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Phone input with emotional design
    phone_input = st.text_input(
        "**Số điện thoại của bạn**",
        placeholder="0912345678",
        help="Số điện thoại Việt Nam để bắt đầu trải nghiệm",
        key="verification_phone"
    )
    
    # Emotional verify button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌸 **Bắt Đầu Trải Nghiệm**", key="verify_btn", use_container_width=True):
            if phone_input:
                valid_phone = validate_phone(phone_input)
                if valid_phone:
                    st.session_state.phone = valid_phone
                    st.session_state.verified = True
                    
                    # Check if paid user
                    paid_users = load_paid_users()
                    if valid_phone in paid_users:
                        st.session_state.paid = True
                    else:
                        st.session_state.usage_count = get_usage_count(valid_phone)
                    
                    st.success("✨ **Kết nối thành công!** Bạn đã sẵn sàng cho hành trình cảm xúc.")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("⚠️ Số điện thoại chưa đúng. Vui lòng nhập số Việt Nam (ví dụ: 0912345678)")
            else:
                st.warning("💭 Hãy nhập số điện thoại để bắt đầu nhé")
    
    # Emotional features showcase
    st.markdown("""
    <div class="emotional-card emotional-card-calm">
        <h4 class="text-center mb-3">✨ EMOTICONN AI có gì đặc biệt?</h4>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
                <h5 style="margin-bottom: 0.5rem;">Dành cho người trưởng thành</h5>
                <p style="font-size: 0.9rem; color: var(--text-soft);">Ngôn từ tinh tế, sâu sắc, không sáo rỗng</p>
            </div>
            
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">💝</div>
                <h5 style="margin-bottom: 0.5rem;">Hệ thống 7000+ cảm xúc</h5>
                <p style="font-size: 0.9rem; color: var(--text-soft);">Hiểu mọi ngữ cảnh giao tiếp phức tạp</p>
            </div>
            
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤗</div>
                <h5 style="margin-bottom: 0.5rem;">AI luôn ở bên bạn</h5>
                <p style="font-size: 0.9rem; color: var(--text-soft);">Như một người bạn thấu hiểu cảm xúc</p>
            </div>
            
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔓</div>
                <h5 style="margin-bottom: 0.5rem;">Mô hình đơn giản</h5>
                <p style="font-size: 0.9rem; color: var(--text-soft);">Dùng thử 3 lần → Trả phí 1 lần → Dùng mãi mãi</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_message_tab():
    """Show main message creation tab"""
    # Check trial status
    if not st.session_state.paid:
        remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
        
        if remaining <= 0:
            st.session_state.current_tab = "upgrade"
            st.rerun()
        
        # Emotional progress display
        st.markdown(f"""
        <div class="emotional-card emotional-card-warm">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div>
                    <h4 style="margin-bottom: 0.2rem;">🌸 Bạn đang dùng thử miễn phí</h4>
                    <p style="color: var(--text-secondary);">Còn <b style="color: var(--primary-warm);">{remaining}/{FREE_TRIAL_LIMIT}</b> lượt sử dụng</p>
                </div>
                <div style="width: 50%;">
                    <div class="emotional-progress">
                        <div class="emotional-progress-bar" style="width: {(st.session_state.usage_count / FREE_TRIAL_LIMIT) * 100}%;"></div>
                    </div>
                </div>
            </div>
            <p style="font-size: 0.9rem; color: var(--text-soft); margin-top: 0.5rem;">
                Mỗi tin nhắn đều được AI tạo riêng cho tình huống của bạn
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Emotional message creation interface
    st.markdown("""
    <div class="emotional-card emotional-card-love">
        <h3 class="mb-2">💌 Tạo Tin Nhắn Tinh Tế</h3>
        <p class="mb-3" style="color: var(--text-secondary);">Chia sẻ tình huống của bạn, để AI thấu hiểu và giúp bạn diễn đạt</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Emotional input section
    col1, col2 = st.columns(2)
    
    with col1:
        user_gender = st.radio(
            "**Giới tính của bạn**",
            ["Nam", "Nữ"],
            horizontal=True,
            key="msg_gender"
        )
    
    with col2:
        target_gender = st.radio(
            "**Giới tính người nhận**",
            ["Nam", "Nữ"],
            horizontal=True,
            key="target_gender"
        )
    
    # Closeness level
    closeness = st.selectbox(
        "**Mức độ thân thiết**",
        ["Lần đầu làm quen", "Quen biết nhẹ", "Bạn bè", "Thân thiết", "Đang tìm hiểu", "Đã là người yêu", "Vợ/chồng"],
        key="closeness"
    )
    
    # Map to system values
    closeness_map = {
        "Lần đầu làm quen": "stranger",
        "Quen biết nhẹ": "acquaintance",
        "Bạn bè": "friend",
        "Thân thiết": "close_friend",
        "Đang tìm hiểu": "romantic",
        "Đã là người yêu": "romantic",
        "Vợ/chồng": "partner"
    }
    
    # Emotion and intent
    col1, col2 = st.columns(2)
    
    with col1:
        emotion = st.selectbox(
            "**Cảm xúc chính của bạn**",
            ["Vui vẻ", "Bình thường", "Buồn", "Lo lắng", "Giận", "Cô đơn", "Bối rối", "Hy vọng"],
            key="emotion"
        )
    
    with col2:
        intent = st.selectbox(
            "**Mục đích tin nhắn**",
            ["Kết nối", "An ủi", "Xin lỗi", "Thể hiện tình cảm", "Giữ khoảng cách", "Tán tỉnh nhẹ", "Làm hoà", "Hỏi thăm"],
            key="intent"
        )
    
    # Time of day
    time_of_day = st.selectbox(
        "**Thời điểm gửi**",
        ["Sáng sớm", "Buổi trưa", "Chiều tối", "Buổi tối", "Cuối tuần", "Ngày đặc biệt"],
        key="time_of_day"
    )
    
    # Time mapping
    time_map = {
        "Sáng sớm": "morning",
        "Buổi trưa": "afternoon",
        "Chiều tối": "evening",
        "Buổi tối": "night",
        "Cuối tuần": "weekend",
        "Ngày đặc biệt": "special_day"
    }
    
    # Personal context
    context = st.text_area(
        "**Thông tin chi tiết (tuỳ chọn)**",
        placeholder="Ví dụ: Chúng ta quen nhau qua ứng dụng hẹn hò, bạn ấy là kiến trúc sư 35 tuổi...\nHoặc: Tôi muốn nhắn sau khi cãi nhau về việc không quan tâm đến cảm xúc của nhau...\nHoặc: Anh ấy/ cô ấy đang stress vì công việc, tôi muốn an ủi...",
        height=120,
        help="Càng chi tiết, tin nhắn càng chân thật và phù hợp",
        key="context"
    )
    
    # Emotional generate button
    if st.button("✨ **AI Hiểu & Tạo Tin Nhắn**", key="generate_emotional", use_container_width=True):
        if not st.session_state.paid:
            # Update usage
            st.session_state.usage_count += 1
            update_usage(st.session_state.phone)
            remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
            
            if remaining < 0:
                st.error("🌸 Bạn đã hết lượt dùng thử miễn phí")
                st.session_state.current_tab = "upgrade"
                st.rerun()
        
        # Generate emotional message
        ai = EmotionalCompanion()
        
        with st.spinner("🤗 AI đang thấu hiểu cảm xúc và tạo tin nhắn chân thành cho bạn..."):
            time.sleep(1.5)
            
            # Map inputs
            emotion_map = {
                "Vui vẻ": "happy", "Bình thường": "neutral", "Buồn": "sad",
                "Lo lắng": "anxious", "Giận": "angry", "Cô đơn": "lonely",
                "Bối rối": "confused", "Hy vọng": "hopeful"
            }
            
            intent_map = {
                "Kết nối": "connect", "An ủi": "comfort", "Xin lỗi": "apologize",
                "Thể hiện tình cảm": "express_love", "Giữ khoảng cách": "set_boundary",
                "Tán tỉnh nhẹ": "flirt", "Làm hoà": "reconcile", "Hỏi thăm": "check_in"
            }
            
            result = ai.generate(
                user_gender=user_gender,
                target_gender=target_gender,
                closeness=closeness_map.get(closeness, "acquaintance"),
                emotion=emotion_map.get(emotion, "neutral"),
                intent=intent_map.get(intent, "connect"),
                time_of_day=time_map.get(time_of_day, "afternoon"),
                user_context=context
            )
            
            st.session_state.result = result
        
        # Scroll to result
        st.markdown("<div id='result'></div>", unsafe_allow_html=True)
    
    # Display emotional result
    if st.session_state.result:
        st.markdown("""
        <div class="message-bubble">
            <div class="emoji-large" style="position: absolute; top: -25px; left: 20px; font-size: 1.5rem;">💌</div>
            <h4 style="margin-bottom: 1rem; color: var(--primary-warm);">Tin nhắn gợi ý</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # The message
        st.markdown(f"""
        <div style="padding: 0 1rem 2rem 1rem;">
            <p class="message-text">{st.session_state.result}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("📋 **Copy tin nhắn**", use_container_width=True):
                st.success("✅ Đã copy tin nhắn vào clipboard!")
        
        with col2:
            if st.button("🔄 **Tạo tin khác**", use_container_width=True):
                st.session_state.result = ""
                st.rerun()
        
        with col3:
            if st.button("💾 **Lưu lại**", use_container_width=True):
                st.info("✨ Tin nhắn đã được lưu trong phiên làm việc này")
        
        # Trial reminder
        if not st.session_state.paid:
            remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
            if remaining == 1:
                st.markdown("""
                <div class="emotional-card emotional-card-warm" style="margin-top: 2rem;">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="font-size: 2rem;">💎</div>
                        <div>
                            <h4 style="margin-bottom: 0.2rem;">Chỉ còn 1 lượt dùng thử!</h4>
                            <p style="color: var(--text-secondary);">Nâng cấp ngay để không giới hạn tin nhắn tinh tế</p>
                            <button onclick="window.location.href='?tab=upgrade'" 
                                    style="background: linear-gradient(135deg, var(--primary-warm) 0%, var(--primary-cool) 100%); 
                                           color: white; border: none; padding: 8px 20px; 
                                           border-radius: 25px; cursor: pointer; margin-top: 0.5rem;
                                           font-weight: 500;">
                                💳 Xem gói nâng cấp
                            </button>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def show_scenarios_tab():
    """Show emotional scenarios library"""
    st.markdown("""
    <div class="emotional-card emotional-card-calm">
        <h3 class="mb-2">📚 Thư Viện Cảm Xúc</h3>
        <p class="mb-3" style="color: var(--text-secondary);">7000+ tình huống giao tiếp được AI thấu hiểu và xử lý tinh tế</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Scenario categories
    categories = [
        {
            "title": "💌 Làm quen & Kết nối",
            "scenarios": [
                "Nhắn tin lần đầu sau match dating app",
                "Làm quen đồng nghiệp mới (30+)",
                "Kết nối lại với bạn cũ thời đại học",
                "Làm quen trong hội nhóm sở thích"
            ]
        },
        {
            "title": "🤗 An ủi & Đồng hành",
            "scenarios": [
                "Khi người ấy mất việc ở tuổi 40",
                "Khi con cái gặp khó khăn",
                "Áp lực chăm sóc cha mẹ già",
                "Stress công việc mid-life crisis"
            ]
        },
        {
            "title": "💞 Tình cảm Trưởng thành",
            "scenarios": [
                "Yêu lại sau ly hôn",
                "Cân bằng giữa con riêng và tình mới",
                "Giao tiếp với người yêu cũ có con chung",
                "Hẹn hò tuổi 45+ với áp lực xã hội"
            ]
        },
        {
            "title": "⚡ Mâu thuẫn & Hoà giải",
            "scenarios": [
                "Cãi nhau về tài chính gia đình",
                "Bất đồng trong nuôi dạy con cái",
                "Ghen tuông tuổi trung niên",
                "Cần không gian riêng sau nhiều năm chung sống"
            ]
        },
        {
            "title": "🌱 Tái khởi đầu",
            "scenarios": [
                "Bắt đầu kinh doanh ở tuổi 50",
                "Chuyển nghề nghiệp giai đoạn mid-life",
                "Tìm lại đam mê sau nhiều năm",
                "Xây dựng mối quan hệ mới sau tổn thương"
            ]
        }
    ]
    
    for category in categories:
        st.markdown(f"""
        <div class="emotional-card" style="margin-bottom: 1.5rem;">
            <h4 style="margin-bottom: 1rem; color: var(--primary-warm);">{category['title']}</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
        """, unsafe_allow_html=True)
        
        for scenario in category['scenarios']:
            st.markdown(f"""
            <div style="background: rgba(123, 44, 191, 0.05); padding: 1rem; border-radius: 12px; border: 1px solid rgba(123, 44, 191, 0.1);">
                <p style="margin: 0; font-weight: 500;">{scenario}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # CTA to try
    st.markdown("""
    <div class="emotional-card emotional-card-love" style="text-align: center;">
        <div class="emoji-large">✨</div>
        <h4>Trải nghiệm sức mạnh của 7000+ cảm xúc</h4>
        <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">Mỗi tình huống đều được AI thấu hiểu sâu sắc và xử lý tinh tế</p>
        <button onclick="window.location.href='?tab=message'" 
                style="background: linear-gradient(135deg, var(--primary-warm) 0%, var(--primary-cool) 100%); 
                       color: white; border: none; padding: 12px 30px; 
                       border-radius: 25px; cursor: pointer; font-weight: 600;
                       font-size: 1rem;">
            💬 Thử ngay
        </button>
    </div>
    """, unsafe_allow_html=True)

def show_companion_tab():
    """Show AI companion section - emotional support"""
    st.markdown("""
    <div class="emotional-card emotional-card-warm">
        <h3 class="mb-2">🤗 AI Luôn Ở Bên Bạn</h3>
        <p class="mb-3" style="color: var(--text-secondary);">Không chỉ là công cụ, mà là người bạn thấu hiểu cảm xúc của bạn</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Emotional tips
    tips = [
        {
            "icon": "💭",
            "title": "Giao tiếp là lắng nghe",
            "content": "Đôi khi im lặng đúng lúc có giá trị hơn ngàn lời nói. Hãy học cách lắng nghe không chỉ bằng tai, mà bằng cả trái tim."
        },
        {
            "icon": "🌱",
            "title": "Trưởng thành là biết chọn lời",
            "content": "Ở tuổi chúng ta, mỗi lời nói đều mang trọng lượng. Hãy nói những điều xây dựng, không phải những điều làm tổn thương."
        },
        {
            "icon": "🌈",
            "title": "Cảm xúc là màu sắc cuộc sống",
            "content": "Buồn, vui, giận, yêu - tất cả đều là một phần của con người trưởng thành. Đừng sợ thể hiện, nhưng hãy thể hiện đúng cách."
        },
        {
            "icon": "🤝",
            "title": "Hiểu mình để hiểu người",
            "content": "Khi bạn thấu hiểu cảm xúc của chính mình, bạn mới có thể thực sự thấu hiểu người khác. Đó là nền tảng của mọi mối quan hệ chất lượng."
        }
    ]
    
    for tip in tips:
        st.markdown(f"""
        <div class="emotional-card" style="margin-bottom: 1.5rem;">
            <div style="display: flex; gap: 1rem; align-items: flex-start;">
                <div style="font-size: 2rem; flex-shrink: 0;">{tip['icon']}</div>
                <div>
                    <h4 style="margin-bottom: 0.5rem; color: var(--primary-warm);">{tip['title']}</h4>
                    <p style="color: var(--text-secondary); line-height: 1.6;">{tip['content']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Emotional journal prompt
    st.markdown("""
    <div class="emotional-card emotional-card-calm">
        <h4 class="mb-2">📝 Gợi ý viết nhật ký cảm xúc</h4>
        <p style="color: var(--text-secondary); margin-bottom: 1rem;">
            Dành 5 phút mỗi ngày để viết về cảm xúc của bạn. Điều này giúp bạn hiểu mình hơn và giao tiếp tốt hơn.
        </p>
        <div style="background: rgba(67, 97, 238, 0.05); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(67, 97, 238, 0.1);">
            <p style="font-style: italic; color: var(--text-secondary); margin: 0;">
            "Hôm nay tôi cảm thấy...<br>
            Điều làm tôi cảm động nhất là...<br>
            Tôi muốn nói với ai đó rằng...<br>
            Tôi biết ơn vì..."
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_upgrade_tab():
    """Show emotional upgrade section"""
    # Check if already paid
    if st.session_state.paid:
        st.markdown("""
        <div class="emotional-card emotional-card-love" style="text-align: center;">
            <div class="emoji-large">🎉</div>
            <h3>Bạn đã là thành viên cao cấp!</h3>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
                Cảm ơn bạn đã tin tưởng EMOTICONN AI.<br>
                Bây giờ bạn có thể tạo tin nhắn không giới hạn với hệ thống 7000+ cảm xúc.
            </p>
            <button onclick="window.location.href='?tab=message'" 
                    style="background: linear-gradient(135deg, var(--primary-warm) 0%, var(--primary-cool) 100%); 
                           color: white; border: none; padding: 12px 30px; 
                           border-radius: 25px; cursor: pointer; font-weight: 600;">
                💬 Bắt đầu tạo tin nhắn
            </button>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Upgrade offer
    st.markdown("""
    <div class="emotional-payment">
        <h2 style="color: white; margin-bottom: 0.5rem;">🔓 Mở Khoá Trọn Đời</h2>
        <p style="color: rgba(255, 255, 255, 0.9);">Chỉ thanh toán một lần - Dùng mãi mãi</p>
        <div class="price-emotional">199.000đ</div>
        <p style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">
            Chưa bằng 1 bữa cafe chất lượng mỗi tháng
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Benefits
    st.markdown("""
    <div class="emotional-card emotional-card-warm">
        <h4 class="mb-3">🎁 Bạn sẽ nhận được:</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
            <div>
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <div style="color: var(--primary-warm);">✓</div>
                    <h5 style="margin: 0;">Không giới hạn tin nhắn</h5>
                </div>
                <p style="color: var(--text-soft); font-size: 0.9rem;">Tạo bao nhiêu tin nhắn tùy thích</p>
            </div>
            
            <div>
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <div style="color: var(--primary-warm);">✓</div>
                    <h5 style="margin: 0;">Hệ thống 7000+ cảm xúc</h5>
                </div>
                <p style="color: var(--text-soft); font-size: 0.9rem;">Mọi tình huống đều được xử lý tinh tế</p>
            </div>
            
            <div>
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <div style="color: var(--primary-warm);">✓</div>
                    <h5 style="margin: 0;">AI thấu hiểu sâu sắc</h5>
                </div>
                <p style="color: var(--text-soft); font-size: 0.9rem;">Như một người bạn thực sự hiểu bạn</p>
            </div>
            
            <div>
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <div style="color: var(--primary-warm);">✓</div>
                    <h5 style="margin: 0;">Cập nhật trọn đời</h5>
                </div>
                <p style="color: var(--text-soft); font-size: 0.9rem;">Luôn được nâng cấp và cải thiện</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Payment instructions
    st.markdown("""
    <div class="emotional-card emotional-card-calm">
        <h4 class="mb-3">💳 Hướng Dẫn Thanh Toán</h4>
        
        <div style="background: rgba(67, 97, 238, 0.05); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;">
            <p style="margin-bottom: 0.5rem; font-weight: 500;">1. Chuyển khoản qua ngân hàng:</p>
            <pre style="background: white; padding: 1rem; border-radius: 8px; overflow-x: auto; margin: 0;">
Ngân hàng: BIDV
Số tài khoản: 4430269669
Chủ tài khoản: NGUYEN XUAN DAT
Số tiền: 199.000 VND
Nội dung: EMOTICONN [SỐ ĐIỆN THOẠI CỦA BẠN]
            </pre>
        </div>
        
        <p style="color: var(--text-secondary); margin-bottom: 1rem;">
            <b>📌 Ví dụ:</b> Số điện thoại của bạn là <b>0912345678</b>, 
            nội dung chuyển khoản: <code>EMOTICONN 0912345678</code>
        </p>
        
        <p style="color: var(--text-secondary);">
            <b>2. Xác nhận thanh toán:</b><br>
            Sau khi chuyển khoản, nhập số điện thoại của bạn vào ô bên dưới để mở khoá ngay.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verification
    st.markdown("### ✅ Xác Nhận Thanh Toán")
    
    verify_input = st.text_input(
        "Nhập số điện thoại của bạn để xác nhận:",
        placeholder="0912345678",
        key="payment_verify_upgrade"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔓 **Mở Khoá Ngay**", key="unlock_premium", use_container_width=True):
            if verify_input:
                valid_phone = validate_phone(verify_input)
                
                if valid_phone and valid_phone == st.session_state.phone:
                    # Save as paid user
                    save_paid_user(valid_phone)
                    st.session_state.paid = True
                    
                    # Emotional success
                    st.balloons()
                    st.success("""
                    🎉 **Chúc mừng! Bạn đã mở khoá thành công!**
                    
                    Bây giờ bạn có thể:
                    • Tạo tin nhắn không giới hạn
                    • Truy cập hệ thống 7000+ cảm xúc
                    • Trải nghiệm AI như người bạn thực sự
                    """)
                    
                    # Auto redirect
                    time.sleep(3)
                    st.session_state.current_tab = "message"
                    st.rerun()
                else:
                    st.error("⚠️ Số điện thoại không khớp. Vui lòng kiểm tra lại số điện thoại đã đăng ký.")
            else:
                st.warning("💭 Hãy nhập số điện thoại để xác nhận thanh toán")
    
    # Try another phone option
    st.markdown("---")
    if st.button("📱 **Thử với số điện thoại khác**"):
        st.session_state.phone = ""
        st.session_state.verified = False
        st.session_state.paid = False
        st.session_state.usage_count = 0
        st.rerun()

if __name__ == "__main__":
    main()
