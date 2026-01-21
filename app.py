import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import uuid

# ==================== CẤU HÌNH ỨNG DỤNG ====================
st.set_page_config(
    page_title="AI Gợi ý Nhắn Tin - Đàn ông trên 40",
    page_icon="💬",
    layout="centered"
)

# ==================== KHỞI TẠO DỮ LIỆU ====================
DATA_FILE = "user_data.json"

def init_data():
    """Khởi tạo file dữ liệu nếu chưa có"""
    if not os.path.exists(DATA_FILE):
        default_data = {
            "trial_users": {},  # Lưu số lần dùng thử: {session_id: count}
            "paid_users": {},   # Lưu user đã thanh toán: {phone: expiry_date}
            "sessions": {}      # Liên kết session với phone
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)

def load_data():
    """Tải dữ liệu từ file"""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    """Lưu dữ liệu vào file"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Khởi tạo dữ liệu
init_data()

# ==================== QUẢN LÝ SESSION ====================
def get_session_id():
    """Lấy hoặc tạo session ID cho người dùng"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

def get_phone_input():
    """Lấy số điện thoại từ người dùng"""
    if "phone_number" not in st.session_state:
        st.session_state.phone_number = ""
    
    phone = st.text_input("📱 Số điện thoại của bạn (để quản lý lượt dùng):", 
                         value=st.session_state.phone_number,
                         placeholder="Nhập số điện thoại...")
    return phone.strip()

# ==================== LOGIC GỢI Ý TIN NHẮN ====================
def generate_response(context, message, relationship_status):
    """Hàm tạo gợi ý trả lời (AI đơn giản)"""
    
    # Template theo tình huống
    templates = {
        "vợ/người yêu": {
            "chúc mừng": [
                "Anh cũng rất vui vì điều đó! Cảm ơn em đã chia sẻ niềm vui với anh ❤️",
                "Thật tuyệt vời! Tối nay mình ăn mừng nhé? Anh sẽ chuẩn bị chút rượu vang.",
                "Anh biết em sẽ làm được mà! Em xứng đáng với thành công này."
            ],
            "buồn/tâm sự": [
                "Anh ở đây với em rồi. Muốn chia sẻ gì cứ nói với anh nhé 💕",
                "Để anh ôm em một cái. Mọi chuyện rồi sẽ ổn thôi, có anh ở đây.",
                "Anh hiểu cảm giác của em. Mình cùng nhau vượt qua nhé."
            ],
            "hỏi về kế hoạch": [
                "Cuối tuần này mình đi ăn tối nhé? Anh đã đặt chỗ ở nhà hàng Ý rồi.",
                "Anh nghĩ mình nên dành thời gian cho nhau nhiều hơn. Em muốn làm gì?",
                "Tối nay anh nấu cơm, em chỉ cần về và thư giãn thôi."
            ],
            "default": [
                "Anh yêu em ❤️",
                "Anh nhớ em nhiều lắm.",
                "Em là người phụ nữ tuyệt vời nhất của anh."
            ]
        },
        "tìm hiểu mới": {
            "chúc mừng": [
                "Thật tuyệt vời! Bạn xứng đáng với thành công đó 🎉",
                "Chúc mừng bạn! Tôi rất vui khi nghe tin này.",
                "Wow, thật ấn tượng! Bạn đã làm rất tốt."
            ],
            "buồn/tâm sự": [
                "Tôi rất tiếc khi nghe điều đó. Nếu cần ai đó lắng nghe, tôi luôn ở đây.",
                "Mong mọi chuyện sẽ tốt đẹp hơn. Đừng ngại chia sẻ nếu bạn muốn.",
                "Tôi hiểu cảm giác đó. Thời gian sẽ giúp mọi thứ dịu lại."
            ],
            "hỏi về kế hoạch": [
                "Cuối tuần này tôi rảnh. Bạn có muốn đi uống cà phê không?",
                "Tôi rất thích ý tưởng đó! Chúng ta nên lên kế hoạch cụ thể.",
                "Nghe hay đấy! Tôi sẽ sắp xếp thời gian phù hợp."
            ],
            "default": [
                "Bạn thật thú vị, tôi rất thích nói chuyện với bạn.",
                "Hy vọng chúng ta có thể hiểu nhau hơn qua những cuộc trò chuyện.",
                "Luôn vui khi được trò chuyện cùng bạn."
            ]
        }
    }
    
    # Phân loại tin nhắn
    message_lower = message.lower()
    category = "default"
    
    if any(word in message_lower for word in ['chúc mừng', 'tốt', 'vui', 'thành công', 'win']):
        category = "chúc mừng"
    elif any(word in message_lower for word in ['buồn', 'mệt', 'khó khăn', 'stress', 'chán']):
        category = "buồn/tâm sự"
    elif any(word in message_lower for word in ['kế hoạch', 'cuối tuần', 'đi đâu', 'làm gì', 'khi nào']):
        category = "hỏi về kế hoạch"
    
    # Chọn template phù hợp
    if relationship_status == "Đã có người yêu / vợ":
        responses = templates["vợ/người yêu"][category]
    else:
        responses = templates["tìm hiểu mới"][category]
    
    # Thêm context nếu có
    if context:
        return f"[{context}] {pd.Series(responses).sample().iloc[0]}"
    return pd.Series(responses).sample().iloc[0]

