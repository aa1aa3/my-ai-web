import streamlit as st
import google.generativeai as genai
from datetime import datetime
import sys

# === تهيئة الصفحة ===
st.set_page_config(
    page_title="Gemini Pro AI - النسخة المتقدمة",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === جلب مفتاح API ===
def get_api_key():
    try:
        if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except:
        pass
    
    import os
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key
    
    return "AIzaSyD5pmXKOY-qhd2k8DeJSeq-V4fgnT1zdqs"

# === تهيئة Gemini ===
@st.cache_resource
def init_gemini():
    try:
        api_key = get_api_key()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        model.generate_content("test", generation_config={"max_output_tokens": 1})
        return True, "✅ API مفعل بنجاح"
    except Exception as e:
        return False, f"❌ خطأ في API: {str(e)}"

# === تهيئة التطبيق ===
with st.spinner("جاري تهيئة الذكاء الاصطناعي..."):
    init_result, init_message = init_gemini()

# === الشريط الجانبي ===
with st.sidebar:
    st.header("⚙️ الإعدادات المتقدمة")
    
    st.subheader("🔧 حالة النظام")
    st.info(init_message)
    python_version = sys.version.split()[0]
    st.metric("إصدار Python", python_version)
    
    st.subheader("🤖 اختيار النموذج")
    model_choice = st.selectbox(
        "النموذج:",
        [
            "gemini-1.5-pro-latest",
            "gemini-1.5-flash-latest", 
            "gemini-1.0-pro-latest",
            "gemini-pro"
        ],
        index=1
    )
    
    st.subheader("🎛️ معايير متقدمة")
    col1, col2 = st.columns(2)
    with col1:
        temperature = st.slider("الإبداع", 0.0, 2.0, 0.7, 0.1)
    with col2:
        max_tokens = st.number_input("الحد الأقصى للرموز", 100, 8192, 2000)
    
    top_p = st.slider("Top-P", 0.0, 1.0, 0.95, 0.05)
    top_k = st.slider("Top-K", 1, 40, 40, 1)
    
    st.subheader("🔍 خيارات إضافية")
    safety_settings = st.checkbox("تفعيل إعدادات الأمان", value=True)
    streaming = st.checkbox("الرد المباشر (Streaming)", value=False)
    
    st.markdown("---")
    with st.expander("ℹ️ معلومات تقنية"):
        st.code(f"""
النموذج: {model_choice}
الإبداع: {temperature}
الحد الأقصى: {max_tokens} رمز
Top-P: {top_p}
Top-K: {top_k}
المفتاح: {'****' + get_api_key()[-4:] if init_result else 'غير مفعل'}
        """)

# === الواجهة الرئيسية ===
st.title("🚀 Gemini AI - النسخة المتقدمة")
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;'>
<h3 style='color: white;'>مميزات النسخة المتقدمة:</h3>
<ul>
<li>دعم Python 3.11+</li>
<li>إعدادات توليد متقدمة (Temperature, Top-P, Top-K)</li>
<li>أربعة نماذج مختلفة من Gemini</li>
<li>نظام إدارة مفاتيح آمن</li>
<li>مراقبة حالة النظام</li>
</ul>
</div>
""", unsafe_allow_html=True)

# === إدارة المحادثة ===
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'model_config' not in st.session_state:
    st.session_state.model_config = {
        "temperature": temperature,
        "max_output_tokens": max_tokens,
        "top_p": top_p,
        "top_k": top_k
    }

# === منطقة المحادثة ===
st.subheader("💬 محادثة ذكية")

# عرض تاريخ المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المستخدم
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    if not init_result:
        st.error("الذكاء الاصطناعي غير مفعل. الرجاء التحقق من إعدادات API.")
        st.stop()
    
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # توليد الرد
    with st.chat_message("assistant"):
        with st.spinner("🔄 جاري توليد الرد..."):
            try:
                generation_config = {
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                    "top_p": top_p,
                    "top_k": top_k,
                }
                
                safety_config = None
                if safety_settings:
                    safety_config = [
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    ]
                
                model = genai.GenerativeModel(
                    model_name=model_choice,
                    generation_config=generation_config,
                    safety_settings=safety_config
                )
                
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.text
                })
                
            except Exception as e:
                error_msg = f"حدث خطأ: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"⚠️ {error_msg}"
                })

# === أدوات التحكم ===
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔄 تحديث الجلسة", use_container_width=True):
        st.rerun()

with col2:
    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

with col3:
    if st.button("📊 حالة النظام", use_container_width=True):
        st.info(f"""
        حالة الذكاء الاصطناعي: {init_message}
        عدد الرسائل: {len(st.session_state.messages)}
        النموذج الحالي: {model_choice}
        إصدار Python: {python_version}
        """)

with col4:
    if st.session_state.messages:
        chat_text = "\n\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        st.download_button(
            label="💾 تصدير المحادثة",
            data=chat_text,
            file_name=f"gemini_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# === تذييل الصفحة ===
st.markdown("---")
footer = f"""
<div style='text-align: center; color: #666; padding: 20px;'>
<p>🚀 Gemini AI Pro | Python {python_version} | Model: {model_choice} | Tokens: {max_tokens}</p>
<p>© {datetime.now().year} - تم التطوير باستخدام Streamlit & Google Gemini API</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)# ============================================
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
