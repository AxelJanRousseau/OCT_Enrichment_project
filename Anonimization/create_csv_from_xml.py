import glob
import pandas as pd

import os
import argparse
import hashlib
from tqdm import tqdm
import secrets
import logging
import xml.etree.ElementTree as ET


def calc_hash(x):
    h = hashlib.sha1()
    h.update(x["FamilyName"].encode("utf-8"))
    h.update(x["GivenName"].encode("utf-8"))
    h.update(x["PatientBirthDate"].encode("utf-8"))
    h.update(x["salt"])
    return h.hexdigest().upper()


def _get_pinfo_xml(tree: ET.ElementTree):
    root = tree.getroot()
    pinf = root.find("PatientInformation")

    b_day = pinf.find("PatientBirthDate").text
    try:
        pid = pinf.find("PatientID").text
    except Exception:
        pid = None

    sex = pinf.find("PatientSex").text
    name = pinf.find("PatientNameGroup1").text
    lname = name.split("^")[0]
    fname = name.split("^")[-1]

    return (pid, lname, fname, b_day, sex)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename="create_csv_from_xml.log",
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s %(message)s",
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, help="Path to the xml files folder")

    args = parser.parse_args()
    # os.path.normpath()
    assert os.path.exists(args.path)
    files = glob.glob(os.path.join(args.path, "**", "*.xml"), recursive=True)
    patient_set = set()
    for f in tqdm(files, mininterval=2):
        try:
            tree: ET.ElementTree = ET.parse(f)
            p_info = _get_pinfo_xml(tree)
        except Exception as e:
            logger.error(f"Error reading {f} {e}")
            continue
        patient_set.add(p_info)

    df = pd.DataFrame(
        patient_set,
        columns=(
            "PatientID",
            "FamilyName",
            "GivenName",
            "PatientBirthDate",
            "PatientSex",
        ),
    )
    # getting a salt could probably be done cleaner using pd
    salt_set = set()
    for item in df[["FamilyName", "GivenName", "PatientBirthDate"]].values.tolist():
        salt_set.add(tuple(item))
    salt_set
    salt_dict = {
        k: secrets.token_bytes(32) for k in salt_set
    }  # Use secrets.token_bytes or secrets.toke_hex instead!!! safer random numbers

    def salt_to_df(x):
        t = (x["FamilyName"], x["GivenName"], x["PatientBirthDate"])
        return salt_dict[t]

    df["salt"] = df.apply(salt_to_df, axis=1)

    df["UnifiedPatientID"] = df.apply(calc_hash, axis=1)
    df["PatientBirthDate"] = pd.to_datetime(
        df["PatientBirthDate"], format="%Y-%m-%dT%H:%M:%S"
    )

    df.to_csv("patients_to_id_xml.csv", index=False)

    duplicateRows = df[
        df.duplicated(
            ["FamilyName", "GivenName", "PatientBirthDate"],
        )
    ]
    if len(duplicateRows) > 0:
        print("Possible duplicate patients found")
        logger.warning("Possible duplicate patients found")
        duplicateRows.to_csv("possible_duplicates.csv")

    no_cannon_id = df[(df.PatientID.isna()) | (df.PatientID == "")]
    if len(no_cannon_id) > 0:
        print("Patients without a PatientID found")
        logger.warning("Patients without a PatientID found")
        no_cannon_id.to_csv("no_cannon_id.csv")

    keep_df = df
    keep_df["PatientBirthDate"] = pd.to_datetime(
        keep_df["PatientBirthDate"], format="%Y%m%d"
    ).dt.year

    keep_df = keep_df.drop(
        [
            "FamilyName",
            "GivenName",
            "salt",
        ],
        axis=1,
    )
    keep_df.to_csv(
        "OCTid_to_PID_list_xml.csv", index=False
    )  # "canon code" to "UnifiedPatientID" mapping, in case this is usefull?
