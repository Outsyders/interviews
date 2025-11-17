import re

"""
Write a function called increment_version that takes a file path string and a version tag prefix (e.g., _v). It should find the current version number, increment it by one, and return the new file path string.

Constraints & Error Handling:

The new version number must maintain zero-padding (e.g., 9 becomes 010 if it started as 009).

The function should return the original path unchanged if no matching version tag is found.

Additionally, if the path contains a frame number pad it with a sequence of hash symbols (#) corresponding to the number of digits in the padding.

The frame number will typically appear before the file extension, preceded by a dot (.)

Propose at least two unit tests or each function
"""

sample_data = [
    "C:\\projects\\outsyders_test\\seq\\ABC\\ABC1010\\work_dir\\ABC1010_comp_v001.nk",
    "X:\\projects\\PROJA\\seq\\NHR\\NHR2770\\stereo_manual\\work_dir\\nk\\PROJA_NHR2770_stereo_manual_v001.nk",
    "Y:\\projects\\dev\\seq\\TD\\TD0011\\plate\\pub_dir\\TD0011_plate_ingest_v009\\exr\\TD0011_plate_ingest_v009.1001.exr",
    "X:\\projects\\PROJA\\seq\\NHR\\NHR2770\\stereo_manual\\work_dir\\nk\\PROJA_NHR2770_stereo_manual_v001.160100.nk"
]

def increment_version(file_path: str, prefix: str = "_v") -> str:
    """
    Finds a version tag (e.g., _vXXX), increments it, and returns the new path.
    """
    pattern = rf"({prefix})(\d+)"
    
    match = re.search(pattern, file_path)
    
    if not match:
        return file_path

    current_version_str = match.group(2)
    current_version_int = int(current_version_str)

    new_version_int = current_version_int + 1
    padding_length = len(current_version_str)

    new_version_str = str(new_version_int).zfill(padding_length)

    return re.sub(pattern, rf"{prefix}{new_version_str}", file_path, count=1)

def change_frame_padding(normalized_file_path: str) -> str:
    """
    Replaces frame number padding (e.g., .1001.exr) with hash notation (e.g., .####.exr).
    """
    match = re.search(r'\.(\d+)\.([^\.]+)$', normalized_file_path)
    
    if match:
        frame_digits = match.group(1)
        extension = match.group(2)

        padding_length = len(frame_digits)
        hash_padding = '#' * padding_length
        return re.sub(r'\.(\d+)\.([^\.]+)$', f'.{hash_padding}.{extension}', normalized_file_path, count=1)
    
    return normalized_file_path


if __name__ == "__main__":
    for item_path in sample_data:
        print(change_frame_padding(increment_version(item_path)))
