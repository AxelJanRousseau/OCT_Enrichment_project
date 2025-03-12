from typing import Literal
import pandas as pd



_RNFL_COLUMNS = [
    "R_FourSectors_Temporal",
    "R_FourSectors_Superior",
    "R_FourSectors_Nasal",
    "R_FourSectors_Inferior",
    "R_TwelveSectors_Temporal",
    "R_TwelveSectors_TemporalSuperiorTemporal",
    "R_TwelveSectors_SuperiorSuperiorTemporal",
    "R_TwelveSectors_Superior",
    "R_TwelveSectors_SuperiorSuperiorNasal",
    "R_TwelveSectors_NasalSuperiorNasal",
    "R_TwelveSectors_Nasal",
    "R_TwelveSectors_NasalInferiorNasal",
    "R_TwelveSectors_InferiorInferiorNasal",
    "R_TwelveSectors_Inferior",
    "R_TwelveSectors_InferiorInferiorTemporal",
    "R_TwelveSectors_TemporalInferiorTemporal",
    "R_RNFLParameters_TSNITAverage",
    "R_RNFLParameters_StandardDeviation",
    "L_FourSectors_Temporal",
    "L_FourSectors_Superior",
    "L_FourSectors_Nasal",
    "L_FourSectors_Inferior",
    "L_TwelveSectors_Temporal",
    "L_TwelveSectors_TemporalSuperiorTemporal",
    "L_TwelveSectors_SuperiorSuperiorTemporal",
    "L_TwelveSectors_Superior",
    "L_TwelveSectors_SuperiorSuperiorNasal",
    "L_TwelveSectors_NasalSuperiorNasal",
    "L_TwelveSectors_Nasal",
    "L_TwelveSectors_NasalInferiorNasal",
    "L_TwelveSectors_InferiorInferiorNasal",
    "L_TwelveSectors_Inferior",
    "L_TwelveSectors_InferiorInferiorTemporal",
    "L_TwelveSectors_TemporalInferiorTemporal",
    "L_RNFLParameters_TSNITAverage",
    "L_RNFLParameters_StandardDeviation",
]

_ONH_COLUMNS = [
    "R_ONHParameters_DiscArea",
    "R_ONHParameters_RimArea",
    "R_ONHParameters_CupVolume",
    "R_ONHParameters_RimVolume",
    "R_ONHParameters_CDArea",
    "R_ONHParameters_CDVertical",
    "R_ONHParameters_CDHorizontal",
    "R_ONHParameters_RDMinimum",
    "R_ONHParameters_RimAbsence",
    "R_ONHParameters_DDLS",
    "L_ONHParameters_DiscArea",
    "L_ONHParameters_RimArea",
    "L_ONHParameters_CupVolume",
    "L_ONHParameters_RimVolume",
    "L_ONHParameters_CDArea",
    "L_ONHParameters_CDVertical",
    "L_ONHParameters_CDHorizontal",
    "L_ONHParameters_RDMinimum",
    "L_ONHParameters_RimAbsence",
    "L_ONHParameters_DDLS",
]

