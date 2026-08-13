"""Tulana Studio — configuration and human-readable naming."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = Path(os.environ.get("TULANA_DATA_DIR", BASE_DIR / "data")).resolve()
STATE_DIR = Path(os.environ.get("TULANA_STATE_DIR", BASE_DIR / "state")).resolve()
DB_PATH = Path(os.environ.get("TULANA_DB", STATE_DIR / "studio.db")).resolve()
CROP_DIR = Path(os.environ.get("TULANA_CROPS", STATE_DIR / "crops")).resolve()
EXPORT_DIR = Path(os.environ.get("TULANA_EXPORTS", STATE_DIR / "exports")).resolve()
PAGE_CACHE = Path(os.environ.get("TULANA_PAGES", STATE_DIR / "pages")).resolve()
for d in (STATE_DIR, CROP_DIR, EXPORT_DIR, PAGE_CACHE):
    d.mkdir(parents=True, exist_ok=True)

HOST = os.environ.get("TULANA_HOST", "0.0.0.0")
PORT = int(os.environ.get("TULANA_PORT", "7862"))

# Rendering. Pages are served at VIEW_DPI for reading; crops are re-rendered
# from the source PDF at CROP_DPI so a clipping is publication quality rather
# than an upscale of what happened to be on screen.
VIEW_DPI = int(os.environ.get("TULANA_VIEW_DPI", "110"))
CROP_DPI = int(os.environ.get("TULANA_CROP_DPI", "300"))

BOARDS = {
    "NCERT": "NCERT / CBSE", "MH": "Maharashtra State Board",
    "PB": "Punjab School Education Board", "GJ": "Gujarat State Board (GSEB)",
    "TN": "Tamil Nadu State Board", "AP": "Andhra Pradesh (BSEAP)",
    "KL": "Kerala State Board (SCERT)", "KA": "Karnataka State Board (KSEEB)",
    "WB": "West Bengal Board (WBBSE)",
}
BOARD_TOKENS = {
    "mh": "MH", "maha": "MH", "maharashtra": "MH",
    "pun": "PB", "pb": "PB", "punjab": "PB", "pseb": "PB",
    "guj": "GJ", "gj": "GJ", "gujarat": "GJ", "gseb": "GJ",
    "tm": "TN", "tn": "TN", "tamilnadu": "TN",
    "ap": "AP", "andhra": "AP",
    "ker": "KL", "kl": "KL", "kerala": "KL",
    "kt": "KA", "ka": "KA", "karnataka": "KA", "kseeb": "KA",
    "ba": "WB", "wb": "WB", "bengal": "WB",
    "ncert": "NCERT", "cbse": "NCERT",
}
LANG_TOKENS = {
    "en": "English", "eng": "English", "english": "English",
    "hi": "Hindi", "hin": "Hindi", "hindi": "Hindi",
    "mr": "Marathi", "mar": "Marathi", "marathi": "Marathi",
    "gu": "Gujarati", "gj": "Gujarati", "guj": "Gujarati", "gujarati": "Gujarati",
    "ta": "Tamil", "tam": "Tamil", "tamil": "Tamil",
    "te": "Telugu", "tel": "Telugu", "telugu": "Telugu",
    "ka": "Kannada", "kn": "Kannada", "kan": "Kannada", "kannada": "Kannada",
    "ml": "Malayalam", "mal": "Malayalam", "malayalam": "Malayalam",
    "pu": "Punjabi", "pa": "Punjabi", "pun": "Punjabi", "punjabi": "Punjabi",
    "bn": "Bengali", "ben": "Bengali", "bengali": "Bengali",
    "ur": "Urdu", "urdu": "Urdu", "or": "Odia", "odia": "Odia",
    "as": "Assamese", "assamese": "Assamese",
}
SCRIPTS = {
    "English": "Latin", "Hindi": "Devanagari", "Marathi": "Devanagari",
    "Gujarati": "Gujarati", "Tamil": "Tamil", "Telugu": "Telugu",
    "Kannada": "Kannada", "Malayalam": "Malayalam", "Punjabi": "Gurmukhi",
    "Bengali": "Bengali", "Urdu": "Perso-Arabic", "Odia": "Odia",
    "Assamese": "Bengali",
}
# Three-letter language codes used in exported file names. A clipping is named
# lang_board_subject_number — eng_ncert_math_1.png and hin_ncert_math_1.png are
# the same passage in two languages, and the name alone says which book it came
# from without opening anything.
EXPORT_CODE = {
    "English": "eng", "Hindi": "hin", "Marathi": "mar", "Gujarati": "guj",
    "Tamil": "tam", "Telugu": "tel", "Kannada": "kan", "Malayalam": "mal",
    "Punjabi": "pan", "Bengali": "ben", "Urdu": "urd", "Odia": "ori",
    "Assamese": "asm", "Sanskrit": "san", "Nepali": "nep",
}
SUBJECT_CODE = {"Mathematics": "math", "Science": "sci", "Social Science": "sst"}


def subject_code(subject):
    return SUBJECT_CODE.get(subject, str(subject or "sub").split()[0].lower())


def project_folder(board, cls, subject):
    """The folder a project exports into: NCERT_class9_math."""
    return f"{str(board or 'BOARD').upper()}_class{cls}_{subject_code(subject)}"


def clip_name(language, board, subject, seq, ext="png"):
    """One clipping: eng_ncert_math_1.png"""
    return (f"{export_code(language)}_{str(board or 'board').lower()}_"
            f"{subject_code(subject)}_{seq}.{ext}")

# Chapters to leave out of the parallel corpus. Geometry and conics are
# excluded by instruction: their content is diagram-led, so a cropped text
# region rarely carries the meaning and the pair would be misleading.
EXCLUDED_TOPICS = [
    "geometry", "geometric", "conic", "conics", "circle", "circles",
    "triangle", "triangles", "quadrilateral", "polygon", "similarity",
    "congruence", "coordinate geometry", "constructions", "mensuration",
    "surface area", "volume", "trigonometry", "ज्यामिति", "ज्यामिती",
    "त्रिकोणमिति", "वृत्त", "त्रिभुज", "ভূমিতি", "வடிவியல்", "జ్యామితి",
    "ಜ್ಯಾಮಿತಿ", "ജ്യാമിതി", "ਜਿਓਮੈਟਰੀ",
]


def board_name(code):
    return BOARDS.get(str(code).upper(), str(code or "Unknown board"))


def script_of(lang):
    return SCRIPTS.get(lang, "Latin")


def export_code(lang):
    return EXPORT_CODE.get(lang, str(lang or "lang").lower().replace(" ", "_"))
