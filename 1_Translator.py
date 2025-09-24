import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os
import gdown

# ==============================
# Page Config
# ==============================
st.set_page_config(page_title="Egyptian Hieroglyphs", layout="wide")

# ==============================
# Load Model
# ==============================
MODEL_DIR = "model"
MODEL_FILE = "InceptionV3_model.h5"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)

if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_DIR, exist_ok=True)
    url = "https://huggingface.co/sonic222/Egyptian-Hieroglyphs/resolve/main/InceptionV3_model.h5"
    gdown.download(url, MODEL_PATH, quiet=False)

model = load_model(MODEL_PATH)

# ==============================
# Label Map (يجب أن يتطابق مع تدريب النموذج)
# ==============================
label_map = {
    0: "N14", 1: "D2", 2: "L1", 3: "R1", 4: "F9",
    5: "S40", 6: "M9", 7: "G17", 8: "S42", 9: "R4"
}

# ==============================
# Gardiner Categories
# ==============================
gardiner_categories = {
    "A": "Man and his occupations",
    "B": "Woman and her occupations",
    "C": "Anthropomorphic deities",
    "D": "Parts of the human body",
    "E": "Mammals",
    "F": "Parts of mammals",
    "G": "Birds",
    "H": "Parts of birds",
    "I": "Amphibious animals, reptiles",
    "K": "Fish and parts of fish",
    "L": "Invertebrates and small plants",
    "M": "Trees and plants",
    "N": "Sky, earth, water",
    "O": "Buildings, parts of buildings",
    "P": "Domestic and funerary furniture",
    "Q": "Vessels of stone and earthenware",
    "R": "Temple furniture and sacred emblems",
    "S": "Crowns, dress, staves, weapons",
    "T": "Warfare, hunting, butchery",
    "U": "Agriculture, crafts, professions",
    "V": "Rope, fiber, baskets, bags",
    "W": "Vessels of wood, stone, metal",
    "X": "Loaves, cakes, offerings",
    "Y": "Writing, games, music",
    "Z": "Strokes, signs, geometrical figures",
    "Aa": "Unclassified signs"
}

# ==============================
# Translation Dictionary (English)
# ==============================
code_to_info = {
    "N14": ("Ankh (☥)", "📖 Meaning: Symbol of eternal life, often simply translated as 'life'. Ancient Egyptians carried it in statues and inscriptions as a sign of immortality and spiritual power."),
    "D2": ("Eye of Horus (Udjat)", "📖 Meaning: Symbol of protection, health, and healing. Named after the myth where Horus lost his eye fighting Seth. Widely used as a powerful amulet."),
    "L1": ("Scarab", "📖 Meaning: Symbol of renewal, rebirth, and transformation. The scarab beetle rolling the sun across the sky represented daily cosmic rebirth."),
    "R1": ("Ra (Sun God)", "📖 Meaning: The Sun God and one of the greatest deities of Egypt. Represents creation, light, and warmth. Often depicted with a falcon head and a solar disk."),
    "F9": ("Djed (Pillar)", "📖 Meaning: Symbol of stability and endurance. Associated with Osiris, representing the backbone and everlasting strength."),
    "S40": ("Was Scepter", "📖 Meaning: Symbol of power, control, and dominion. Frequently shown in the hands of kings and gods as a tool of cosmic authority."),
    "M9": ("Lotus Flower", "📖 Meaning: Symbol of creation, rebirth, and purity. The lotus opens at sunrise and closes at night, symbolizing the sun's rebirth and the cycle of life."),
    "G17": ("Feather of Ma'at", "📖 Meaning: Symbol of truth, justice, and cosmic order. Used in the Judgment of Osiris, where the heart of the deceased was weighed against the feather."),
    "S42": ("Crook & Flail", "📖 Meaning: Royal authority symbol. The crook represents care and guardianship (the king as shepherd), while the flail represents discipline and power."),
    "R4": ("Rosetta Stone", "📖 Meaning: The key to deciphering hieroglyphs. Inscribed in three scripts (Hieroglyphic, Demotic, and Greek). Enabled Champollion to unlock hieroglyphic writing in 1822.")
}

