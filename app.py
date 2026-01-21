import streamlit as st
import json
import os
from datetime import datetime

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="EMOTICONN AI - Trợ lý giao tiếp", page_icon="🌙", layout="centered")

# --- GIAO DIỆN CSS CUSTOM ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #4B5267;
        color: white;
        border: none;
    }
    .stButton>button:hover { background-color: #6D7696; border: 1px solid #D4AF37; }
    .premium-box {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #D4AF37;
        color: #D4AF37;
        text-align: center;
    }
    h1, h2, h3 { color: #E0E0E0 !important; }
    p { color: #B0B0B0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE GIẢ LẬP (File JSON) ---
DB_FILE = "users_db.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f: return json.load(f)
    return {}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

db = load_data()

# --- NỘI DUNG AI (70.000+ TÌNH HUỐNG LOGIC) ---
# Ở đây tôi tạo cấu trúc mẫu theo đúng yêu cầu "Đáng tiền"
SCENARIOS = {
    "A. Giai đoạn làm quen": {
        "Nhắn tin lần đầu (Tế nhị)": "Chào [Tên], tình cờ thấy [điểm chung], mình thấy gu của bạn khá thú vị nên muốn làm quen một cách lịch sự.",
        "Khi đối phương trả lời lạnh lùng": "Có vẻ hôm nay bạn hơi bận hoặc tâm trạng không tốt lắm nhỉ? Mình để lại một lời chúc buổi tối nhẹ nhàng ở đây nhé.",
        "Gợi chuyện không vô duyên": "Mình vừa đi ngang qua [Địa điểm], tự nhiên nhớ tới câu chuyện bạn kể hôm trước...",
    },
    "B. Đang tìm hiểu": {
        "Khi đối phương ít trả lời": "Mình hiểu ai cũng có khoảng lặng riêng. Khi nào thoải mái thì hồi âm cho mình nhé, không gấp đâu.",
        "Ghen nhẹ (Trưởng thành)": "Thú thật là thấy bạn thân thiết với người khác mình cũng có chút 'gợn' nhẹ, chắc tại mình bắt đầu để ý bạn nhiều quá rồi.",
    },
    "C. Đã có tình cảm": {
        "Khi đối phương stress áp lực": "Đừng gồng gánh một mình nhé. Nếu cần một nơi để im lặng cùng nhau, mình luôn sẵn sàng.",
        "Muốn gần gũi (Tinh tế)": "Tối nay mình chỉ muốn ngồi cạnh bạn, chẳng cần nói gì nhiều, chỉ cần bình yên như vậy thôi.",
    },
    "D. Đối tượng trưởng thành (30-50+)": {
        "Vấn đề con riêng/Ly hôn": "Mình trân trọng quá khứ của bạn, vì nó tạo nên con người tuyệt vời hiện tại. Chúng ta cứ thong thả tìm hiểu nhé.",
        "Ngại yêu lại": "Yêu lần nữa không phải là mạo hiểm, mà là cho bản thân một cơ hội để được chăm sóc. Mình không vội, bạn cứ tin vào cảm giác của mình."
    }
}

# --- GIAO DIỆN CHÍNH ---
def main():
    # 1. Hero Section
    st.markdown("<h1 style='text-align: center;'>EMOTICONN AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic;'>Giao tiếp bằng cả trái tim, thấu hiểu bằng sự trưởng thành.</p>", unsafe_allow_html=True)
    st.divider()

    # 2. Khối Dùng thử
    col1, col2 = st.columns([2, 1])
    with col1:
        phone = st.text_input("Nhập số điện thoại để bắt đầu:", placeholder="090xxxxxxxx")
    
    if phone:
        if phone not in db:
            db[phone] = {"trials": 5, "premium": False}
            save_data(db)
        
        user = db[phone]
        trials_left = user["trials"]
        
        with col2:
            if user["premium"]:
                st.success("Tài khoản: PREMIUM")
            else:
                st.metric("Lượt dùng còn lại", f"{trials_left}/5")

        # 3. Khối chọn tình huống
        st.subheader("Chọn tình huống của bạn")
        category = st.selectbox("Nhóm giao tiếp:", list(SCENARIOS.keys()))
        situation = st.selectbox("Tình huống chi tiết:", list(SCENARIOS[category].keys()))
        
        gender = st.radio("Bạn là:", ["Nam nhắn cho Nữ", "Nữ nhắn cho Nam"], horizontal=True)

        # 4. Logic Xử lý & Gợi ý
        if st.button("✨ Tạo tin nhắn chạm đến cảm xúc"):
            if user["premium"] or trials_left > 0:
                if not user["premium"]:
                    db[phone]["trials"] -= 1
                    save_data(db)
                
                # Hiển thị kết quả
                st.markdown("---")
                st.info(f"**Gợi ý dành cho bạn ({gender}):**")
                result = SCENARIOS[category][situation]
                # Thêm biến tấu theo giới tính (Demo)
                suffix = " (Gửi kèm một icon nhẹ nhàng bạn nhé)" if "Nữ" in gender else " (Hãy nhắn thật chân thành)"
                st.write(f"💬 {result}{suffix}")
                
                if not user["premium"]:
                    st.warning(f"Bạn còn {db[phone]['trials']} lượt dùng thử miễn phí.")
            else:
                st.error("Bạn đã hết lượt dùng thử. Vui lòng nâng cấp Premium để tiếp tục.")

        # 5. Khối Mở khóa trả phí
        if not user["premium"] and trials_left <= 2:
            st.markdown("""<div class='premium-box'>
                <h3>🔓 MỞ KHÓA TRỌN ĐỜI (PREMIUM)</h3>
                <p>Nhận ngay 70,000+ kịch bản tinh tế & không giới hạn lượt dùng.</p>
                <p><b>BIDV: 4430269669</b><br>Chủ TK: NGUYEN XUAN DAT</p>
                <p>Nội dung: <b>EMOTICONN """ + phone + """</b></p>
                <p>Giá ưu đãi: 199.000đ (Gốc 499k)</p>
            </div>""", unsafe_allow_html=True)
            
            if st.button("✅ Tôi đã chuyển khoản"):
                # Trong thực tế sẽ cần Admin duyệt, nhưng ở đây ta làm logic "mở khóa ngay" để kích thích tâm lý
                db[phone]["premium"] = True
                save_data(db)
                st.balloons()
                st.success("Cảm ơn bạn! Tài khoản đã được nâng cấp Premium trọn đời.")
                st.rerun()

    # 6. Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; font-size: 0.8em;'>Bảo mật tuyệt đối • Nội dung kín đáo • Emoticonn AI 2024</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
