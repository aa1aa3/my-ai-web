import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Moltbook Extra", layout="wide")

# جلب المفتاح بأمان من إعدادات المنصة
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

st.title("📖 Moltbook AI - النسخة المطورة")

# القائمة الجانبية
st.sidebar.title("⚙️ الإعدادات")
mode = st.sidebar.selectbox("اختر النمط:", ["محادثة ذكية", "توليد صور"])

if mode == "محادثة ذكية":
    user_input = st.text_input("اسألني أي شيء...")
    if st.button("إرسال"):
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_input)
        st.markdown(f"### الرد:\n{response.text}")

elif mode == "توليد صور":
    img_prompt = st.text_input("صف الصورة بالإنجليزية:")
    if st.button("رسم"):
        url = f"https://pollinations.ai/p/{img_prompt.replace(' ', '%20')}?width=1024&height=1024&nologo=true"
        st.image(url, caption="الصورة الناتجة")
