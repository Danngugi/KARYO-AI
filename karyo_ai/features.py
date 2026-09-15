import numpy as np
from .domain import ChromosomeObject

def add_features(objects: list[ChromosomeObject], gray: np.ndarray) -> None:
    for obj in objects:
        x0,y0,x1,y1=obj.bbox; crop=gray[y0:y1,x0:x1]
        h,w=crop.shape; long=max(h,w); short=max(1,min(h,w))
        profile=(crop.mean(axis=1) if h >= w else crop.mean(axis=0)).tolist()
        # This is a proxy only, not a validated centromere measurement.
        centromere=float(np.argmin(profile)/max(1,len(profile)-1)) if profile else 0.5
        obj.features={"length_px": int(long), "width_px": int(short), "aspect_ratio": round(long/short,2),
                      "centromere_proxy": round(centromere,2), "band_profile": [round(float(v),1) for v in profile[::max(1,len(profile)//32)]]}
