import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moltbook AI", layout="wide")

# ضع مفتاحك هنا مباشرة للتجربة النهائية
MY_API_KEY = "AIzaSyA4eST225RA5V_APuoTUrdHVpJ8_JimlCk"
genai.configure(api_key=MY_API_KEY)

st.title("📖 Moltbook AI - الاختبار النهائي")

user_input = st.text_input("اسألني أي شيء...")

if st.button("إرسال"):
    if user_input:
        try:
            # تجربة الموديل الأكثر استقراراً
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(user_input)
            st.success("نجح الاتصال!")
            st.markdown(response.text)
        except Exception as e:
            # إظهار الخطأ الحقيقي للمستخدم
            st.error(f"الخطأ التقني الحقيقي هو: {e}")
            st.info("إذا كان الخطأ يحتوي على 403، فالمشكلة في القيود الجغرافية أو صلاحية المفتاح.")
