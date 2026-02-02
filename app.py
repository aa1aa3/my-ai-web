import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moltbook AI", layout="wide")

# وضع المفتاح مباشرة
MY_API_KEY = "AIzaSyA4eST225RA5V_APuoTUrdHVpJ8_JimlCk"

# إعداد المكتبة
genai.configure(api_key=MY_API_KEY)

st.title("📖 Moltbook AI - النسخة النهائية")

user_input = st.text_input("اسألني أي شيء...")

if st.button("إرسال"):
    if user_input:
        with st.spinner('جاري جلب الإجابة...'):
            try:
                # استخدمنا اسم الموديل بدون إصدارات بيتا لضمان النجاح
                model = genai.GenerativeModel('gemini-1.5-flash') 
                # إذا فشل الفلاش، سنستخدم البرو فوراً
                response = model.generate_content(user_input)
                st.markdown(response.text)
            except Exception as e:
                try:
                    # الخيار البديل المضمون
                    model = genai.GenerativeModel('models/gemini-pro')
                    response = model.generate_content(user_input)
                    st.markdown(response.text)
                except Exception as e2:
                    st.error(f"عذراً، يبدو أن هناك ضغطاً على السيرفر: {e2}")
    else:
        st.warning("الرجاء كتابة سؤال أولاً.")
