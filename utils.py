import re
from rapidfuzz import fuzz

NUMBER_REGEX = re.compile(r"([-+]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)")

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def extract_numbers(text: str):
    matches = NUMBER_REGEX.findall(text)
    return [float(m.replace(",", "")) for m in matches]

def fuzzy_match_line_item(raw_item: str, canonical_dict: dict, threshold=80):
    raw_clean = clean_text(raw_item)

    best_match = None
    best_score = 0

    for canonical, variants in canonical_dict.items():
        for variant in variants:
            score = fuzz.partial_ratio(raw_clean, variant)
            if score > best_score:
                best_score = score
                best_match = canonical

    if best_score >= threshold:
        return best_match, best_score

    return None, best_score
