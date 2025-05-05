selected_discipline_map = {
    "archeo": "Archaeology and Prehistory",
    "archi": "Architecture and Space Management",
    "envir": "Environmental studies",
    "hist": "History",
    "relig": "Religions",
    "socio": "Sociology",
}

language_code_map = {
    "ar": "Arabic",
    "it": "Italian",
    "pl": "Polish",
    "hr": "Croatian",
    "el": "Greek",
    "de": "German",
    "sv": "Swedish",
    "ru": "Russian",
    "en": "English",
    "undefined": "Undefined",
    "es": "Spanish",
    "nl": "Dutch",
    "other": "Other",
    "tr": "Turkish",
    "pt": "Portuguese",
    "fr": "French",
    "uk": "Ukrainian",
    "sr": "Serbian",
    "hu": "Hungarian",
    "no": "Norwegian",
    "ca": "Catalan",
    "fi": "Finnish",
    "sq": "Albanian",
    "sl": "Slovenian",
    "he": "Hebrew",
    "da": "Danish",
}

TOPICS = [_ for _ in selected_discipline_map]
LANGUAGES = [_ for _ in language_code_map]
HAS_PDF_PARAMS = True
