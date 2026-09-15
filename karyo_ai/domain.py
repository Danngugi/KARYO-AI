from dataclasses import asdict, dataclass, field
from typing import Optional

@dataclass
class ChromosomeObject:
    object_id: int
    bbox: tuple[int, int, int, int]
    area: int
    centroid: tuple[float, float]
    label: Optional[str] = None
    confidence: float = 0.0
    status: str = "full"
    migrated: bool = False
    dislocated: bool = False
    touching: bool = False
    features: dict = field(default_factory=dict)
    notes: str = ""

    def to_dict(self): return asdict(self)

@dataclass
class AnalysisResult:
    source: str
    species: str
    modality: str
    objects: list[ChromosomeObject]
    qc: dict
    flags: list[str]
    reviewer: str = ""
    approved: bool = False

    def to_dict(self):
        return {"source": self.source, "species": self.species, "modality": self.modality,
                "objects": [x.to_dict() for x in self.objects], "qc": self.qc,
                "flags": self.flags, "reviewer": self.reviewer, "approved": self.approved}
