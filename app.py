import streamlit as st
import random
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Ancient Egypt AI Explorer",
    page_icon="🏺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DATA ---

# Hieroglyph mapping (Letter -> Image URL, Tooltip)
# For a real app, you would host these images or find a reliable API.
# Using unicode characters as a fallback with placeholder image URLs
HIEROGLYPHS = {
    'A': ('https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhHY58QVPvhRIp7c01N1uLhliXD9Tc-wkakPkpIp2Nd3m8VZNKjDgriynzJzP43e2q9rJkiVLGY6HpZVOJn_uvz356MoYezBOkrgBn4mAshof2ZwPvXb-VjxH7TFKAHhaX_x23lPapy6KQ/s1600/vulture.jpg', 'Vulture (Ah)'), 'B': ('https://i.imgur.com/7l6gU5Y.png', 'Foot (B)'),
    'C': ('https://i.imgur.com/iJp4u8X.png', 'Basket with handle (K)'), 'D': ('https://i.imgur.com/7l6gU5Y.png', 'Hand (D)'),
    'E': ('https://i.imgur.com/gOkp2dQ.png', 'Vulture (Ah)'), 'F': ('https://i.imgur.com/iJp4u8X.png', 'Horned Viper (F)'),
    'G': ('https://i.imgur.com/7l6gU5Y.png', 'Jar Stand (G)'), 'H': ('https://i.imgur.com/iJp4u8X.png', 'Wick of Twisted Flax (H)'),
    'I': ('https://i.imgur.com/gOkp2dQ.png', 'Flowering Reed (Ee)'), 'J': ('https://i.imgur.com/iJp4u8X.png', 'Cobra (Dj)'),
    'K': ('https://i.imgur.com/iJp4u8X.png', 'Basket with handle (K)'), 'L': ('https://i.imgur.com/7l6gU5Y.png', 'Lion (L)'),
    'M': ('https://i.imgur.com/gOkp2dQ.png', 'Owl (M)'), 'N': ('https://i.imgur.com/iJp4u8X.png', 'Water Ripple (N)'),
    'O': ('https://i.imgur.com/gOkp2dQ.png', 'Lasso (O)'), 'P': ('https://i.imgur.com/7l6gU5Y.png', 'Stool (P)'),
    'Q': ('https://i.imgur.com/iJp4u8X.png', 'Hill (Q)'), 'R': ('https://i.imgur.com/7l6gU5Y.png', 'Mouth (R)'),
    'S': ('https://i.imgur.com/iJp4u8X.png', 'Folded Cloth (S)'), 'T': ('https://i.imgur.com/7l6gU5Y.png', 'Bread Loaf (T)'),
    'U': ('https://i.imgur.com/gOkp2dQ.png', 'Quail Chick (Oo)'), 'V': ('https://i.imgur.com/iJp4u8X.png', 'Horned Viper (F)'),
    'W': ('https://i.imgur.com/gOkp2dQ.png', 'Quail Chick (Oo)'), 'X': ('https://i.imgur.com/iJp4u8X.png', 'Basket & Folded Cloth (KS)'),
    'Y': ('https://i.imgur.com/gOkp2dQ.png', 'Two Flowering Reeds (Y)'), 'Z': ('https://i.imgur.com/iJp4u8X.png', 'Door Bolt (S)')
}

# Quiz Questions
QUIZ_QUESTIONS = [
    {
        "question": "Who was the god of the sun, often considered the king of the gods?",
        "options": ["Osiris", "Anubis", "Ra", "Thoth"],
        "answer": "Ra",
        "explanation": "Ra was the powerful sun god of Ancient Egypt. He was often depicted with a falcon head and a sun disk on top."
    },
    {
        "question": "What is the name of the ancient Egyptian writing system?",
        "options": ["Cuneiform", "Hieroglyphs", "Sanskrit", "Runes"],
        "answer": "Hieroglyphs",
        "explanation": "Hieroglyphs are a system of writing that uses characters in the form of pictures. The ancient Egyptians used them for formal inscriptions."
    },
    {
        "question": "The Great Sphinx of Giza has the head of a human and the body of a what?",
        "options": ["Eagle", "Lion", "Scorpion", "Horse"],
        "answer": "Lion",
        "explanation": "The Great Sphinx is a limestone statue of a reclining sphinx, a mythical creature with the body of a lion and the head of a human."
    },
    {
        "question": "Which pharaoh's tomb, discovered in 1922, was famously intact?",
        "options": ["Ramesses II", "Cleopatra", "Akhenaten", "Tutankhamun"],
        "answer": "Tutankhamun",
        "explanation": "Howard Carter's discovery of Tutankhamun's nearly intact tomb was a landmark archaeological find, revealing incredible treasures."
    }
]

