import streamlit as st
import requests
from PIL import Image

# Địa chỉ API backend của bạn
API_URL = "http://localhost:8000"

def send_message(message, endpoint):
    """Hàm để gửi tin nhắn đến API và nhận câu trả lời."""
    if endpoint == "/chat":
        payload = {"human_input": message, "session_id": "default"}
    else:
        payload = {"question": message}
    response = requests.post(f"{API_URL}{endpoint}", json=payload)
    return response.json()

st.title('Chatbot Demo')

# Tạo sidebar để lựa chọn endpoint
endpoint = st.sidebar.selectbox(
    "Chọn chế độ:",
    ("Chat", "Hỏi")
)

# Map lựa chọn của người dùng tới endpoint tương ứng
endpoint_map = {
    "Chat": "/chat",
    "Hỏi": "/generative_ai"
}
selected_endpoint = endpoint_map[endpoint]

# Khởi tạo lịch sử trò chuyện trong session state nếu chưa có
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Hàm để xử lý khi người dùng gửi tin nhắn
def send_user_message():
    user_input = st.session_state.user_input
    if user_input:
        if "Vòng đời của một hệ thống nhúng" in user_input:
            st.session_state.chat_history.append({"user": user_input, "bot": "Vòng đời của một hệ thống nhúng"})
            st.session_state.chat_history.append({"image": "picture/image19.png"})
        else:
            response = send_message(user_input, selected_endpoint)
            st.session_state.chat_history.append({"user": user_input, "bot": response.get("answer", "")})
        st.session_state.user_input = ""  # Xóa nội dung hộp nhập liệu

# Hộp nhập liệu để người dùng nhập câu hỏi
st.text_input("Bạn muốn hỏi gì?", key="user_input", on_change=send_user_message)

# Hiển thị lịch sử trò chuyện
for chat in st.session_state.chat_history:
    if "user" in chat:
        st.write(f"Bạn: {chat['user']}")
        st.write(f"Bot: {chat['bot']}")
    elif "image" in chat:
        image = Image.open(chat["image"])
        st.image(image, caption="Vòng đời của một hệ thống nhúng", width=600)