# ==============================
# Helper Function
# ==============================
def predict_image(img_path):
    try:
        img = load_img(img_path, target_size=(299, 299))
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        preds = model.predict(img_array, verbose=0)
        class_idx = np.argmax(preds)
        confidence = np.max(preds)

        code = label_map.get(class_idx, "Unknown")
        
        if code in code_to_info:
            name, desc = code_to_info[code]
        else:
            prefix = ''.join([c for c in code if c.isalpha()])
            category = gardiner_categories.get(prefix, "Unknown Category")
            name, desc = code, f"Hieroglyph in category: {category}"

        return code, name, desc, confidence
    
    except Exception as e:
        return "Error", f"Prediction Error: {str(e)}", "", 0.0

# ==============================
# Hero Section
# ==============================
st.image("https://i.pinimg.com/736x/69/d7/ab/69d7ab0e81142160f0d61d5e143fa90b.jpg",
         caption="Ancient Egyptian Hieroglyphic Inscriptions", width=300)

st.title("🌍 Egyptian Hieroglyphs Portal")
st.markdown("""
Welcome to the **Egyptian Hieroglyphs Portal** —  
A digital gateway to explore the beauty, mystery, and science of the symbols that shaped Ancient Egypt.
""")

# ==============================
# Pharaohs Section
# ==============================
st.markdown("---")
st.subheader("👑 Famous Pharaohs of Ancient Egypt")

pharaohs = {
    "Tutankhamun": (
        "https://i.pinimg.com/736x/c7/99/e6/c799e617f29aadf5f49b522968e60af6.jpg",
        "👑 Tutankhamun (King Tut, 1332–1323 BC)\n\n"
        "Tutankhamun became pharaoh at a very young age. "
        "He is famous for his intact tomb discovered in 1922 by Howard Carter, "
        "which revealed a treasure trove of Egyptian artifacts."
    ),
    "Ramses II": (
        "https://i.pinimg.com/736x/d7/73/f4/d773f41104392ba33c8fbd6b20b674a2.jpg",
        "👑 Ramses II (Ramses the Great, 1279–1213 BC)\n\n"
        "One of Egypt's most powerful and celebrated pharaohs. "
        "He led military campaigns, built many temples including Abu Simbel, "
        "and reigned for 66 years."
    ),
    "Cleopatra VII": (
        "https://i.pinimg.com/736x/dd/61/58/dd6158c88cb6ed637ffbe1a75bd408fe.jpg",
        "👑 Cleopatra VII (69–30 BC)\n\n"
        "The last active ruler of the Ptolemaic Kingdom. "
        "Known for her intelligence, political skills, and relationships with Julius Caesar and Mark Antony. "
        "She played a critical role in the final decades of Ancient Egypt."
    ),
    "Hatshepsut": (
        "https://i.pinimg.com/736x/e4/bc/4c/e4bc4c0864fedade31261ddcd1de73e2.jpg",
        "👑 Hatshepsut (1479–1458 BC)\n\n"
        "One of the most successful female pharaohs. "
        "She expanded trade networks, commissioned monumental building projects, "
        "and ruled Egypt peacefully and effectively."
    ),
    "Khufu": (
        "https://i.pinimg.com/736x/74/96/5d/74965d3d9b77c730df05ea241c841a54.jpg",
        "👑 Khufu (Cheops, 2589–2566 BC)\n\n"
        "Famous for commissioning the Great Pyramid of Giza, "
        "one of the Seven Wonders of the Ancient World. "
        "His reign was marked by major construction projects and centralized administration."
    )
}

search_pharaoh = st.text_input("🔍 Search for a Pharaoh (e.g., Tutankhamun, Ramses II):", key="pharaoh_search").strip().lower()
filtered_pharaohs = {k: v for k, v in pharaohs.items() if search_pharaoh in k.lower()} if search_pharaoh else pharaohs

cols = st.columns(3)
for idx, (name, (img, desc)) in enumerate(filtered_pharaohs.items()):
    with cols[idx % 3]:
        st.image(img, use_container_width=True)
        st.markdown(f"<h4 style='text-align:center'>{name}</h4>", unsafe_allow_html=True)
        if st.button(f"📖 Show Info for {name}", key=f"pharaoh_{idx}"):
            st.info(desc)

# ==============================
# Translator Section
# ==============================
st.markdown("---")
st.subheader("📸 Hieroglyph Translator")
st.write("Upload a photo of a hieroglyph, and our AI model will predict its meaning.")

