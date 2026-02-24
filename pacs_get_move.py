import os
from pynetdicom import AE, evt,debug_logger
from pynetdicom.sop_class import StudyRootQueryRetrieveInformationModelMove
from pydicom.dataset import Dataset
from config import PACS_AE_TITLE, PACS_IP, PACS_PORT, LOCAL_AE_TITLE

# Local folder to temporarily store DICOMs
TEMP_FOLDER = "./temp_first_image"
os.makedirs(TEMP_FOLDER, exist_ok=True)

debug_logger()  # optional



def retrieve_image(sop_instance_uid, series_instance_uid):
    """
    C-MOVE: holt ein DICOM anhand SOPInstanceUID
    """
    ae = AE(ae_title=LOCAL_AE_TITLE)
    assoc = ae.associate(PACS_IP, PACS_PORT, ae_title=PACS_AE_TITLE)
    if not assoc.is_established:
        raise ConnectionError("PACS Verbindung fehlgeschlagen")

    downloaded_files = []

    def handle_store(event):
        ds = event.dataset
        ds.file_meta = event.file_meta
        filename = os.path.join(TEMP_FOLDER, ds.SOPInstanceUID + ".dcm")
        ds.save_as(filename, write_like_original=False)
        downloaded_files.append(filename)
        return 0x0000

    handlers = [(evt.EVT_C_STORE, handle_store)]

    ds_move = Dataset()
    ds_move.QueryRetrieveLevel = "IMAGE"
    ds_move.SeriesInstanceUID = series_instance_uid
    ds_move.SOPInstanceUID = sop_instance_uid

    assoc.send_c_move(ds_move, LOCAL_AE_TITLE, StudyRootQueryRetrieveInformationModelMove, evt_handlers=handlers)
    assoc.release()

    if not downloaded_files:
        raise FileNotFoundError(f"Failed to retrieve image {sop_instance_uid}")

    return downloaded_files[0]

def __retrieve_first_image(series_instance_uid):
    """
    Retrieves the first DICOM file of a series from PACS via C-MOVE.
    Returns the path to the downloaded DICOM file.
    """
    ae = AE(ae_title=LOCAL_AE_TITLE)
    
    # Associate to PACS
    assoc = ae.associate(PACS_IP, PACS_PORT, ae_title=PACS_AE_TITLE)
    if not assoc.is_established:
        raise ConnectionError("PACS connection failed")

    # Build the query dataset for series
    ds = Dataset()
    ds.QueryRetrieveLevel = "IMAGE"  # retrieve image-level
    ds.SeriesInstanceUID = series_instance_uid
    ds.SOPInstanceUID = ""           # request all images in series
    ds.PatientID = ""

    # C-MOVE stores the images in the local folder
    from pynetdicom import StorageSOPClassList
    from pynetdicom import evt

    downloaded_files = []

    # Define a handler to save incoming images
    def handle_store(event):
        """Handle incoming C-STORE requests (save DICOM)"""
        ds = event.dataset
        ds.file_meta = event.file_meta
        filename = os.path.join(TEMP_FOLDER, ds.SOPInstanceUID + ".dcm")
        ds.save_as(filename, write_like_original=False)
        downloaded_files.append(filename)
        return 0x0000

    handlers = [(evt.EVT_C_STORE, handle_store)]

    # Perform C-MOVE
    status = assoc.send_c_move(ds, LOCAL_AE_TITLE, StudyRootQueryRetrieveInformationModelMove, evt_handlers=handlers)

    assoc.release()

    if not downloaded_files:
        raise FileNotFoundError(f"No images retrieved for series {series_instance_uid}")

    # Return first image path
    downloaded_files.sort()  # optional: sort by SOPInstanceUID
    return downloaded_files[0]