# tools/ingest_annotations.py
import argparse
import pandas as pd
from dotenv import load_dotenv
from storage.mssql import mssql_engine_from_env, bulk_insert

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to annotations.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    # Chuẩn hoá tên cột về đúng DDL
    rename_map = {
        "ann_id": "AnnID",
        "study_id": "StudyID",
        "series_uid": "SeriesUID",
        "x": "X", "y": "Y", "z": "Z",
        "diameter_mm": "DiameterMM",
        "location_label": "LocationLabel",
    }
    df = df.rename(columns=rename_map)
    required = ["AnnID","StudyID","X","Y","Z"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Thiếu cột bắt buộc: {col}")

    engine = mssql_engine_from_env()
    bulk_insert(df, "AneurysmFindings", engine)
    print("Inserted annotations:", len(df))
