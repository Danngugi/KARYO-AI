from collections import Counter
from PIL import Image, ImageDraw
from .domain import ChromosomeObject
from .species import chromosome_sort_key, get_species

def count_flags(objects: list[ChromosomeObject], species: str) -> list[str]:
    config=get_species(species); counts=Counter(o.label for o in objects if o.label)
    flags=[]
    for label in config.autosome_labels:
        n=counts.get(label,0)
        if n != 2: flags.append(f"Draft count for chromosome {label}: {n}; expected 2. Human review required.")
    if any(o.touching for o in objects): flags.append("Touching/overlapping candidate objects detected; segmentation needs review.")
    return flags

def render_karyogram(image: Image.Image, objects: list[ChromosomeObject], path: str) -> None:
    tiles=[]
    for obj in sorted(objects,key=lambda o:(chromosome_sort_key(o.label),o.object_id)):
        x0,y0,x1,y1=obj.bbox; crop=image.crop((x0,y0,x1,y1)); crop.thumbnail((100,150))
        tile=Image.new("RGB",(120,190),"white"); tile.paste(crop,((120-crop.width)//2,10)); d=ImageDraw.Draw(tile)
        d.text((5,165),f"{obj.object_id}: {obj.label or '?'}",fill="black"); tiles.append(tile)
    cols=8; rows=max(1,(len(tiles)+cols-1)//cols); out=Image.new("RGB",(cols*120,rows*190),(245,245,245))
    for i,tile in enumerate(tiles): out.paste(tile,((i%cols)*120,(i//cols)*190))
    out.save(path)