uploaded_file = st.file_uploader("Upload a hieroglyph image", type=["jpg", "jpeg", "png"], key="file_uploader")

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Hieroglyph", use_container_width=True)
    
    # حفظ الصورة مؤقتاً
    temp_path = "temp_hieroglyph.jpg"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # عرض مؤشر التحميل
    with st.spinner("🔮 Analyzing hieroglyph..."):
        code, name, desc, confidence = predict_image(temp_path)
    
    if code != "Error":
        st.markdown(f"### 🔮 Prediction: **{name}** ({code})")
        st.markdown(f"**Confidence:** {confidence:.2%}")
        
        if st.button("📖 Show Meaning", key="meaning_btn"):
            st.info(desc)
    else:
        st.error(f"❌ {name}")

# ==============================
# Museum Gallery
# ==============================
st.markdown("---")
st.subheader("🏺 Explore the Hieroglyphic Museum")

search_gallery = st.text_input("🔍 Search for a hieroglyph (e.g., Ankh, Ra, Scarab):", key="gallery_search").strip().lower()

gallery = {
    "Ankh (☥)": ("https://i.pinimg.com/736x/9f/10/5e/9f105e86710d63371bd404b80d7cb5ae.jpg", code_to_info["N14"][1]),
    "Eye of Horus (Udjat)": ("https://i.pinimg.com/1200x/2d/bc/75/2dbc75da05593bdad03af9b27ebc42d8.jpg", code_to_info["D2"][1]),
    "Scarab": ("https://i.pinimg.com/736x/04/c5/94/04c5944110b8f438d71a158517424872.jpg", code_to_info["L1"][1]),
    "Ra (Sun God)": ("https://i.pinimg.com/736x/f8/e0/d8/f8e0d84d967b8cd6be58fe8efcf4ebbe.jpg", code_to_info["R1"][1]),
    "Djed (Pillar)": ("https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Amulette_en_forme_de_pilier_Djed_au_nom_de_Rams%C3%A8s_IX_%28Louvre%29.jpg/250px-Amulette_en_forme_de_pilier_Djed_au_nom_de_Rams%C3%A8s_IX_%28Louvre%29.jpg", code_to_info["F9"][1]),
    "Was Scepter": ("https://i.pinimg.com/736x/e3/d9/b2/e3d9b28c687102861811965dfafa5dbb.jpg", code_to_info["S40"][1]),
    "Lotus Flower": ("https://i.pinimg.com/1200x/dc/38/f6/dc38f6485aa43ae1d6a310b38f65cc83.jpg", code_to_info["M9"][1]),
    "Feather of Ma'at": ("https://i.pinimg.com/1200x/e1/d9/2d/e1d92d368338f8ee3cadcaf0e63a93b0.jpg", code_to_info["G17"][1]),
    "Crook & Flail": ("https://i.pinimg.com/736x/7c/79/74/7c7974f386ed02fdceea9dcb783e1f02.jpg", code_to_info["S42"][1]),
    "Rosetta Stone": ("https://i.pinimg.com/736x/31/b6/a6/31b6a6d00c595a086a7430065fa7f370.jpg", code_to_info["R4"][1])
}

filtered_gallery = {k: v for k, v in gallery.items() if search_gallery in k.lower()} if search_gallery else gallery

cols = st.columns(3)
for idx, (name, (path, desc)) in enumerate(filtered_gallery.items()):
    with cols[idx % 3]:
        st.image(path, use_container_width=True)
        st.markdown(f"<h4 style='text-align:center'>{name}</h4>", unsafe_allow_html=True)

        if st.button(f"📖 Show Meaning for {name}", key=f"gallery_{idx}"):
            st.info(desc)

# ==============================
# Trivia Section
# ==============================
st.markdown("---")
st.subheader("📖 Did You Know?")
st.info("""
- The **Rosetta Stone** was the key to deciphering hieroglyphs.  
- Only about **1% of Ancient Egyptians** could read and write.  
- Hieroglyphs were called **"mdw nṯr"**, meaning *words of the gods*.  
- The system used **over 700 symbols** by the Late Period.
""")

# تنظيف الملف المؤقت
if os.path.exists("temp_hieroglyph.jpg"):
    os.remove("temp_hieroglyph.jpg")












