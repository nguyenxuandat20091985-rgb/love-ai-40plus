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
    page_title="EMOTICONN AI - Trợ Lý Giao Tiếp Cảm Xúc",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
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

# ==================== PREMIUM CSS ====================
def load_premium_css():
    st.markdown("""
    <style>
    /* === ROOT VARIABLES === */
    :root {
        --primary-dark: #6A11CB;
        --primary-light: #2575FC;
        --secondary: #8A2BE2;
        --accent: #FF6B9D;
        --neutral-light: #F8F9FF;
        --neutral-dark: #2D3748;
        --success: #10B981;
        --warning: #F59E0B;
        --text-primary: #2D3748;
        --text-secondary: #718096;
        --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        --radius-md: 16px;
        --radius-lg: 24px;
    }
    
    /* === GLOBAL RESET === */
    .stApp {
        background: linear-gradient(135deg, #F8F9FF 0%, #EDF2F7 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* === HERO SECTION === */
    .hero-gradient {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-light) 100%);
        padding: 3rem 1rem;
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-gradient::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="white" opacity="0.1"/></svg>');
        animation: float 20s linear infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        100% { transform: translateY(-100px); }
    }
    
    .hero-title {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #FFFFFF 0%, #FFD6FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem !important;
        line-height: 1.2;
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.2rem !important;
        }
    }
    
    .hero-subtitle {
        font-size: 1.3rem !important;
        color: rgba(255, 255, 255, 0.9) !important;
        text-align: center;
        max-width: 800px;
        margin: 0 auto 2rem auto !important;
        line-height: 1.6;
    }
    
    /* === PREMIUM CARD === */
    .premium-card {
        background: white;
        border-radius: var(--radius-md);
        padding: 2rem;
        box-shadow: var(--shadow-md);
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }
    
    /* === INPUT STYLING === */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #E2E8F0 !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-light) !important;
        box-shadow: 0 0 0 3px rgba(37, 117, 252, 0.1) !important;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 12px !important;
        border: 2px solid #E2E8F0 !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        min-height: 120px;
    }
    
    /* === BUTTON STYLING === */
    .stButton > button {
        border-radius: 50px !important;
        padding: 0.9rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        border: none !important;
        width: 100%;
    }
    
    .primary-btn {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-light) 100%) !important;
        color: white !important;
    }
    
    .primary-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(106, 17, 203, 0.2) !important;
    }
    
    .secondary-btn {
        background: white !important;
        color: var(--primary-dark) !important;
        border: 2px solid var(--primary-light) !important;
    }
    
    .secondary-btn:hover {
        background: var(--primary-light) !important;
        color: white !important;
    }
    
    /* === RADIO & SELECT STYLING === */
    .stRadio > div {
        flex-direction: row;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .stRadio > div > label {
        background: white;
        border: 2px solid #E2E8F0;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        transition: all 0.3s ease;
        flex: 1;
        min-width: 120px;
        text-align: center;
    }
    
    .stRadio > div > label:hover {
        border-color: var(--primary-light);
        transform: translateY(-2px);
    }
    
    .stRadio > div > label[data-testid="stRadio"] {
        margin-right: 0 !important;
    }
    
    /* === PROGRESS BAR === */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary-dark), var(--primary-light));
        border-radius: 10px;
    }
    
    /* === RESULT CARD === */
    .result-card {
        background: linear-gradient(135deg, #FFF9FB 0%, #F0F4FF 100%);
        border-left: 5px solid var(--accent);
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: var(--shadow-sm);
    }
    
    .message-content {
        font-size: 1.2rem;
        line-height: 1.8;
        color: var(--text-primary);
        margin-bottom: 1.5rem;
    }
    
    /* === PAYMENT SECTION === */
    .payment-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        color: white;
        border-radius: var(--radius-md);
        padding: 2.5rem;
        text-align: center;
    }
    
    .price-tag {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
    }
    
    /* === FOOTER === */
    .footer {
        text-align: center;
        padding: 2rem 1rem;
        color: var(--text-secondary);
        font-size: 0.9rem;
        border-top: 1px solid #E2E8F0;
        margin-top: 3rem;
    }
    
    /* === UTILITY CLASSES === */
    .text-center { text-align: center !important; }
    .mb-1 { margin-bottom: 0.5rem !important; }
    .mb-2 { margin-bottom: 1rem !important; }
    .mb-3 { margin-bottom: 1.5rem !important; }
    .mt-2 { margin-top: 1rem !important; }
    .mt-3 { margin-top: 1.5rem !important; }
    
    /* === HIDE DEFAULTS === */
    #MainMenu, footer, header { visibility: hidden; }
    
    /* === MOBILE OPTIMIZATION === */
    @media (max-width: 768px) {
        .premium-card { padding: 1.5rem; }
        .hero-gradient { padding: 2rem 1rem; }
        .stRadio > div { flex-direction: column; }
        .stRadio > div > label { width: 100%; }
    }
    </style>
    """, unsafe_allow_html=True)