# Timeline Data
TIMELINE_DATA = [
    {"period": "Early Dynastic Period", "dynasty": "Dynasties I-II", "pharaoh_icon": "👑", "details": "Unification of Upper and Lower Egypt by Narmer. Hieroglyphic script develops."},
    {"period": "Old Kingdom", "dynasty": "Dynasties III-VI", "pharaoh_icon": " pyramids ", "details": "The 'Age of the Pyramids.' Djoser's Step Pyramid and the Great Pyramids of Giza were built."},
    {"period": "New Kingdom", "dynasty": "Dynasties XVIII-XX", "pharaoh_icon": " tut ", "details": "The 'Golden Age.' Reigns of powerful pharaohs like Hatshepsut, Akhenaten, Tutankhamun, and Ramesses II."},
    {"period": "Ptolemaic Period", "dynasty": "Ptolemaic Dynasty", "pharaoh_icon": " cleo ", "details": "Rule by Greek pharaohs after Alexander the Great's conquest. Ends with the death of Cleopatra VII."}
]

# "Did You Know" Facts
FACTS = [
    {"icon": " M ", "text": "Ancient Egyptians believed cats were sacred animals and were associated with the goddess Bastet."},
    {"icon": " ️ ", "text": "Both men and women in ancient Egypt wore makeup, particularly kohl eyeliner, which they believed had healing properties."},
    {"icon": " ", "text": "The pyramids were not built by slaves, but by paid, skilled laborers who lived in well-established communities."},
    {"icon": "⚖️", "text": "When a person died, their heart was weighed against the 'feather of truth' (Ma'at) to determine if they were worthy of the afterlife."},
    {"icon": " ", "text": "The Book of the Dead was not a single book, but a collection of spells and texts intended to guide the deceased through the underworld."},
    {"icon": " ", "text": "Scribes were highly respected professionals. They spent years learning the complex hieroglyphic and hieratic scripts."},
]

# --- SESSION STATE INITIALIZATION ---
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = [None] * len(QUIZ_QUESTIONS)


# --- HELPER FUNCTIONS ---
def load_css():
    """Inject custom CSS into the Streamlit app."""
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    """Convert binary file to base64 string."""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- UI SECTIONS ---
def hero_section():
    """Display the main hero section with title and CTA."""
    st.markdown("""
        <div class="hero-section">
            <div class="hero-text">
                <h1 class="cinzel-decorative-bold">Ancient Egypt AI Explorer</h1>
                <p class="subtitle">An AI-Powered Journey into the Land of the Pharaohs</p>
                <a href="#scribe-your-name-in-hieroglyphs" class="cta-button">Explore the Pharaonic civilization in a different way</a>
            </div>
        </div>
    """, unsafe_allow_html=True)




def educational_section():
    """Display the detailed educational introduction."""
    st.markdown("""
        <div class="section-container">
            <h2 class="section-title">A Civilization Carved in Stone</h2>
            <p>Welcome to the world of Ancient Egypt, a civilization that flourished for over 3,000 years along the fertile banks of the Nile River. Renowned for its monumental architecture, complex religious beliefs, and revolutionary writing system, ancient Egypt left an indelible mark on history. From the towering <span class="keyword" title="The Great Pyramids of Giza are the last surviving of the Seven Wonders of the Ancient World.">Pyramids of Giza</span> to the enigmatic gaze of the Sphinx, its legacy continues to captivate and inspire.</p>
            <p>At the heart of Egyptian culture was a profound connection to religion. They worshipped a vast pantheon of gods and goddesses, such as <span class="keyword" title="The sun god, often considered the most important deity.">Ra</span>, the sun god; <span class="keyword" title="The god of the afterlife and resurrection.">Osiris</span>, god of the underworld; and <span class="keyword" title="The goddess of magic and healing, wife of Osiris.">Isis</span>, his devoted wife. Their beliefs about the afterlife led to sophisticated mummification practices and the construction of elaborate tombs, most famously in the Valley of the Kings.</p>
            <p>The Egyptians communicated through a beautiful and complex script known as <span class="keyword" title="Meaning 'sacred carvings' in Greek.">hieroglyphs</span>, or 'medu netjer' (the god's words). Famous inscriptions like those on the <span class="keyword" title="An ancient stone slab that was key to deciphering hieroglyphs.">Rosetta Stone</span> provided the key for modern scholars to unlock the secrets of this ancient language, revealing stories of pharaohs, poetry, and administrative records.</p>
        </div>
    """, unsafe_allow_html=True)


