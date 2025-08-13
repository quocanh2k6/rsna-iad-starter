# core/entities.py
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Tuple

@dataclass
class Study:
    study_id: str
    patient_id: str
    site: Optional[str]
    modalities: List[str]
    root_dir: Path
    has_aneurysm: Optional[bool] = None

@dataclass
class Series:
    study_id: str
    series_uid: str
    modality: str
    plane: Optional[str]
    n_instances: int
    dirpath: Path

@dataclass
class Instance:
    series_uid: str
    sop_uid: str
    instance_number: int
    filepath: Path
    spacing_xyz: Optional[Tuple[float, float, float]] = None
    origin_xyz: Optional[Tuple[float, float, float]] = None

@dataclass
class AneurysmAnnotation:
    ann_id: str
    study_id: str
    series_uid: Optional[str]
    x: float
    y: float
    z: float
    d_mm: Optional[float]
    location_label: Optional[str]
