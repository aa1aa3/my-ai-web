import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moltbook AI", layout="wide")

# إعداد الـ API بأمان
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("المفتاح غير موجود في Secrets!")

st.title("📖 Moltbook AI - النسخة المطورة")

user_input = st.text_input("اسألني أي شيء...")

if st.button("إرسال"):
    if user_input:
        with st.spinner('جاري الاتصال...'):
            # مصفوفة النماذج: سيجرب الأول، إذا فشل ينتقل للثاني تلقائياً
            models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            success = False
            
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(user_input)
                    st.markdown(response.text)
                    success = True
                    break # توقف إذا نجح أحد النماذج
                except:
                    continue
            
            if not success:
                st.error("عذراً، جميع محاولات الاتصال بالنماذج فشلت. تأكد من صلاحية مفتاح API الخاص بك.")
