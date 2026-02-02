import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moltbook AI 2026", layout="wide")

# المفتاح المباشر
genai.configure(api_key="AIzaSyA4eST225RA5V_APuoTUrdHVpJ8_JimlCk")

st.title("📖 Moltbook AI - النسخة المحدثة")

user_input = st.text_input("اسألني أي شيء...")

if st.button("إرسال"):
    if user_input:
        with st.spinner('جاري الاتصال بالعقل الاصطناعي...'):
            # قائمة المحركات (سنجرب الأحدث فالأقدم)
            models_to_try = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-pro']
            success = False
            
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(user_input)
                    st.success(f"تم الرد بواسطة: {model_name}")
                    st.markdown(response.text)
                    success = True
                    break
                except Exception:
                    continue
            
            if not success:
                st.error("نعتذر، السيرفر لا يزال يستخدم إصداراً قديماً. يرجى الضغط على Reboot من إعدادات Streamlit.")
    else:
        st.warning("الرجاء كتابة سؤال.")
