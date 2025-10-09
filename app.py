import streamlit as st
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Egyptian Hieroglyphs Portal",
    page_icon="🏺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- LOAD ASSETS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

# =====================================================================
# --- DATA FOR NEW SECTIONS ---
# ====================================================================

# --- Hieroglyph Map ---
HIEROGLYPH_MAP = {
    'a': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhHY58QVPvhRIp7c01N1uLhliXD9Tc-wkakPkpIp2Nd3m8VZNKjDgriynzJzP43e2q9rJkiVLGY6HpZVOJn_uvz356MoYezBOkrgBn4mAshof2ZwPvXb-VjxH7TFKAHhaX_x23lPapy6KQ/s1600/vulture.jpg', 'b': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhYHq0ydhYQlzJJL6nvTr_T1_-3KR77rgfSJ7JWz77O5JCVi5u-Ubm6QWaTbnlv7vul_dWDAQ8OR0vuh2C0VLzlBod_is-tvCCkqOvSvgQbHkf0HiL_YcXdjTxpzytppogmkKkDyGs8hOM/s1600/letter-B.jpg',
    'c': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjse13Wox3M2YCpbhKFMqJwqs14HIwrD3LTAybXUXXfWhbog6D5LMd4dif2Us-UPWjhV8D-u387JFyLPep4x2qgFA0X2O2sYJ2ZqFKwli3G77g01WmahVxi8b5mUhEy-6W4BEhaY0XF1go/s1600/C-bowl.jpg', 'd': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjPsStVf9wCpzd3w13ulpRgzDkkaGLEMGX8bGSKx6z5ebC6782ZNU3-vt0Cv6pdwP_i4TPddwDnzNjbSjgAGYtGtnTXDQS1-_Hfe4061AZCrc7i4RxAEy1FN6AxQA8nt_DAfw3VTMgBcmo/s1600/D-hand.png',
    'e': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEix4a23s5hI2M51QayP_TDgNLzNtTy5mLTQip_-lRY3FBvqD8AQBdeK4Fy_enrjn6w07OQwDDSfgB0HR7ckgXJeVnz9HYEcWuY55dvUsyoOeslC0Jl3uS202ukHpC9kdMmpSuGrPArf61Q/s1600/E-feather.png', 'f': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEicm61FgwfgudtsVZTYYw0m_gPVirujmFRhDdNO4z4E2ktv86j48Izo2KSW3_u-nsX-DH_ibMj64wFvP7pLF1U30U0Lx4zqbdH52VRHOK-D39FlQZVzWR0VswrGqHnffHI-c_tx3WNcXsI/s1600/F-viper.jpg',
    'g': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgbe2Rsk_H9ZWEE9WeZHhIwL4ZkysobZuzAfQoIifSetnO0224i6GqpTHTQuCOsGHgLI5cuvV2iExxD0yHTMcYdrPyQtn7CDYsYHAjS7c87f107UO36x84UAOaObf6oao54HcHY0MYlySc/s1600/G-cobra.png', 'h': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhnBnw-E1qH4Y0hzRmwR3s4cMRxT48weL_tNzJKbhyphenhyphenMIZhUYiut9gE-I6Vr4kbm9Iig7qENEFcrdj2rGJUlG83sSrUOXJ-5rooFLUUffRKcPxciIo390t1nG3734bP_a0R1EQ8HAWo29kk/s1600/H-dwelling.png',
    'i': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiTBCLMQvn8nMfuFZ8gbCL_bTnJcAwO1Ij1z_V8dMqn7HB2JBQh1h6Q8HdpHADDPOahD4oDff69spxS48JB_vkg4i5wYGqHyspFnSAxfAU4bQSzA8Lx7El_n7tkhCqRnDIjXWDJWhkcRV8/s1600/i-feather.png', 'j': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgop-uKMvq4l5ExfwNwUjSp6yj5bk1yfDkSIw_sTM7rvwQYdyXX3-JKro32Z699CM4GlB6vkts73QOVU2rHz5vKGL5oSlKQ4F_P2_-bkiOaPvHB5vJ4cViiG-lOTQVu5uEc_vdNChqVI54/s1600/J-cobra.png',
    'k': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgDW6iyQQvVQYoJ3JtQocaMU-5l3oCjMlIzx1wyHj95MwL-yMqLLWFXhWwAlTY79G9Bt-hwOtfg3u5cmxQ6D3mGzhWDsVsD1-QM3lAgNyz3s3ULBSkuTt6ZWhe9Ic-A0E_nkiPmbQ7MPhk/s1600/K-bowl.png', 'l': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi0v5E8ipyYuka_avtg8l5ojXX2VrmHvL_ZtkIs029v42jkE9daFN1o6rOJ5-AYvrJxCIKgvtY8oksJI1qLJc93mMQKqfEYTQqvLg-_tYIYv3cPOQYqzHMCMVAfYYK9XmBtMUEIfwpDhhA/s1600/L-lion.jpg',
    'm': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgjGglviV3QyOA2tDA8kKweCY1cOkATjWpqIrCHuxHCQvz2LDy3XIQyUcZ9jCb5r36TsS66iFcfbjLuJk-ldJNMjzCtkyt9XWwVi-ybqRCrfJ0OsTfh6Df29Ub-LCdDtESlJIJr6Plqq6o/s1600/M-owl.png', 'n': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjokqUV1r8tt9-SpK8iq2sCQxC-qltasH-k9h9retY-zlobxbLJ7C1OyU9A2zHhrji9xKgWOxGJy4sZG3yfM4566J4o6iB4R9YyMnoQQzVrmFT-SBB9N1zhMAPWU3PvQvAOCBLshM5qqCM/s200/N-water.png',
    'o': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjmsDNYPdExgAzwgAGeioo_yy5Hee-wKz_WfGgLpU36ChPWQeGY4Iwb-5RqE2gyxURwLs3Vtkmh24fRQDbI8d-4lqpg_HJ6pYoK80-hqioOcb4ss8NOGeyiWfs191iUChGQrgFnhhoOh60/s1600/O-bird.png', 'p': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiXV8rWG8YPT2BMTQRj72paLcRi6K3k3AnN3VWAqIfB-NNdhC4g38VmIx3qfHd_e8Cf1uzGisWNO71xZP3tynA9KKqhYDguNKdp6DQEuD2mqg10ZbyLg-n6LXy6VplWTTx2ozwY563ZtOc/s1600/P-Stool.png',
    'q': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEitkb07oddHupsmcxd14JzyuEyqoJtG404yvVesZuOGvaUedON7MkR2HVh6Cg4mwhCh4gy1dtOgVRO5gK9j601jeOgl4Dk8a34R5qZX9xD3kwRg6VQqSIE2ljteyMPnhk5PbtJsLerqGtk/s1600/Q-hillside.png', 'r': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh00nd_KMeRum_Qv8hFoC8Kuf2KDPTEnI5lj70mUg2RoVL0oWumP5m-6Ucis45oO6Pf4IpCDUc9Q8J25zoGc6DDM5dOhSf38yb24KLFggbvIGLz07-oEdftLWSbsHI2qq_wIkBy3ZqjTpU/s1600/R-mouth.png',
    's': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiDp_lCWiSIS5S9mxa-jy7egmZZKTyiT0BufVCTWVUHtchvXrmAcskxhqiZV1bsnuRAhXCQEjt00VORrjBTN-7zMKt9oJf7adZyHQS5ZBBdukSXbS3TutmHNiywdFWeM8uMyNqzZJ36exU/s400/Letter-S-Egyptian-hieroglyphics.jpg', 't': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiuB8yZws6Hx3KI0ZY6p7P5gtDqJ-daEhqHYFNaU_QTY3cgHgz3WclGZDJ1_lBMESoT7s1N4-PhJly3cYOqfHCu7GkaNxE9_9bDOrQPso3PvZ2tF13PT1HgF-MR9RgSOS1HjNCJPf6bGAI/s200/Letter-T-Egyptian-hieroglyphics.jpg',
    'u': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj1h3Ex-aLqI0le_z757m8HFO4IuxkQyCFoFeah5eII5w2gt8HHAZd7korNkFyfddyPtYF9QJT5-w-D3hRW7a1ptDyHbVUGdhY1Mc8Q7dO8wKhGTK0hGEZwQXdVPOa7T3Jen203Wz6vy3U/s400/Letter-U-in-hieroglyphics.jpg', 'v': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiAXLnPCFKthMpEjPgLCFE3EgiZ-YPgbQDIRaRLFH_npat_tYQVXkm2Yjhyp5zWdPDKh5faAG2lrO73moegpuVW1EzJlOUkRxFIrnCeUkpZ40tBPfkZLvux2N0nBTal41r1Nrmf5NWTO9w/s200/V-viper.png',
    'w': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgYD01X5EV0rMBVVVyfixalO50mpD9QyzTDYiZwM0jblcQT1S27LvchlLCcDQ3QRMAQ9PORZ2ydKS7-LGB981YPW3_KQr_XdS7FozFMgGfdEtH0J9fDpdmtSrKNor608zqy1wUpUq_IlsE/s1600/W-bird.png', 'x': 'https://i.imgur.com/GplnC5A.png',
    'y': 'https://i.imgur.com/p0S2k9A.png', 'z': 'https://i.imgur.com/9y8zL7R.png'
}



