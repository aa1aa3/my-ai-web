import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moltbook AI", layout="wide")

# وضع المفتاح مباشرة
MY_API_KEY = "AIzaSyA4eST225RA5V_APuoTUrdHVpJ8_JimlCk"
genai.configure(api_key=MY_API_KEY)

st.title("📖 Moltbook AI - النسخة المستقرة")

user_input = st.text_input("اسألني أي شيء...")

if st.button("إرسال"):
    if user_input:
        with st.spinner('جاري المحاولة عبر المحرك المستقر...'):
            try:
                # التبديل للموديل الأكثر توفراً في الحسابات المجانية
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                response = model.generate_content(user_input)
                
                st.success("تم الرد!")
                st.markdown(response.text)
            except Exception as e:
                if "429" in str(e):
                    st.error("⚠️ يبدو أن ضغط الأسئلة كبير جداً حالياً على جوجل. حاول مجدداً بعد قليل أو استخدم مفتاح API آخر.")
                else:
                    st.error(f"حدث خطأ: {e}")
    else:
        st.warning("الرجاء كتابة سؤال أولاً.")
