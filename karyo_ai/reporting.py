import json
from collections import Counter
from pathlib import Path
from .domain import AnalysisResult
from .species import chromosome_sort_key

DISCLAIMER = "RESEARCH/WORKFLOW-ASSISTANCE ONLY — not a diagnostic result. A certified cytogeneticist must independently review this draft before any use, and formal analytical validation is required before clinical/SOP use."

def write_json(result: AnalysisResult, path: str) -> None:
    Path(path).write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")

def write_report(result: AnalysisResult, path: str) -> None:
    objs=result.objects; counts=Counter(o.label for o in objs if o.label)
    lines=["# Draft Karyotype Image Analysis Report", "", f"**{DISCLAIMER}**", "", "## Source and QC", f"- Source image: `{result.source}`", f"- Species mode: {result.species}", f"- Detected/selected modality: {result.modality}"]
    lines += [f"- {k.replace('_',' ').title()}: {v}" for k,v in result.qc.items()]
    lines += ["", "## Candidate chromosome objects", f"- Objects segmented: {len(objs)}", f"- Full: {sum(o.status=='full' for o in objs)}", f"- Half/fragment: {sum(o.status=='half' for o in objs)}", f"- Marked migrated: {sum(o.migrated for o in objs)}", f"- Marked dislocated: {sum(o.dislocated for o in objs)}", "", "## Draft chromosome counts"]
    lines += [f"- `{key}`: {value}" for key,value in sorted(counts.items(), key=lambda x:chromosome_sort_key(x[0]))] or ["- No labels assigned."]
    lines += ["", "## Review flags"] + ([f"- {x}" for x in result.flags] if result.flags else ["- No automatic flags; this does not establish normality."])
    lines += ["", "## Object review table", "| Object | Draft label | Confidence | Status | Migrated | Dislocated | Touching | Notes |", "|---:|---|---:|---|---|---|---|---|"]
    for o in objs: lines.append(f"| {o.object_id} | {o.label or 'Unassigned'} | {o.confidence:.2f} | {o.status} | {o.migrated} | {o.dislocated} | {o.touching} | {o.notes} |")
    lines += ["", "## Human sign-off", f"- Reviewer: {result.reviewer or 'Not supplied'}", f"- Approved after manual review: {'Yes' if result.approved else 'No — draft only'}", "", "---", DISCLAIMER]
    Path(path).write_text("\n".join(lines)+"\n", encoding="utf-8")
