import streamlit as st
import google.generativeai as genai
import time

# ============================================
# إصلاح: منع إعادة التحميل المتكرر
# ============================================
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.chat_history = []
    st.session_state.last_refresh = time.time()

# إعداد الصفحة بدون إعادة تحميل
st.set_page_config(
    page_title="Gemini AI - الإصدار المستقر",
    page_icon="🤖",
    layout="centered",  # غيرت من "wide" لتقليل المشاكل
    initial_sidebar_state="collapsed"  # تقليل العناصر
)

# ============================================
# تهيئة API بسيطة
# ============================================
try:
    api_key = "AIzaSyD5pmXKOY-qhd2k8DeJSeq-V4fgnT1zdqs"
    genai.configure(api_key=api_key)
    
    # اختبار سريع
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.success("✅ تم تهيئة الذكاء الاصطناعي بنجاح")
except Exception as e:
    st.error(f"⚠️ خطأ في التهيئة: {e}")

# ============================================
# واجهة بسيطة جداً
# ============================================
st.title("🤖 مساعد Gemini AI")

# شريط جانبي مخفي (تقليل المشاكل)
with st.sidebar:
    st.markdown("### الإعدادات البسيطة")
    model_type = st.radio(
        "اختر النموذج:",
        ["gemini-1.5-flash", "gemini-1.5-pro"]
    )
    if st.button("🔄 إعادة ضبط"):
        st.session_state.chat_history = []
        st.rerun()

# ============================================
# منطقة المحادثة (بدون تعقيد)
# ============================================
st.subheader("💬 ابدأ المحادثة")

# عرض المحادثة السابقة
if st.session_state.chat_history:
    for msg in st.session_state.chat_history:
        role_icon = "👤" if msg["role"] == "user" else "🤖"
        st.markdown(f"**{role_icon} {msg['role'].title()}:** {msg['content']}")
        st.markdown("---")

# ============================================
# إدخال المستخدم (نسخة مبسطة)
# ============================================
user_input = st.text_area("اكتب رسالتك هنا:", height=100)

col1, col2 = st.columns(2)
with col1:
    send_btn = st.button("🚀 إرسال", type="primary", use_container_width=True)
with col2:
    clear_btn = st.button("🗑️ مسح المحادثة", use_container_width=True)

if clear_btn:
    st.session_state.chat_history = []
    st.rerun()

if send_btn and user_input:
    with st.spinner("جاري التفكير..."):
        try:
            # إضافة رسالة المستخدم
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # توليد الرد
            model = genai.GenerativeModel(model_type)
            response = model.generate_content(user_input)
            
            # إضافة رد المساعد
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response.text
            })
            
            # إعادة التحميل بعناية
            time.sleep(0.5)  # تأخير قصير
            st.rerun()
            
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")
            st.info("جرب تحديث الصفحة (F5)")

# ============================================
# نصائح استكشاف الأخطاء
# ============================================
with st.expander("🛠️ إذا استمر الخطأ:"):
    st.markdown("""
    1. **افتح نافذة متصفح خاصة** (Incognito)
    2. **تأكد من عنوان URL الصحيح**: [https://my-ai-web.streamlit.app](https://my-ai-web.streamlit.app)
    3. **جرب متصفحاً آخر**: Chrome / Firefox / Edge
    4. **تعطيل إضافات المتصفح** مؤقتاً
    5. **انتظر 5 دقائق** ثم جرب مرة أخرى
    """)

# ============================================
# تذييل الصفحة
# ============================================
st.markdown("---")
st.caption("✨ الإصدار المستقر | Gemini API | Streamlit")# منطقة المحادثة
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