# ==================== KIỂM TRA QUYỀN SỬ DỤNG ====================
def check_access(phone):
    """Kiểm tra người dùng có quyền sử dụng không"""
    data = load_data()
    session_id = get_session_id()
    
    # Kiểm tra user đã thanh toán
    if phone and phone in data["paid_users"]:
        expiry_str = data["paid_users"][phone]
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d")
        if datetime.now() < expiry_date:
            return True, "paid"
    
    # Kiểm tra dùng thử
    trial_count = data["trial_users"].get(session_id, 0)
    if trial_count < 3:
        return True, "trial"
    
    return False, "locked"

def update_trial_count():
    """Cập nhật số lần dùng thử"""
    data = load_data()
    session_id = get_session_id()
    
    current_count = data["trial_users"].get(session_id, 0)
    data["trial_users"][session_id] = current_count + 1
    save_data(data)
    
    return current_count + 1

# ==================== GIAO DIỆN CHÍNH ====================
def main_page():
    """Trang chính của ứng dụng"""
    
    st.title("💬 AI Gợi Ý Nhắn Tin Cho Đàn Ông Trên 40")
    
    st.markdown("""
    Ứng dụng AI giúp bạn trả lời tin nhắn một cách tinh tế và phù hợp, 
    dựa trên kinh nghiệm và sự thấu hiểu tâm lý đàn ông trưởng thành.
    
    **Dễ dàng - Tinh tế - Hiệu quả**
    """)
    
    # Lấy số điện thoại
    phone = get_phone_input()
    if phone:
        st.session_state.phone_number = phone
    
    # Kiểm tra quyền truy cập
    has_access, access_type = check_access(phone)
    
    if not has_access:
        st.error("⚠️ Bạn đã hết lượt dùng thử!")
        st.info("Vui lòng chuyển sang trang **Thanh Toán** để tiếp tục sử dụng dịch vụ.")
        return
    
    # Hiển thị thông tin lượt dùng
    if access_type == "trial":
        data = load_data()
        session_id = get_session_id()
        trial_count = data["trial_users"].get(session_id, 0)
        remaining = 3 - trial_count
        st.warning(f"Lượt dùng thử còn lại: **{remaining}/3**")
    
    st.divider()
    
    # Form nhập thông tin
    st.subheader("🎯 Tạo gợi ý nhắn tin")
    
    # Chọn tình huống
    relationship_status = st.radio(
        "Bạn đang trong tình huống nào?",
        ["Đã có người yêu / vợ", "Đang tìm hiểu bạn gái mới"],
        horizontal=True
    )
    
    # Nhập context
    context = st.text_input(
        "📝 Hoàn cảnh / Bối cảnh (nếu có):",
        placeholder="Ví dụ: Cô ấy vừa được thăng chức, Cô ấy đang buồn vì công việc..."
    )
    
    # Nhập tin nhắn của cô ấy
    her_message = st.text_area(
        "💌 Tin nhắn của cô ấy:",
        placeholder="Nhập/dán tin nhắn bạn nhận được tại đây...",
        height=100
    )
    
    # Nút gợi ý
    if st.button("🎯 Gợi Ý Trả Lời", type="primary", use_container_width=True):
        if not her_message:
            st.error("Vui lòng nhập tin nhắn của cô ấy!")
        else:
            # Tạo gợi ý
            with st.spinner("AI đang phân tích và tạo gợi ý..."):
                response = generate_response(context, her_message, relationship_status)
                
                # Cập nhật lượt dùng nếu là trial
                if access_type == "trial":
                    update_trial_count()
                
                # Hiển thị kết quả
                st.success("✅ Đây là gợi ý của AI:")
                st.info(f"**{response}**")
                
                # Nút copy
                st.code(response, language="text")

