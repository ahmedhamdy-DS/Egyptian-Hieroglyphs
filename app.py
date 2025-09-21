import streamlit as st

# ==============================
# Page Config
# ==============================
st.set_page_config(page_title="Egyptian Hieroglyphs & Civilization", layout="wide")

# ==============================
# Custom CSS for Article-Style Dark Theme
# ==============================
st.markdown("""
<style>
body {
    background-color: #1e1e2f;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #ffffff;
}

.main-title {
    font-size: 44px !important;
    color: #e1bee7;
    font-weight: bold;
    text-align: center;
    margin-bottom: 40px;
    text-shadow: 1px 1px 3px #000;
}

.section-header {
    font-size: 32px !important;
    color: #bb86fc;
    margin-top: 50px;
    margin-bottom: 20px;
    border-bottom: 2px solid #bb86fc;
    padding-bottom: 5px;
}

.content-text {
    font-size: 18px !important;
    line-height: 1.8;
    margin-bottom: 25px;
}

.footer {
    background: linear-gradient(to right, #4b0082, #6a1b9a);
    color: #ffffff;
    padding: 20px;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    margin-top: 50px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# Hero Image
# ==============================
st.image(
    "assets/Egyptian_hieroglyphics.jpg",
    caption="✨ Ancient Egyptian hieroglyphic inscriptions ✨",
    width=700
)

# ==============================
# Main Title
# ==============================
st.markdown('<div class="main-title">Egyptian Hieroglyphs & Civilization</div>', unsafe_allow_html=True)

# ==============================
# Introduction
# ==============================
st.markdown("""
<div class="content-text">
Egyptian hieroglyphs are the ancient writing system used to record the Egyptian language and for sacred purposes.  
The oldest hieroglyphic text dates back to <b>4000–3500 BC</b>, making it older than Mesopotamian cuneiform.
</div>
""", unsafe_allow_html=True)

# ==============================
# Section 1: Civilization Overview
# ==============================
st.markdown('<div class="section-header">🏺 Ancient Egyptian Civilization</div>', unsafe_allow_html=True)
st.markdown("""
<div class="content-text">
The civilization of Ancient Egypt thrived for over 3,000 years along the Nile River, known for its monumental architecture, rich religion, and advances in science and art.  
Key aspects include:

- **Pharaohs**: The rulers of Egypt, considered divine and the bridge between gods and humans. Famous pharaohs include Khufu, Ramses II, and Cleopatra.  
- **Religion**: Polytheistic, with gods like Ra (Sun), Osiris (Afterlife), Isis (Motherhood), and Anubis (Mummification). Temples were central to worship.  
- **Architecture**: Pyramids, temples, and tombs were engineering marvels. The Great Pyramid of Giza remains one of the Seven Wonders of the Ancient World.  
- **Science & Mathematics**: Egyptians developed a calendar, advanced medicine, geometry, and methods for irrigation and agriculture.  
- **Art & Writing**: Hieroglyphs recorded history, religious texts, and daily life. Art depicted gods, pharaohs, and societal activities in detailed, symbolic forms.  
- **Daily Life**: Agriculture, trade, crafts, and rituals dominated. Social classes included pharaohs, priests, scribes, artisans, and farmers.  
</div>
""", unsafe_allow_html=True)

# ==============================
# Section 2: Usage of Hieroglyphs
# ==============================
st.markdown('<div class="section-header">📜 Usage in Ancient Egypt</div>', unsafe_allow_html=True)
col1, col2 = st.columns([2,1])

with col1:
    st.markdown("""
    <div class="content-text">
    Hieroglyphs were primarily used for sacred, ceremonial, and official purposes:

    - Inscriptions on temples, tombs, and monuments  
    - Religious texts such as the <i>Book of the Dead</i>  
    - Carved onto statues, stelae, and decorated coffins  

    Writing a person's name was believed to help secure eternal life.  
    Example: <b>"Chief Scribe Amenemhat, True of Voice."</b>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("assets/Egypt_bookofthedead.jpg",
             caption="Book of the Dead – Osiris receiving the righteous",
             use_container_width=True)

# ==============================
# Section 3: Evolution of Writing
# ==============================
st.markdown('<div class="section-header">🔤 Evolution of Egyptian Writing</div>', unsafe_allow_html=True)
col3, col4 = st.columns([1,1])

with col3:
    st.markdown("""
    <div class="content-text">
    Egyptian writing evolved into four main forms:

    1. <b>Hieroglyphic</b> – formal monumental script  
    2. <b>Hieratic</b> – simplified script for priests and administrative documents  
    3. <b>Demotic</b> – cursive script for everyday use  
    4. <b>Coptic</b> – Greek alphabet + 7 Demotic signs, representing the final stage of the language  

    Hieroglyphs influenced many modern writing systems through Proto-Sinaitic → Phoenician → Greek → Latin → Cyrillic.
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.image("assets/حجر رشيد2.jpg",
             caption="The Rosetta Stone – key to deciphering hieroglyphs",
             use_container_width=True)

# ==============================
# Section 4: Religion & Beliefs
# ==============================
st.markdown('<div class="section-header">🛕 Religion & Beliefs</div>', unsafe_allow_html=True)
st.markdown("""
<div class="content-text">
Ancient Egyptians believed in a rich pantheon of gods and the afterlife.  
- **Ra**: Sun god, creator of all life  
- **Osiris**: God of the afterlife and resurrection  
- **Isis**: Goddess of motherhood and magic  
- **Anubis**: God of mummification and guide of souls  

Rituals, offerings, and temple ceremonies were essential to maintain ma’at (cosmic order).
</div>
""", unsafe_allow_html=True)

# ==============================
# Section 5: Achievements
# ==============================
st.markdown('<div class="section-header">🌟 Achievements</div>', unsafe_allow_html=True)
st.markdown("""
<div class="content-text">
Ancient Egypt contributed significantly to human knowledge:

- **Architecture**: Pyramids, temples, and monumental statues  
- **Medicine**: Advanced surgical techniques and herbal remedies  
- **Mathematics & Astronomy**: Calendars, geometry, and timekeeping  
- **Art & Culture**: Sculptures, paintings, jewelry, and literature  
- **Engineering**: Irrigation systems and stone constructions  
</div>
""", unsafe_allow_html=True)

# ==============================
# Section 6: Legacy
# ==============================
st.markdown('<div class="section-header">🏛️ Legacy of Ancient Egypt</div>', unsafe_allow_html=True)
st.markdown("""
<div class="content-text">
- Hieroglyphs remain a symbol of Egyptian identity and are studied worldwide.  
- Architectural principles influenced Greek and Roman constructions.  
- Many cultural ideas, like concepts of kingship, law, and astronomy, trace back to Egypt.  
- Museums across the globe preserve artifacts and educate people about this incredible civilization.
</div>
""", unsafe_allow_html=True)

# ==============================
# Footer
# ==============================
st.markdown('<div class="footer">✅ Explore Egyptian culture and try the translation tool in the next page!</div>', unsafe_allow_html=True)