# --- Data for Quiz ---
QUIZ_QUESTIONS = [
    {
        "question": "What does this symbol, the Ankh, represent?",
        "options": ["Life, and Immortality", "Power and Authority", "Sun and Creation"],
        "answer": "Life, and Immortality",
        "image": "https://i.pinimg.com/736x/23/0e/4d/230e4d58025077c7d76ffd20ae98feae.jpg"
    },
    {
        "question": "The Eye of Horus is a symbol of:",
        "options": ["War and Chaos", "Protection, Health, and Restoration", "Knowledge and Wisdom"],
        "answer": "Protection, Health, and Restoration",
        "image": "https://i.pinimg.com/1200x/ab/8b/01/ab8b01bb0189f3f15536ba898b4d89eb.jpg"
    },
    {
        "question": "What does the Scarab beetle symbolize in ancient Egypt?",
        "options": ["Darkness and the Underworld", "Royalty and Pharaohs", "Rebirth and Transformation"],
        "answer": "Rebirth and Transformation",
        "image": "https://i.pinimg.com/1200x/b3/08/21/b30821176c423dd7702742e0f6a02ab0.jpg"
    }
]

# --- Data for Timeline ---
DYNASTIES = [
    {"period": "Early Dynastic Period", "date": "c. 3100–2686 BCE", "detail": "Unification of Upper and Lower Egypt. Development of foundational Egyptian culture and writing."},
    {"period": "Old Kingdom", "date": "c. 2686–2181 BCE", "detail": "The 'Age of the Pyramids.' Construction of the Great Pyramids of Giza. Centralized pharaonic rule."},
    {"period": "Middle Kingdom", "date": "c. 2055–1650 BCE", "detail": "A period of cultural renaissance, literature, and art. Egypt's influence expanded into Nubia."},
    {"period": "New Kingdom", "date": "c. 1550–1069 BCE", "detail": "The 'Imperial Age.' Era of famous pharaohs like Hatshepsut, Akhenaten, Tutankhamun, and Ramesses II."},
    {"period": "Ptolemaic Period", "date": "332–30 BCE", "detail": "Following Alexander the Great's conquest, ruled by a Greek dynasty. Cleopatra VII was the last ruler."},
]


