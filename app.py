"""
HỆ THỐNG AI NHẮN TIN TRƯỞNG THÀNH CHO NAM 40+
"""
import re
import random
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib
from enum import Enum

class RelationshipStage(Enum):
    """Giai đoạn quan hệ"""
    NEW = "new"           # Mới quen, đang tán
    DATING = "dating"     # Đang hẹn hò
    SERIOUS = "serious"   # Nghiêm túc
    COMMITTED = "committed" # Gắn bó
    
class ResponseStrategy(Enum):
    """Chiến lược phản hồi"""
    MAINTAIN_VALUE = "giu_gia_tri"
    MODERATE_CARE = "quan_tam_vua_du"
    GIVE_SPACE = "cho_khong_gian"
    EMOTIONAL_CONNECT = "ket_noi_cam_xuc"
    PLAYFUL_TEASE = "tinh_te_dua"
    DEEP_SHARE = "chia_se_sau"

@dataclass
class MessageAnalysis:
    """Kết quả phân tích tin nhắn"""
    original_text: str
    detected_context: str
    emotion_level: str  # 'nhẹ', 'vừa', 'sâu'
    urgency: float  # 0-1
    emotional_tone: Dict[str, float]  # positive, negative, neutral
    keywords: List[str]
    implied_needs: List[str]
    requires_follow_up: bool = False
    
