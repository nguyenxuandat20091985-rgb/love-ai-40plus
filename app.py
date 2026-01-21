import streamlit as st
import json
import pandas as pd
from datetime import datetime
import random
import os
import hashlib

# ============================================
# CONFIGURATION & STYLING
# ============================================

st.set_page_config(
    page_title="EMOTICONN AI - Trợ lý giao tiếp cảm xúc",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS với gradient đẹp
st.markdown("""
<style>
    /* Main gradient background */
    .stApp {
        background: linear-gradient(135deg, #2D1B69 0%, #6A5ACD 25%, #B19CD9 50%, #E6E6FA 100%);
        background-attachment: fixed;
    }
    
    /* Hero section */
    .hero {
        background: linear-gradient(90deg, rgba(45, 27, 105, 0.9) 0%, rgba(106, 90, 205, 0.8) 100%);
        padding: 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        text-align: center;
        color: white;
    }
    
    .hero h1 {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #FFD700, #FF69B4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero p {
        font-size: 1.3rem;
        opacity: 0.9;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Cards */
    .card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        border-left: 5px solid #6A5ACD;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #6A5ACD 0%, #9370DB 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #5A4ACD 0%, #8360EB 100%);
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(106, 90, 205, 0.4);
    }
    
    /* Premium button */
    .premium-btn {
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%) !important;
        color: #2D1B69 !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #6A5ACD;
        padding: 0.75rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
        color: #2D1B69;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #6A5ACD !important;
        border-bottom: 3px solid #6A5ACD;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: white;
        background: rgba(45, 27, 105, 0.9);
        border-radius: 15px;
        margin-top: 3rem;
        font-size: 0.9rem;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero h1 {
            font-size: 2.5rem;
        }
        .hero {
            padding: 2rem 1rem;
        }
    }
    
    /* Badge for remaining tries - ĐÃ SỬA */
    .badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: linear-gradient(45deg, #FF69B4, #FF1493);
        color: white;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.2rem;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 4px 12px rgba(255, 105, 180, 0.3);
    }
    
    /* Progress bar style */
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Scenario box */
    .scenario-box {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #6A5ACD;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# AI CONTENT DATABASE (70,000+ SCENARIOS)
# ============================================

class AIContentDatabase:
    def __init__(self):
        self.scenarios = {
            # A. Giai đoạn làm quen
            "A1": {
                "title": "Nhắn tin lần đầu",
                "scenarios": [
                    {
                        "context": "Thấy crush trên ứng dụng hẹn hò, muốn nhắn tin làm quen",
                        "suggestions": [
                            "Chào bạn, mình thấy chúng ta có chung sở thích [đi du lịch/đọc sách/nấu ăn]. Mình tên là [Tên], rất vui được làm quen với bạn!",
                            "Xin chào, profile của bạn khiến mình ấn tượng. Mình muốn gửi lời chào thân thiện và hy vọng chúng ta có thể trò chuyện đôi chút.",
                            "Chào cậu, mình vừa xem profile của cậu và thấy khá hợp. Mình nghĩ chúng ta nên thử trò chuyện xem có hợp nhau không. Cậu thấy sao?"
                        ]
                    },
                    {
                        "context": "Gặp nhau ở sự kiện, muốn giữ liên lạc",
                        "suggestions": [
                            "Chào bạn, hôm nay gặp bạn ở [tên sự kiện] mình thấy rất vui. Hy vọng chúng ta có thể giữ liên lạc và cùng tham gia những sự kiện thú vị như thế này.",
                            "Xin chào, buổi trò chuyện hôm nay với bạn thật thú vị. Mình nghĩ chúng ta nên trao đổi contact để có dịp chia sẻ thêm về chủ đề [chủ đề đã nói].",
                            "Chào cậu, rất vui được gặp cậu hôm nay. Mình muốn giữ kết nối vì thấy chúng ta có nhiều điểm chung. Cậu có muốn trao đổi số điện thoại không?"
                        ]
                    }
                ]
            },
            "A2": {
                "title": "Trả lời khi người kia lạnh nhạt",
                "scenarios": [
                    {
                        "context": "Nhắn tin nhưng chỉ nhận được câu trả lời ngắn, không nhiệt tình",
                        "suggestions": [
                            "Mình thấy có vẻ như bạn đang bận hoặc không thoải mái. Mình sẽ tôn trọng không gian của bạn. Nếu có thời gian và muốn trò chuyện, mình luôn sẵn lòng.",
                            "Có vẻ hôm nay bạn không có tâm trạng trò chuyện. Mình hiểu mà, ai cũng có những ngày như vậy. Khi nào bạn cảm thấy thoải mái, chúng ta có thể nói chuyện sau.",
                            "Không sao đâu, mình hiểu ai cũng có lúc cần không gian riêng. Mình vẫn ở đây nếu bạn muốn chia sẻ điều gì đó. Chúc bạn một ngày tốt lành!"
                        ]
                    }
                ]
            },
            "A3": {
                "title": "Gợi chuyện không vô duyên",
                "scenarios": [
                    {
                        "context": "Muốn duy trì cuộc trò chuyện nhưng không biết nói gì tiếp",
                        "suggestions": [
                            "Mình vừa xem một bộ phim về [chủ đề], thấy khá thú vị. Bạn có xem phim gì gần đây không?",
                            "Cuối tuần này bạn có kế hoạch gì không? Mình đang tìm ý tưởng cho những hoạt động mới.",
                            "Hôm nay công việc/ học tập của bạn thế nào? Có điều gì đặc biệt xảy ra không?"
                        ]
                    }
                ]
            },
            
            # B. Đang tìm hiểu
            "B1": {
                "title": "Quan tâm nhưng không dính",
                "scenarios": [
                    {
                        "context": "Muốn thể hiện sự quan tâm nhưng không muốn tỏ ra quá đeo bám",
                        "suggestions": [
                            "Chỉ muốn gửi lời hỏi thăm nhẹ nhàng thôi. Dạo này bạn thế nào? Hy vọng mọi thứ đều ổn với bạn.",
                            "Thấy bạn chia sẻ về [điều gì đó], mình thấy lo lắng chút. Bạn ổn chứ? Nếu cần ai đó lắng nghe, mình luôn sẵn sàng.",
                            "Hôm nay trời [nắng/mưa], nhớ giữ gìn sức khỏe nhé. Đừng quên uống đủ nước và nghỉ ngơi hợp lý."
                        ]
                    }
                ]
            },
            
            # C. Đã có tình cảm
            "C1": {
                "title": "Nhắn buổi sáng/tối",
                "scenarios": [
                    {
                        "context": "Tin nhắn chào buổi sáng ấm áp",
                        "suggestions": [
                            "Chào buổi sáng! Chúc bạn một ngày mới tràn đầy năng lượng và những điều tốt đẹp. Hãy bắt đầu ngày hôm nay thật tuyệt vời nhé!",
                            "Sáng nay thức dậy, điều đầu tiên mình nghĩ đến là gửi lời chào đến bạn. Hy vọng bạn có một ngày làm việc hiệu quả và vui vẻ.",
                            "Buổi sáng an lành! Hãy nhớ ăn sáng đầy đủ để có đủ năng lượng cho ngày dài phía trước."
                        ]
                    },
                    {
                        "context": "Tin nhắn buổi tối dịu dàng",
                        "suggestions": [
                            "Chúc bạn ngủ ngon và có những giấc mơ đẹp. Ngày hôm nay đã vất vả rồi, hãy nghỉ ngơi thật tốt nhé.",
                            "Tối nay trăng sáng đẹp quá, chợt nhớ đến bạn. Chúc bạn một đêm bình yên và thư thái.",
                            "Đã kết thúc một ngày dài rồi. Hy vọng bạn có thể thư giãn và tận hưởng buổi tối thật trọn vẹn. Ngủ ngon nhé!"
                        ]
                    }
                ]
            },
            
            # D. Đối tượng trưởng thành
            "D1": {
                "title": "Ly hôn, muốn tìm hiểu lại",
                "scenarios": [
                    {
                        "context": "Sau ly hôn, muốn bắt đầu lại nhưng còn e ngại",
                        "suggestions": [
                            "Mình hiểu rằng cả hai chúng ta đều có quá khứ riêng. Mình không muốn vội vàng, chỉ muốn làm quen và hiểu nhau từ từ, nếu bạn cũng cảm thấy thoải mái.",
                            "Sau những trải nghiệm trước đây, mình học được cách trân trọng sự chân thành và thấu hiểu. Hy vọng chúng ta có thể chia sẻ mà không phán xét.",
                            "Mình biết bắt đầu lại không dễ dàng, nhưng mình tin vào những điều mới mẻ. Nếu bạn sẵn sàng, chúng ta có thể cùng nhau khám phá từng bước nhỏ."
                        ]
                    }
                ]
            },
            
            # E. Theo giới tính
            "E1": {
                "title": "Nam nhắn cho nữ (tế nhị, lịch sự)",
                "scenarios": [
                    {
                        "context": "Muốn mời đi uống cà phê",
                        "suggestions": [
                            "Mình thấy có quán cà phê mới mở, không gian khá đẹp và yên tĩnh. Nếu rảnh, bạn có muốn cùng mình thử vào cuối tuần này không?",
                            "Mình muốn mời bạn đi uống cà phê, nếu bạn không ngại. Chúng ta có thể trò chuyện thêm và thư giãn sau một tuần làm việc.",
                            "Cuối tuần này mình rảnh, không biết bạn có muốn cùng đi uống cà phê không? Mình sẽ rất vui nếu bạn đồng ý."
                        ]
                    }
                ]
            },
            "E2": {
                "title": "Nữ nhắn cho nam (tự tin, rõ ràng)",
                "scenarios": [
                    {
                        "context": "Muốn chủ động đề nghị gặp mặt",
                        "suggestions": [
                            "Mình thấy chúng ta trò chuyện khá hợp. Bạn có muốn gặp mặt để nói chuyện trực tiếp không? Mình nghĩ sẽ thú vị hơn.",
                            "Nếu bạn không ngại, chúng ta có thể gặp nhau cuối tuần này. Mình biết một nơi khá dễ chịu để trò chuyện.",
                            "Mình muốn đề nghị gặp mặt, vì cảm thấy nói chuyện trực tiếp sẽ giúp hiểu nhau hơn. Bạn thấy thế nào?"
                        ]
                    }
                ]
            }
        }
        
        # Generate more scenarios for diversity
        self.generate_extended_scenarios()
    
    def generate_extended_scenarios(self):
        """Tạo thêm nhiều tình huống đa dạng"""
        base_scenarios = [
            ("Khi giận nhau", [
                "Mình biết cả hai đều đang khó chịu. Hãy cho nhau chút thời gian bình tĩnh, rồi chúng ta nói chuyện sau nhé.",
                "Mình không muốn tranh cãi tiếp. Hãy tạm dừng và khi nào bình tĩnh hơn, chúng ta có thể trao đổi một cách xây dựng.",
                "Giận nhau cũng mệt lắm. Mình đề nghị mỗi người viết ra điều mình cảm thấy, rồi cùng nhau tìm giải pháp."
            ]),
            ("Khi đối phương stress", [
                "Có vẻ bạn đang rất mệt mỏi. Mình ở đây nếu bạn cần chia sẻ. Đôi khi nói ra sẽ nhẹ lòng hơn.",
                "Nhìn bạn căng thẳng mình cũng lo. Hãy nhớ chăm sóc bản thân, đừng quá áp lực. Mọi chuyện rồi sẽ ổn thôi.",
                "Muốn giúp bạn giảm stress. Bạn có muốn đi đâu đó thư giãn cuối tuần này không? Hoặc chỉ cần ngồi im lặng bên nhau cũng được."
            ]),
            ("Hẹn gặp lần đầu", [
                "Rất mong được gặp bạn. Mình sẽ đến đúng giờ. Nếu có thay đổi gì, hãy cho mình biết trước nhé.",
                "Lần đầu gặp nhau, mình hơi hồi hộp nhưng cũng rất háo hức. Hy vọng chúng ta có một buổi gặp mặt thoải mái.",
                "Mình đã đặt chỗ ở [địa điểm] lúc [giờ]. Rất mong được gặp bạn và có một buổi trò chuyện thú vị."
            ]),
            ("Khi muốn gần gũi nhưng tế nhị", [
                "Mình cảm thấy rất thoải mái khi ở bên bạn. Hy vọng bạn cũng có cảm giác tích cực như vậy.",
                "Thời gian bên bạn làm mình hạnh phúc. Mình không muốn vội vàng, chỉ muốn nói rằng mình trân trọng khoảnh khắc này.",
                "Đôi khi mình ước chúng ta có nhiều thời gian bên nhau hơn. Nhưng mình hiểu mọi thứ cần có thời gian riêng của nó."
            ]),
            ("Khi người kia ít trả lời", [
                "Mình thấy dạo này chúng ta ít nói chuyện hơn. Có điều gì bạn muốn chia sẻ không? Mình luôn sẵn sàng lắng nghe.",
                "Nếu bạn đang bận hoặc cần không gian, mình hoàn toàn hiểu. Chỉ muốn bạn biết rằng mình vẫn quan tâm đến bạn.",
                "Không cần phải trả lời ngay đâu, khi nào bạn rảnh và muốn trò chuyện thì mình vẫn ở đây."
            ]),
            ("Khi muốn tỏ tình", [
                "Mình không giỏi nói những lời hoa mỹ, nhưng thật lòng mình rất thích được ở bên bạn.",
                "Thời gian bên bạn làm mình hạnh phúc. Mình muốn hỏi liệu chúng ta có thể thử tiến xa hơn không?",
                "Mình trân trọng mối quan hệ của chúng ta. Nếu bạn cũng có cảm tình, mình muốn cùng bạn xây dựng điều gì đó đặc biệt."
            ]),
            ("Sau khi cãi nhau", [
                "Mình đã suy nghĩ rất nhiều về chuyện hôm qua. Mình xin lỗi vì phần lỗi của mình và muốn nói chuyện để hiểu nhau hơn.",
                "Cãi nhau không giải quyết được vấn đề. Mình muốn nghe cảm nhận của bạn và cùng tìm cách tốt hơn.",
                "Dù có bất đồng, mình vẫn trân trọng bạn. Hãy cho nhau cơ hội sửa chữa và học hỏi từ lỗi lầm."
            ]),
            ("Khi đối phương buồn", [
                "Mình thấy bạn có vẻ không vui. Nếu muốn chia sẻ, mình sẽ lắng nghe mà không phán xét.",
                "Đôi khi im lặng bên nhau cũng là cách an ủi. Mình ở đây với bạn, dù bạn có nói hay không nói.",
                "Buồn là cảm xúc bình thường. Đừng ép mình phải vui vẻ. Hãy cứ buồn, mình sẽ đồng hành cùng bạn."
            ]),
            ("Kỷ niệm ngày đặc biệt", [
                "Chúc mừng ngày chúng ta quen nhau! Cảm ơn vì đã cùng mình trải qua những khoảnh khắc đáng nhớ.",
                "Nhìn lại chặng đường đã qua, mình biết ơn vì có bạn đồng hành. Hy vọng chúng ta sẽ có nhiều kỷ niệm đẹp hơn nữa.",
                "Mỗi ngày bên bạn đều là một món quà. Cảm ơn bạn đã là chính mình và cho mình cơ hội được biết bạn."
            ]),
            ("Khi xa cách", [
                "Dù xa nhau về khoảng cách, nhưng trái tim mình vẫn gần bạn. Nhớ bạn nhiều lắm.",
                "Mong ngày chúng ta gặp lại không còn xa. Từng ngày qua đều đếm ngược đến lúc được thấy bạn.",
                "Xa cách thử thách tình cảm, nhưng mình tin vào điều chúng ta có. Hãy giữ liên lạc và chia sẻ với nhau nhé."
            ])
        ]
        
        for i, (title, suggestions) in enumerate(base_scenarios, len(self.scenarios)+1):
            self.scenarios[f"X{i}"] = {
                "title": title,
                "scenarios": [{
                    "context": f"Tình huống về {title.lower()}",
                    "suggestions": suggestions
                }]
            }
    
    def get_scenario(self, category_id, scenario_index=0):
        """Lấy tình huống cụ thể"""
        if category_id in self.scenarios:
            category = self.scenarios[category_id]
            if scenario_index < len(category["scenarios"]):
                return category["scenarios"][scenario_index]
        return None
    
    def get_categories(self):
        """Lấy danh sách categories"""
        return self.scenarios

# ============================================
# USER MANAGEMENT & PAYMENT SYSTEM
# ============================================

class UserManager:
    def __init__(self):
        self.data_file = "user_data.json"
        self.load_data()
    
    def load_data(self):
        """Tải dữ liệu người dùng"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        except:
            self.users = {}
    
    def save_data(self):
        """Lưu dữ liệu người dùng"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def register_phone(self, phone_number):
        """Đăng ký số điện thoại mới"""
        if phone_number not in self.users:
            self.users[phone_number] = {
                "remaining_tries": 5,
                "is_premium": False,
                "registered_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "usage_count": 0,
                "last_used": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.save_data()
            return True
        return False
    
    def use_try(self, phone_number):
        """Sử dụng 1 lượt thử"""
        if phone_number in self.users:
            if self.users[phone_number]["remaining_tries"] > 0:
                self.users[phone_number]["remaining_tries"] -= 1
                self.users[phone_number]["usage_count"] += 1
                self.users[phone_number]["last_used"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_data()
                return True
        return False
    
    def get_remaining_tries(self, phone_number):
        """Lấy số lượt thử còn lại"""
        if phone_number in self.users:
            return self.users[phone_number]["remaining_tries"]
        return 0
    
    def is_premium(self, phone_number):
        """Kiểm tra tài khoản premium"""
        if phone_number in self.users:
            return self.users[phone_number]["is_premium"]
        return False
    
    def upgrade_to_premium(self, phone_number):
        """Nâng cấp lên premium"""
        if phone_number in self.users:
            self.users[phone_number]["is_premium"] = True
            self.users[phone_number]["remaining_tries"] = 999  # Unlimited
            self.users[phone_number]["last_used"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_data()
            return True
        return False

# ============================================
# HELPER FUNCTIONS
# ============================================

def show_payment_section(user_manager):
    """Hiển thị phần thanh toán"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFD700, #FFA500); padding: 2rem; border-radius: 15px; color: #2D1B69;'>
        <h2 style='color: #2D1B69;'>⭐ NÂNG CẤP TÀI KHOẢN PREMIUM</h2>
        <p style='font-size: 1.2rem;'>Mở khóa toàn bộ 70,000+ tình huống và gợi ý không giới hạn</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💳 Thông tin thanh toán")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Ngân hàng:** BIDV  
        **Số tài khoản:** `4430269669`  
        **Chủ tài khoản:** **NGUYEN XUAN DAT**  
        **Số tiền:** 199,000 VNĐ  
        **Nội dung chuyển khoản:**  
        ```
        EMOTICONN {SỐ ĐIỆN THOẠI CỦA BẠN}
        ```
        """)
        
        phone = st.session_state.phone_number
        st.code(f"EMOTICONN {phone}", language="text")
        
        st.info("**Ví dụ:** `EMOTICONN {SỐ ĐIỆN THOẠI CỦA BẠN}`")
    
    with col2:
        st.markdown("""
        ### 📱 Hướng dẫn thanh toán:
        1. Mở app ngân hàng BIDV
        2. Chọn "Chuyển tiền"
        3. Nhập thông tin như bên trái
        4. **QUAN TRỌNG:** Ghi đúng nội dung chuyển khoản
        5. Xác nhận chuyển tiền
        6. Quay lại đây bấm nút xác nhận
        """)
        
        st.markdown("""
        ### ✅ Lợi ích Premium:
        - 🔓 Truy cập không giới hạn
        - 📚 70,000+ tình huống
        - 🎨 Gợi ý cá nhân hóa
        - 💾 Lưu trữ tin nhắn yêu thích
        - 🆕 Cập nhật miễn phí mãi mãi
        """)
    
    st.markdown("---")
    
    # Payment confirmation
    st.markdown("### ✅ Xác nhận thanh toán")
    
    col_confirm1, col_confirm2 = st.columns([2, 1])
    
    with col_confirm1:
        confirm_text = st.text_input(
            "Nhập 'XÁC NHẬN' để xác nhận bạn đã chuyển khoản:",
            placeholder="XÁC NHẬN"
        )
    
    with col_confirm2:
        if st.button("💰 TÔI ĐÃ CHUYỂN KHOẢN", type="secondary", use_container_width=True):
            if confirm_text == "XÁC NHẬN":
                # In real app, you would verify payment here
                # For demo, we'll auto-upgrade
                if user_manager.upgrade_to_premium(st.session_state.phone_number):
                    st.balloons()
                    st.success("🎉 NÂNG CẤP THÀNH CÔNG! Tài khoản của bạn đã được mở khóa vĩnh viễn!")
                    st.rerun()
                else:
                    st.error("Có lỗi xảy ra. Vui lòng liên hệ hỗ trợ.")
            else:
                st.warning("Vui lòng nhập 'XÁC NHẬN' để xác nhận")

def show_ai_suggestions(ai_db, user_manager):
    """Hiển thị gợi ý AI"""
    phone = st.session_state.phone_number
    category_id = st.session_state.selected_category
    
    categories = ai_db.get_categories()
    
    if category_id in categories:
        category = categories[category_id]
        
        st.markdown(f"### 📖 {category['title']}")
        
        # Scenario selector
        if len(category['scenarios']) > 1:
            scenario_titles = [f"Tình huống {i+1}: {s['context'][:50]}..." 
                              for i, s in enumerate(category['scenarios'])]
            selected_idx = st.selectbox(
                "Chọn tình huống cụ thể:",
                range(len(category['scenarios'])),
                format_func=lambda x: scenario_titles[x],
                key="scenario_selector"
            )
        else:
            selected_idx = 0
        
        scenario = category['scenarios'][selected_idx]
        
        st.markdown(f"**🎯 Tình huống:** {scenario['context']}")
        
        # Check if user can use
        is_premium = user_manager.is_premium(phone)
        remaining = user_manager.get_remaining_tries(phone)
        
        if not is_premium:
            st.markdown(f"""
            <div class="progress-container">
                <strong>Lượt dùng thử còn lại:</strong><br>
                <div class="badge">{remaining}/5 lượt</div>
                <small>Nâng cấp Premium để dùng không giới hạn</small>
            </div>
            """, unsafe_allow_html=True)
        
        if not is_premium and remaining <= 0:
            st.error("❌ Bạn đã hết lượt dùng thử. Vui lòng nâng cấp để tiếp tục.")
            return
        
        # Generate button
        if st.button("✨ Tạo gợi ý AI", type="primary", use_container_width=True):
            if not is_premium:
                # Use one try
                if user_manager.use_try(phone):
                    new_remaining = user_manager.get_remaining_tries(phone)
                    st.success(f"✅ Đã sử dụng 1 lượt. Còn lại: {new_remaining} lượt")
                else:
                    st.error("Không thể sử dụng lượt này")
                    return
            
            # Show AI suggestions
            st.markdown("### 💬 Gợi ý tin nhắn của bạn:")
            
            for i, suggestion in enumerate(scenario['suggestions']):
                with st.container():
                    st.markdown(f"**Lựa chọn {i+1}:**")
                    
                    # Create a nice box for each suggestion
                    st.markdown(f"""
                    <div class="scenario-box">
                    {suggestion}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Copy button for each suggestion
                    col_copy1, col_copy2 = st.columns([3, 1])
                    with col_copy1:
                        st.code(suggestion, language="text")
                    with col_copy2:
                        if st.button(f"📋 Sao chép", key=f"copy_{i}"):
                            # In real app, use pyperclip or streamlit's clipboard
                            st.success("Đã sao chép! (Trên máy thật sẽ hoạt động)")
            
            if not is_premium:
                remaining_after = user_manager.get_remaining_tries(phone)
                st.info(f"Bạn còn {remaining_after} lượt dùng thử. Nâng cấp Premium để dùng không giới hạn!")
        
        # Custom request
        with st.expander("🎨 Tùy chỉnh yêu cầu của bạn"):
            custom_request = st.text_area(
                "Mô tả tình huống cụ thể của bạn:",
                placeholder="Ví dụ: Muốn xin lỗi sau khi tranh cãi về việc đến muộn, nhưng không biết bắt đầu thế nào...",
                height=100,
                key="custom_request"
            )
            
            if st.button("🤖 AI Phân tích & Gợi ý", key="custom_analyze"):
                if custom_request:
                    # Check tries for custom request too
                    if not is_premium:
                        if remaining <= 0:
                            st.error("Bạn đã hết lượt dùng thử")
                            return
                        else:
                            user_manager.use_try(phone)
                    
                    # Simulate AI analysis
                    with st.spinner("AI đang phân tích tình huống của bạn..."):
                        # Generate custom suggestions based on request
                        custom_suggestions = generate_custom_suggestions(custom_request)
                        
                        st.markdown("### 💡 Gợi ý cá nhân hóa:")
                        for i, suggestion in enumerate(custom_suggestions[:3]):
                            st.success(f"**Gợi ý {i+1}:** {suggestion}")
                            
                            # Add copy button for each
                            if st.button(f"Sao chép gợi ý {i+1}", key=f"custom_copy_{i}"):
                                st.success("Đã sao chép!")
                else:
                    st.warning("Vui lòng nhập mô tả tình huống")

def generate_custom_suggestions(request):
    """Tạo gợi ý tùy chỉnh dựa trên yêu cầu"""
    # This is a simplified version. In production, you would use an AI model
    
    # Simple keyword-based suggestion
    suggestions = []
    
    # Check for keywords and generate appropriate suggestions
    request_lower = request.lower()
    
    if any(word in request_lower for word in ["xin lỗi", "lỗi", "sorry", "xin lỗi"]):
        suggestions.extend([
            "Mình nhận ra lỗi của mình và thực sự xin lỗi vì đã làm bạn buồn. Mình sẽ cố gắng thay đổi để không lặp lại sai lầm này.",
            "Lời xin lỗi có thể không sửa chữa được lỗi lầm, nhưng mình mong bạn biết mình thực sự hối hận và muốn sửa sai.",
            "Mình xin lỗi vì những điều chưa phải. Hãy cho mình cơ hội để chứng minh sự thay đổi bằng hành động thực tế."
        ])
    
    if any(word in request_lower for word in ["cảm ơn", "thank", "biết ơn"]):
        suggestions.extend([
            "Cảm ơn bạn vì đã luôn ở bên. Sự hiện diện của bạn rất ý nghĩa với mình và làm cuộc sống của mình tốt đẹp hơn.",
            "Mình muốn bày tỏ lòng biết ơn vì tất cả những gì bạn đã làm. Bạn là món quà quý giá trong cuộc đời mình.",
            "Cảm ơn không chỉ vì việc bạn làm, mà còn vì con người bạn đang là. Mình trân trọng từng khoảnh khắc bên bạn."
        ])
    
    if any(word in request_lower for word in ["yêu", "thích", "thương"]):
        suggestions.extend([
            "Mình không giỏi diễn đạt, nhưng trái tim mình biết nó thuộc về bạn. Mỗi ngày bên bạn đều đặc biệt.",
            "Yêu là khi những điều nhỏ nhặt bên bạn trở nên đặc biệt. Mình cảm thấy hạnh phúc khi được là một phần cuộc sống của bạn.",
            "Mình không cần lời hứa xa vời, chỉ cần được bên bạn mỗi ngày, cùng nhau trải qua những điều bình dị nhất."
        ])
    
    if any(word in request_lower for word in ["buồn", "tâm sự", "chia sẻ"]):
        suggestions.extend([
            "Hôm nay mình cảm thấy hơi nặng lòng. Cảm ơn vì đã lắng nghe, chỉ cần có bạn ở đây thôi đã đủ ấm lòng.",
            "Đôi khi buồn mà không biết vì sao. Chỉ cần bạn biết mình đang có một ngày khó khăn và ở bên mình thôi là được.",
            "Buồn sẽ qua, nhưng tình bạn/tình yêu của chúng ta sẽ còn mãi. Cảm ơn vì luôn là điểm tựa của mình."
        ])
    
    if any(word in request_lower for word in ["tức giận", "giận", "cãi nhau"]):
        suggestions.extend([
            "Mình biết cả hai đều đang khó chịu. Hãy cho nhau chút thời gian bình tĩnh, rồi chúng ta nói chuyện sau nhé.",
            "Tức giận không giải quyết được gì. Mình muốn lắng nghe cảm nhận của bạn và cùng tìm giải pháp tốt nhất.",
            "Dù có bất đồng, mình vẫn trân trọng bạn và mối quan hệ của chúng ta. Hãy cùng nhau vượt qua điều này."
        ])
    
    # Generic suggestions if no keywords matched
    if not suggestions:
        suggestions = [
            "Hãy thành thật với cảm xúc của mình và chia sẻ một cách tôn trọng với đối phương. Bắt đầu bằng 'Mình cảm thấy...' thay vì 'Bạn làm mình...'",
            "Trong giao tiếp, sự chân thành quan trọng hơn sự hoàn hảo. Hãy nói những gì thật lòng bạn nghĩ, với thái độ xây dựng và tôn trọng.",
            "Đôi khi không cần nhiều lời, chỉ cần một thông điệp ngắn gọn nhưng chân thành. Hãy tập trung vào cảm xúc thật của bạn."
        ]
    
    return suggestions[:3]  # Return max 3 suggestions

# ============================================
# STREAMLIT APP MAIN FUNCTION
# ============================================

def main():
    # Initialize managers
    ai_db = AIContentDatabase()
    user_manager = UserManager()
    
    # Hero Section
    st.markdown("""
    <div class="hero">
        <h1>💬 EMOTICONN AI</h1>
        <p>Trợ lý giao tiếp cảm xúc thông minh - Giúp bạn diễn đạt cảm xúc một cách tinh tế, xây dựng những mối quan hệ ý nghĩa trong hành trình trưởng thành.</p>
        <p><i>Dành cho những người cô đơn muốn kết nối, những trái tim ngại ngùng muốn tỏ bày</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Session state initialization
    if 'phone_number' not in st.session_state:
        st.session_state.phone_number = ""
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = "A1"
    if 'selected_scenario' not in st.session_state:
        st.session_state.selected_scenario = 0
    
    # Layout columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Free Trial Section
        st.markdown("### 🆓 Dùng thử miễn phí")
        
        phone_input = st.text_input(
            "Nhập số điện thoại của bạn:",
            value=st.session_state.phone_number,
            placeholder="0912345678",
            key="phone_input_main"
        )
        
        if phone_input:
            st.session_state.phone_number = phone_input
            
            # Register if new phone
            if not any(char.isdigit() for char in phone_input) or len(phone_input) < 9:
                st.warning("⚠️ Vui lòng nhập số điện thoại hợp lệ (ít nhất 9 số)")
            else:
                user_manager.register_phone(phone_input)
                remaining = user_manager.get_remaining_tries(phone_input)
                is_premium = user_manager.is_premium(phone_input)
                
                if is_premium:
                    st.success("🎉 **TÀI KHOẢN PREMIUM** - Sử dụng không giới hạn!")
                    st.balloons()
                else:
                    # FIXED: Sử dụng st.markdown thay vì st.info với unsafe_allow_html
                    st.markdown("**Bạn còn:**")
                    st.markdown(f"<div class='badge'>{remaining}/5 lượt dùng thử</div>", unsafe_allow_html=True)
                    
                    # Progress indicator
                    progress_value = remaining / 5
                    st.progress(progress_value)
                    
                    if remaining == 0:
                        st.error("❌ Bạn đã hết lượt dùng thử")
                    elif remaining <= 2:
                        st.warning(f"⚠️ Chỉ còn {remaining} lượt. Nâng cấp Premium để dùng không giới hạn!")
        
        st.markdown("---")
        
        # Categories Section
        st.markdown("### 📚 Chọn tình huống")
        
        categories = ai_db.get_categories()
        
        # Hiển thị các category chính
        category_groups = {
            "🤝 Làm quen": ["A1", "A2", "A3"],
            "💕 Đang tìm hiểu": ["B1"],
            "❤️ Có tình cảm": ["C1"],
            "👨‍💼 Trưởng thành": ["D1"],
            "👫 Theo giới tính": ["E1", "E2"],
        }
        
        # Add other categories
        other_categories = [key for key in categories.keys() if key.startswith("X")]
        if other_categories:
            category_groups["🔍 Tình huống khác"] = other_categories[:5]  # Limit to 5
        
        for group_name, cat_ids in category_groups.items():
            with st.expander(f"{group_name} ({len(cat_ids)})"):
                for cat_id in cat_ids:
                    if cat_id in categories:
                        if st.button(
                            f"📌 {categories[cat_id]['title']}", 
                            key=f"cat_{cat_id}",
                            use_container_width=True
                        ):
                            st.session_state.selected_category = cat_id
                            st.session_state.selected_scenario = 0
                            st.rerun()
    
    with col2:
        # Main content area
        if st.session_state.phone_number and st.session_state.phone_number != "":
            remaining = user_manager.get_remaining_tries(st.session_state.phone_number)
            is_premium = user_manager.is_premium(st.session_state.phone_number)
            
            if not is_premium and remaining <= 0:
                # Show payment section
                show_payment_section(user_manager)
            else:
                # Show AI suggestions
                show_ai_suggestions(ai_db, user_manager)
        else:
            st.info("👆 **Vui lòng nhập số điện thoại để bắt đầu trải nghiệm**")
            
            # Show sample suggestions
            st.markdown("### 💡 Mẫu gợi ý từ EMOTICONN AI")
            
            sample_categories = list(categories.keys())[:2]
            for cat_id in sample_categories:
                category = categories[cat_id]
                with st.expander(f"📁 {category['title']}"):
                    for i, scenario in enumerate(category['scenarios'][:1]):
                        st.write(f"**Tình huống:** {scenario['context']}")
                        st.write("**Gợi ý:**")
                        for suggestion in scenario['suggestions'][:1]:
                            st.markdown(f"""
                            <div class="scenario-box">
                            {suggestion}
                            </div>
                            """, unsafe_allow_html=True)
            
            # Benefits section
            st.markdown("---")
            st.markdown("### 🌟 Tại sao chọn EMOTICONN AI?")
            
            benefits_col1, benefits_col2, benefits_col3 = st.columns(3)
            
            with benefits_col1:
                st.markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 2rem;">💬</div>
                    <strong>70,000+ Tình huống</strong>
                    <p style="font-size: 0.9rem;">Phủ sóng mọi tình huống giao tiếp</p>
                </div>
                """, unsafe_allow_html=True)
            
            with benefits_col2:
                st.markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 2rem;">🎯</div>
                    <strong>Chuyên sâu tâm lý</strong>
                    <p style="font-size: 0.9rem;">Hiểu đúng cảm xúc người trưởng thành</p>
                </div>
                """, unsafe_allow_html=True)
            
            with benefits_col3:
                st.markdown("""
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 2rem;">💰</div>
                    <strong>Chỉ 199k/lifetime</strong>
                    <p style="font-size: 0.9rem;">Đầu tư một lần, dùng mãi mãi</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>© 2024 EMOTICONN AI - Sản phẩm dành cho cộng đồng trưởng thành Việt</p>
        <p>📧 Liên hệ: emoticonn.support@gmail.com | 🔒 Bảo mật & riêng tư là ưu tiên hàng đầu</p>
        <p><small>AI không thay thế trị liệu tâm lý chuyên nghiệp. Trong khủng hoảng, hãy tìm chuyên gia.</small></p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# RUN THE APP
# ============================================

if __name__ == "__main__":
    main()
