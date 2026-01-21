import streamlit as st
import random

st.set_page_config(page_title="Yêu AI 40+", layout="centered")

st.title("❤️ Yêu AI 40+")
st.caption("Gợi ý nhắn tin tinh tế – đúng đàn ông trưởng thành")

# ================== DATA CORE ==================

DATA = {
    "hoi_tham": {
        "nhe": [
            "Anh vẫn ổn, ngày trôi qua khá nhẹ. Còn em thì sao?",
            "Anh ổn, em hỏi vậy là anh thấy vui rồi.",
            "Anh ổn, không có gì đặc biệt. Em thì thế nào?",
            "Anh vẫn như mọi ngày, chỉ là nghe em hỏi thì thấy dễ chịu."
        ],
        "vua": [
            "Anh ổn, nhưng hôm nay nghe em hỏi tự nhiên thấy ấm hơn.",
            "Anh ổn, cũng có chút mệt nhưng không sao. Còn em?",
            "Anh ổn, chỉ là muốn nghe thêm về ngày hôm nay của em.",
            "Anh ổn, em quan tâm vậy là anh thấy đủ rồi."
        ],
        "manh": [
            "Anh ổn, nhưng nghe em hỏi là thấy mình được để ý.",
            "Anh ổn, chỉ là những lúc thế này anh lại nghĩ tới em.",
            "Anh ổn, và thật lòng là anh thích cảm giác được em hỏi han.",
            "Anh ổn, nhưng anh muốn nghe em nói nhiều hơn một chút."
        ]
    },

    "co_ay_met": {
        "nhe": [
            "Mệt thì nghỉ sớm chút đi em.",
            "Nghe vậy là biết hôm nay em không nhẹ rồi.",
            "Mệt thì đừng cố quá.",
            "Có những ngày chỉ cần yên tĩnh là đủ."
        ],
        "vua": [
            "Mệt thì nghỉ ngơi chút, đừng ép mình quá.",
            "Nghe em nói vậy là anh cũng thấy thương.",
            "Hôm nay chắc không dễ với em rồi.",
            "Mệt thì cho phép mình chậm lại một chút."
        ],
        "manh": [
            "Mệt thì nghỉ đi, để anh lo phần quan tâm này.",
            "Nghe em nói vậy là anh chỉ muốn em được nhẹ người hơn.",
            "Có anh ở đây, em không cần phải gồng.",
            "Những lúc mệt thế này, em không cần phải một mình."
        ]
    },

    "lanh": {
        "nhe": [
            "Ừ, anh hiểu.",
            "Không sao đâu.",
            "Anh để em thoải mái nhé.",
            "Khi nào em muốn nói thì nói."
        ],
        "vua": [
            "Có lẽ hôm nay em muốn yên tĩnh.",
            "Anh cảm giác em đang hơi mệt.",
            "Không sao, anh không vội.",
            "Anh ở đây, nhưng không làm phiền."
        ],
        "manh": [
            "Anh tôn trọng khoảng lặng của em.",
            "Khi em cần, anh vẫn ở đây.",
            "Anh không hỏi thêm, nhưng anh để ý.",
            "Sự im lặng này anh hiểu."
        ]
    },

    "vui": {
        "nhe": [
            "Nghe em vui là thấy nhẹ hẳn.",
            "Vậy là hôm nay ổn rồi.",
            "Nghe cũng vui theo.",
            "Có vẻ là ngày đẹp."
        ],
        "vua": [
            "Nghe em vui là tự nhiên anh cũng thấy dễ chịu.",
            "Những lúc thế này nói chuyện với em thích thật.",
            "Cảm giác tích cực này lan sang anh luôn.",
            "Em vui là đủ lý do để ngày này trọn vẹn."
        ],
        "manh": [
            "Nghe em vui là anh thấy ngày mình cũng sáng hơn.",
            "Anh thích nhất là những lúc em vui thế này.",
            "Cảm xúc của em ảnh hưởng tới anh nhiều hơn em nghĩ.",
            "Em vui, anh cũng thấy mình được ở gần em hơn."
        ]
    },

    "chu_dong": {
        "nhe": [
            "Em chủ động thế này cũng dễ thương.",
            "Anh thấy thoải mái khi nói chuyện với em.",
            "Nói chuyện thế này nhẹ nhàng thật.",
            "Anh thích cách em mở câu chuyện."
        ],
        "vua": [
            "Anh thấy dễ chịu khi em chủ động như vậy.",
            "Cách em nói chuyện làm anh muốn nghe thêm.",
            "Nói chuyện thế này không bị gượng.",
            "Anh thích cảm giác tự nhiên này."
        ],
        "manh": [
            "Anh thích sự chủ động này của em.",
            "Nói chuyện với em làm anh thấy gần hơn.",
            "Cảm giác này không phải lúc nào cũng có.",
            "Anh trân trọng cách em bắt đầu câu chuyện."
        ]
    }
}

# ================== ANALYSIS ==================

def detect_category(msg):
    msg = msg.lower()
    if any(x in msg for x in ["khỏe", "sao rồi", "thế nào", "ổn không"]):
        return "hoi_tham"
    if any(x in msg for x in ["mệt", "stress", "buồn", "áp lực"]):
        return "co_ay_met"
    if any(x in msg for x in ["ừ", "ok", "tùy", "sao cũng được"]):
        return "lanh"
    if any(x in msg for x in ["vui", "haha", "thích", "vui ghê"]):
        return "vui"
    return "chu_dong"

def pick_level():
    return random.choice(["nhe", "vua", "manh"])

# ================== UI ==================

last_message = st.text_area(
    "Tin nhắn cuối cùng cô ấy gửi",
    placeholder="Ví dụ: Hôm nay em mệt quá..."
)

if st.button("AI gợi ý trả lời"):
    if not last_message.strip():
        st.warning("Anh nhập tin nhắn của cô ấy trước nhé.")
    else:
        cat = detect_category(last_message)
        level = pick_level()
        reply = random.choice(DATA[cat][level])
        st.success(f"💬 {reply}")
