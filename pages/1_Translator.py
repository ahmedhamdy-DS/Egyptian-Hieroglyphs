import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os
import gdown

# ===============================================
# 1. PAGE CONFIG & CSS STYLING
# ===============================================

st.set_page_config(page_title="Egyptian Hieroglyphs Portal", layout="wide")

# Function to load and inject CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the custom CSS
load_css("assets/css.css")

# ===============================================
# 2. MODEL LOADING (Your original code)
# ===============================================

# Use st.cache_resource to load the model only once
@st.cache_resource
def get_model():
    MODEL_DIR = "model"
    MODEL_FILE = "InceptionV3_model.h5"
    MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)
    
    if not os.path.exists(MODEL_PATH):
        with st.spinner("Downloading AI model for the first time..."):
            os.makedirs(MODEL_DIR, exist_ok=True)
            url = "https://huggingface.co/sonic222/Egyptian-Hieroglyphs/resolve/main/InceptionV3_model.h5"
            gdown.download(url, MODEL_PATH, quiet=False)
    
    model = load_model(MODEL_PATH)
    return model

model = get_model()

# ===============================================
# 3. DATA DICTIONARIES (Your original code)
# ===============================================

label_map = {
    # A: Man and his Occupations
    0: "A1",    # Man, Seated
    1: "A2",    # Man with Hand to Mouth
    2: "A13",   # Man with a Stick
    3: "A17",   # Child, Seated
    4: "A21",   # Man Striking
    5: "A40",   # God, Seated

    # B: Woman and her Occupations
    6: "B1",    # Woman, Seated
    7: "B3",    # Pregnant Woman
    8: "B7",    # Woman Nursing Child

    # C: Anthropomorphic Deities
    9: "C1",    # Osiris, Seated
    10: "C2",   # Ptah, Seated
    11: "C3",   # Ra with Falcon Head

    # D: Parts of the Human Body
    12: "D1",   # Head in Profile
    13: "D2",   # Eye of Horus (Udjat)
    14: "D4",   # Human Eye
    15: "D10",  # Pupil of the Eye
    16: "D21",  # Mouth
    17: "D36",  # Forearm
    18: "D46",  # Hand
    19: "D58",  # Leg and Foot

    # E: Mammals
    20: "E1",   # Bull
    21: "E6",   # Calf
    22: "E9",   # Lion, Recumbent
    23: "E23",  # Jackal (Anubis)
    24: "E34",  # Hare

    # F: Parts of Mammals
    25: "F9",   # Djed Pillar
    26: "F13",  # Horn
    27: "F20",  # Tongue of an Ox
    28: "F31",  # Animal Hide
    29: "F35",  # Heart

    # G: Birds
    30: "G1",   # Egyptian Vulture
    31: "G5",   # Falcon (Horus)
    32: "G17",  # Owl
    33: "G25",  # Quail Chick, standing
    34: "G39",  # Duck
    35: "G43",  # Quail Chick

    # H: Parts of Birds
    36: "H6",   # Feather of Ma'at

    # I: Amphibious Animals, Reptiles
    37: "I9",   # Cobra (Uraeus)
    38: "I10",  # Horned Viper
    39: "I12",  # Tadpole

    # K: Fish and Parts of Fish
    40: "K1",   # Tilapia Fish
    41: "K5",   # Catfish

    # L: Invertebrata and Lesser Animals
    42: "L1",   # Scarab Beetle (Kheper)
    43: "L2",   # Bee

    # M: Trees and Plants
    44: "M1",   # Papyrus Clump
    45: "M8",   # Lotus Flower on a Long Stem
    46: "M9",   # Lotus Flower (Same as M8, but often used)
    47: "M17",  # Reed Leaf
    48: "M23",  # Sedge Plant

    # N: Sky, Earth, Water
    49: "N1",   # Sky
    50: "N5",   # Sun (Ra)
    51: "N14",  # Ankh
    52: "N17",  # Land, Flat Alluvial
    53: "N23",  # Irrigation Canal
    54: "N25",  # Hill Country or Desert
    55: "N29",  # Hill or Slope
    56: "N35",  # Water (Ripple)

    # O: Buildings and Parts of Buildings
    57: "O1",   # House or Building
    58: "O4",   # Courtyard
    59: "O28",  # Pyramid
    60: "O34",  # Gate or Door
    61: "O42",  # Shrine

    # P: Ships and Parts of Ships
    62: "P1",   # Boat on Water
    63: "P5",   # Sail

    # Q: Domestic and Funerary Furniture
    64: "Q1",   # Seat or Stool
    65: "Q3",   # Throne or Chair
    66: "Q6",   # Headrest

    # R: Temple Furniture and Sacred Emblems
    67: "R1",   # Ra (Sun God) - Note: Often represented by N5
    68: "R4",   # Offering Table
    69: "R8",   # Standard of a God (Neter)
    70: "R11",  # Was Scepter
    71: "R12",  # Shen Ring

    # S: Crowns, Dress, Staves
    72: "S1",   # White Crown (Hedjet)
    73: "S3",   # Red Crown (Deshret)
    74: "S5",   # Double Crown (Pschent)
    75: "S29",  # Folded Cloth
    76: "S34",  # Sandal
    77: "S40",  # Was Scepter
    78: "S42",  # Crook & Flail

    # T: Warfare, Hunting, Butchery
    79: "T3",   # Mace (Hedj)
    80: "T7",   # Bow
    81: "T11",  # Arrow
    82: "T14",  # Dagger

    # U: Agriculture, Crafts, Professions
    83: "U1",   # Sickle
    84: "U6",   # Hoe
    85: "U13",  # Plough
    86: "U23",  # Adze
    87: "U30",  # Kiln

    # V: Rope, Fiber, Baskets
    88: "V1",   # Coil of Rope
    89: "V13",  # Wick of Twisted Flax
    90: "V28",  # Flax / Rope
    91: "V30",  # Basket
    92: "V31",  # Basket with Handle

    # W: Vessels of Stone and Earthenware
    93: "W9",   # Alabaster Basin
    94: "W11",  # Cup
    95: "W24",  # Water Pot

    # X: Loaves and Cakes
    96: "X1",   # Bread Loaf
    97: "X4",   # Offering Slice of Bread
    98: "X8",   # Offering Cake on a Mat

    # Y: Writings, Games, Music
    99: "Y1",   # Papyrus Scroll, Tied
    100: "Y5",  # Scribe's Kit

    # Z: Strokes, Geometrical Figures
    101: "Z1",  # Single Stroke
    102: "Z2",  # Plural Strokes
    103: "Z4",  # Diagonal Strokes
    104: "Z7",  # Enclosure

    # Aa: Unclassified
    105: "Aa1", # Pedestal or Support
    106: "Aa11",# Heart and Windpipe (Nefer)
    107: "Aa15",# Spine and Ribs
}

