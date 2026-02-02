import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Moltbook AI", layout="wide")

# وضع المفتاح مباشرة داخل الكود
MY_API_KEY = "AIzaSyA4eST225RA5V_APuoTUrdHVpJ8_JimlCk"
genai.configure(api_key=MY_API_KEY)

st.title("📖 Moltbook AI - النسخة المطورة")

user_input = st.text_input("اسألني أي شيء...")

if st.button("إرسال"):
    if user_input:
        with st.spinner('جاري الاتصال المباشر بالنموذج...'):
            # قائمة النماذج لتجربتها بالترتيب
            models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            success = False
            
            for model_name in models_to_try:
                try:
                    # محاولة الاتصال بالنموذج
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(user_input)
                    
                    st.success(f"تم الرد باستخدام نموذج: {model_name}")
                    st.markdown(response.text)
                    success = True
                    break 
                except Exception as e:
                    # إذا فشل نموذج، ينتقل للذي يليه
                    continue
            
            if not success:
                st.error("فشلت جميع المحاولات. قد يكون المفتاح غير مفعل في منطقتك الجغرافية أو يحتاج لتفعيل من Google AI Studio.")
    else:
        st.warning("الرجاء كتابة سؤال أولاً.")
