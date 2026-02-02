import streamlit as st
import google.generativeai as genai

# إعداد واجهة الموقع
st.set_page_config(page_title="Moltbook AI 2026", layout="wide")
st.title("📖 Moltbook AI")

# المفتاح مباشرة
genai.configure(api_key="AIzaSyA4eST225RA5V_APuoTUrdHVpJ8_JimlCk")

user_input = st.text_input("اسألني أي شيء...")

if st.button("إرسال"):
    if user_input:
        try:
            # استخدام الموديل المستقر جداً والمتوفر عالمياً
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(user_input)
            st.write(response.text)
        except Exception as e:
            st.error(f"خطأ: {e}")
            st.info("إذا رأيت خطأ 404، فالسيرفر يحتاج لـ Reboot إجباري.")