gardiner_categories = {
    "A": "Man and his occupations", "B": "Woman and her occupations", "C": "Anthropomorphic deities",
    "D": "Parts of the human body", "E": "Mammals", "F": "Parts of mammals", "G": "Birds",
    "H": "Parts of birds", "I": "Amphibious animals, reptiles", "K": "Fish and parts of fish",
    "L": "Invertebrates and small plants", "M": "Trees and plants", "N": "Sky, earth, water",
    "O": "Buildings, parts of buildings", "P": "Domestic and funerary furniture", "Q": "Vessels of stone and earthenware",
    "R": "Temple furniture and sacred emblems", "S": "Crowns, dress, staves, weapons", "T": "Warfare, hunting, butchery",
    "U": "Agriculture, crafts, professions", "V": "Rope, fiber, baskets, bags", "W": "Vessels of wood, stone, metal",
    "X": "Loaves, cakes, offerings", "Y": "Writing, games, music", "Z": "Strokes, signs, geometrical figures",
    "Aa": "Unclassified signs"
}

code_to_info = {
    # ===============================================
    # A: Man and his Occupations
    # ===============================================
    "A1": ("Man, Seated ( determinaive for 'I', 'man')", "📖 Meaning: Represents a man and is used as a determinative for words related to men, their roles (like 'father' or 'priest'), and personal names. It signifies identity and humanity."),
    "A2": ("Man with Hand to Mouth", "📖 Meaning: A determinative for actions involving the mouth, such as eating, drinking, speaking, and thinking. It visualizes the source of sensory input and expression."),
    "A13": ("Man with a Stick", "📖 Meaning: Represents a man of authority or an elder. Used as a determinative for officials, nobles, and respected figures, symbolizing leadership and social standing."),
    "A17": ("Child, Seated with Finger to Mouth", "📖 Meaning: Represents a child, youth, or heir. The finger-to-mouth gesture was a conventional sign of childhood in ancient Egyptian art. It signifies youthfulness and lineage."),
    "A21": ("Man Striking with a Stick", "📖 Meaning: A determinative for words involving effort, strength, or violence. It conveys the idea of power, control, and forceful action, often used in contexts of command or labor."),
    "A40": ("God, Seated", "📖 Meaning: Represents a deity. This sign is used as a determinative for the names of gods, indicating divine status. The seated posture denotes authority and presence."),

    # ===============================================
    # B: Woman and her Occupations
    # ===============================================
    "B1": ("Woman, Seated", "📖 Meaning: The counterpart to A1, this is the determinative for 'woman' and related concepts like 'mother', 'wife', or 'goddess'. It signifies femininity and female identity."),
    "B3": ("Pregnant Woman", "📖 Meaning: Used as a determinative for words related to pregnancy, conception, and childbirth. It is a clear symbol of creation, fertility, and the continuation of life."),
    "B7": ("Woman Nursing a Child", "📖 Meaning: A determinative for words like 'nurse' or 'guardian'. It symbolizes nourishment, care, and the maternal bond, highlighting the protective role of women."),

    # ===============================================
    # C: Anthropomorphic Deities
    # ===============================================
    "C1": ("Osiris, Seated", "📖 Meaning: Represents Osiris, the god of the afterlife, resurrection, and fertility. He is typically shown mummified, holding the crook and flail, symbols of divine authority and kingship."),
    "C2": ("Ptah, Seated in a Shrine", "📖 Meaning: Represents Ptah, the creator god of Memphis, patron of craftsmen. He is shown as a mummified man holding a scepter, symbolizing his role in creation and craftsmanship."),
    "C3": ("Ra with Falcon Head and Sun-Disk", "📖 Meaning: Represents Ra (or Re), the ancient Egyptian sun god. The falcon head and solar disk symbolize his celestial power, sovereignty, and role as the creator of the world."),

    # ===============================================
    # D: Parts of the Human Body
    # ===============================================
    "D1": ("Head in Profile", "📖 Meaning: Represents the concept of 'head' and is used phonetically for the sound *tp*. It signifies the top, chief, or beginning of something, embodying leadership and primacy."),
    "D2": ("Eye of Horus (Udjat)", "📖 Meaning: Symbol of protection, health, and healing. Named after the myth where Horus lost his eye fighting Seth. Widely used as a powerful amulet to ward off evil."),
    "D4": ("Human Eye (👁️)", "📖 Meaning: Represents the eye and the act of seeing. It is used as a determinative for words related to sight, looking, and observation. Phonetically, it stands for the sound *iri*."),
    "D10": ("Pupil of the Eye", "📖 Meaning: A determinative for the pupil, or the center of something. It signifies focus, precision, and the core of an issue."),
    "D21": ("Mouth (👄)", "📖 Meaning: Represents the mouth and is used as a phonetic sign for the sound *r*. It is one of the most common uniliteral (single-sound) signs in the hieroglyphic alphabet."),
    "D36": ("Forearm (ꜥ)", "📖 Meaning: A phonetic sign for the sound *ꜥ* (ayin). It represents the forearm and actions performed with it, such as working or giving."),
    "D46": ("Hand (✋)", "📖 Meaning: A phonetic sign for the sound *d*. It represents the hand and is used in words related to actions, giving, and taking."),
    "D58": ("Leg and Foot (🦶)", "📖 Meaning: A phonetic sign for the sound *b*. It is used as a determinative for words related to walking, movement, and place."),

    # ===============================================
    # E: Mammals
    # ===============================================
    "E1": ("Bull (🐂)", "📖 Meaning: Represents strength, power, and fertility. The bull was a symbol of the pharaoh's might and was associated with several gods, including Apis and Mnevis."),
    "E6": ("Calf", "📖 Meaning: A phonetic sign for the sound *iw*. It symbolizes youth, innocence, and potential."),
    "E9": ("Lion, Recumbent (🦁)", "📖 Meaning: A phonetic sign for the sound *rw*. The lion symbolized royalty, power, and ferocity, often guarding temples and tombs."),
    "E23": ("Jackal, Seated (Anubis)", "📖 Meaning: Represents the jackal god Anubis, who presided over mummification and the afterlife. The sign is a determinative for jackals and deities associated with the dead."),
    "E34": ("Hare (🐇)", "📖 Meaning: A phonetic sign for *wn* (wen). The hare was associated with speed, keen senses, and the concept of 'to exist' or 'to be'."),

    # ===============================================
    # F: Parts of Mammals
    # ===============================================
    "F9": ("Djed Pillar", "📖 Meaning: Symbol of stability and endurance. Originally representing the backbone of the god Osiris, it came to signify the eternal and unchanging aspects of the universe."),
    "F13": ("Horn ( horns)", "📖 Meaning: A phonetic sign for *db*. Horns symbolized power, divinity, and protection in ancient Egypt."),
    "F20": ("Tongue of an Ox", "📖 Meaning: Represents the tongue and is a determinative for words related to taste and speech. Phonetically, it represents the sound *ns*."),
    "F31": ("Animal Hide", "📖 Meaning: Represents leather, skin, and hides. It is also used phonetically for the sound *ꜣb*."),
    "F35": ("Heart (❤️)", "📖 Meaning: Symbol of life, intelligence, and emotion. The Egyptians believed the heart was the seat of the mind and would be weighed against the feather of Ma'at in the afterlife."),

    # ===============================================
    # G: Birds
    # ===============================================
    "G1": ("Egyptian Vulture (Vulture  vultures)", "📖 Meaning: A phonetic sign for the sound *ꜣ* (aleph). It is one of the foundational letters of the Egyptian alphabet."),
    "G5": ("Falcon (Horus)", "📖 Meaning: Represents the god Horus, a primary deity associated with the sky, kingship, and protection. The falcon symbolized divine power and royalty."),
    "G17": ("Owl (🦉)", "📖 Meaning: A phonetic sign for the sound *m*. This common uniliteral sign is often seen in the words for 'in', 'with', and 'from'."),
    "G25": ("Quail Chick, standing", "📖 Meaning: Represents a quail chick. It is used as a determinative for young birds."),
    "G39": ("Duck", "📖 Meaning: Represents a pintail duck and is used as a generic determinative for birds. It also appears in the phrase *sꜣ rꜥ* ('Son of Ra'), a core part of the pharaoh's royal titulary."),
    "G43": ("Quail Chick (🐥)", "📖 Meaning: A phonetic sign for the sound *w*. It is another of the most common uniliteral signs in the Egyptian alphabet."),

    # ===============================================
    # H: Parts of Birds
    # ===============================================
    "H6": ("Feather of Ma'at (🪶)", "📖 Meaning: Symbol of truth, justice, balance, and cosmic order. In the judgment of the dead, the deceased's heart was weighed against this feather. If the heart was lighter, they achieved eternal life."),

    # ===============================================
    # I: Amphibious Animals, Reptiles
    # ===============================================
    "I9": ("Cobra (Uraeus) (🐍)", "📖 Meaning: The Uraeus is a symbol of royalty, divinity, and divine authority. Worn on the pharaoh's brow, it was believed to protect them by spitting fire at their enemies."),
    "I10": ("Horned Viper (🐍)", "📖 Meaning: A phonetic sign for the sound *f*. It represents the horned viper, a snake native to the Egyptian desert."),
    "I12": ("Tadpole (🐸)", "📖 Meaning: Represents the number 100,000. Due to the vast number of tadpoles that appeared in the Nile, it became a symbol for a huge, uncountable quantity."),

    # ===============================================
    # K: Fish and Parts of Fish
    # ===============================
    "K1": ("Tilapia Fish (🐟)", "📖 Meaning: Associated with fertility, rebirth, and the sun. The tilapia was observed carrying its eggs in its mouth, which Egyptians connected to self-creation."),
    "K5": ("Catfish", "📖 Meaning: A phonetic sign for *nꜥr*. The catfish was a common fish in the Nile and a source of food."),

    # ===============================================
    # L: Invertebrata and Lesser Animals
    # ===============================================
    "L1": ("Scarab Beetle (Kheper)", "📖 Meaning: Symbol of creation, renewal, and rebirth. The beetle rolling a ball of dung was seen as an earthly parallel to the sun god Ra rolling the sun across the sky each day."),
    "L2": ("Bee (🐝)", "📖 Meaning: Symbolized the King of Lower Egypt (*bjt*). It was also associated with royalty, diligence, and the production of honey, a valuable commodity."),

    # ===============================================
    # M: Trees and Plants
    # ===============================================
    "M1": ("Papyrus Clump", "📖 Meaning: Symbolized the land of Lower Egypt (the Nile Delta). Papyrus was a vital resource, used for everything from writing material to building boats."),
    "M8": ("Lotus Flower on a Long Stem", "📖 Meaning: A phonetic sign for *sšn*. The lotus symbolized creation, rebirth, and purity. It closes at night and opens in the morning, mirroring the cycle of the sun."),
    "M17": ("Reed Leaf (🌱)", "📖 Meaning: A phonetic sign for the sound *j* or *i*. It is one of the most common single-sound signs and often used as the pronoun 'I'."),
    "M23": ("Sedge Plant", "📖 Meaning: Symbolized the land of Upper Egypt. This sign was part of the *nsw-bjt* title, representing the pharaoh's rule over a unified 'Two Lands' of Upper and Lower Egypt."),

    # ===============================================
    # N: Sky, Earth, Water
    # ===============================================
    "N1": ("Sky Petal", "📖 Meaning: Represents the sky or heavens. As a determinative, it is used in words like 'sky', 'night', and 'rain'. It depicts the sky as a solid ceiling held up over the earth."),
    "N5": ("Sun (Ra) (☀️)", "📖 Meaning: Represents the sun and the god Ra. It is a determinative for words related to the sun, light, and time (e.g., 'day'). It is central to Egyptian cosmology and religion."),
    "N14": ("Ankh (☥)", "📖 Meaning: Symbol of eternal life, often simply translated as 'life'. Ancient Egyptians carried it in statues and inscriptions as a sign of immortality and divine protection."),
    "N17": ("Land, Flat Alluvial", "📖 Meaning: A determinative for 'land' or 'earth'. It represents a flat piece of fertile land, crucial for agriculture along the Nile."),
    "N23": ("Irrigation Canal", "📖 Meaning: Represents a channel or canal, and is used phonetically for the sound *mr* (as in 'pyramid'). It signifies the managed landscape of Egypt."),
    "N25": ("Hill Country or Desert", "📖 Meaning: Represents foreign lands, the desert, or hilly terrain outside the fertile Nile valley. It is a determinative for places considered 'other' than Egypt."),
    "N29": ("Hill or Slope", "📖 Meaning: A phonetic sign for the sound *q*. It represents an incline or a slope."),
    "N35": ("Water (Ripple)", "📖 Meaning: A phonetic sign for the sound *n*. As a determinative, three of these signs represent 'water' or 'lake', symbolizing the life-giving Nile."),

    # ===============================================
    # O: Buildings and Parts of Buildings
    # ===============================================
    "O1": ("House or Building (🏠)", "📖 Meaning: A determinative for 'house', 'temple', or 'palace'. Phonetically, it stands for *pr* (per), meaning 'house'."),
    "O4": ("Courtyard", "📖 Meaning: A phonetic sign for *h*. It represents a rectangular courtyard or enclosure as seen from above."),
    "O28": ("Pyramid (△)", "📖 Meaning: Represents a pyramid or tomb. It is a determinative for such structures and related concepts."),
    "O34": ("Gate or Door", "📖 Meaning: A phonetic sign for *s*. It represents a door bolt, and by extension, security and passage."),
    "O42": ("Shrine", "📖 Meaning: Represents a shrine or sacred enclosure. It is a determinative for holy places and temples."),

    # ===============================================
    # P: Ships and Parts of Ships
    # ===============================================
    "P1": ("Boat on Water (⛵)", "📖 Meaning: A determinative for boats, ships, and the act of traveling by water. Boats were essential for transport, trade, and religious processions on the Nile."),
    "P5": ("Sail", "📖 Meaning: Represents a sail and is used phonetically for the sound *nfw*. It signifies wind, breath, and air."),

    # ===============================================
    # Q: Domestic and Funerary Furniture
    # ===============================================
    "Q1": ("Seat or Stool", "📖 Meaning: A phonetic sign for *p*. It represents a simple reed stool, a common piece of furniture."),
    "Q3": ("Throne or Chair", "📖 Meaning: Represents a throne and is a determinative for 'seat'. Phonetically, it stands for *ws*."),
    "Q6": ("Headrest", "📖 Meaning: Represents a headrest, a common funerary item placed in tombs to support the deceased's head, magically protecting them in the afterlife."),

    # ===============================================
    # R: Temple Furniture and Sacred Emblems
    # ===============================================
    "R4": ("Offering Table", "📖 Meaning: Represents a table with loaves of bread, symbolizing an offering. It is used as a determinative for 'offering' and the phonetic value *ḥtp* (hetep), meaning 'peace' or 'to be satisfied'."),
    "R8": ("Standard of a God (Neter)", "📖 Meaning: Represents divinity. The flag-like symbol is a determinative for the word 'god' (*nṯr*) and for the names of specific deities."),
    "R11": ("Was Scepter", "📖 Meaning: Symbol of power, control, and dominion. Frequently shown in the hands of kings and gods as a tool of cosmic authority and a sign of their divine power."),
    "R12": ("Shen Ring", "📖 Meaning: A circle of rope representing eternity and protection. The cartouche, which encircled royal names, was an elongated version of the Shen ring, offering eternal protection to the pharaoh's name."),
    "R1": ("Ra (Sun God)", "📖 Meaning: The Sun God and one of the greatest deities of Egypt. Represents creation, light, and warmth. Often depicted with a falcon head and a solar disk."),
    # ===============================================
    # S: Crowns, Dress, Staves
    # ===============================================
    "S1": ("White Crown (Hedjet)", "📖 Meaning: The crown of Upper Egypt (southern Egypt). It symbolized the pharaoh's rule over this region."),
    "S3": ("Red Crown (Deshret)", "📖 Meaning: The crown of Lower Egypt (the northern Nile Delta). It symbolized the pharaoh's rule over this region."),
    "S5": ("Double Crown (Pschent)", "📖 Meaning: The combined White and Red Crowns, symbolizing the unification of Upper and Lower Egypt and the pharaoh's rule over the entire country."),
    "S29": ("Folded Cloth", "📖 Meaning: A phonetic sign for the sound *s*. It represents a folded piece of linen, a key textile in ancient Egypt."),
    "S34": ("Sandal (🩴)", "📖 Meaning: A phonetic sign for *b*. Sandals were a sign of status, and the right to wear them was often restricted to royalty and high officials."),
    "S40": ("Was Scepter", "📖 Meaning: Symbol of power, control, and dominion. Frequently shown in the hands of kings and gods as a tool of cosmic authority."),
    "S42": ("Crook & Flail", "📖 Meaning: Royal authority symbols. The crook represents care and guardianship (the king as shepherd), while the flail represents discipline and the fertility of the land."),

    # ===============================================
    # T: Warfare, Hunting, Butchery
    # ===============================================
    "T3": ("Mace (Hedj)", "📖 Meaning: A pear-shaped mace, symbolizing power and authority. It was an early symbol of kingship and appears on some of the oldest artifacts, like the Narmer Palette."),
    "T7": ("Bow", "📖 Meaning: Represents a bow and is a determinative for words related to archery, warfare, and foreign peoples (who were often depicted as archers)."),
    "T11": ("Arrow (→)", "📖 Meaning: Represents an arrow and is a determinative for words related to shooting and projectiles."),
    "T14": ("Dagger", "📖 Meaning: Represents a dagger or knife. It is a determinative for sharp objects and cutting."),

    # ===============================================
    # U: Agriculture, Crafts, Professions
    # ===============================================
    "U1": ("Sickle", "📖 Meaning: A phonetic sign for *mꜣ*. It represents a sickle used for harvesting grain, a fundamental activity for Egyptian civilization."),
    "U6": ("Hoe", "📖 Meaning: A phonetic sign for *mr*. The hoe was an essential tool for breaking up earth and preparing fields for planting."),
    "U13": ("Plough", "📖 Meaning: Represents a plough and is a determinative for 'ploughing' and 'cultivating'."),
    "U23": ("Adze", "📖 Meaning: A woodworking tool, used as a determinative for 'carpenter' and 'craft'. It was also used in the 'Opening of the Mouth' ceremony to reanimate the deceased."),
    "U30": ("Kiln", "📖 Meaning: Represents a potter's kiln and is used phonetically for *tꜣ*. It signifies heat, baking, and creation."),

    # ===============================================
    # V: Rope, Fiber, Baskets
    # ===============================================
    "V1": ("Coil of Rope", "📖 Meaning: Represents a coil of rope and is a phonetic sign for the number 100."),
    "V13": ("Wick of Twisted Flax", "📖 Meaning: A phonetic sign for the sound *h*. It represents the wick of an oil lamp."),
    "V28": ("Flax / Rope", "📖 Meaning: A phonetic sign for the sound *ḥ*. It represents a hank of flax fiber, crucial for making linen and rope."),
    "V30": ("Basket", "📖 Meaning: A phonetic sign for the sound *k*. It represents a simple basket."),
    "V31": ("Basket with Handle", "📖 Meaning: A phonetic sign for the sound *nb*. It means 'lord' or 'master' and is also used for the word 'all'."),

    # ===============================================
    # W: Vessels of Stone and Earthenware
    # ===============================================
    "W9": ("Alabaster Basin", "📖 Meaning: Represents a ceremonial basin and is used phonetically for *ḥb*, as in *ḥb-sd* (Heb Sed festival)."),
    "W11": ("Cup", "📖 Meaning: A phonetic sign for *ḥnt*. It represents a small stone or ceramic cup."),
    "W24": ("Water Pot", "📖 Meaning: A phonetic sign for *nw*. When repeated three times, it can stand for the primordial waters of 'Nu' or 'Nun'."),

    # ===============================================
    # X: Loaves and Cakes
    # ===============================================
    "X1": ("Bread Loaf", "📖 Meaning: A phonetic sign for the sound *t*. It also serves as a determinative for bread and offerings."),
    "X4": ("Offering Slice of Bread", "📖 Meaning: A phonetic sign for *d*. It often appears in the offering formula 'hetep-di-nesu' ('an offering which the king gives')."),
    "X8": ("Offering Cake on a Mat", "📖 Meaning: Represents an offering and is the phonetic sign for *ḥtp* (hetep), meaning 'peace', 'offering', or 'to be content'."),

    # ===============================================
    # Y: Writings, Games, Music
    # ===============================================
    "Y1": ("Papyrus Scroll, Tied", "📖 Meaning: A determinative for abstract concepts, writing, and documents. It signifies knowledge, records, and the intellectual world."),
    "Y5": ("Scribe's Kit", "📖 Meaning: Represents the tools of a scribe (palette, water pot, and reed pens). It is a determinative for 'scribe', 'writing', and 'to write'."),

    # ===============================================
    # Z: Strokes, Geometrical Figures
    # ===============================================
    "Z1": ("Single Stroke", "📖 Meaning: A determinative used to indicate that a sign should be read for its literal meaning (logogram) rather than its phonetic sound."),
    "Z2": ("Plural Strokes", "📖 Meaning: Three vertical strokes used to indicate the plural form of a noun. It transforms a singular concept into a multiple one (e.g., 'god' becomes 'gods')."),
    "Z4": ("Diagonal Strokes", "📖 Meaning: A determinative used for dual nouns (indicating two of something) and sometimes as a phonetic complement."),
    "Z7": ("Enclosure", "📖 Meaning: Represents an enclosure, like a town or a fortified area. Often seen in the names of cities."),

    # ===============================================
    # Aa: Unclassified
    # ===============================================
    "Aa1": ("Pedestal or Support", "📖 Meaning: A phonetic sign for *mꜣꜥ* (as in Ma'at). It represents a pedestal or support, symbolizing foundation, stability, and order."),
    "Aa11": ("Heart and Windpipe", "📖 Meaning: A phonetic sign for *nfr* (nefer), meaning 'beautiful', 'good', or 'perfect'. It is one of the most recognizable and positive symbols in Egyptian writing."),
    "Aa15": ("Spine and Ribs", "📖 Meaning: Represents the back or spine. Used as a determinative for words related to the back."),
}
# ===============================================
# 4. HELPER FUNCTION (Your original code)
# ===============================================

