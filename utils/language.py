"""
Language utility — detection and basic multilingual support.
"""

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "हिन्दी (Hindi)",
    "ta": "தமிழ் (Tamil)",
    "te": "తెలుగు (Telugu)",
    "bn": "বাংলা (Bengali)",
    "mr": "मराठी (Marathi)",
    "pa": "ਪੰਜਾਬੀ (Punjabi)",
    "gu": "ગુજરાતી (Gujarati)",
    "kn": "ಕನ್ನಡ (Kannada)",
    "ml": "മലയാളം (Malayalam)",
}

# Unicode ranges for script detection
SCRIPT_RANGES = {
    "hi": (0x0900, 0x097F),   # Devanagari
    "ta": (0x0B80, 0x0BFF),   # Tamil
    "te": (0x0C00, 0x0C7F),   # Telugu
    "bn": (0x0980, 0x09FF),   # Bengali
    "mr": (0x0900, 0x097F),   # Marathi (also Devanagari)
    "pa": (0x0A00, 0x0A7F),   # Gurmukhi
    "gu": (0x0A80, 0x0AFF),   # Gujarati
    "kn": (0x0C80, 0x0CFF),   # Kannada
    "ml": (0x0D00, 0x0D7F),   # Malayalam
}


def detect_language(text: str) -> str:
    """Detect the language of input text based on Unicode script ranges."""
    if not text:
        return "en"

    # Count characters in each script
    script_counts = {}
    for char in text:
        code = ord(char)
        for lang, (start, end) in SCRIPT_RANGES.items():
            if start <= code <= end:
                script_counts[lang] = script_counts.get(lang, 0) + 1
                break

    if not script_counts:
        return "en"

    # Return the most common script
    # Marathi and Hindi share Devanagari — default to Hindi for simplicity
    detected = max(script_counts, key=script_counts.get)
    if detected == "mr":
        # Ambiguous — could be Hindi or Marathi. Default to Hindi.
        return "hi"
    return detected


def translate_text(text: str, target_lang: str) -> str:
    """
    Placeholder for translation. In production, integrate with:
    - Google Translate API
    - IndicTrans (AI4Bharat)
    - Bhashini API (Indian govt translation service)

    For now, returns text as-is and lets the LLM handle multilingual responses.
    """
    # The LLM is prompted to respond in the user's language,
    # so we rely on it rather than a separate translation service.
    return text