_GLUACOMA_COLUMNS = [
    "R_Total_Thickness_GCL_IPL",
    "R_Total_Thickness_NFL_GCL_IPL",
    "R_TwoSect_Thickness_GCL_IPL_Superior",
    "R_TwoSect_Thickness_GCL_IPL_Inferior",
    "R_TwoSect_DifferenceSI_GCL_IPL_Superior",
    "R_TwoSect_DifferenceSI_GCL_IPL_Inferior",
    "R_TwoSect_Thickness_NFL_GCL_IPL_Superior",
    "R_TwoSect_Thickness_NFL_GCL_IPL_Inferior",
    "R_TwoSect_DifferenceSI_NFL_GCL_IPL_Superior",
    "R_TwoSect_DifferenceSI_NFL_GCL_IPL_Inferior",
    "R_EightSect_Thickness_GCL_IPL_ParaInferiorNasal",
    "R_EightSect_Thickness_GCL_IPL_ParaInferiorTemporal",
    "R_EightSect_Thickness_GCL_IPL_ParaSuperiorTemporal",
    "R_EightSect_Thickness_GCL_IPL_ParaSuperiorNasal",
    "R_EightSect_Thickness_GCL_IPL_PeriInferiorNasal",
    "R_EightSect_Thickness_GCL_IPL_PeriInferiorTemporal",
    "R_EightSect_Thickness_GCL_IPL_PeriSuperiorTemporal",
    "R_EightSect_Thickness_GCL_IPL_PeriSuperiorNasal",
    "R_EightSect_DifferenceSI_GCL_IPL_ParaInferiorNasal",
    "R_EightSect_DifferenceSI_GCL_IPL_ParaInferiorTemporal",
    "R_EightSect_DifferenceSI_GCL_IPL_ParaSuperiorTemporal",
    "R_EightSect_DifferenceSI_GCL_IPL_ParaSuperiorNasal",
    "R_EightSect_DifferenceSI_GCL_IPL_PeriInferiorNasal",
    "R_EightSect_DifferenceSI_GCL_IPL_PeriInferiorTemporal",
    "R_EightSect_DifferenceSI_GCL_IPL_PeriSuperiorTemporal",
    "R_EightSect_DifferenceSI_GCL_IPL_PeriSuperiorNasal",
    "R_EightSect_Thickness_NFL_GCL_IPL_ParaInferiorNasal",
    "R_EightSect_Thickness_NFL_GCL_IPL_ParaInferiorTemporal",
    "R_EightSect_Thickness_NFL_GCL_IPL_ParaSuperiorTemporal",
    "R_EightSect_Thickness_NFL_GCL_IPL_ParaSuperiorNasal",
    "R_EightSect_Thickness_NFL_GCL_IPL_PeriInferiorNasal",
    "R_EightSect_Thickness_NFL_GCL_IPL_PeriInferiorTemporal",
    "R_EightSect_Thickness_NFL_GCL_IPL_PeriSuperiorTemporal",
    "R_EightSect_Thickness_NFL_GCL_IPL_PeriSuperiorNasal",
    "R_EightSect_DifferenceSI_NFL_GCL_IPL_ParaInferiorNasal",
    "R_EightSect_DifferenceSI_NFL_GCL_IPL_ParaInferiorTemporal",
    "R_EightSect_DifferenceSI_NFL_GCL_IPL_ParaSuperiorTemporal",
    "R_EightSect_DifferenceSI_NFL_GCL_IPL_ParaSuperiorNasal",
    "R_EightSect_DifferenceSI_NFL_GCL_IPL_PeriInferiorNasal",
    "R_EightSect_DifferenceSI_NFL_GCL_IPL_PeriInferiorTemporal",
    "R_EightSect_DifferenceSI_NFL_GCL_IPL_PeriSuperiorTemporal",
    "R_EightSect_DifferenceSI_NFL_GCL_IPL_PeriSuperiorNasal",
    "L_Total_Thickness_GCL_IPL",
    "L_Total_Thickness_NFL_GCL_IPL",
    "L_TwoSect_Thickness_GCL_IPL_Superior",
    "L_TwoSect_Thickness_GCL_IPL_Inferior",
    "L_TwoSect_DifferenceSI_GCL_IPL_Superior",
    "L_TwoSect_DifferenceSI_GCL_IPL_Inferior",
    "L_TwoSect_Thickness_NFL_GCL_IPL_Superior",
    "L_TwoSect_Thickness_NFL_GCL_IPL_Inferior",
    "L_TwoSect_DifferenceSI_NFL_GCL_IPL_Superior",
    "L_TwoSect_DifferenceSI_NFL_GCL_IPL_Inferior",
    "L_EightSect_Thickness_GCL_IPL_ParaInferiorNasal",
    "L_EightSect_Thickness_GCL_IPL_ParaInferiorTemporal",
    "L_EightSect_Thickness_GCL_IPL_ParaSuperiorTemporal",
    "L_EightSect_Thickness_GCL_IPL_ParaSuperiorNasal",
    "L_EightSect_Thickness_GCL_IPL_PeriInferiorNasal",
    "L_EightSect_Thickness_GCL_IPL_PeriInferiorTemporal",
    "L_EightSect_Thickness_GCL_IPL_PeriSuperiorTemporal",
    "L_EightSect_Thickness_GCL_IPL_PeriSuperiorNasal",
    "L_EightSect_DifferenceSI_GCL_IPL_ParaInferiorNasal",
    "L_EightSect_DifferenceSI_GCL_IPL_ParaInferiorTemporal",
    "L_EightSect_DifferenceSI_GCL_IPL_ParaSuperiorTemporal",
    "L_EightSect_DifferenceSI_GCL_IPL_ParaSuperiorNasal",
    "L_EightSect_DifferenceSI_GCL_IPL_PeriInferiorNasal",
    "L_EightSect_DifferenceSI_GCL_IPL_PeriInferiorTemporal",
    "L_EightSect_DifferenceSI_GCL_IPL_PeriSuperiorTemporal",
    "L_EightSect_DifferenceSI_GCL_IPL_PeriSuperiorNasal",
    "L_EightSect_Thickness_NFL_GCL_IPL_ParaInferiorNasal",
    "L_EightSect_Thickness_NFL_GCL_IPL_ParaInferiorTemporal",
    "L_EightSect_Thickness_NFL_GCL_IPL_ParaSuperiorTemporal",
    "L_EightSect_Thickness_NFL_GCL_IPL_ParaSuperiorNasal",
    "L_EightSect_Thickness_NFL_GCL_IPL_PeriInferiorNasal",
    "L_EightSect_Thickness_NFL_GCL_IPL_PeriInferiorTemporal",
    "L_EightSect_Thickness_NFL_GCL_IPL_PeriSuperiorTemporal",
    "L_EightSect_Thickness_NFL_GCL_IPL_PeriSuperiorNasal",
    "L_EightSect_DifferenceSI_NFL_GCL_IPL_ParaInferiorNasal",
    "L_EightSect_DifferenceSI_NFL_GCL_IPL_ParaInferiorTemporal",
    "L_EightSect_DifferenceSI_NFL_GCL_IPL_ParaSuperiorTemporal",
    "L_EightSect_DifferenceSI_NFL_GCL_IPL_ParaSuperiorNasal",
    "L_EightSect_DifferenceSI_NFL_GCL_IPL_PeriInferiorNasal",
    "L_EightSect_DifferenceSI_NFL_GCL_IPL_PeriInferiorTemporal",
    "L_EightSect_DifferenceSI_NFL_GCL_IPL_PeriSuperiorTemporal",
    "L_EightSect_DifferenceSI_NFL_GCL_IPL_PeriSuperiorNasal",
]