def predict_image(img_path):
    """
    Analyzes a hieroglyph image and returns its identification, description, and confidence.
    
    This function implements a robust fallback system:
    1. Tries to find a specific symbol match in `code_to_info`.
    2. If not found, it uses the symbol's Gardiner code prefix to identify its category.
    3. If the category or code is completely unknown, it returns a "Mystery Symbol" message.
    """
    try:
        # 1. Preprocess the image for the model
        img = load_img(img_path, target_size=(299, 299))
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # 2. Get AI model's prediction
        preds = model.predict(img_array, verbose=0)
        class_idx = np.argmax(preds)
        confidence = np.max(preds)
        
        # 3. Map prediction index to a Gardiner code
        code = label_map.get(class_idx)

        # 4. Determine the symbol's name and description with fallbacks
        if code and code in code_to_info:
            # Case 1: Perfect Match - The symbol is fully recognized.
            name, desc = code_to_info[code]
        
        elif code:
            # Case 2: Category Match - The symbol's code is valid but not in our detailed list.
            # We infer its meaning from the general Gardiner category.
            prefix = ''.join(filter(str.isalpha, code))
            category = gardiner_categories.get(prefix)
            
            if category:
                name = code  # Display the code itself as the name
                desc = f"📖 Meaning: A hieroglyph from the '{category}' category. While this specific symbol is not in our detailed database, it belongs to signs representing '{category.lower()}'."
            else:
                # Fallback 1: The code's prefix is not a known Gardiner category.
                name = "Mystery Symbol"
                code = "Unclassified"
                desc = "📖 Meaning: A rare or unclassified hieroglyph. Its category is not recognized in the standard Gardiner system."
        
        else:
            # Fallback 2: The model's output doesn't map to any known hieroglyph code.
            name = "Mystery Symbol"
            code = "Unknown"
            desc = "📖 Meaning: A rare or unidentified hieroglyph from ancient Egypt. Our AI could not match it to a known symbol."
            
        return code, name, desc, confidence
    
    except Exception as e:
        # General error handling for issues like corrupted image files
        return "Error", f"Prediction Error: {str(e)}", "", 0.0

