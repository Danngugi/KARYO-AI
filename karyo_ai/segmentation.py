import numpy as np
from scipy import ndimage
from .domain import ChromosomeObject

# 4-connectivity, matching the original baseline's neighbour rule.
_FOUR_CONNECTED = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])


def segment(mask: np.ndarray, min_area: int = 25) -> list[ChromosomeObject]:
    """Label connected foreground regions into draft ChromosomeObject candidates.

    Uses scipy.ndimage's vectorized labelling instead of a pixel-by-pixel
    Python flood fill: on real (larger, noisier) chromosome spread images the
    Python version does not scale, since its cost grows with total foreground
    pixel count rather than component count. Region sizes and centroids are
    computed with np.bincount rather than ndimage.sum/center_of_mass, which
    are much slower once there are more than a few hundred labelled regions.
    Regions smaller than ``min_area`` pixels are dropped as noise, matching
    the original baseline's behaviour.
    """
    labelled, count = ndimage.label(mask, structure=_FOUR_CONNECTED)
    if count == 0:
        return []

    flat_labels = labelled.ravel()
    foreground = np.flatnonzero(flat_labels)
    labels_at_foreground = flat_labels[foreground]
    rows, cols = np.unravel_index(foreground, mask.shape)

    sizes = np.bincount(labels_at_foreground, minlength=count + 1)[1:]
    sum_rows = np.bincount(labels_at_foreground, weights=rows, minlength=count + 1)[1:]
    sum_cols = np.bincount(labels_at_foreground, weights=cols, minlength=count + 1)[1:]
    slices = ndimage.find_objects(labelled)

    kept_ids = np.flatnonzero(sizes >= min_area) + 1
    if kept_ids.size == 0:
        return []
    median = float(np.median(sizes[kept_ids - 1]))

    objects = []
    for object_id, label_id in enumerate(kept_ids, 1):
        idx = label_id - 1
        size = sizes[idx]
        cy = sum_rows[idx] / size
        cx = sum_cols[idx] / size
        y_slice, x_slice = slices[idx]
        bbox = (x_slice.start, y_slice.start, x_slice.stop, y_slice.stop)
        touching = bool(size > max(1, median) * 2.5)
        objects.append(ChromosomeObject(object_id, bbox, int(size), (float(cx), float(cy)), touching=touching))
    return objects
