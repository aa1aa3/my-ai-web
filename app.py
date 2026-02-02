import streamlit as st
import google.generativeai as genai
from datetime import datetime

# إعداد الصفحة
st.set_page_config(
    page_title="Gemini Pro AI - متعدد النماذج",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة Gemini API
@st.cache_resource
def init_gemini():
    api_key = "AIzaSyD5pmXKOY-qhd2k8DeJSeq-V4fgnT1zdqs"
    genai.configure(api_key=api_key)
    return True

# تهيئة API
init_success = init_gemini()

# العنوان الرئيسي
st.title("🤖 Gemini Pro AI - المحاور الذكي")
st.markdown("---")

# الشريط الجانبي
with st.sidebar:
    st.header("⚙️ الإعدادات")
    
    # اختيار النموذج
    model_choice = st.selectbox(
        "اختر نموذج الذكاء الاصطناعي:",
        ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro", "gemini-1.0-pro"]
    )
    
    # إعدادات النموذج
    st.subheader("🔧 معايير النموذج")
    temperature = st.slider("الإبداع (Temperature)", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.slider("الحد الأقصى للإجابة", 100, 2000, 1000, 100)
    
    # ميزات إضافية
    st.subheader("✨ ميزات إضافية")
    enable_web = st.checkbox("تفعيل البحث على الويب", value=False)
    show_details = st.checkbox("عرض تفاصيل النموذج", value=True)
    
    # معلومات النظام
    st.markdown("---")
    st.info(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption("مفتاح API: مفعل ✓")

# عرض معلومات النموذج
if show_details:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("النموذج المختار", model_choice)
    with col2:
        st.metric("درجة الإبداع", f"{temperature}")
    with col3:
        st.metric("طول الإجابة", f"{max_tokens} كلمة")

# منطقة المحادثة
st.subheader("💬 محادثتك مع الذكاء الاصطناعي")

# تهيئة history في session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# عرض تاريخ المحادثة
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المستخدم
user_input = st.chat_input("اكتب رسالتك هنا...")

if user_input:
    # إضافة رسالة المستخدم إلى التاريخ
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # عرض رسالة المستخدم
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # إنشاء الرد
    with st.chat_message("assistant"):
        with st.spinner("🤔 يفكر النموذج..."):
            try:
                # إعداد النموذج
                generation_config = {
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                }
                
                # إنشاء النموذج
                model = genai.GenerativeModel(
                    model_name=model_choice,
                    generation_config=generation_config
                )
                
                # إنشاء المحتوى
                response = model.generate_content(user_input)
                
                # عرض الرد
                st.markdown(response.text)
                
                # حفظ الرد في التاريخ
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": response.text
                })
                
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
                st.info("جرب تغيير النموذج أو تقليل طول الإجابة")

# ميزات إضافية في الجزء السفلي
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

with col2:
    if st.button("📋 نسخ آخر رد", use_container_width=True):
        if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "assistant":
            st.code(st.session_state.chat_history[-1]["content"])

with col3:
    st.download_button(
        label="💾 حفظ المحادثة",
        data="\n\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history]),
        file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# تذييل الصفحة
st.markdown("---")
st.caption("⚡ Powered by Google Gemini API | تم التطوير باستخدام Streamlit")boot إجباري.")
