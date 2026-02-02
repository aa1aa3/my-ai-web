import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moltbook Extra", layout="wide")

# محاولة جلب المفتاح من الإعدادات
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("خطأ: لم يتم العثور على مفتاح API في إعدادات Secrets.")

st.title("📖 Moltbook AI - النسخة المطورة")

user_input = st.text_input("اسألني أي شيء...")

if st.button("إرسال"):
    if user_input:
        try:
            # استخدام أحدث موديل متاح
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(user_input)
            st.markdown(f"### الرد:\n{response.text}")
        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
    else:
        st.warning("الرجاء كتابة سؤال أولاً.")