class MatureMessagingAI:
    """Hệ thống AI nhắn tin trưởng thành"""
    
    def __init__(self, data_path: str = "scenario_data.json"):
        self.data_path = data_path
        self.context_groups = self._load_scenario_data()
        self.conversation_history = []
        self.relationship_stage = RelationshipStage.DATING
        self.user_profile = {
            "gender": "male",
            "age_group": "40+",
            "communication_style": "mature_refined"
        }
        
        # Từ khóa cảm xúc để nhận diện
        self.emotion_keywords = {
            "buồn": ["buồn", "chán", "tệ", "mệt", "thất vọng"],
            "vui": ["vui", "tốt", "tuyệt", "hạnh phúc", "thích"],
            "giận": ["giận", "tức", "bực", "khó chịu", "phiền"],
            "lo": ["lo", "sợ", "băn khoăn", "bất an", "căng thẳng"],
            "trung_lập": ["ổn", "bình thường", "tạm được", "cũng được"]
        }
        
        # Mapping ngữ cảnh với từ khóa
        self.context_patterns = self._build_context_patterns()
        
    def _load_scenario_data(self) -> Dict:
        """Tải dữ liệu tình huống từ file JSON"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Trả về dữ liệu mẫu nếu file không tồn tại
            return self._create_sample_data()
    
    def _create_sample_data(self) -> Dict:
        """Tạo dữ liệu mẫu với ít nhất 25 nhóm ngữ cảnh"""
        sample_data = {
            "context_groups": [
                {
                    "name": "hỏi thăm",
                    "keywords": ["khỏe không", "thế nào", "có ổn không", "dạo này", "sao rồi"],
                    "typical_scenarios": ["Hỏi thăm thông thường", "Hỏi thăm sau thời gian không liên lạc"],
                    "response_strategy": "quan_tam_vua_du",
                    "emotion_levels": {
                        "nhẹ": {
                            "variants": [
                                {"text": "Anh ổn. Em thế nào?", "delay_range": [2, 4], "follow_up": 0.2},
                                {"text": "Vẫn bình thường. Còn em?", "delay_range": [1, 3], "follow_up": 0.1},
                                {"text": "Ổn cả. Em dạo này sao?", "delay_range": [2, 5], "follow_up": 0.3}
                            ]
                        },
                        "vừa": {
                            "variants": [
                                {"text": "Cảm ơn em quan tâm. Anh vẫn ổn, dù hơi bận. Em thế nào?", "delay_range": [3, 6], "follow_up": 0.4},
                                {"text": "Cũng tạm ổn. Có gì mới không em?", "delay_range": [2, 4], "follow_up": 0.3}
                            ]
                        },
                        "sâu": {
                            "variants": [
                                {"text": "Cảm ơn em nhớ hỏi. Có đôi chút mệt mỏi nhưng ổn. Em có gì muốn chia sẻ không?", "delay_range": [4, 8], "follow_up": 0.6},
                                {"text": "Gần đây có nhiều chuyện, nhưng anh xoay xở được. Nghe giọng em có vẻ lo lắng gì đó?", "delay_range": [5, 10], "follow_up": 0.5}
                            ]
                        }
                    }
                },
                {
                    "name": "mệt",
                    "keywords": ["mệt", "mỏi", "kiệt sức", "đuối", "hết năng lượng"],
                    "typical_scenarios": ["Mệt sau làm việc", "Mệt vì công việc", "Mệt tinh thần"],
                    "response_strategy": "quan_tam_vua_du",
                    "emotion_levels": {
                        "nhẹ": {
                            "variants": [
                                {"text": "Nghỉ ngơi chút đi em.", "delay_range": [2, 4], "follow_up": 0.3},
                                {"text": "Uống nước ấm vào. Anh cũng hay thế.", "delay_range": [3, 5], "follow_up": 0.2}
                            ]
                        },
                        "vừa": {
                            "variants": [
                                {"text": "Công việc nhiều quá hả? Nghỉ ngơi đi, sức khỏe quan trọng lắm.", "delay_range": [3, 6], "follow_up": 0.4},
                                {"text": "Anh hiểu cảm giác đó. Cố gắng sắp xếp lại công việc xem sao.", "delay_range": [4, 7], "follow_up": 0.5}
                            ]
                        },
                        "sâu": {
                            "variants": [
                                {"text": "Nghe em nói mà anh thấy lo. Mệt quá thì nghỉ ngơi đi, đừng cố quá. Có cần anh giúp gì không?", "delay_range": [5, 10], "follow_up": 0.7},
                                {"text": "Anh từng trải qua rồi. Đôi khi mệt mỏi là dấu hiệu cần thay đổi. Muốn nói chuyện không em?", "delay_range": [6, 12], "follow_up": 0.8}
                            ]
                        }
                    }
                },
                # Thêm 23+ nhóm khác tương tự...
                {
                    "name": "stress",
                    "keywords": ["stress", "căng thẳng", "áp lực", "đầu óc căng", "quá tải"]
                },
                {
                    "name": "lạnh",
                    "keywords": ["lạnh", "trời lạnh", "rét", "ớn lạnh", "lạnh buốt"]
                },
                {
                    "name": "thử lòng",
                    "keywords": ["có nhớ không", "có yêu không", "có thương không", "thử xem", "kiểm tra"]
                },
                {
                    "name": "giận nhẹ",
                    "keywords": ["hờn", "giận", "không thèm nói", "không quan tâm", "mặc kệ"]
                },
                {
                    "name": "im lặng",
                    "keywords": ["...", "im lặng", "không nói gì", "thôi", "kệ"]
                }
            ]
        }
        return sample_data
    
    def _build_context_patterns(self) -> Dict:
        """Xây dựng patterns nhận diện ngữ cảnh"""
        patterns = {}
        for group in self.context_groups.get("context_groups", []):
            patterns[group["name"]] = {
                "keywords": group.get("keywords", []),
                "regex_patterns": [re.compile(rf'\b{kw}\b', re.IGNORECASE) for kw in group["keywords"]]
            }
        return patterns
    
    def analyze_message(self, message: str) -> MessageAnalysis:
        """Phân tích tin nhắn đến"""
        message_lower = message.lower()
        
        # Nhận diện ngữ cảnh
        detected_context = self._detect_context(message_lower)
        
        # Phân tích cảm xúc
        emotion_level, emotional_tone = self._analyze_emotion(message_lower)
        
        # Phân tích từ khóa
        keywords = self._extract_keywords(message_lower)
        
        # Đánh giá độ khẩn cấp
        urgency = self._assess_urgency(message_lower, emotional_tone)
        
        # Xác định nhu cầu ẩn
        implied_needs = self._identify_implied_needs(message_lower, detected_context)
        
        return MessageAnalysis(
            original_text=message,
            detected_context=detected_context,
            emotion_level=emotion_level,
            urgency=urgency,
            emotional_tone=emotional_tone,
            keywords=keywords,
            implied_needs=implied_needs,
            requires_follow_up=self._should_follow_up(message_lower, emotional_tone)
        )
    
    def _detect_context(self, message: str) -> str:
        """Nhận diện ngữ cảnh của tin nhắn"""
        best_match = "unknown"
        highest_score = 0
        
        for context_name, patterns in self.context_patterns.items():
            score = 0
            for keyword in patterns["keywords"]:
                if keyword in message:
                    score += 1
            for pattern in patterns["regex_patterns"]:
                if pattern.search(message):
                    score += 2
            
            if score > highest_score:
                highest_score = score
                best_match = context_name
        
        return best_match if highest_score > 0 else "neutral"
    
    def _analyze_emotion(self, message: str) -> Tuple[str, Dict]:
        """Phân tích mức độ cảm xúc"""
        emotion_scores = {
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "intensity": 0
        }
        
        # Đếm từ khóa cảm xúc
        for emotion_type, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in message:
                    if emotion_type == "vui":
                        emotion_scores["positive"] += 1
                    elif emotion_type in ["buồn", "giận", "lo"]:
                        emotion_scores["negative"] += 1
                    else:
                        emotion_scores["neutral"] += 1
        
        # Phát hiện dấu hiệu cảm xúc mạnh
        intensity_indicators = ["rất", "quá", "cực kỳ", "vô cùng", "hơi", "khá"]
        for indicator in intensity_indicators:
            if indicator in message:
                emotion_scores["intensity"] += 1
        
        # Xác định mức độ cảm xúc
        total_emotion_words = sum(emotion_scores.values()) - emotion_scores["intensity"]
        
        if total_emotion_words == 0:
            emotion_level = "nhẹ"
        elif total_emotion_words <= 2:
            emotion_level = "nhẹ" if emotion_scores["intensity"] < 2 else "vừa"
        else:
            if emotion_scores["intensity"] >= 3:
                emotion_level = "sâu"
            elif emotion_scores["intensity"] >= 1:
                emotion_level = "vừa"
            else:
                emotion_level = "nhẹ"
        
        return emotion_level, emotion_scores
    
    def _extract_keywords(self, message: str) -> List[str]:
        """Trích xuất từ khóa quan trọng"""
        # Đơn giản: tách từ và lọc các từ có ý nghĩa
        words = message.split()
        stop_words = ["và", "nhưng", "mà", "thì", "là", "có", "không", "rất", "quá"]
        keywords = [word for word in words if len(word) > 2 and word not in stop_words]
        return keywords[:10]  # Giới hạn 10 từ khóa
    
    def _assess_urgency(self, message: str, emotional_tone: Dict) -> float:
        """Đánh giá độ khẩn cấp của tin nhắn"""
        urgency_signals = [
            ("gấp", 0.8), ("ngay", 0.7), ("lập tức", 0.9),
            ("cứu", 1.0), ("giúp", 0.6), ("nguy hiểm", 0.9),
            ("?", 0.3), ("???", 0.6), ("!", 0.4), ("!!!", 0.7)
        ]
        
        urgency_score = 0
        for signal, weight in urgency_signals:
            if signal in message:
                urgency_score += weight
        
        # Cảm xúc tiêu cực mạnh làm tăng độ khẩn
        if emotional_tone["negative"] > 2:
            urgency_score += 0.3
        
        return min(1.0, urgency_score / 5.0)  # Chuẩn hóa về 0-1
    
    def _identify_implied_needs(self, message: str, context: str) -> List[str]:
        """Xác định nhu cầu ẩn trong tin nhắn"""
        needs = []
        
        # Phân tích dựa trên ngữ cảnh
        if context in ["mệt", "stress"]:
            needs.extend(["comfort", "understanding", "space"])
        elif context in ["buồn vu vơ", "cần an ủi"]:
            needs.extend(["comfort", "listening", "empathy"])
        elif context in ["thử lòng", "giận nhẹ"]:
            needs.extend(["reassurance", "attention", "validation"])
        elif context in ["muốn gặp", "chủ động"]:
            needs.extend(["connection", "meeting", "time"])
        
        # Thêm nhu cầu dựa trên từ khóa
        if "một mình" in message or "ở một mình" in message:
            needs.append("space")
        if "nói chuyện" in message or "tâm sự" in message:
            needs.append("talking")
        
        return list(set(needs))  # Remove duplicates
    
    def _should_follow_up(self, message: str, emotional_tone: Dict) -> bool:
        """Quyết định có cần follow-up không"""
        # Nếu có dấu hỏi và cảm xúc mạnh
        if "?" in message and (emotional_tone["positive"] > 1 or emotional_tone["negative"] > 1):
            return True
        
        # Nếu có dấu hiệu cần sự chú ý
        attention_seekers = ["chán quá", "buồn quá", "không ai nói chuyện", "cô đơn"]
        for phrase in attention_seekers:
            if phrase in message:
                return True
        
        return False
    
    def generate_response(self, analysis: MessageAnalysis) -> Dict:
        """Tạo câu trả lời phù hợp"""
        # Lấy nhóm ngữ cảnh phù hợp
        context_group = None
        for group in self.context_groups.get("context_groups", []):
            if group["name"] == analysis.detected_context:
                context_group = group
                break
        
        if not context_group:
            # Fallback về neutral response
            return self._generate_fallback_response(analysis)
        
        # Chọn mức cảm xúc phù hợp
        emotion_level = analysis.emotion_level
        if emotion_level not in context_group.get("emotion_levels", {}):
            # Fallback về mức vừa nếu không có mức cụ thể
            emotion_level = "vừa"
        
        # Lấy các biến thể có thể
        variants = context_group["emotion_levels"][emotion_level]["variants"]
        
        # Chọn ngẫu nhiên một biến thể
        selected_variant = random.choice(variants)
        
        # Tính độ trễ
        delay_range = selected_variant.get("delay_range", [2, 5])
        delay_minutes = random.uniform(delay_range[0], delay_range[1])
        
        # Thêm tính ngẫu nhiên tự nhiên
        response = self._add_natural_variations(selected_variant["text"])
        
        # Xây dựng kết quả
        result = {
            "response_text": response,
            "delay_minutes": round(delay_minutes, 1),
            "context": analysis.detected_context,
            "emotion_level": emotion_level,
            "strategy": context_group.get("response_strategy", "quan_tam_vua_du"),
            "needs_addressed": analysis.implied_needs,
            "requires_follow_up": selected_variant.get("follow_up", 0.3) > random.random(),
            "timestamp": datetime.now().isoformat()
        }
        
        # Lưu vào lịch sử
        self.conversation_history.append({
            "received": analysis.original_text,
            "sent": result,
            "time": datetime.now().isoformat()
        })
        
        return result
    
    def _generate_fallback_response(self, analysis: MessageAnalysis) -> Dict:
        """Tạo câu trả lời mặc định khi không xác định được ngữ cảnh"""
        fallback_responses = [
            "Ừ, anh nghe đây.",
            "Em nói đi.",
            "Có chuyện gì vậy?",
            "Anh đang nghe.",
            "Hmm, tiếp đi em."
        ]
        
        # Chọn dựa trên cảm xúc
        if analysis.emotional_tone["negative"] > 1:
            response = "Nghe có vẻ không ổn. Muốn nói gì không em?"
        elif analysis.emotional_tone["positive"] > 1:
            response = "Vui quá nhỉ. Kể anh nghe đi."
        else:
            response = random.choice(fallback_responses)
        
        return {
            "response_text": response,
            "delay_minutes": random.uniform(1, 3),
            "context": "neutral",
            "emotion_level": "nhẹ",
            "strategy": "quan_tam_vua_du",
            "needs_addressed": ["acknowledgment"],
            "requires_follow_up": False,
            "timestamp": datetime.now().isoformat()
        }
    
    def _add_natural_variations(self, text: str) -> str:
        """Thêm biến thể tự nhiên vào câu trả lời"""
        variations = {
            ".": ["", "...", ".."],
            "!": ["", "!", "!!"],
            "?": ["", "?", "??"]
        }
        
        # Đôi khi thêm/ bớt dấu câu
        if random.random() < 0.3:
            for original, replacements in variations.items():
                if original in text:
                    if random.random() < 0.5:
                        text = text.replace(original, random.choice(replacements))
        
        # Đôi khi viết tắt
        abbreviations = {
            "không": "ko",
            "được": "đc",
            "biết": "bit",
            "gì": "j"
        }
        
        if random.random() < 0.2:  # 20% cơ hội viết tắt
            for full, short in abbreviations.items():
                if full in text and random.random() < 0.5:
                    text = text.replace(full, short)
        
        # Thêm emoji nhẹ nhàng (rất ít)
        emojis = ["", "", "☕", ""]
        if random.random() < 0.1:  # Chỉ 10% cơ hội dùng emoji
            text += " " + random.choice(emojis)
        
        return text
    
    def auto_respond(self, message: str) -> Dict:
        """Tự động phản hồi từ đầu đến cuối"""
        # Phân tích tin nhắn
        analysis = self.analyze_message(message)
        
        # Tạo phản hồi
        response = self.generate_response(analysis)
        
        # Thêm metadata
        response["analysis"] = {
            "detected_context": analysis.detected_context,
            "emotion_level": analysis.emotion_level,
            "urgency": analysis.urgency,
            "keywords": analysis.keywords[:5]
        }
        
        return response

# ==================== EXTENSION FOR ANDROID ====================

class AndroidAutoMessaging:
    """Extension cho tích hợp Android"""
    
    def __init__(self, ai_engine: MatureMessagingAI):
        self.ai = ai_engine
        self.message_queue = []
        self.is_active = False
        
    def process_incoming_message(self, contact_name: str, message: str, timestamp: str) -> Dict:
        """Xử lý tin nhắn đến từ Android"""
        # Phân tích và tạo phản hồi
        response_data = self.ai.auto_respond(message)
        
        # Thêm thông tin người gửi
        response_data["contact"] = contact_name
        response_data["received_time"] = timestamp
        
        # Xếp hàng đợi để gửi
        self.message_queue.append(response_data)
        
        return response_data
    
    def get_next_message_to_send(self) -> Optional[Dict]:
        """Lấy tin nhắn tiếp theo cần gửi"""
        if not self.message_queue:
            return None
            
        # Kiểm tra xem đã đến lúc gửi chưa
        current_time = time.time()
        for i, msg in enumerate(self.message_queue):
            # Kiểm tra delay
            if current_time >= msg.get("scheduled_time", 0):
                return self.message_queue.pop(i)
        
        return None
    
    def schedule_messages(self):
        """Lên lịch gửi tin nhắn"""
        current_time = time.time()
        for msg in self.message_queue:
            if "scheduled_time" not in msg:
                # Tính thời gian gửi dựa trên delay
                delay_seconds = msg["delay_minutes"] * 60
                msg["scheduled_time"] = current_time + delay_seconds
                
    def auto_pipeline(self, incoming_messages: List[Dict]) -> List[Dict]:
        """Chạy pipeline tự động hoàn toàn"""
        responses = []
        
        for msg_data in incoming_messages:
            # Xử lý mỗi tin nhắn
            response = self.process_incoming_message(
                msg_data.get("contact", "Unknown"),
                msg_data.get("message", ""),
                msg_data.get("timestamp", "")
            )
            
            responses.append(response)
        
        # Lên lịch gửi
        self.schedule_messages()
        
        return responses

# ==================== WEB INTERFACE (Streamlit) ====================

import streamlit as st

def create_web_interface():
    """Giao diện web dùng Streamlit"""
    st.set_page_config(page_title="AI Nhắn Tin Trưởng Thành", layout="wide")
    
    st.title("🤵 AI Nhắn Tin Trưởng Thành (Nam 40+)")
    st.markdown("---")
    
    # Khởi tạo AI engine
    if "ai_engine" not in st.session_state:
        st.session_state.ai_engine = MatureMessagingAI()
        st.session_state.conversation = []
    
    # Sidebar cài đặt
    with st.sidebar:
        st.header("⚙️ Cài đặt")
        relationship_stage = st.selectbox(
            "Giai đoạn quan hệ",
            ["Mới quen", "Đang hẹn hò", "Nghiêm túc", "Gắn bó"]
        )
        
        response_style = st.select_slider(
            "Mức độ thân mật",
            options=["Xã giao", "Thân thiết", "Thân mật"]
        )
        
        auto_delay = st.checkbox("Tự động delay", value=True)
        
        if st.button("Làm mới hội thoại"):
            st.session_state.conversation = []
    
    # Main chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Hội thoại")
        
        # Hiển thị lịch sử hội thoại
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.conversation:
                if msg["type"] == "received":
                    st.markdown(f"""
                    <div style='background-color: #f0f2f6; padding: 10px; border-radius: 10px; margin: 5px;'>
                    <strong>Họ:</strong> {msg["text"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background-color: #d1ecf1; padding: 10px; border-radius: 10px; margin: 5px;'>
                    <strong>AI:</strong> {msg["text"]}<br>
                    <small>Delay: {msg.get("delay", 0)} phút | Ngữ cảnh: {msg.get("context", "")}</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Nhập tin nhắn mới
        new_message = st.text_area("Tin nhắn từ đối phương:", height=100)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Phân tích & Trả lời", type="primary"):
                if new_message:
                    # Phân tích
                    analysis = st.session_state.ai_engine.analyze_message(new_message)
                    
                    # Thêm vào hội thoại (tin nhận)
                    st.session_state.conversation.append({
                        "type": "received",
                        "text": new_message,
                        "time": datetime.now().strftime("%H:%M")
                    })
                    
                    # Tạo phản hồi
                    response = st.session_state.ai_engine.generate_response(analysis)
                    
                    # Thêm vào hội thoại (tin gửi)
                    st.session_state.conversation.append({
                        "type": "sent",
                        "text": response["response_text"],
                        "delay": response["delay_minutes"],
                        "context": response["context"],
                        "time": datetime.now().strftime("%H:%M")
                    })
                    
                    st.rerun()
        
        with col_btn2:
            if st.button("Xóa hội thoại"):
                st.session_state.conversation = []
                st.rerun()
    
    with col2:
        st.subheader("🔍 Phân tích chi tiết")
        
        if new_message:
            with st.spinner("Đang phân tích..."):
                analysis = st.session_state.ai_engine.analyze_message(new_message)
                
                st.metric("Ngữ cảnh", analysis.detected_context)
                st.metric("Mức cảm xúc", analysis.emotion_level)
                st.metric("Độ khẩn", f"{analysis.urgency*100:.0f}%")
                
                st.write("**Từ khóa phát hiện:**")
                for kw in analysis.keywords[:5]:
                    st.caption(f"• {kw}")
                
                st.write("**Nhu cầu ẩn:**")
                for need in analysis.implied_needs:
                    st.caption(f"• {need}")
        
        st.subheader("📊 Thống kê")
        st.metric("Số tin nhắn", len(st.session_state.conversation)//2)
        
        if st.session_state.conversation:
            contexts = [msg.get("context", "") for msg in st.session_state.conversation if msg["type"] == "sent"]
            if contexts:
                most_common = max(set(contexts), key=contexts.count)
                st.metric("Ngữ cảnh thường gặp", most_common)

# ==================== MAIN EXECUTION ====================

def main():
    """Hàm chính để chạy hệ thống"""
    print("🚀 Khởi động AI Nhắn Tin Trưởng Thành...")
    
    # 1. Khởi tạo engine
    ai = MatureMessagingAI()
    
    # 2. Test với tin nhắn mẫu
    test_messages = [
        "Anh ơi, em mệt quá",
        "Dạo này anh có khỏe không?",
        "Trời lạnh thế này, nhớ anh quá",
        "Anh có yêu em không?",
        "...",
        "Công việc căng thẳng quá, em stress lắm"
    ]
    
    print("\n🧪 Test hệ thống:")
    for msg in test_messages:
        print(f"\n📩 Nhận: {msg}")
        response = ai.auto_respond(msg)
        print(f"🤖 Trả lời: {response['response_text']}")
        print(f"   ⏱ Delay: {response['delay_minutes']} phút")
        print(f"   🎭 Ngữ cảnh: {response['context']}")
        print(f"   💡 Chiến lược: {response['strategy']}")
    
    print("\n✅ Hệ thống sẵn sàng!")
    print("\n📱 Các tùy chọn chạy:")
    print("1. Web Interface: streamlit run mature_messaging_ai.py")
    print("2. Command Line: python mature_messaging_ai.py --test")
    print("3. Android Backend: Sử dụng class AndroidAutoMessaging")
    
    return ai

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Chạy test")
    parser.add_argument("--web", action="store_true", help="Chạy web interface")
    args = parser.parse_args()
    
    if args.web:
        # Chạy web interface (cần streamlit)
        create_web_interface()
    else:
        # Chạy test mẫu
        main()
