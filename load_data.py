import os
import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np


def _parse_common(path):
    """
    Parses the common parts of XML file at the given path to extract patient and examination information.
    Args:
        path (str): The file path to the XML file.
    Returns:
        tuple: A tuple containing:
            - laterality (str): The laterality information extracted from the file path.
            - root (xml.etree.ElementTree.Element): The root element of the parsed XML tree.
            - pinf_dict (dict): A dictionary containing patient information extracted from the XML.
            - ex_dict (dict): A dictionary containing examination information extracted from the XML,
              with the "PatientID" field updated to match the directory name.
    Raises:
        AssertionError: If the laterality extracted from the file path does not match the laterality
                        in the examination information, or if the patient ID in the directory name
                        does not match the patient ID in the patient information.
    """
    pid = os.path.dirname(path).split(os.sep)[-1]
    laterality = path[-5]
    tree = ET.parse(path)
    root = tree.getroot()

    pinf = root.find("PatientInformation")
    pinf_dict = {p.tag: p.text for p in pinf}
    pinf_dict.pop("PatientNameGroup1", None)
    ex = root.find("ExaminationInformation")
    ex_dict = {el.tag: el.text for el in ex}
    try:
        assert laterality == ex_dict["Laterality"]
    except AssertionError:
        print(
            f"Error in {path} laterality {laterality} does not match {ex_dict['Laterality']}"
        )

    try:
        assert pid == pinf_dict["PatientID"]
    except AssertionError:
        print(f"Error in {path} pid {pid} does not match {pinf_dict['PatientID']}")
    ex_dict["PatientID"] = pid
    return laterality, root, pinf_dict, ex_dict


def read_disc_file(path):
    """
    Reads and parses a "disc" XML file to extract optic disc measurement data.
    Args:
        path (str): The file path to the disc file.
    Returns:
        tuple: A tuple containing three dictionaries:
            - pinf_dict (dict): Patient information dictionary.
            - ex_dict (dict): Examination information dictionary.
            - disc_dict (dict): Disc measurement data dictionary, with keys formatted as
              "{laterality}_{top_tag}_{element_tag}" and values as the corresponding text.
    """
    laterality, root, pinf_dict, ex_dict = _parse_common(path)

    disc_measure = root.find("DiscMeasurementData")
    disc_dict = {
        laterality + "_" + top.tag + "_" + element.tag: element.text
        for top in disc_measure
        for element in top
    }

    return pinf_dict, ex_dict, disc_dict


def read_glaucoma_file(path):
    """
    Reads and parses a glaucoma measurement data file.
    Args:
        path (str): The file path to the glaucoma measurement data file.
    Returns:
        tuple: A tuple containing:
            - pinf_dict (dict): Patient information dictionary.
            - ex_dict (dict): Examination information dictionary.
            - measurement_dict (dict): Dictionary containing parsed measurement data with keys indicating the laterality, sector, and measurement type.
    """
    laterality, root, pinf_dict, ex_dict = _parse_common(path)
    measurement = root.find("GlaucomaMeasurementData")
    tot = measurement.find("TotalSector/Thickness")
    measurement_dict = {
        laterality + "_Total_Thickness_" + el.tag: el[0].text for el in tot
    }

    two = measurement.find("TwoSectors")

    for element in two.find("Thickness/GCL_IPL"):
        measurement_dict[laterality + "_TwoSect_Thickness_GCL_IPL_" + element.tag] = (
            element.text
        )
    for element in two.find("DifferenceSI/GCL_IPL"):
        measurement_dict[
            laterality + "_TwoSect_DifferenceSI_GCL_IPL_" + element.tag
        ] = element.text
    for element in two.find("Thickness/NFL_GCL_IPL"):
        measurement_dict[
            laterality + "_TwoSect_Thickness_NFL_GCL_IPL_" + element.tag
        ] = element.text
    for element in two.find("DifferenceSI/NFL_GCL_IPL"):
        measurement_dict[
            laterality + "_TwoSect_DifferenceSI_NFL_GCL_IPL_" + element.tag
        ] = element.text

    eight = measurement.find("EightSectors")
    for element in eight.find("Thickness/GCL_IPL"):
        measurement_dict[laterality + "_EightSect_Thickness_GCL_IPL_" + element.tag] = (
            element.text
        )
    for element in eight.find("DifferenceSI/GCL_IPL"):
        measurement_dict[
            laterality + "_EightSect_DifferenceSI_GCL_IPL_" + element.tag
        ] = element.text
    for element in eight.find("Thickness/NFL_GCL_IPL"):
        measurement_dict[
            laterality + "_EightSect_Thickness_NFL_GCL_IPL_" + element.tag
        ] = element.text
    for element in eight.find("DifferenceSI/NFL_GCL_IPL"):
        measurement_dict[
            laterality + "_EightSect_DifferenceSI_NFL_GCL_IPL_" + element.tag
        ] = element.text

    return pinf_dict, ex_dict, measurement_dict


