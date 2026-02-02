import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Moltbook Extra", layout="wide")

# جلب المفتاح بأمان
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
    else:
        st.error("⚠️ لم يتم العثور على GEMINI_API_KEY في الإعدادات المتقدمة (Secrets).")
except Exception as e:
    st.error(f"❌ خطأ في الإعدادات: {e}")

st.title("📖 Moltbook AI - النسخة المطورة")
st.markdown("---")

user_input = st.text_input("اسألني أي شيء...", placeholder="اكتب سؤالك هنا...")

if st.button("إرسال"):
    if user_input:
        with st.spinner('جاري الاتصال بالعقل الاصطناعي...'):
            try:
                # محاولة استخدام الموديل الأكثر استقراراً
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(user_input)
                
                st.success("تمت الإجابة:")
                st.markdown(response.text)
            except Exception as e:
                # في حال فشل الموديل الأول، نجرب الموديل الاحتياطي
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(user_input)
                    st.markdown(response.text)
                except:
                    st.error(f"نعتذر، هناك مشكلة في توفر الخدمة حالياً. نوع الخطأ: {e}")
    else:
        st.warning("الرجاء كتابة سؤال أولاً.")