def timeline_section():
    """Display the interactive historical timeline."""
    st.markdown('<h2 class="section-title">Timeline of Dynasties</h2>', unsafe_allow_html=True)
    st.markdown("""
        <div class="timeline">
            <div class="timeline-item left">
                <div class="timeline-content">
                    <h3>Early Dynastic Period (c. 3100-2686 BCE)</h3>
                    <p><strong>Dynasties I-II:</strong> The unification of Upper and Lower Egypt by King Narmer marks the beginning. The capital city of Memphis was founded. Hieroglyphic writing was developed and standardized.</p>
                </div>
            </div>
            <div class="timeline-item right">
                <div class="timeline-content">
                    <h3>Old Kingdom (c. 2686-2181 BCE)</h3>
                    <p><strong>Dynasties III-VI:</strong> Known as the 'Age of the Pyramids.' Pharaoh Djoser's Step Pyramid was built, followed by the magnificent Great Pyramids and Sphinx at Giza. A strong central government was established.</p>
                </div>
            </div>
            <div class="timeline-item left">
                <div class="timeline-content">
                    <h3>New Kingdom (c. 1550-1069 BCE)</h3>
                    <p><strong>Dynasties XVIII-XX:</strong> Egypt's 'Golden Age.' A period of immense wealth, power, and territorial expansion. Featured famous pharaohs like Hatshepsut, Akhenaten, Tutankhamun, and Ramesses the Great.</p>
                </div>
            </div>
            <div class="timeline-item right">
                <div class="timeline-content">
                    <h3>Ptolemaic Period (332-30 BCE)</h3>
                    <p><strong>Ptolemaic Dynasty:</strong> Following Alexander the Great's conquest, Egypt was ruled by a Greek dynasty. The period ended with the death of the famous queen, Cleopatra VII, and Egypt became a Roman province.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def quiz_section():
    """Handle the interactive quiz logic and UI."""
    st.markdown('<h2 class="section-title">Test Your Knowledge</h2>', unsafe_allow_html=True)

    if not st.session_state.quiz_started:
        if st.button("Begin the Challenge!", key="start_quiz"):
            st.session_state.quiz_started = True
            st.rerun()
    else:
        q_index = st.session_state.current_question
        if q_index < len(QUIZ_QUESTIONS):
            question_data = QUIZ_QUESTIONS[q_index]
            
            # Using custom HTML for papyrus card effect
            st.markdown(f"""
            <div class="quiz-card">
                <p class="question-text">{q_index + 1}. {question_data['question']}</p>
            </div>
            """, unsafe_allow_html=True)

            options = question_data["options"]
            user_choice = st.radio("Choose your answer:", options, key=f"q_{q_index}", index=None)

            if user_choice:
                st.session_state.user_answers[q_index] = user_choice
                correct_answer = question_data["answer"]
                
                if user_choice == correct_answer:
                    st.session_state.score += 1
                    st.success(f"Correct! {question_data['explanation']}", icon="✅")
                else:
                    st.error(f"Not quite. The correct answer was {correct_answer}. {question_data['explanation']}", icon="❌")

                if st.button("Next Question →", key=f"next_{q_index}"):
                    st.session_state.current_question += 1
                    st.rerun()
        else:
            # Display final score
            score_percent = (st.session_state.score / len(QUIZ_QUESTIONS)) * 100
            st.markdown(f"""
            <div class="score-scroll">
                <h3>Quiz Complete!</h3>
                <p>Your Final Score:</p>
                <p class="final-score">{st.session_state.score} out of {len(QUIZ_QUESTIONS)} ({score_percent:.0f}%)</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Try Again?", key="reset_quiz"):
                # Reset session state for the quiz
                st.session_state.quiz_started = False
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.user_answers = [None] * len(QUIZ_QUESTIONS)
                st.rerun()


def did_you_know_section():
    """Display random interesting facts in styled cards."""
    st.markdown('<h2 class="section-title">Did You Know?</h2>', unsafe_allow_html=True)
    
    selected_facts = random.sample(FACTS, k=3)
    cols = st.columns(3)
    
    for i, fact in enumerate(selected_facts):
        with cols[i]:
            st.markdown(f"""
            <div class="fact-card">
                <span class="fact-icon">{fact['icon']}</span>
                <p>{fact['text']}</p>
            </div>
            """, unsafe_allow_html=True)


def footer_section():
    """Display the app footer."""
    st.markdown("""
        <hr>
        <div class="footer">
            <p>© 2025 AI Egypt Explorer. All Rights Reserved.</p>
            <p class="quote">"To speak the names of the dead is to make them live again." - Ancient Egyptian Proverb</p>
            </div>
    """, unsafe_allow_html=True)


# --- MAIN APP LAYOUT ---
def main():
    load_css()
    
    hero_section()
    educational_section()
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    timeline_section()

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    did_you_know_section()
    
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    quiz_section()
    
    footer_section()

if __name__ == "__main__":
    main()










