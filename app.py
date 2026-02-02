import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Moltbook AI", layout="wide")

# وضع المفتاح مباشرة
MY_API_KEY = "AIzaSyA4eST225RA5V_APuoTUrdHVpJ8_JimlCk"

# إعداد المكتبة لتستخدم الإصدار المستقر v1
genai.configure(api_key=MY_API_KEY)

st.title("📖 Moltbook AI - التشغيل الأكيد")

user_input = st.text_input("اسألني أي شيء...")

if st.button("إرسال"):
    if user_input:
        with st.spinner('جاري الاتصال...'):
            try:
                # محاولة استخدام الموديل المستقر
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(user_input)
                st.success("تم الاتصال بنجاح!")
                st.markdown(response.text)
            except Exception as e:
                # إذا فشل، سنعرض النماذج المتاحة فعلياً في حسابك لنعرف السبب
                st.error(f"عذراً، لا يزال هناك تعارض. الخطأ: {e}")
                st.write("النماذج المتوفرة في مكتبتك حالياً:")
                try:
                    available_models = [m.name for m in genai.list_models()]
                    st.write(available_models)
                except:
                    st.write("لا يمكن جلب قائمة النماذج، تأكد من صلاحية المفتاح.")
