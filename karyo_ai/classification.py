from .domain import ChromosomeObject
from .species import get_species

def classify_heuristic(objects: list[ChromosomeObject], species: str) -> None:
    """Draft morphology ordering only. Never use this as a clinical chromosome call."""
    labels=get_species(species).autosome_labels
    ordered=sorted(objects,key=lambda o:o.features.get("length_px",0),reverse=True)
    for i,obj in enumerate(ordered):
        if obj.label: continue
        obj.label=labels[min(i//2, len(labels)-1)] if labels else "unassigned"
        obj.confidence=0.15

def apply_annotations(objects: list[ChromosomeObject], annotations: dict[int,dict]) -> None:
    for obj in objects:
        row=annotations.get(obj.object_id)
        if not row: continue
        obj.label=row.get("chromosome_label") or obj.label
        obj.status=row.get("status") or obj.status
        obj.migrated=str(row.get("migrated", "")).lower() in {"1","true","yes","y"}
        obj.dislocated=str(row.get("dislocated", "")).lower() in {"1","true","yes","y"}
        obj.notes=row.get("notes", "")
        obj.confidence=1.0
