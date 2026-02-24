import pydicom

def read_metadata(filepath):
    ds = pydicom.dcmread(filepath, stop_before_pixels=True)

    return {
        "StudyInstanceUID": getattr(ds, "StudyInstanceUID", None),
        "SeriesInstanceUID": getattr(ds, "SeriesInstanceUID", None),
        "StudyDate": getattr(ds, "StudyDate", None),
        "SeriesDescription": str(getattr(ds, "SeriesDescription", "")).lower(),
        "BodyPart": str(getattr(ds, "BodyPartExamined", "")).lower(),
        "SliceThickness": getattr(ds, "SliceThickness", None),
        "ConvolutionKernel": str(getattr(ds, "ConvolutionKernel", "")).lower(),
        "ImageOrientation": getattr(ds, "ImageOrientationPatient", None),
        "KVP": getattr(ds, "KVP", None)
    }



def series_ok(series_meta):
    modality_ok = series_meta.get("Modality", "").upper() == "CT"
    bodypart_ok = series_meta.get("BodyPartExamined", "").lower() in ["abdomen", "thorax", "thoraxabdomen"]
    return modality_ok and bodypart_ok