_MACULA_COLUMNS = [
    "R_ETDRSSectors_ILM_RPE_ParaTemporal",
    "R_ETDRSSectors_ILM_RPE_PeriTemporal",
    "R_ETDRSSectors_ILM_RPE_ParaNasal",
    "R_ETDRSSectors_ILM_RPE_PeriNasal",
    "R_ETDRSSectors_ILM_RPE_ParaSuperior",
    "R_ETDRSSectors_ILM_RPE_PeriSuperior",
    "R_ETDRSSectors_ILM_RPE_ParaInferior",
    "R_ETDRSSectors_ILM_RPE_PeriInferior",
    "R_ETDRSSectors_ILM_RPE_Central",
    "R_ETDRSSectors_ILM_BM_ParaTemporal",
    "R_ETDRSSectors_ILM_BM_PeriTemporal",
    "R_ETDRSSectors_ILM_BM_ParaNasal",
    "R_ETDRSSectors_ILM_BM_PeriNasal",
    "R_ETDRSSectors_ILM_BM_ParaSuperior",
    "R_ETDRSSectors_ILM_BM_PeriSuperior",
    "R_ETDRSSectors_ILM_BM_ParaInferior",
    "R_ETDRSSectors_ILM_BM_PeriInferior",
    "R_ETDRSSectors_ILM_BM_Central",
    "R_FullRetinal_ILM_RPE_Minimum",
    "R_FullRetinal_ILM_RPE_Average",
    "R_FullRetinal_ILM_RPE_Volume",
    "R_FullRetinal_ILM_BM_Minimum",
    "R_FullRetinal_ILM_BM_Average",
    "R_FullRetinal_ILM_BM_Volume",
    "L_ETDRSSectors_ILM_RPE_ParaTemporal",
    "L_ETDRSSectors_ILM_RPE_PeriTemporal",
    "L_ETDRSSectors_ILM_RPE_ParaNasal",
    "L_ETDRSSectors_ILM_RPE_PeriNasal",
    "L_ETDRSSectors_ILM_RPE_ParaSuperior",
    "L_ETDRSSectors_ILM_RPE_PeriSuperior",
    "L_ETDRSSectors_ILM_RPE_ParaInferior",
    "L_ETDRSSectors_ILM_RPE_PeriInferior",
    "L_ETDRSSectors_ILM_RPE_Central",
    "L_ETDRSSectors_ILM_BM_ParaTemporal",
    "L_ETDRSSectors_ILM_BM_PeriTemporal",
    "L_ETDRSSectors_ILM_BM_ParaNasal",
    "L_ETDRSSectors_ILM_BM_PeriNasal",
    "L_ETDRSSectors_ILM_BM_ParaSuperior",
    "L_ETDRSSectors_ILM_BM_PeriSuperior",
    "L_ETDRSSectors_ILM_BM_ParaInferior",
    "L_ETDRSSectors_ILM_BM_PeriInferior",
    "L_ETDRSSectors_ILM_BM_Central",
    "L_FullRetinal_ILM_RPE_Minimum",
    "L_FullRetinal_ILM_RPE_Average",
    "L_FullRetinal_ILM_RPE_Volume",
    "L_FullRetinal_ILM_BM_Minimum",
    "L_FullRetinal_ILM_BM_Average",
    "L_FullRetinal_ILM_BM_Volume",
]


def _create_drop_list(columns: list[str], keep: list | str | None) -> list[str]:
    if keep is None:
        return columns
    if isinstance(keep, str):
        keep = [keep]
    drop_colums = []
    for col in columns:
        keep_col = False
        for k in keep:
            if k in col:
                keep_col = True
                break
        if not keep_col:
            drop_colums.append(col)
    return drop_colums


