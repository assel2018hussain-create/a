
import streamlit as st
from zxcvbn import zxcvbn
import base64

def convert_crack_time(seconds):
    seconds = int(seconds)
    if seconds < 1:
        return "أقل من ثانية"
    time_units = [
        ("قرن", 3153600000),
        ("سنة", 31536000),
        ("شهر", 2628000),
        ("يوم", 86400),
        ("ساعة", 3600),
        ("دقيقة", 60),
        ("ثانية", 1)
    ]
    parts = []
    for name, count_in_seconds in time_units:
        value = seconds // count_in_seconds
        if value:
            parts.append(f"{value} {name}")
            seconds %= count_in_seconds
    return " و ".join(parts)
    if seconds < 60:
        return f"{int(seconds)} ثانية"
    elif seconds < 3600:
        return f"{int(seconds // 60)} دقيقة"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} ساعة"
    elif seconds < 2628000:
        return f"{int(seconds // 86400)} يوم"
    elif seconds < 31536000:
        return f"{int(seconds // 2628000)} شهر"
    elif seconds < 3153600000:
        return f"{round(seconds / 31536000, 1)} سنة"
    elif seconds < 315360000000:
        return f"{round(seconds / 3153600000, 1)} قرن"
    else:
        return f"{round(seconds / 3153600000, 1)} قرن (تقدير تقريبي)"

def play_sound_loop_hidden(level):
    sounds = {
        0: "alarm.mp3",
        1: "weak.mp3",
        2: "medium.mp3",
        3: "strong.mp3",
        4: "celebration.mp3"
    }
    file = sounds.get(level, "medium.mp3")
    with open(f"sounds/{file}", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <audio autoplay loop style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

colors = {
    0: ("#ff1e1e", "ضعيفة جدًا", "🔴"),
    1: ("#ff6f00", "ضعيفة", "🟠"),
    2: ("#ffc107", "متوسطة", "🟡"),
    3: ("#8bc34a", "قوية", "🟢"),
    4: ("#009688", "قوية جدًا", "🎉🟢")
}

st.set_page_config(page_title="تحقق من قوة كلمة المرور", layout="centered")

st.markdown("""
    <style>
    body, .stApp {
        background-color: #5a2476;
        font-family: 'Arial', sans-serif;
    }
    .password-box input {
        background-color: white !important;
        color: black !important;
    }
    .password-box {
        background-color: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.1);
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🔐 تحقق من زمن اختراق كلمة مرورك باستخدام الذكاء الاصطناعي</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='password-box'>", unsafe_allow_html=True)
    password = st.text_input('', type='password', placeholder='أدخل كلمة المرور')
    if st.button("تحليل"):
        if password:
            result = zxcvbn(password)
            crack_time_seconds = result['crack_times_seconds']['offline_slow_hashing_1e4_per_second']

            if crack_time_seconds <= 3600:
                score = 0
            elif crack_time_seconds <= 604800:
                score = 1
            elif crack_time_seconds <= 5184000:
                score = 2
            elif crack_time_seconds >= 63072000:
                score = 4
            elif crack_time_seconds >= 7862400:
                score = 3
            else:
                score = 2

            crack_time = convert_crack_time(crack_time_seconds)

            color, label, emoji = colors[score]
            play_sound_loop_hidden(score)
            st.markdown(f"""
                <div style="background-color:{color};padding:20px;border-radius:10px;text-align:center;color:white;">
                    <h2>{label} {emoji}</h2>
                    <p>زمن الاختراق التقريبي: {crack_time}</p>
                </div>
            """, unsafe_allow_html=True)
            if score == 4:
                st.balloons()
        else:
            st.warning("الرجاء إدخال كلمة مرور")
    st.markdown("</div>", unsafe_allow_html=True)
