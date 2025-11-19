"""
Write a function called sanitize_paths that takes a list of raw file path strings and performs two main tasks:

Normalize Separators: Convert all path separators to the forward slash (/).

Deduplicate: Remove any duplicate paths. The output order is not critical.
"""

raw_paths = [
    "C:\\projects\\outsyders_test\\seq\\ABC\\ABC1010\\work_dir\\ABC1010_comp_v001.nk",
    "/projects/outsyders_test/seq/s010/comp/layer.exr",
    "C:/projects/outsyders_test/seq/ABC/ABC1010/work_dir/ABC1010_comp_v001.nk",
    "\\\\server\\projects\\outsyders_test\\"
]

def sanitize_paths(raw_paths: list[str]) -> list[str]:
    return []