# ===============================================
# 5. UI LAYOUT & SECTIONS
# ===============================================

# Main container to center the content
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- HERO SECTION ---
st.title(" Egyptian Hieroglyphs Portal")
st.markdown("""
Welcome to the **Egyptian Hieroglyphs Portal** —  
A digital gateway to explore the beauty, mystery, and science of the symbols that shaped Ancient Egypt.
""")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


import os
from PIL import Image

# --- PHARAOHS SECTION ---
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("👑 Famous Pharaohs of Ancient Egypt")

pharaohs = {
    "Tutankhamun": ("assets/c799e617f29aadf5f49b522968e60af6.jpg", "👑 Tutankhamun (King Tut, 1332–1323 BC)\n\nTutankhamun became pharaoh at a very young age. He is famous for his intact tomb discovered in 1922 by Howard Carter, which revealed a treasure trove of Egyptian artifacts."),
    "Ramses II": ("assets/d773f41104392ba33c8fbd6b20b674a2.jpg", "👑 Ramses II (Ramses the Great, 1279–1213 BC)\n\nOne of Egypt's most powerful and celebrated pharaohs. He led military campaigns, built many temples including Abu Simbel, and reigned for 66 years."),
    "Cleopatra VII": ("assets/dd6158c88cb6ed637ffbe1a75bd408fe.jpg", "👑 Cleopatra VII (69–30 BC)\n\nThe last active ruler of the Ptolemaic Kingdom. Known for her intelligence, political skills, and relationships with Julius Caesar and Mark Antony. She played a critical role in the final decades of Ancient Egypt."),
    "Hatshepsut": ("assets/944d5d3f2aa155d76159ba6cb6a856ee.jpg", "👑 Hatshepsut (1479–1458 BC)\n\nOne of the most successful female pharaohs. She expanded trade networks, commissioned monumental building projects, and ruled Egypt peacefully and effectively."),
    "Khufu": ("assets/74965d3d9b77c730df05ea241c841a54.jpg", "👑 Khufu (Cheops, 2589–2566 BC)\n\nFamous for commissioning the Great Pyramid of Giza, one of the Seven Wonders of the Ancient World. His reign was marked by major construction projects and centralized administration.")
}
import os
from PIL import Image