def filter_RNFL_groups(
    df: pd.DataFrame,
    keep: Literal["TSNITAverage", "FourSectors", "TwelveSectors"] | list[str],
) -> pd.DataFrame:
    drop_colums = _create_drop_list(_RNFL_COLUMNS, keep)
    df = df.drop(drop_colums, axis=1)
    return df


def filter_ONH_groups(df, keep):
    drop_colums = _create_drop_list(_ONH_COLUMNS, keep)
    df = df.drop(drop_colums, axis=1)
    return df


def filter_MACULA_groups(
    df, keep_sector, keep_layers: Literal["both", "ILM_BM", "ILM_RPE"]
):
    drop_colums = _create_drop_list(_MACULA_COLUMNS, keep_sector)
    if keep_layers == "both":
        pass
    elif keep_layers == "ILM_BM":
        drop_colums.extend([col for col in _MACULA_COLUMNS if "ILM_RPE" in col])
    elif keep_layers == "ILM_RPE":
        drop_colums.extend([col for col in _MACULA_COLUMNS if "ILM_BM" in col])
    df = df.drop(drop_colums, axis=1)
    return df


def filter_GLAUCOMA_groups(
    df, keep_sector, keep_layers: Literal["both", "GCL_IPL", "NFL_GCL_IPL"] = "both"
):
    drop_colums = _create_drop_list(_GLUACOMA_COLUMNS, keep_sector)
    if keep_layers == "both":
        pass
    elif keep_layers == "GCL_IPL":
        drop_colums.extend([col for col in _GLUACOMA_COLUMNS if "NFL" in col])
    elif keep_layers == "NFL_GCL_IPL":
        drop_colums.extend([col for col in _GLUACOMA_COLUMNS if "NFL" not in col])
    df = df.drop(drop_colums, axis=1)
    return df


def filter_GCL_IPL_groups(
    df: pd.DataFrame, keep: Literal["TwoSect", "EightSect", "TotalSector"]
) -> pd.DataFrame:
    sel_columns = [
        col
        for col in df.columns
        if ("TwoSect" in col) or ("EightSect" in col) or ("TotalSector" in col)
    ]
    drop_colums = _create_drop_list(sel_columns, keep)
    df = df.drop(drop_colums, axis=1)
    return df


def filter_glaucoma3d(
    df: pd.DataFrame, keep: Literal["TotalSector", "TwoSectors", "EightSectors"]
) -> pd.DataFrame:
    columns = [
        col
        for col in df.columns
        if ("TotalSector" in col) or ("TwoSectors" in col) or ("EightSectors" in col)
    ]
    drop_colums = [col for col in columns if keep not in col]
    df = df.drop(drop_colums, axis=1)
    return df


def add_RNFL_summaries(df):
    for side in ["R", "L"]:
        tmp = df[
            [
                f"{side}_TwelveSectors_Temporal",
                f"{side}_TwelveSectors_TemporalSuperiorTemporal",
                f"{side}_TwelveSectors_SuperiorSuperiorTemporal",
                f"{side}_TwelveSectors_Superior",
                f"{side}_TwelveSectors_SuperiorSuperiorNasal",
                f"{side}_TwelveSectors_NasalSuperiorNasal",
                f"{side}_TwelveSectors_Nasal",
                f"{side}_TwelveSectors_NasalInferiorNasal",
                f"{side}_TwelveSectors_InferiorInferiorNasal",
                f"{side}_TwelveSectors_Inferior",
                f"{side}_TwelveSectors_InferiorInferiorTemporal",
                f"{side}_TwelveSectors_TemporalInferiorTemporal",
            ]
        ]
        df[f"{side}_RNFLParameters_Minimum"] = tmp.min(axis=1)
        df[f"{side}_RNFLParameters_Maximum"] = tmp.max(axis=1)
        df[f"{side}_RNFLParameters_Maximum"] = tmp.mean(axis=1)
    return df

def add_MACULA_summaries():
    pass

def split_eyes(df):
    left_c=[]
    right_c=[]
    for c in df.columns:
        # if not R_ the left or patient data
        if not c.startswith('R_'):
            left_c.append(c)
        if not c.startswith('L_'):
            right_c.append(c)

    df_r = df[right_c].copy()
    df_l= df[left_c].copy()
    df_r['Eye']='R'
    df_l['Eye']='L'
    df_r.rename(columns=lambda x: x[2:] if x.startswith('R_') else x,inplace=True)
    df_l.rename(columns=lambda x: x[2:] if x.startswith('L_') else x,inplace=True)
    split_df=pd.concat([df_r,df_l],axis=0).reset_index(drop=True)

    return split_df

