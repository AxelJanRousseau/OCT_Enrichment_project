import os

import pandas as pd
import glob
import xml.etree.ElementTree as ET
import argparse
import logging
import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="scrub_xml_files.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)


def _scrub_xml(tree: ET.ElementTree, df: pd.DataFrame) -> ET.ElementTree | None:
    root = tree.getroot()
    pinf = root.find("PatientInformation")
    ex = root.find("ExaminationInformation")
    ex_date = ex.find("ExaminationDateTime").text

    ex_date = datetime.datetime.strptime(ex_date[:-2], "%Y-%m-%dT%H:%M:%S.%f")
    ex.find("ExaminationDateTime").text = ex_date.strftime("%Y-%m-%d")
    b_day = pinf.find("PatientBirthDate").text
    b_day = b_day.split("-")[0] + "-00-00"
    pinf.find("PatientBirthDate").text = b_day # scrubbing the day and month -> only year is kept

    try:
        pinf.find("PatientNameGroup1").text = ""
    except AttributeError:
        pass

    pid = pinf.find("PatientID").text
    new_id = df[df["PatientID"] == pid]["UnifiedPatientID"]
    if new_id.empty:
        logger.error(f"Could not find patient {pid}, skipping")
        return None
    elif len(new_id) > 1:
        logger.error(f"Multiple patients found for {pid}, skipping")
        return None
    pinf.find("PatientID").text = new_id.values[0]

    return tree


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--abs_path", type=str, help="Path to the xml files folder"
    )
    parser.add_argument(
        "--csv",
        type=str,
        help="Path to the csv file containing the mapping between patient names and unique_ids",
    )
    parser.add_argument("--out_path", type=str, help="Path to the output folder")
    args = parser.parse_args()
    assert os.path.exists(args.abs_path)
    assert os.path.exists(args.out_path)
    assert os.path.exists(args.csv)
    df = pd.read_csv(args.csv)

    files = glob.glob(os.path.join(args.abs_path, "**", "*.xml"), recursive=True)
    files = sorted(files)

    for f in files:
        tree: ET.ElementTree = ET.parse(f)
        tree = _scrub_xml(tree, df)
        if tree is None:
            continue
        id = tree.find("PatientInformation").find("PatientID").text
        ex_date = tree.find("ExaminationInformation").find("ExaminationDateTime").text
        fname = os.path.basename(f)
        name_parts = fname.split("_")[-2:]
        name_parts.insert(0, ex_date)
        new_fname = "_".join(name_parts)
        save_path = os.path.join(args.out_path, id, new_fname)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        tree.write(save_path, encoding="utf-8", xml_declaration=True)
