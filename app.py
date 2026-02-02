import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moltbook AI", layout="wide")

# وضع المفتاح مباشرة كما أردت
MY_API_KEY = "AIzaSyA4eST225RA5V_APuoTUrdHVpJ8_JimlCk"
genai.configure(api_key=MY_API_KEY)

st.title("📖 Moltbook AI - الإصدار الأحدث 2026")

user_input = st.text_input("اسألني أي شيء...")

if st.button("إرسال"):
    if user_input:
        with st.spinner('جاري الاتصال بأحدث نماذج الذكاء الاصطناعي...'):
            try:
                # استخدمنا هنا النموذج المتاح في قائمتك رقم 2
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content(user_input)
                
                st.success("تم الرد بنجاح!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"حدث خطأ غير متوقع: {e}")
    else:
        st.warning("الرجاء كتابة سؤال أولاً.")
