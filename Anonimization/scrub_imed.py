import os

import pandas as pd

import argparse
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="scrub_imed.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--imed_path", type=str, help="Path to the imed file")
    parser.add_argument(
        "--imed_columns_file",
        type=str,
        help="Path to the file containing the columns that should be kept in the imed file",
    )
    parser.add_argument(
        "--csv",
        type=str,
        help="Path to the csv file containing the mapping between patient names and unique_ids",
    )
    args = parser.parse_args()

    # read csv containing the mapping between patient names and unique_ids
    id_df = pd.read_csv(args.csv)
    # normalize the strings and date to facilitate comparison
    for column in ["FamilyName", "GivenName", "PatientSex"]:
        id_df.loc[:, column] = id_df.loc[:, column].str.lower()
    id_df.loc["PatientBirthDate"] = pd.to_datetime(
        id_df["PatientBirthDate"], format="%Y-%m-%d"
    )
    id_df = id_df.drop(
        columns="PatientID"
    )  # drop the 'Canon' patient id to avoid confusion

    # read the imed file
    imed_df_dict = pd.read_excel(args.imed_path, sheet_name=None)
    # get patient identification data to campare with the patient -> unique_id mapping
    imed_id_df = imed_df_dict["Identification"][
        ["Patient ID", "Last Name", "First Name", "Birth Date", "Gender"]
    ].copy()
    for column in ["Last Name", "First Name", "Gender"]:
        imed_id_df.loc[:, column] = imed_id_df.loc[:, column].str.lower()

    imed_id_df.loc[:, "Birth Date"] = pd.to_datetime(
        imed_id_df.loc[:, "Birth Date"], format="%d.%m.%Y"
    )

    dupes = imed_id_df.duplicated(
        subset=["Last Name", "First Name", "Gender"], keep=False
    )
    if dupes.any():
        logger.error(
            f"Found apperent duplicates in imed file: {dupes.sum()} \n writing to imed_duplicates.csv"
        )
        imed_id_df[dupes].to_csv("imed_duplicates.csv", index=False)
        imed_id_df = imed_id_df.drop_duplicates(
            subset=["Last Name", "First Name", "Gender"]
        )
    # get patientes that are both in the id_df and imed_id_df
    merged_id = pd.merge(
        left=id_df,
        right=imed_id_df,
        how="inner",
        left_on=["FamilyName", "GivenName", "PatientSex", "PatientBirthDate"],
        right_on=["Last Name", "First Name", "Gender", "Birth Date"],
    )
    assert not merged_id.duplicated(
        subset=["Last Name", "First Name", "Gender"], keep=False
    ).any()

    if not id_df["UnifiedPatientID"].isin(merged_id["UnifiedPatientID"]).all():
        logger.error(
            "Not all patients in id_df are in imed_id_df \n writing to id_not_in_imed.csv"
        )
        id_df[~id_df["UnifiedPatientID"].isin(merged_id["UnifiedPatientID"])].to_csv(
            "id_not_in_imed.csv", index=False
        )

    if not imed_id_df["Patient ID"].isin(merged_id["Patient ID"]).all():
        logger.error(
            "Not all patients in imed_id_df are in id_df \n writing to imed_not_in_id.csv"
        )
        imed_id_df[~imed_id_df["Patient ID"].isin(merged_id["Patient ID"])].to_csv(
            "imed_not_in_id.csv", index=False
        )

    for sheet_name, df in imed_df_dict.items():
        if len(df) == 0:
            continue
        df = df[df["Patient ID"].isin(merged_id["Patient ID"])].copy()

        new_ids = df.loc[:, "Patient ID"].apply(
            lambda x: merged_id.loc[
                merged_id["Patient ID"] == x, "UnifiedPatientID"
            ].values[0]
        )
        df["Patient ID"] = df["Patient ID"].astype("object")
        df.loc[:, "Patient ID"] = new_ids
        imed_df_dict[sheet_name] = df

    # load file containing the columns that should be kept in the imed file
    imed_colums_dict = pd.read_excel(args.imed_columns_file, sheet_name=None)
    # write the new anonymous imed file
    with pd.ExcelWriter("anon_imed.xlsx") as writer:
        for sheet_name, df in imed_df_dict.items():
            df = df[imed_colums_dict[sheet_name].columns]  # filter out unneeded columns
            df.to_excel(writer, sheet_name=sheet_name, index=False)