# ... (الكود السابق: التعريفات وقاموس الفراعنة) ...

# شريط البحث
search_pharaoh = st.text_input("🔍 Search for a Pharaoh (e.g., Tutankhamun, Ramses II):", key="pharaoh_search").strip().lower()
filtered_pharaohs = {k: v for k, v in pharaohs.items() if search_pharaoh in k.lower()} if search_pharaoh else pharaohs
cols = st.columns(3)

for idx, (name, (img_path, desc)) in enumerate(filtered_pharaohs.items()):
    with cols[idx % 3]:

        # -----------------------------
        # 1️⃣ التحقق من مسار الصورة
        # -----------------------------
        if not isinstance(img_path, str) or img_path.strip() == "":
            st.warning(f"⚠️ No image defined for {name}")
            st.markdown(f"<h4 style='text-align:center'>{name}</h4>", unsafe_allow_html=True)
            with st.expander(f"📖 Read about {name}"):
                st.info(desc)
            continue

        # -----------------------------
        # 2️⃣ محاولة تحميل الصورة بأمان
        # -----------------------------
        image_obj = None

        possible_paths = [
            img_path,                            # assets/xxx.jpg
            os.path.join("assets", os.path.basename(img_path)),  # تأمين إضافي
            os.path.join("..", img_path),        # عند التشغيل من pages
        ]

        for path in possible_paths:
            if os.path.isfile(path):
                try:
                    image_obj = Image.open(path)
                    image_obj = image_obj.convert("RGB")  # مهم جدًا
                    break
                except Exception as e:
                    image_obj = None

        # -----------------------------
        # 3️⃣ العرض الآمن
        # -----------------------------
        if image_obj is not None:
            st.image(image_obj, use_column_width=True)
        else:
            st.warning(f"⚠️ Image not found for {name}")

        st.markdown(f"<h4 style='text-align:center'>{name}</h4>", unsafe_allow_html=True)

        with st.expander(f"📖 Read about {name}"):
            st.info(desc)


