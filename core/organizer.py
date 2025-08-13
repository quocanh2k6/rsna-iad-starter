# core/organizer.py
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional
from .entities import Series, Instance
import pydicom
from tqdm import tqdm

class RSNAIADOrganizer:
    def __init__(self, data_root: str):
        self.root = Path(data_root)

    def scan_series(self) -> List[Series]:
        """Quét tất cả series từ thư mục DICOM (dựa trên .dcm rải rác)."""
        seen = set()
        series_list: List[Series] = []
        for dcm_file in tqdm(list(self.root.rglob("*.dcm")), desc="Scanning DICOM (series)"):
            try:
                ds = pydicom.dcmread(dcm_file, stop_before_pixels=True)
                study_id = str(ds.StudyInstanceUID)
                series_uid = str(ds.SeriesInstanceUID)
                modality = str(getattr(ds, "Modality", "UNK"))
                key = (study_id, series_uid)
                if key in seen:
                    continue
                seen.add(key)
                series_list.append(
                    Series(study_id, series_uid, modality, None, 0, dcm_file.parent)
                )
            except Exception as e:
                print("Error reading", dcm_file, e)
        return series_list

    def scan_instances(self, series_path: Path, series_uid: str) -> List[Instance]:
        """Quét instance trong 1 series (dựa trên thư mục series_path)."""
        instances: List[Instance] = []
        for dcm_file in sorted(series_path.glob("*.dcm")):
            try:
                ds = pydicom.dcmread(dcm_file, stop_before_pixels=True)
                sop_uid = str(ds.SOPInstanceUID)
                instance_number = int(getattr(ds, "InstanceNumber", 0))
                spacing = getattr(ds, "PixelSpacing", [None, None])
                spacing_z = getattr(ds, "SliceThickness", None)
                sx = float(spacing[0]) if spacing and spacing[0] is not None else None
                sy = float(spacing[1]) if spacing and spacing[1] is not None else None
                sz = float(spacing_z) if spacing_z is not None else None
                instances.append(
                    Instance(series_uid, sop_uid, instance_number, dcm_file, (sx, sy, sz), None)
                )
            except Exception as e:
                print("Error reading", dcm_file, e)
        return instances