def read_macula_file(path):
    """
    Reads and parses a macula file to extract measurement data.
    Args:
        path (str): The file path to the macula file.
    Returns:
        tuple: A tuple containing:
            - pinf_dict (dict): Patient information dictionary.
            - ex_dict (dict): Examination information dictionary.
            - measurement_dict (dict): Dictionary containing macula measurement data.
                The keys are formatted as "<laterality>_<MeasurementType>_<ILMType>_<ElementTag>".
    """
    laterality, root, pinf_dict, ex_dict = _parse_common(path)
    measurement = root.find("MaculaMeasurementData")
    measurement_dict = {}
    ETDRSSectors = measurement.find("ETDRSSectors")
    for ilm_type in ETDRSSectors:
        for element in ilm_type:
            key = laterality + "_ETDRSSectors_" + ilm_type.tag + "_" + element.tag
            measurement_dict[key] = element.text

    FullRetinal = measurement.find("FullRetinalParameters")
    for ilm_type in FullRetinal:
        for element in ilm_type:
            key = laterality + "_FullRetinal_" + ilm_type.tag + "_" + element.tag
            measurement_dict[key] = element.text

    return pinf_dict, ex_dict, measurement_dict


def xml_to_df(path):
    if "Disc3D" in path:
        res = read_disc_file(path)
    elif "Glaucoma3D" in path:
        res = read_glaucoma_file(path)
    elif "Macula3D" in path:
        res = read_macula_file(path)
    else:
        raise Exception("File not recognised")

    res = {**res[0], **res[1], **res[2]}
    res = pd.Series(res)
    res["PatientBirthDate"] = pd.to_datetime(
        res["PatientBirthDate"], format="%Y-00-00"
    ).year
    
    res["ExaminationDate"] = pd.to_datetime(
        res["ExaminationDateTime"], format="%Y-%m-%d"
    ).date()
    return res


def _handle_same_date_scans(dfs):
    """
    Handles scans taken on the same date by separating them into left and right eye scans,
    dropping retakes, and merging the results.
    Args:
        dfs (list of pd.DataFrame): List of DataFrames, each containing scan data with columns
                                    "ScanMode", "Laterality", "ExaminationDateTime", "ExaminationDate",
                                    "PatientBirthDate", "PatientID", "PatientSex", "EthnicGroup",
                                    "PatientComment", and "PatientDisease".
    Returns:
        pd.DataFrame: A DataFrame containing the merged scan data for left and right eyes, with
                      duplicate scans removed and unnecessary columns dropped.
    Raises:
        AssertionError: If the scan modes are not consistent across all DataFrames or if the laterality
                        is not consistent within each DataFrame.
        ValueError: If there is an issue with merging the left and right DataFrames.
    """
    left = []
    right = []
    scanmode = []
    for df in dfs:
        scanmode.append(df["ScanMode"][0])
        if all(df["Laterality"] == "R"):
            right.append(df)
        else:
            assert all(df["Laterality"] == "L")
            left.append(df)
    assert len(set(scanmode)) <= 1
    right = pd.concat(right)
    left = pd.concat(left)

    def drop_retakes(df):
        df = df.sort_values("ExaminationDateTime", ascending=True)
        return df.drop_duplicates(
            [
                "ExaminationDate",
                "PatientBirthDate",
                "PatientID",
                "PatientSex",
                "EthnicGroup",
            ],
            keep="last",
        )

    right = drop_retakes(right)
    left = drop_retakes(left)

    right = right.drop(
        [
            "Laterality",
            "ScanMode",
            "ExaminationDateTime",
            "PatientComment",
            "PatientDisease",
        ],
        axis="columns",
        errors="ignore",
    )
    left = left.drop(
        [
            "Laterality",
            "ScanMode",
            "ExaminationDateTime",
            "PatientComment",
            "PatientDisease",
        ],
        axis="columns",
        errors="ignore",
    )

    try:
        df = right.merge(
            left,
            on=[
                "ExaminationDate",
                "PatientBirthDate",
                "PatientID",
                "PatientSex",
                "EthnicGroup",
            ],
            how="outer",
            suffixes=(False, False),
        )
    except ValueError as e:
        print(e)
        print(right.columns)
        print(left.columns)
        raise e
    return df


