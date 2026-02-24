from config import PREFERRED_SLICE_THICKNESS, PHASE_PRIORITY_KEYWORDS

def score_series(series_meta):
    score = 0
    desc = series_meta.get("SeriesDescription", "").lower()

    for phase, keywords in PHASE_PRIORITY_KEYWORDS.items():
        for kw in keywords:
            if kw in desc:
                if phase == "venous": score += 3
                elif phase == "arterial": score += 2
                elif phase == "native": score += 1

    if series_meta.get("SliceThickness") == PREFERRED_SLICE_THICKNESS:
        score += 2

    if "abdomen" in desc:
        score += 2

    return score