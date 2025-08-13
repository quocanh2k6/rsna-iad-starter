# tools/ingest_dicoms.py
import argparse, os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from core.organizer import RSNAIADOrganizer
from storage.mssql import mssql_engine_from_env, bulk_insert

def scan_series(data_root: str) -> pd.DataFrame:
    org = RSNAIADOrganizer(data_root)
    series_list = org.scan_series()
    df = pd.DataFrame([{
        "StudyID": s.study_id,
        "SeriesUID": s.series_uid,
        "Modality": s.modality,
        "Plane": s.plane,
        "NInstances": s.n_instances,
        "DirPath": str(s.dirpath)
    } for s in series_list])
    return df

def scan_instances(df_series: pd.DataFrame) -> pd.DataFrame:
    org = RSNAIADOrganizer("")  # dùng phương thức, không cần root ở đây
    rows = []
    for _, row in df_series.iterrows():
        series_uid = row["SeriesUID"]
        series_path = Path(row["DirPath"]).resolve()
        instances = org.scan_instances(series_path, series_uid)
        for ins in instances:
            sx, sy, sz = (ins.spacing_xyz or (None, None, None))
            rows.append({
                "SOPInstanceUID": ins.sop_uid,
                "SeriesUID": ins.series_uid,
                "InstanceNumber": ins.instance_number,
                "FilePath": str(ins.filepath),
                "SpacingX": sx, "SpacingY": sy, "SpacingZ": sz,
                "OriginX": None, "OriginY": None, "OriginZ": None
            })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan", choices=["series", "instances"], required=True)
    parser.add_argument("--data_root", default=os.getenv("DATA_ROOT", "./data"))
    args = parser.parse_args()

    engine = mssql_engine_from_env()

    if args.scan == "series":
        df_series = scan_series(args.data_root)
        if not df_series.empty:
            print("Found", len(df_series), "series")
            bulk_insert(df_series, "Series", engine)
            print("Inserted Series ->", len(df_series))
        else:
            print("No series found.")

    elif args.scan == "instances":
        # cần Series đã có trong DB; để đơn giản, đọc lại từ DB có thể lập trình thêm.
        # ở đây đọc từ file tạm CSV nếu có.
        csv_path = Path("outputs/series_cache.csv")
        if csv_path.exists():
            df_series = pd.read_csv(csv_path)
        else:
            print("Vui lòng chạy --scan series và lưu tạm df_series ra outputs/series_cache.csv")
            exit(1)
        df_instances = scan_instances(df_series)
        if not df_instances.empty:
            print("Found", len(df_instances), "instances")
            bulk_insert(df_instances, "Instances", engine)
            print("Inserted Instances ->", len(df_instances))