def fix_dtypes(
    df: pd.DataFrame,
    keep=[
        "PatientID",
        "PatientSex",
        "EthnicGroup",
        "ExaminationDate",
        "Target",
    ],
):
    for column in df.columns:
        if column not in keep:
            df[column] = pd.to_numeric(df[column])
    return df


def patient_to_df(files):
    """
    Converts patient data from a list of XML files into a consolidated DataFrame.
    This function processes a list of file paths, categorizing them into Disc, Glaucoma, 
    and Macula groups based on the file names. It then converts each XML file into a 
    DataFrame, handles scans taken on the same date, and merges the data into a single 
    DataFrame.
    Parameters:
    files (list): A list of file paths to the XML files containing patient data.
    Returns:
    pandas.DataFrame: A DataFrame containing the consolidated patient data from the 
    provided XML files.
    """
    disc = []
    glauc = []
    macula = []
    for path in files:
        path = str(path)
        if "Disc3D" in path:
            disc.append(path)
        elif "Glaucoma3D" in path:
            glauc.append(path)
        elif "Macula3D" in path:
            macula.append(path)
    disc_dfs = [xml_to_df(file).to_frame().T for file in disc]
    glauc_dfs = [xml_to_df(file).to_frame().T for file in glauc]
    macula_dfs = [xml_to_df(file).to_frame().T for file in macula]
    disc = _handle_same_date_scans(disc_dfs)
    glauc = _handle_same_date_scans(glauc_dfs)
    macula = _handle_same_date_scans(macula_dfs)
    df = disc.merge(
        glauc,
        on=[
            "ExaminationDate",
            "PatientBirthDate",
            "PatientID",
            "PatientSex",
            "EthnicGroup",
        ],
        how="outer",
        suffixes=(False, False),
    )
    df = df.merge(
        macula,
        on=[
            "ExaminationDate",
            "PatientBirthDate",
            "PatientID",
            "PatientSex",
            "EthnicGroup",
        ],
        how="outer",
        suffixes=(False, False),
    )

    return df


def load_xml_data(path):
    xml_file_loc = Path(path)
    df = patient_to_df(xml_file_loc.glob("**/*.xml"))
    df = fix_dtypes(df)
    return df


def load_data(xml_path, imed_path) -> pd.DataFrame:
    """
    Get all the data from the xml and imed files and combine them into a single dataframe.
        xml_path (str): Path to the xml files directory.
        imed_path (str): Path to the imed file.
    Returns:
        pd.DataFrame: A dataframe containing the combined data from the xml and imed files.
    """
    xml_df = load_xml_data(xml_path)
    imed_df_dict = pd.read_excel(Path(imed_path), sheet_name=None)
    imed_df = imed_df_dict["Identification"][
        ["Patient ID", "Birth Date", "Date of onset"]
    ]
    imed_df.loc[:, "Date of onset"] = pd.to_datetime(
        imed_df.loc[:, "Date of onset"], format="%d.%m.%Y"
    ).apply(lambda x: x.date())

    visist_df = imed_df_dict["Visits"]
    visist_df.loc[:, "Visit Date"] = pd.to_datetime(
        visist_df.loc[:, "Visit Date"], format="%d.%m.%Y"
    ).apply(lambda x: x.date())

    visist_df = visist_df[["Patient ID", "Visit Date", "EDSS"]]
    df = pd.merge(xml_df, imed_df, left_on="PatientID", right_on="Patient ID").drop(
        ["Patient ID", "Birth Date"], axis=1
    )
    df = pd.merge(
        df,
        visist_df,
        left_on=["PatientID", "ExaminationDate"],
        right_on=["Patient ID", "Visit Date"],
        how="inner",
    ).drop(["Patient ID", "Visit Date"], axis=1)

    df.loc[:, "EDSS"] = df["EDSS"].apply(
        lambda x: float(x.replace(",", ".")) if not pd.isnull(x) else np.nan
    )

    return df
