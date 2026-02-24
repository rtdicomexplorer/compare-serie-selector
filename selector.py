import os
from collections import defaultdict
from dicom_utils import read_metadata
from filters import passes_hard_filters
from scoring import score_series


# def collect_series(root_folder):
#     series_dict = defaultdict(list)

#     for root, _, files in os.walk(root_folder):
#         for file in files:
#             if file.endswith(".dcm"):
#                 path = os.path.join(root, file)
#                 meta = read_metadata(path)
#                 series_dict[meta["SeriesInstanceUID"]].append(meta)

#     return series_dict


# def select_best_series(root_folder):
#     series_dict = collect_series(root_folder)

#     candidates = []

#     for series_uid, metas in series_dict.items():
#         meta = metas[0]  # eine Datei repräsentiert Serie

#         if passes_hard_filters(meta):
#             score = score_series(meta)
#             candidates.append((series_uid, score, meta))

#     if not candidates:
#         return None

#     candidates.sort(key=lambda x: x[1], reverse=True)

#     return candidates[0]


def select_best_series(series_list):
    candidates = []
    for s in series_list:
        if passes_hard_filters(s):
            score = score_series(s)
            candidates.append((s, score))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0]