from selector import select_best_series
from pacs_query import query_studies,query_series,query_image

from dicom_utils import series_ok, read_metadata
from pacs_get_move import  retrieve_image

FROMPACS = False



def __execute_from_pacs():
    import datetime
    
    patients = [
        {"PatientID": "12345", "DiagnosisDate": "20240315", "TherapyStart": "20240410"},
    ]

    for p in patients:
        start_window = (datetime.datetime.strptime(p["DiagnosisDate"], "%Y%m%d") - datetime.timedelta(days=90)).strftime("%Y%m%d")
        end_window = (datetime.datetime.strptime(p["TherapyStart"], "%Y%m%d") - datetime.timedelta(days=1)).strftime("%Y%m%d")

        # Studien abrufen
        studies = query_studies(p["PatientID"], start_window, end_window)

        candidate_series = []

        #sort(studies) neueste zuvor

        for study in studies:
            # Für jede Studie die Serien abfragen
            series_list  = query_series(study["StudyInstanceUID"])
            for s in series_list:

                if not series_ok(s):
                    continue
                sop_uids = query_image(s["SeriesInstanceUID"])
                if not sop_uids:
                    continue
                first_sop_uid = sop_uids[0]
                first_image_file = retrieve_image(first_sop_uid, s["SeriesInstanceUID"])
                meta = read_metadata(first_image_file)
                s.update(meta)
                candidate_series.append(s)
                           


        best_series = select_best_series(candidate_series)

        if best_series:
            meta, score = best_series
            print(f"Patient {p['PatientID']} -> Best Serie: {meta['SeriesInstanceUID']}, Score: {score}, Description: {meta['SeriesDescription']}")
        else:
            print(f"Patient {p['PatientID']} -> No ideal Serie found")



def __execute_from_folder(dicom_folder):
    import os
    from dicom_utils import read_metadata
    from selector import select_best_series

    # Alle DICOM-Dateien aus dem Ordner einlesen
    series_list = []
    for root, _, files in os.walk(dicom_folder):
        for f in files:
            if f.endswith(".dcm"):
                meta = read_metadata(os.path.join(root, f))
                series_list.append(meta)

    best_series = select_best_series(series_list)

    if best_series:
        meta, score = best_series
        print("Best Serie found:")
        print("UID:", meta["SeriesInstanceUID"])
        print("Score:", score)
        print("Description:", meta["SeriesDescription"])
    else:
        print("No ideal Serie found.")

if __name__ == "__main__":
    dicom_folder =  './data'# "PATH_TO_DICOM_FOLDER"

    if(FROMPACS):
        __execute_from_pacs()
    else:
        __execute_from_folder(dicom_folder)

    