# --- TRANSLATOR SECTION ---
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("📸 AI Hieroglyph Translator")
st.write("Upload a photo of a hieroglyph, and our AI model will predict its meaning.")

uploaded_file = st.file_uploader("Upload a hieroglyph image", type=["jpg", "jpeg", "png"], key="file_uploader", label_visibility="collapsed")

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Hieroglyph", use_column_width=True)
    temp_path = "temp_hieroglyph.jpg"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner("🔮 Analyzing hieroglyph..."):
        code, name, desc, confidence = predict_image(temp_path)
    
    if code != "Error":
        st.markdown(f"### 🔮 Prediction: **{name}** ({code})")
        st.progress(int(confidence * 100))
        st.markdown(f"**Confidence:** {confidence:.2%}")
        st.info(desc)
    else:
        st.error(f"❌ {name}")
st.markdown('</div>', unsafe_allow_html=True)


# --- MUSEUM GALLERY SECTION ---
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("🏺 Explore the Hieroglyphic Museum")

gallery = {
    "Ankh (☥)": ("assets/Ankh.jpg", code_to_info["N14"][1]),
    "Eye of Horus (Udjat)": ("assets/Eye_of_Horus.jpg", code_to_info["D2"][1]),
    "Scarab": ("assets/scarab.jpg", code_to_info["L1"][1]),
    "Ra (Sun God)": ("assets/Ra.jpg", code_to_info["R1"][1]),
    "Djed (Pillar)": ("assets/djed.jpg", code_to_info["F9"][1]),
    "Was Scepter": ("assets/was.jpg", code_to_info["S40"][1])
}

