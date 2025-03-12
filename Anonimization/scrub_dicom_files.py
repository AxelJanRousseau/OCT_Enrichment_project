import glob
import logging
import pandas as pd
import pydicom
import os
import argparse
from tqdm import tqdm
import datetime


def remove_UIDs(ds: pydicom.dataset.FileDataset) -> pydicom.dataset.FileDataset:
    ds.SOPClassUID = ""
    ds.SOPInstanceUID = ""
    ds.SeriesInstanceUID = ""
    ds.StudyInstanceUID = ""
    ds.FrameOfReferenceUID = ""
    ds.StudyID = ""
    ds.file_meta.TransferSyntaxUID = ""
    ds.file_meta.MediaStorageSOPClassUID = ""
    ds.file_meta.MediaStorageSOPInstanceUID = ""
    ds.file_meta.ImplementationClassUID = ""
    ds.AccessionNumber = ""
    return ds


def remove_acquisition_time(
    ds: pydicom.dataset.FileDataset,
) -> pydicom.dataset.FileDataset:
    # ds.StudyDate = ""
    # ds.SeriesDate = ""
    # ds.ContentDate = ""

    ds.AcquisitionDateTime = ""
    ds.StudyTime = ""
    ds.SeriesTime = ""
    ds.ContentTime = ""

    return ds


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--abs_path", type=str, help="Path to the dicom files folder"
    )
    parser.add_argument(
        "--csv",
        type=str,
        help="Path to the csv file containing the mapping between patient names and unique_ids",
    )
    parser.add_argument("--out_path", type=str, help="Path to the output folder")

    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename=os.path.join(args.out_path, "scrub_dicom_files.log"),
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s %(message)s",
    )

    df = pd.read_csv(args.csv)

    assert os.path.exists(args.abs_path)
    files = glob.glob(os.path.join(args.abs_path, "**", "*.dcm"), recursive=True)
 
    for f in tqdm(files, mininterval=10):
        try:
            ds = pydicom.dcmread(f)
        except pydicom.errors.InvalidDicomError as e:
            logger.error(f"Error reading {f} {e}, skipping")
            continue

        family_name = ds.PatientName.family_name
        given_name = ds.PatientName.given_name
        birthdate = datetime.datetime.strptime(ds.PatientBirthDate, "%Y%m%d").strftime(
            "%Y-%m-%d"
        )
        # dit is stom, gebruik PatientId -> UnifiedPatientID ipv (FamilyName, GivenName, BirthDate) -> UnifiedPatientID
        # new_id = df[
        #     (df.FamilyName == family_name)
        #     & (df.GivenName == given_name)
        #     & (df.PatientBirthDate == birthdate)
        # ].UnifiedPatientID

        new_id = df[df.PatientID == ds.PatientID].UnifiedPatientID

        if new_id.empty:
            logger.error(
                f"Could not find patient {family_name} {given_name} {birthdate}, skipping"
            )
            continue
        elif len(new_id) > 1:
            logger.error(
                f"Multiple patients found for {family_name} {given_name} {birthdate}, skipping"
            )
            continue
        new_id = new_id.iloc[0]
        sdate = ds.StudyDate

        ds.PatientName = pydicom.valuerep.PersonName("")
        ds.PatientID = new_id
        ds.PerformingPhysicianName = ""
        ds.ReferringPhysicianName = ""
        ds.OperatorsName = ""

        clean_birthdate = datetime.datetime.strptime(ds.PatientBirthDate, "%Y%m%d")
        clean_birthdate = clean_birthdate.replace(day=1, month=1)

        ds.PatientBirthDate = clean_birthdate.strftime("%Y%m%d")
        ds.EthnicGroup = ""
        ds = remove_UIDs(ds)
        ds = remove_acquisition_time(ds)

        fname = os.path.basename(f)
        # niet de properste manier voor string / path manipulatie
        name_parts = fname.split("_")[-3:]
        name_parts.insert(0, sdate)
        new_name = "_".join(name_parts)
        new_path = os.path.join(args.out_path, new_id, new_name)
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        ds.save_as(
            new_path
        )  # same as pydicom.filewriter.dcmwrite(new_path,ds,write_like_original=True)