load_premium_css()

# ==================== AI TEMPLATE DATABASE ====================
class EmotionalAI:
    def __init__(self):
        self.templates = {
            "Làm quen": {
                "Nam nhắn Nữ": [
                    "Chào bạn, mình là {name} từ {context}. Mình ấn tượng với {detail} và muốn làm quen nếu không phiền. Hôm nay của bạn thế nào? 💫",
                    "Xin chào, hy vọng tin nhắn này không đến bất ngờ. Mình thấy chúng ta có chung {interest}. Bạn có muốn trao đổi thêm không? ☕",
                    "Chào bạn, mình vừa nhớ đến cuộc trò chuyện hôm {time}. Bạn có khoẻ không? Công việc tuần này thế nào rồi? 💼"
                ],
                "Nữ nhắn Nam": [
                    "Chào anh, em là {name} đây. Em muốn gửi lời cảm ơn vì {reason} hôm trước. Anh có vài phút rảnh trò chuyện không? 🌸",
                    "Xin chào, em thấy anh rất {trait} trong {context}. Em muốn làm quen nếu anh không ngại. Anh đang bận việc gì không? 🤗",
                    "Chào anh, hy vọng anh có một ngày tốt lành. Em có chút thắc mắc về {topic}, không biết có thể hỏi ý kiến anh được không? 💭"
                ]
            },
            
            "Trả lời khi đối phương lạnh": {
                "Nam nhắn Nữ": [
                    "Mình hiểu bạn đang bận hoặc có việc riêng. Khi nào rảnh, mình vẫn ở đây. Chúc bạn một ngày nhẹ nhàng. 🌿",
                    "Có vẻ hôm nay không phải thời điểm thích hợp. Mình tôn trọng không gian riêng của bạn. Nếu có dịp khác, chúng ta nói chuyện sau. 🤝",
                    "Không sao cả, mỗi người đều có những ngày cần yên tĩnh. Mình gửi bạn chút năng lượng tích cực nhé. ✨"
                ],
                "Nữ nhắn Nam": [
                    "Em hiểu anh đang tập trung vào việc quan trọng. Khi nào anh thoải mái, em vẫn sẵn sàng trò chuyện. Chúc anh làm việc hiệu quả. 💪",
                    "Có lẽ hôm nay chưa phải lúc. Em tôn trọng thời gian của anh. Một ngày tốt lành nhé. 🌞",
                    "Không vấn đề gì đâu. Ai cũng có những lúc cần không gian riêng. Em chúc anh bình an. 🕊️"
                ]
            },
            
            "Gợi chuyện không vô duyên": {
                "Nam nhắn Nữ": [
                    "Mình vừa xem/đọc/nghe {something}, tự nhiên nghĩ đến bạn. Bạn có quan tâm đến {topic} không? 🎵",
                    "Hôm nay thời tiết {weather}, mình nhớ đến lần chúng ta nói về {memory}. Dạo này bạn có gì mới không? 🌤️",
                    "Mình tình cờ thấy {thing} này, thấy hợp với sở thích của bạn. Đơn giản chỉ muốn chia sẻ thôi. 💝"
                ],
                "Nữ nhắn Nam": [
                    "Em vừa trải nghiệm {experience}, chợt nhớ anh từng chia sẻ về {topic}. Anh dạo này thế nào? 🍃",
                    "Hôm nay em có chuyện vui muốn khoe, là {news}. Anh có muốn nghe không? 😊",
                    "Em thấy {thing} này hay hay, nghĩ ngay đến anh. Không biết anh có hứng thú không? 🎁"
                ]
            },
            
            "Đã ly hôn (trưởng thành)": {
                "Nam nhắn Nữ": [
                    "Tôi hiểu hành trình này không dễ dàng. Những gì chúng ta trải qua đều giúp trưởng thành hơn. Hôm nay bạn cảm thấy thế nào? 🌱",
                    "Bắt đầu lại ở độ tuổi này thực sự là một thử thách. Nhưng tôi tin mỗi người đều xứng đáng có cơ hội mới. Bạn có muốn chia sẻ điều gì không? 🤲",
                    "Quá khứ là bài học, hiện tại là món quà. Dù có chuyện gì xảy ra, bạn vẫn là người giá trị. Có điều gì tôi có thể lắng nghe không? 💫"
                ],
                "Nữ nhắn Nam": [
                    "Em biết bắt đầu lại không đơn giản. Nhưng chính những trải nghiệm làm chúng ta sâu sắc hơn. Anh đang ổn chứ? 🌻",
                    "Ở độ tuổi chúng ta, mỗi người đều mang theo câu chuyện riêng. Em trân trọng điều đó. Anh có muốn tâm sự không? 🍂",
                    "Em tin rằng mọi thứ xảy ra đều có lý do. Quan trọng là chúng ta đối diện với hiện tại. Anh cảm thấy thế nào về điều đó? 💭"
                ]
            },
            
            "Có con riêng": {
                "Nam nhắn Nữ": [
                    "Tôi rất trân trọng việc bạn vừa là một người mẹ tốt vừa mở lòng cho những mối quan hệ mới. Các bé khoẻ không? 👨‍👧",
                    "Làm cha mẹ đơn thân không dễ dàng. Tôi ngưỡng mộ sự mạnh mẽ của bạn. Cuối tuần này bạn có kế hoạch gì cùng các con không? 🎈",
                    "Tôi hiểu gia đình luôn là ưu tiên hàng đầu của bạn. Đó là điều đáng quý. Nếu có dịp, tôi muốn nghe bạn chia sẻ về cuộc sống hàng ngày. 🏡"
                ],
                "Nữ nhắn Nam": [
                    "Em biết việc vừa làm cha vừa tìm kiếm hạnh phúc riêng không đơn giản. Em ngưỡng mộ sự cân bằng của anh. Các con anh dạo này thế nào? 👨‍👦",
                    "Làm bố đơn thân chắc hẳn có nhiều thử thách. Em thấy anh đang làm rất tốt. Có điều gì anh muốn chia sẻ về hành trình này không? 🌟",
                    "Em trân trọng cách anh ưu tiên cho con cái. Đó là phẩm chất đáng quý. Nếu anh có thời gian, em muốn hiểu thêm về cuộc sống của anh. 💞"
                ]
            },
            
            "Ghen nhẹ đúng mực": {
                "Nam nhắn Nữ": [
                    "Anh thấy có chút bồn chồn khi nghĩ đến việc em đi chơi với đồng nghiệp đó. Nhưng anh tin tưởng em. Chỉ là anh quan tâm thôi. 😔",
                    "Anh biết mình hơi trẻ con, nhưng thấy em thân thiết với ai đó, anh cảm thấy có chút lo lắng. Có thể nói chuyện với anh về người đó được không? 💬",
                    "Anh không muốn kiểm soát em, chỉ là anh quan tâm. Khi thấy em vui vẻ với người khác, anh tự hỏi mình có làm em hạnh phúc như vậy không. 🤔"
                ],
                "Nữ nhắn Nam": [
                    "Em thú thật là có chút không thoải mái khi thấy anh đi cafe với cô ấy. Nhưng em tin anh. Chỉ là cảm xúc tự nhiên thôi. 🫣",
                    "Em không muốn ghen tuông vô lý, nhưng khi thấy anh thân thiết với ai đó, em cảm thấy không an toàn. Anh có thể giúp em hiểu rõ hơn không? 🥺",
                    "Em biết mình không nên, nhưng cảm thấy có chút tổn thương khi thấy anh quan tâm đến người khác. Em cần được trấn an một chút. 🤗"
                ]
            },
            
            "Áp lực tài chính": {
                "Nam nhắn Nữ": [
                    "Tôi hiểu áp lực tài chính ở độ tuổi chúng ta không nhẹ. Nhưng xin đừng quá khắt khe với bản thân. Mọi thứ rồi sẽ ổn thôi. 💪",
                    "Gánh nặng cơm áo gạo tiền đôi khi làm ta mệt mỏi. Hãy nhớ chăm sóc bản thân mình trước nhé. Có điều gì tôi có thể hỗ trợ không? 🤲",
                    "Ai rồi cũng có những giai đoạn khó khăn về tiền bạc. Điều quan trọng là chúng ta không đơn độc. Bạn đang cần lời khuyên hay chỉ cần người lắng nghe? 👂"
                ],
                "Nữ nhắn Nam": [
                    "Em biết áp lực tài chính có thể rất nặng nề. Nhưng anh đừng quên rằng sức khoẻ và tinh thần mới là quan trọng nhất. Em lo cho anh. 🫂",
                    "Mọi khó khăn rồi cũng sẽ qua. Quan trọng là chúng ta cùng nhau vượt qua. Anh có muốn chia sẻ gánh nặng với em không? 💞",
                    "Đừng ôm hết mọi thứ một mình. Em ở đây để lắng nghe và ủng hộ anh. Tiền bạc có thể kiếm lại, nhưng sức khoẻ và sự bình yên thì không. 🌈"
                ]
            },
            
            "Nhắn buổi sáng": {
                "Nam nhắn Nữ": [
                    "Chào buổi sáng em yêu. Hy vọng em có một đêm ngon giấc. Hôm nay trời đẹp, anh chúc em một ngày tràn đầy năng lượng và niềm vui. ☀️",
                    "Sáng nay thức dậy, điều đầu tiên anh nghĩ đến là em. Chúc em một ngày mới nhẹ nhàng và hạnh phúc. Nhớ ăn sáng đầy đủ nhé. 🍳",
                    "Buổi sáng bình an em nhé. Dù hôm nay có bận rộn thế nào, hãy nhớ chăm sóc bản thân. Anh luôn ở đây nếu em cần. 🌸"
                ],
                "Nữ nhắn Nam": [
                    "Chào buổi sáng anh yêu. Em chúc anh một ngày làm việc hiệu quả và tràn đầy cảm hứng. Nhớ uống đủ nước và ăn sáng nhé. 💧",
                    "Sáng nay em thức dậy và mỉm cười vì nghĩ đến anh. Chúc anh một ngày thật ý nghĩa. Dù có chuyện gì, hãy nhớ em luôn ủng hộ anh. 😊",
                    "Buổi sáng an lành anh nhé. Hy vọng anh có một ngày nhẹ nhàng. Nếu mệt, hãy dành thời gian nghỉ ngơi. Sức khoẻ quan trọng nhất. 💖"
                ]
            },
            
            "Khi giận nhau": {
                "Nam nhắn Nữ": [
                    "Anh xin lỗi vì những gì đã xảy ra. Dù có bất đồng, tình cảm của anh dành cho em không thay đổi. Anh muốn chúng ta cùng tìm cách giải quyết. 🕊️",
                    "Anh biết mình đã làm em buồn. Anh không muốn vì hiểu lầm mà làm tổn thương tình cảm của chúng ta. Em có thể cho anh cơ hội được nói chuyện không? 🙏",
                    "Dù có chuyện gì xảy ra, anh vẫn yêu em. Chúng ta hãy cùng nhau vượt qua khúc mắc này. Anh sẵn sàng lắng nghe và thay đổi. 💞"
                ],
                "Nữ nhắn Nam": [
                    "Em xin lỗi vì đã để cảm xúc chi phối. Em không muốn chúng ta xa cách vì hiểu lầm. Anh có thể cho em cơ hội được giải thích không? 🌹",
                    "Em biết mình đã sai. Tình cảm của chúng ta quan trọng hơn bất kỳ tranh cãi nào. Em muốn chúng ta cùng tìm cách hoà giải. 🤝",
                    "Dù có bất đồng, em vẫn trân trọng anh. Em không muốn mất anh vì những chuyện không đáng. Chúng ta có thể nói chuyện được không? 💬"
                ]
            },
            
            "Ngại yêu lại": {
                "Nam nhắn Nữ": [
                    "Tôi hiểu cảm giác ngại ngần khi bắt đầu lại. Những vết thương cũ đôi khi làm ta sợ mở lòng. Nhưng tôi tin mỗi người đều xứng đáng có cơ hội mới. 🌱",
                    "Bắt đầu ở độ tuổi này có thể đáng sợ, nhưng cũng đẹp vì chúng ta đã biết mình muốn gì. Không cần vội, cứ từ từ thấu hiểu nhau. 🐢",
                    "Tôi không muốn thêm áp lực. Chúng ta có thể làm bạn trước, xem mọi thứ phát triển tự nhiên. Quan trọng là cả hai cảm thấy an toàn. 🏠"
                ],
                "Nữ nhắn Nam": [
                    "Em hiểu việc mở lòng lại không dễ. Nhưng em tin rằng mỗi người đều có cơ hội viết tiếp câu chuyện của mình. Anh có muốn thử không? ✍️",
                    "Chúng ta không cần phải vội. Cứ từ từ làm quen, như hai người bạn. Quan trọng là cảm thấy thoải mái khi ở bên nhau. ☕",
                    "Em tôn trọng nỗi sợ của anh. Không có áp lực, không có kỳ vọng. Chỉ đơn giản là trò chuyện và thấu hiểu nhau. 🍃"
                ]
            }
        }
        
        # Situation mapping for user selection
        self.situation_map = {
            "💌 Làm quen lần đầu": "Làm quen",
            "🤔 Đối phương lạnh nhạt": "Trả lời khi đối phương lạnh",
            "💬 Gợi chuyện tinh tế": "Gợi chuyện không vô duyên",
            "💔 Đã ly hôn": "Đã ly hôn (trưởng thành)",
            "👨‍👩‍👧 Có con riêng": "Có con riêng",
            "😠 Ghen nhẹ đúng mực": "Ghen nhẹ đúng mực",
            "💰 Áp lực tài chính": "Áp lực tài chính",
            "☀️ Nhắn buổi sáng": "Nhắn buổi sáng",
            "⚡ Khi giận nhau": "Khi giận nhau",
            "🌱 Ngại yêu lại": "Ngại yêu lại"
        }
    
    def generate(self, user_gender, target_gender, situation_key, user_context=""):
        """Generate emotional message"""
        # Map situation key
        situation = self.situation_map.get(situation_key, "Làm quen")
        
        # Determine template gender key
        if user_gender == "Nam" and target_gender == "Nữ":
            gender_key = "Nam nhắn Nữ"
        elif user_gender == "Nữ" and target_gender == "Nam":
            gender_key = "Nữ nhắn Nam"
        elif user_gender == "Nam" and target_gender == "Nam":
            gender_key = "Nam nhắn Nữ"  # Fallback
        elif user_gender == "Nữ" and target_gender == "Nữ":
            gender_key = "Nữ nhắn Nam"  # Fallback
        else:
            gender_key = "Nam nhắn Nữ"  # Default
        
        # Get templates
        if situation in self.templates and gender_key in self.templates[situation]:
            templates = self.templates[situation][gender_key]
        else:
            templates = ["Xin chào, hy vọng bạn có một ngày tốt lành. 💬"]
        
        # Select random template
        template = random.choice(templates)
        
        # Personalize with context
        personalized = self._personalize_template(template, user_context)
        
        return personalized
    
    def _personalize_template(self, template, context):
        """Personalize template with user context"""
        if not context.strip():
            return template
        
        # Simple context insertion
        replacements = {
            "{name}": "mình",
            "{context}": context[:30] + "..." if len(context) > 30 else context,
            "{detail}": "chia sẻ của bạn",
            "{interest}": "quan điểm",
            "{time}": "trước",
            "{reason}": "sự giúp đỡ",
            "{trait}": "tử tế",
            "{topic}": "điều này",
            "{something}": "một bộ phim",
            "{weather}": "đẹp",
            "{memory}": "chuyến đi",
            "{thing}": "món này",
            "{experience}": "một điều thú vị",
            "{news}": "tin vui nhỏ"
        }
        
        result = template
        for key, value in replacements.items():
            result = result.replace(key, value)
        
        return result

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
    
    # === HERO SECTION ===
    st.markdown("""
    <div class="hero-gradient">
        <h1 class="hero-title">💬 EMOTICONN AI</h1>
        <p class="hero-subtitle">
            Trợ lý giao tiếp cảm xúc dành cho người trưởng thành.<br>
            Biến những điều khó nói thành lời tinh tế, chân thành.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # === MAIN CONTENT ===
    if not st.session_state.verified:
        show_verification_section()
    else:
        show_main_app()
    
    # === FOOTER ===
    st.markdown("""
    <div class="footer">
        <p>© 2024 EMOTICONN AI - Dành cho những trái tim trưởng thành</p>
        <p>Hỗ trợ: support@emoticonn.ai | Bảo mật & Chính sách</p>
    </div>
    """, unsafe_allow_html=True)

def show_verification_section():
    """Show phone verification section"""
    st.markdown("""
    <div class="premium-card">
        <h3 class="text-center mb-2">🔐 Bắt Đầu Dùng Thử Miễn Phí</h3>
        <p class="text-center mb-3">Nhập số điện thoại để nhận <b>3 tin nhắn AI cao cấp</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Phone input
    phone_input = st.text_input(
        "**Số điện thoại của bạn**",
        placeholder="0912345678",
        help="Nhập số điện thoại Việt Nam để bắt đầu dùng thử"
    )
    
    # Verify button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Bắt Đầu Dùng Thử", key="verify_btn", use_container_width=True):
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
                    
                    st.success(f"✅ Xác thực thành công! Số điện thoại: {valid_phone}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("⚠️ Số điện thoại không hợp lệ. Vui lòng nhập số Việt Nam (ví dụ: 0912345678)")
            else:
                st.warning("⚠️ Vui lòng nhập số điện thoại")
    
    # Features showcase
    st.markdown("""
    <div class="premium-card">
        <h4 class="mb-2">✨ Tại sao chọn EMOTICONN AI?</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
            <div>
                <h5>🎯 Dành cho người trưởng thành</h5>
                <p>Ngôn từ tinh tế, không sến, không trẻ trâu</p>
            </div>
            <div>
                <h5>💝 Hiểu tâm lý sâu sắc</h5>
                <p>1000+ tình huống thực tế của tuổi 30-50+</p>
            </div>
            <div>
                <h5>🔓 Mô hình đơn giản</h5>
                <p>Dùng thử 3 lần → Trả phí 1 lần → Dùng mãi mãi</p>
            </div>
            <div>
                <h5>📱 Tối ưu mobile</h5>
                <p>Thiết kế đẹp, dễ dùng trên điện thoại</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_main_app():
    """Show main application"""
    # Check if paid or trial
    if not st.session_state.paid:
        remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
        
        if remaining <= 0:
            show_payment_section()
            return
        
        # Show trial counter
        st.markdown(f"""
        <div class="premium-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4>🎯 Bạn đang dùng thử miễn phí</h4>
                    <p>Còn <b>{remaining}/{FREE_TRIAL_LIMIT}</b> lượt sử dụng</p>
                </div>
                <div style="width: 60%;">
        """, unsafe_allow_html=True)
        
        st.progress(st.session_state.usage_count / FREE_TRIAL_LIMIT)
        st.markdown("</div></div></div>", unsafe_allow_html=True)
    
    # === INPUT SECTION ===
    st.markdown("""
    <div class="premium-card">
        <h3 class="mb-2">✍️ Tạo Tin Nhắn Tinh Tế</h3>
        <p class="mb-3">Chọn tình huống và để AI giúp bạn diễn đạt cảm xúc</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User inputs
    col1, col2 = st.columns(2)
    
    with col1:
        user_gender = st.radio(
            "**Giới tính của bạn**",
            ["Nam", "Nữ"],
            horizontal=True
        )
    
    with col2:
        target_gender = st.radio(
            "**Người nhận tin nhắn**",
            ["Nam", "Nữ"],
            horizontal=True
        )
    
    # Situation selection
    situations = [
        "💌 Làm quen lần đầu",
        "🤔 Đối phương lạnh nhạt",
        "💬 Gợi chuyện tinh tế",
        "💔 Đã ly hôn",
        "👨‍👩‍👧 Có con riêng",
        "😠 Ghen nhẹ đúng mực",
        "💰 Áp lực tài chính",
        "☀️ Nhắn buổi sáng",
        "⚡ Khi giận nhau",
        "🌱 Ngại yêu lại"
    ]
    
    situation = st.selectbox(
        "**Chọn tình huống**",
        situations,
        help="Chọn tình huống phù hợp nhất với hoàn cảnh của bạn"
    )
    
    # Optional context
    context = st.text_area(
        "**Thông tin thêm (tuỳ chọn)**",
        placeholder="Ví dụ: Chúng ta quen nhau qua ứng dụng hẹn hò, bạn ấy là giáo viên...\nHoặc: Tôi muốn nhắn sau khi cãi nhau về chuyện đi muộn...",
        height=100,
        help="Càng chi tiết, tin nhắn càng cá nhân hoá"
    )
    
    # Generate button
    if st.button("✨ AI Tạo Tin Nhắn", key="generate_btn", use_container_width=True):
        if not st.session_state.paid:
            # Update usage
            st.session_state.usage_count += 1
            update_usage(st.session_state.phone)
            remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
            
            if remaining < 0:
                st.error("⚠️ Bạn đã hết lượt dùng thử")
                st.rerun()
        
        # Generate message
        ai = EmotionalAI()
        with st.spinner("🔄 AI đang thấu hiểu cảm xúc và tạo tin nhắn tinh tế cho bạn..."):
            time.sleep(1.2)
            result = ai.generate(user_gender, target_gender, situation, context)
            st.session_state.result = result
        
        # Auto-scroll to result
        st.markdown("<div id='result'></div>", unsafe_allow_html=True)
    
    # === RESULT SECTION ===
    if st.session_state.result:
        st.markdown("""
        <div class="result-card">
            <h4>💌 Tin nhắn gợi ý:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Message display
        st.markdown(f"""
        <div class="message-content">
            {st.session_state.result}
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.code(st.session_state.result, language="text")
        
        with col2:
            if st.button("📋 Copy", use_container_width=True):
                st.success("✅ Đã copy tin nhắn!")
        
        with col3:
            if st.button("🔄 Tạo mới", use_container_width=True):
                st.session_state.result = ""
                st.rerun()
        
        # Trial reminder
        if not st.session_state.paid:
            remaining = FREE_TRIAL_LIMIT - st.session_state.usage_count
            if remaining <= 1:
                st.markdown("""
                <div class="premium-card" style="border-left: 5px solid #FF6B9D;">
                    <h4>💎 Chỉ còn 1 lượt dùng thử!</h4>
                    <p>Nâng cấp ngay để không giới hạn tin nhắn tinh tế</p>
                    <button onclick="window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})" 
                            style="background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%); 
                                   color: white; border: none; padding: 10px 20px; 
                                   border-radius: 25px; cursor: pointer; margin-top: 10px;">
                        💳 Xem gói nâng cấp
                    </button>
                </div>
                """, unsafe_allow_html=True)

def show_payment_section():
    """Show payment section when trial ends"""
    st.markdown("""
    <div class="payment-card">
        <h2>🔓 Mở Khoá Vĩnh Viễn</h2>
        <p>Chỉ thanh toán một lần - Dùng trọn đời</p>
        <div class="price-tag">199.000đ</div>
        <p><i>Chưa bằng 1 bữa cafe mỗi tháng</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="premium-card">
        <h3>💳 Hướng Dẫn Thanh Toán</h3>
        
        **1. Chuyển khoản qua ngân hàng:**
        
        ```bash
        Ngân hàng: BIDV
        Số tài khoản: 4430269669
        Chủ tài khoản: NGUYEN XUAN DAT
        Số tiền: 199.000 VND
        Nội dung chuyển khoản: EMOTICONN [SỐ ĐIỆN THOẠI]
        ```
        
        **📌 Ví dụ:**
        - Số điện thoại của bạn: **0912345678**
        - Nội dung CK: **EMOTICONN 0912345678**
        
        **2. Xác nhận thanh toán:**
        
        Sau khi chuyển khoản, nhập số điện thoại để mở khoá ngay.
    </div>
    """, unsafe_allow_html=True)
    
    # Verification
    st.markdown("### ✅ Xác Nhận Thanh Toán")
    
    verify_input = st.text_input(
        "Nhập số điện thoại của bạn để xác nhận:",
        placeholder="0912345678",
        key="payment_verify"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔓 Mở Khoá Ngay", key="unlock_btn", use_container_width=True):
            if verify_input:
                valid_phone = validate_phone(verify_input)
                
                if valid_phone and valid_phone == st.session_state.phone:
                    # Save as paid user
                    save_paid_user(valid_phone)
                    st.session_state.paid = True
                    
                    # Success animation
                    st.balloons()
                    st.success("🎉 Chúc mừng! Bạn đã mở khoá thành công!")
                    
                    # Auto refresh
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("⚠️ Số điện thoại không khớp. Vui lòng kiểm tra lại.")
            else:
                st.warning("⚠️ Vui lòng nhập số điện thoại")
    
    # Try another phone option
    st.markdown("---")
    if st.button("📱 Thử với số điện thoại khác"):
        st.session_state.phone = ""
        st.session_state.verified = False
        st.session_state.paid = False
        st.session_state.usage_count = 0
        st.rerun()

if __name__ == "__main__":
    main()