search_gallery = st.text_input(
    "🔍 Search for a hieroglyph (e.g., Ankh, Ra, Scarab):",
    key="gallery_search"
).strip().lower()

filtered_gallery = {
    k: v for k, v in gallery.items()
    if search_gallery in k.lower()
} if search_gallery else gallery

import os
from PIL import Image

cols = st.columns(3)

for idx, (name, (path, desc)) in enumerate(filtered_gallery.items()):
    with cols[idx % 3]:

        # عرض الصورة بشكل آمن
        if isinstance(path, str) and os.path.isfile(path):
            try:
                img = Image.open(path).convert("RGB")
                st.image(img, use_column_width=True)
            except Exception:
                st.warning("⚠️ Failed to load image")
        else:
            st.warning("⚠️ Image not found")

        st.markdown(
            f"<h4 style='text-align:center'>{name}</h4>",
            unsafe_allow_html=True
        )

        if st.button(
            f"📖 Show Meaning for {name}",
            key=f"gallery_{idx}"
        ):
            st.info(desc)

st.markdown('</div>', unsafe_allow_html=True)

# --- TRIVIA SECTION ---
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("📖 Did You Know?")
st.info("""
- The **Rosetta Stone** was the key to deciphering hieroglyphs.
- Only about **1% of Ancient Egyptians** could read and write.
- Hieroglyphs were called **"mdw nṯr"**, meaning *words of the gods*.
- The system used **over 700 symbols** by the Late Period.
""")
st.markdown('</div>', unsafe_allow_html=True)

# Close the main container
st.markdown('</div>', unsafe_allow_html=True)

# --- CLEANUP (Your original code) ---
if os.path.exists("temp_hieroglyph.jpg"):
    os.remove("temp_hieroglyph.jpg")


