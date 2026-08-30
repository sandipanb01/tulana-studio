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

    # State and regional boards, so a textbook from any of them is named
    # properly instead of falling through to Unknown.
    "AS": "Assam Board (SEBA)",
    "OD": "Odisha Board (BSE)",
    "TS": "Telangana State Board",
    "RJ": "Rajasthan Board (RBSE)",
    "UP": "Uttar Pradesh Board",
    "BR": "Bihar Board (BSEB)",
    "MP": "Madhya Pradesh Board (MPBSE)",
    "JK": "Jammu & Kashmir Board (JKBOSE)",
    "HP": "Himachal Pradesh Board (HPBOSE)",
    "HR": "Haryana Board (BSEH)",
    "JH": "Jharkhand Board (JAC)",
    "CG": "Chhattisgarh Board (CGBSE)",
    "UK": "Uttarakhand Board (UBSE)",
    "GA": "Goa Board",
    "TR": "Tripura Board",
    "ML": "Meghalaya Board (MBOSE)",
    "MN": "Manipur Board (BSEM)",
    "MZ": "Mizoram Board (MBSE)",
    "NL": "Nagaland Board (NBSE)",
    "SK": "Sikkim Board",
    "AR": "Arunachal Pradesh Board",
    "DL": "Delhi (DoE)",
    "ICSE": "CISCE (ICSE / ISC)",
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

    # More boards, plus the abbreviations people actually type.
    "arunachal": "AR",
    "assam": "AS",
    "bihar": "BR",
    "br": "BR",
    "bseb": "BR",
    "bseh": "HR",
    "bsem": "MN",
    "cg": "CG",
    "cgbse": "CG",
    "chhattisgarh": "CG",
    "cisce": "ICSE",
    "delhi": "DL",
    "ga": "GA",
    "goa": "GA",
    "haryana": "HR",
    "himachal": "HP",
    "hp": "HP",
    "hpbose": "HP",
    "hr": "HR",
    "icse": "ICSE",
    "isc": "ICSE",
    "jac": "JH",
    "jh": "JH",
    "jharkhand": "JH",
    "jk": "JK",
    "jkbose": "JK",
    "mbose": "ML",
    "mbse": "MZ",
    "meghalaya": "ML",
    "mizoram": "MZ",
    "mp": "MP",
    "mpbse": "MP",
    "nagaland": "NL",
    "nbse": "NL",
    "od": "OD",
    "odisha": "OD",
    "orissa": "OD",
    "rajasthan": "RJ",
    "rbse": "RJ",
    "rj": "RJ",
    "seba": "AS",
    "sikkim": "SK",
    "tbse": "TR",
    "telangana": "TS",
    "tripura": "TR",
    "ts": "TS",
    "ubse": "UK",
    "uk": "UK",
    "up": "UP",
    "upmsp": "UP",
    "uttarakhand": "UK",
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

    # The ISO code, the common abbreviation and the full name all resolve,
    # so a language is never silently invisible because of how it was typed.
    "asm": "Assamese",
    "bangla": "Bengali",
    "bodo": "Bodo",
    "brx": "Bodo",
    "dogri": "Dogri",
    "doi": "Dogri",
    "gurmukhi": "Punjabi",
    "kas": "Kashmiri",
    "kashmiri": "Kashmiri",
    "kok": "Konkani",
    "konkani": "Konkani",
    "ks": "Kashmiri",
    "mai": "Maithili",
    "maithili": "Maithili",
    "manipuri": "Manipuri",
    "meitei": "Manipuri",
    "mni": "Manipuri",
    "ne": "Nepali",
    "nep": "Nepali",
    "nepali": "Nepali",
    "ori": "Odia",
    "oriya": "Odia",
    "pan": "Punjabi",
    "pnb": "Punjabi",
    "sa": "Sanskrit",
    "san": "Sanskrit",
    "sanskrit": "Sanskrit",
    "santali": "Santali",
    "sat": "Santali",
    "sd": "Sindhi",
    "sindhi": "Sindhi",
    "snd": "Sindhi",
    "urd": "Urdu",
}
SCRIPTS = {
    "English": "Latin", "Hindi": "Devanagari", "Marathi": "Devanagari",
    "Gujarati": "Gujarati", "Tamil": "Tamil", "Telugu": "Telugu",
    "Kannada": "Kannada", "Malayalam": "Malayalam", "Punjabi": "Gurmukhi",
    "Bengali": "Bengali", "Urdu": "Perso-Arabic", "Odia": "Odia",
    "Assamese": "Bengali",

    # A language and its script are different things: Sanskrit and Konkani
    # are Devanagari, Sindhi and Kashmiri Perso-Arabic. Defaulting these to
    # Latin would mislabel every chunk downstream.
    "Sanskrit": "Devanagari",
    "Nepali": "Devanagari",
    "Maithili": "Devanagari",
    "Konkani": "Devanagari",
    "Bodo": "Devanagari",
    "Dogri": "Devanagari",
    "Sindhi": "Perso-Arabic",
    "Kashmiri": "Perso-Arabic",
    "Manipuri": "Bengali",
    "Santali": "Ol Chiki",
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


# Boards whose name is two words. A folder called "Tamil Nadu" splits into
# `tamil` and `nadu`, and `tamil` is a *language* token — so without this the
# board is read as the language and the textbook disappears from the dropdown.
BOARD_PHRASES = {
    ("tamil", "nadu"): "TN", ("west", "bengal"): "WB",
    ("andhra", "pradesh"): "AP", ("madhya", "pradesh"): "MP",
    ("himachal", "pradesh"): "HP", ("uttar", "pradesh"): "UP",
    ("arunachal", "pradesh"): "AR", ("jammu", "kashmir"): "JK",
    ("tamilnadu",): "TN", ("westbengal",): "WB",
}


def free_port(preferred: int = None, tries: int = 20) -> int:
    """The first port that will actually bind, starting at the preferred one.

    A fixed port fails whenever something else already holds it — another copy
    of the studio, a stale process, or an unrelated service — and the failure
    is an unhelpful "address already in use" at the moment someone wants to
    start work. Walking forward turns that into a different number in the
    banner."""
    import socket
    start = int(preferred or PORT)
    for n in range(max(1, tries)):
        p = start + n
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind((HOST if HOST != "0.0.0.0" else "", p))
                return p
            except OSError:
                continue
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST if HOST != "0.0.0.0" else "", 0))
        return s.getsockname()[1]
