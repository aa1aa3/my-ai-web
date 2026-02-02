import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moltbook AI 2026", layout="wide")

# المفتاح مباشرة
genai.configure(api_key="AIzaSyA4eST225RA5V_APuoTUrdHVpJ8_JimlCk")

st.title("📖 Moltbook AI - النسخة المحدثة")

user_input = st.text_input("اسألني أي شيء...")

if st.button("إرسال"):
    if user_input:
        with st.spinner('جاري الاتصال...'):
            try:
                # استخدام الموديل المستقر من قائمتك
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                response = model.generate_content(user_input)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"حدثت مشكلة بسيطة: {e}")
    else:
        st.warning("الرجاء كتابة سؤال.")