# =====================================================================
# --- UI SECTIONS ---
# =====================================================================

# --- HERO SECTION ---
st.markdown("""
<div class="hero-section">
    <div class="hero-text">
        <h1 class="title">Egyptian Hieroglyphs Portal</h1>
        <p class="subtitle">Unveiling the Language of the Gods with AI</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- ABOUT HIEROGLYPHS SECTION (Original Section, Enhanced) ---
st.markdown("""
<div class="section-container">
    <h2 class="section-header">The Sacred Carvings</h2>
    <p style="text-align:center; max-width:800px; margin:auto;">
        Hieroglyphs were the formal writing system of ancient Egypt. Combining pictures, sounds, and concepts, this sacred script adorned tombs and temples, preserving a civilization's deepest secrets for millennia.
    </p>
</div>
""", unsafe_allow_html=True)


# --- NEW: AI HIEROGLYPH NAME GENERATOR ---
st.markdown("""
<div class="section-container">
    <h2 class="section-header">Scribe Your Name in a Cartouche</h2>
    <p style="text-align:center; max-width:800px; margin:auto; margin-bottom: 2rem;">
        Enter your name below and let the AI scribe translate it into hieroglyphs, framed within a royal cartouche, the sacred rope loop that protected a pharaoh's name.
    </p>
""", unsafe_allow_html=True)

name_input = st.text_input("Enter your name :", "", key="name_generator", help="Use letters A-Z")

if name_input:
    st.markdown('<div class="cartouche-container">', unsafe_allow_html=True)
    for char in name_input.lower():
        if char in HIEROGLYPH_MAP:
            glyph_url = HIEROGLYPH_MAP[char]
            st.markdown(f'<img src="{glyph_url}" alt="{char}">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# --- NEW: VISUAL TIMELINE OF DYNASTIES ---
st.markdown("""
<div class="section-container">
    <h2 class="section-header">Timeline of the Dynasties</h2>
    <div class="timeline">
""", unsafe_allow_html=True)

for i, dynasty in enumerate(DYNASTIES):
    direction = "left" if i % 2 == 0 else "right"
    st.markdown(f"""
        <div class="timeline-item {direction}">
            <div class="timeline-content">
                <h3>{dynasty['period']}</h3>
                <p><strong>{dynasty['date']}</strong></p>
                <p>{dynasty['detail']}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)


