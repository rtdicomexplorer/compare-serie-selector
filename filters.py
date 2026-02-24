from config import MAX_SLICE_THICKNESS, KERNEL_EXCLUDE_KEYWORDS

def is_axial(orientation):
    if orientation is None:
        return False
    return abs(orientation[2]) < 0.01 and abs(orientation[5]) < 0.01


def passes_hard_filters(meta):
    if meta["SliceThickness"] is None:
        return False

    if meta["SliceThickness"] > MAX_SLICE_THICKNESS:
        return False

    if not is_axial(meta["ImageOrientation"]):
        return False

    for keyword in KERNEL_EXCLUDE_KEYWORDS:
        if keyword in meta["ConvolutionKernel"]:
            return False

    return True