from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind
from pydicom.dataset import Dataset
from config import PACS_AE_TITLE, PACS_IP, PACS_PORT, LOCAL_AE_TITLE


debug_logger()


def query_studies(patient_id, start_date, end_date):
    ae = AE(ae_title=LOCAL_AE_TITLE)
    assoc = ae.associate(PACS_IP, PACS_PORT, ae_title=PACS_AE_TITLE)
    if not assoc.is_established:
        raise ConnectionError("PACS-Connection failed")

    ds = Dataset()
    ds.QueryRetrieveLevel = "STUDY"
    ds.PatientID = patient_id
    ds.ModalitiesInStudy = "CT"
    ds.StudyDate = f"{start_date}-{end_date}"

    responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
    studies = []
    for status, identifier in responses:
        if status and status.Status in (0xFF00, 0xFF01):
            studies.append(identifier)

    assoc.release()
    return studies


def query_series(study_instance_uid):
    ae = AE(ae_title=LOCAL_AE_TITLE)
    assoc = ae.associate(PACS_IP, PACS_PORT, ae_title=PACS_AE_TITLE)
    if not assoc.is_established:
        raise ConnectionError("PACS-Connection failed")

    ds = Dataset()
    ds.QueryRetrieveLevel = "SERIES"
    ds.StudyInstanceUID = study_instance_uid

    # Wichtige Serie-Level Tags
    ds.SeriesInstanceUID = ""
    ds.SeriesDescription = ""
    ds.Modality = ""
    ds.BodyPartExamined = ""

    responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
    series_list = []
    for status, identifier in responses:
        if status and status.Status in (0xFF00, 0xFF01):
            series_list.append(identifier)

    assoc.release()
    return series_list


def query_image(series_instance_uid):

    ae = AE(ae_title=LOCAL_AE_TITLE)
    assoc = ae.associate(PACS_IP, PACS_PORT, ae_title=PACS_AE_TITLE)
    if not assoc.is_established:
        raise ConnectionError("PACS Connection failed")

    ds = Dataset()
    ds.QueryRetrieveLevel = "IMAGE"
    ds.SeriesInstanceUID = series_instance_uid
    ds.SOPInstanceUID = ""  # alle Images

    responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
    sop_uids = []
    for status, identifier in responses:
        if status and status.Status in (0xFF00, 0xFF01):
            sop_uids.append(identifier.SOPInstanceUID)

    assoc.release()
    return sorted(sop_uids)


def __query_series(study_instance_uid):
    """
    Fragt alle Serien einer Studie vom PACS ab.
    study_instance_uid: str
    Rückgabe: Liste von Serien-Metadaten (Dataset)
    """
    debug_logger()  # optional für Debug
    
    ae = AE(ae_title='LOCAL_AE')
    assoc = ae.associate('10.0.0.1', 104, ae_title='MY_AE')
    
    if not assoc.is_established:
        raise ConnectionError("PACS Connection failed")
    
    ds = Dataset()
    ds.QueryRetrieveLevel = 'SERIES'
    ds.StudyInstanceUID = study_instance_uid
    ds.ModalitiesInStudy = 'CT'
    
    # Du kannst direkt gewünschte Tags anfordern:
    ds.SeriesInstanceUID = ""
    ds.SeriesDescription = ""
    ds.BodyPartExamined = ""




    ds.ConvolutionKernel = ""
    ds.SliceThickness = ""
    ds.ImageOrientationPatient = ""
    ds.KVP = ""
    
    responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
    
    series_list = []
    for (status, identifier) in responses:
        if status and status.Status in (0xFF00, 0xFF01):
            series_list.append(identifier)
    
    assoc.release()
    return series_list