# --- NEW: HIEROGLYPH QUIZ ---
st.markdown("""
<div class="section-container quiz-container">
    <h2 class="section-header">Guess the Symbol</h2>
    <p style="text-align:center;">Test your knowledge of common hieroglyphic symbols!</p>
""", unsafe_allow_html=True)

# Initialize session state for the quiz
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.quiz_started = False
    st.session_state.show_result = False

def next_question():
    if st.session_state.current_question < len(QUIZ_QUESTIONS) - 1:
        st.session_state.current_question += 1
    else:
        st.session_state.show_result = True

def restart_quiz():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.quiz_started = False
    st.session_state.show_result = False

if not st.session_state.quiz_started and not st.session_state.show_result:
    if st.button("📜 Start the Hieroglyph Challenge!"):
        st.session_state.quiz_started = True
        st.rerun()

elif st.session_state.quiz_started and not st.session_state.show_result:
    q = QUIZ_QUESTIONS[st.session_state.current_question]
    st.image(q["image"], width=150)
    st.subheader(q["question"])
    user_answer = st.radio("Choose your answer:", q["options"], key=f"q{st.session_state.current_question}")
    
    if st.button("Submit Answer"):
        if user_answer == q["answer"]:
            st.success("Correct! Well done, scribe. ✨")
            st.session_state.score += 1
        else:
            st.error(f"Not quite. The correct answer was: {q['answer']}")
        
        # This button moves to the next question
        next_question()
        st.rerun()

elif st.session_state.show_result:
    st.markdown("""
    <style>
    /* Papyrus Scroll Animation */
    @keyframes scrollOpen {
        0% {
            transform: scaleY(0.1);
            opacity: 0;
        }
        60% {
            transform: scaleY(1.05);
            opacity: 1;
        }
        100% {
            transform: scaleY(1);
        }
    }

    .papyrus-scroll {
        background: url('https://i.pinimg.com/originals/9e/55/aa/9e55aa5bcac5a0e40d47e801c7d2c4c5.jpg');
        background-size: cover;
        padding: 40px;
        margin: 40px auto;
        width: 80%;
        border: 3px solid #d4af37;
        border-radius: 12px;
        font-family: 'Cinzel Decorative', cursive;
        color: #3b2f2f;
        text-align: center;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.4);
        animation: scrollOpen 1.2s ease-out forwards;
        transform-origin: top center;
    }

    .papyrus-title {
        font-size: 2rem;
        color: #b8860b;
        text-shadow: 0 0 10px #f0e68c;
    }

    .papyrus-text {
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        margin-top: 10px;
    }

    .papyrus-glow {
        color: #FFD700;
        font-size: 1.5rem;
        text-shadow: 0 0 10px #FFD700, 0 0 20px #FFA500, 0 0 40px #FFD700;
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { text-shadow: 0 0 10px #FFD700, 0 0 20px #FFA500; }
        to { text-shadow: 0 0 20px #FFD700, 0 0 40px #FFA500, 0 0 60px #FFD700; }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="papyrus-scroll">
        <div class="papyrus-title">📜 Quiz Complete!</div>
        <div class="papyrus-text">Your final score: <b>{st.session_state.score} / {len(QUIZ_QUESTIONS)}</b></div>
        <div class="papyrus-glow">✨ “You walk the path of the Pharaohs!” ✨</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Try Again?"):
        restart_quiz()
        st.rerun()


st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)