# ==================== TRANG THANH TOÁN ====================
def payment_page():
    """Trang thanh toán"""
    
    st.title("💰 Thanh Toán & Kích Hoạt")
    
    tab1, tab2 = st.tabs(["📋 Thông Tin Thanh Toán", "🔑 Kích Hoạt Dịch Vụ"])
    
    with tab1:
        st.header("Thông Tin Chuyển Khoản")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image("https://api.vietqr.io/image/BIDV-123456-nguyenvana.jpg?accountName=NGUYEN%20VAN%20A&addInfo=AI40_SDT", 
                    caption="QR Code chuyển khoản", use_column_width=True)
        
        with col2:
            st.markdown("""
            ### Ngân hàng: **BIDV**
            ### Số tài khoản: **`4430269669`**
            ### Tên chủ tài khoản: **NGUYỄN VĂN A**
            
            ---
            
            ### 📌 Hướng dẫn:
            1. Chuyển khoản với nội dung: **`AI40_SĐT_CỦA_BẠN`**
            2. Giữ lại biên lai chuyển khoản
            3. Quay lại trang này để kích hoạt
            
            ⚠️ **Lưu ý:** Thay `SĐT_CỦA_BẠN` bằng số điện thoại thật của bạn
            """)
        
        st.divider()
        
        st.header("📊 Bảng Giá Dịch Vụ")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🎯 GÓI 3 NGÀY")
            st.markdown("### 99.000 VND")
            st.caption("• Toàn quyền sử dụng")
            st.caption("• Hỗ trợ 24/7")
        
        with col2:
            st.subheader("🚀 GÓI 7 NGÀY")
            st.markdown("### 199.000 VND")
            st.caption("• Toàn quyền sử dụng")
            st.caption("• Ưu tiên hỗ trợ")
            st.caption("• +5% độ chính xác")
            st.success("**Phổ biến nhất**")
        
        with col3:
            st.subheader("👑 GÓI 30 NGÀY")
            st.markdown("### 699.000 VND")
            st.caption("• Toàn quyền sử dụng")
            st.caption("• Hỗ trợ VIP")
            st.caption("• +10% độ chính xác")
            st.caption("• Tính năng đặc biệt")
    
    with tab2:
        st.header("Kích Hoạt Dịch Vụ")
        
        st.markdown("""
        ### 🔄 Quy trình kích hoạt:
        1. Bạn chuyển khoản
        2. Chúng tôi xác nhận
        3. Bạn nhập số điện thoại để kích hoạt
        
        ⏳ **Thời gian xử lý:** 5-15 phút trong giờ hành chính
        """)
        
        # Form kích hoạt thủ công (cho admin)
        st.divider()
        st.subheader("🔧 Kích Hoạt Thủ Công (Dành cho Admin)")
        
        with st.expander("Quản lý kích hoạt", expanded=False):
            admin_pass = st.text_input("Mật khẩu Admin:", type="password")
            
            if admin_pass == "admin123":  # Mật khẩu đơn giản, có thể thay đổi
                col1, col2 = st.columns(2)
                
                with col1:
                    phone_to_activate = st.text_input("Số điện thoại cần kích hoạt:")
                    days_option = st.selectbox(
                        "Gói dịch vụ:",
                        ["3 ngày", "7 ngày", "30 ngày"]
                    )
                    
                    days_map = {"3 ngày": 3, "7 ngày": 7, "30 ngày": 30}
                    
                    if st.button("✅ Kích Hoạt", type="primary"):
                        if phone_to_activate:
                            data = load_data()
                            expiry_date = datetime.now() + timedelta(days=days_map[days_option])
                            data["paid_users"][phone_to_activate] = expiry_date.strftime("%Y-%m-%d")
                            save_data(data)
                            st.success(f"Đã kích hoạt thành công cho {phone_to_activate}!")
                
                with col2:
                    st.subheader("Danh sách đã kích hoạt")
                    data = load_data()
                    if data["paid_users"]:
                        df = pd.DataFrame([
                            {"SĐT": phone, "Hết hạn": expiry} 
                            for phone, expiry in data["paid_users"].items()
                        ])
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("Chưa có người dùng nào được kích hoạt")

# ==================== ĐIỀU HƯỚNG ====================
def main():
    """Hàm chính điều hướng ứng dụng"""
    
    # Sidebar điều hướng
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
        st.title("AI Nhắn Tin 40+")
        
        st.divider()
        
        page = st.radio(
            "Điều hướng",
            ["🏠 Trang Chính", "💰 Thanh Toán & Kích Hoạt"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Hiển thị thông tin người dùng
        if st.session_state.get("phone_number"):
            st.caption(f"SĐT: {st.session_state.phone_number}")
            
            data = load_data()
            phone = st.session_state.phone_number
            
            if phone in data["paid_users"]:
                expiry = data["paid_users"][phone]
                st.success(f"✅ Đã kích hoạt đến {expiry}")
            else:
                st.warning("⚠️ Chưa kích hoạt")
        
        st.divider()
        
        st.caption("""
        **Hỗ trợ khách hàng:**
        📞 1900 1000
        ✉️ support@ai40.com
        
        *Dành cho đàn ông trên 40 tuổi*
        """)
    
    # Điều hướng trang
    if page == "🏠 Trang Chính":
        main_page()
    else:
        payment_page()

if __name__ == "__main__":
    main()
