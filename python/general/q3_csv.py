import csv
import tempfile
import os
from typing import List, Dict, Any

SAMPLE_MANIFEST_CSV = """shot_name,sg_sequence,nuke_version,sg_comp_status,comp_artist
SH_010,SEQ_001,15,cmp,JSmith
SH_010,SEQ_001,12,cmp,JSmith
SH_020,SEQ_001,3,wtg,ASmith
SH_030,SEQ_002,5,na,JSmith
SH_030,SEQ_002,8,ip,JSmith
SH_040,SEQ_002,1,ip,RKhan
SH_040,SEQ_002,WIP,ip,ASmith
SH_050,SEQ_003,1,dep,RKhan
SH_060,SEQ_003,NA,dep,RKhan
"""

EMPTY_MANIFEST_CSV = """shot_name,sg_sequence,nuke_version,sg_comp_status,comp_artist"""

TEST_DATA = [SAMPLE_MANIFEST_CSV, EMPTY_MANIFEST_CSV]

def process_shot_manifest(file_path: str) -> List[Dict[str, Any]]:
    """
    Reads a Shot manifest, finds the record with the highest nuke_version for each unique shot.
    Handles non-numeric version strings gracefully.
    """
    latest_shots: Dict[str, Dict[str, Any]] = {}

    try:
        with open(file_path, newline="") as f:
            for row in csv.DictReader(f):
                try:
                    version = int(row["nuke_version"])
                except (ValueError, TypeError, KeyError):
                    continue  # skip rows with non-numeric versions
                shot = row["shot_name"]
                current = latest_shots.get(shot)
                if current is None or version > current["nuke_version"]:
                    record = dict(row)
                    record["nuke_version"] = version
                    latest_shots[shot] = record
    except FileNotFoundError:
        return []

    return list(latest_shots.values())


if __name__ == "__main__":
    temp_file_name = None
    for test_data in TEST_DATA:
        try:
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, newline='', encoding='utf-8')
            temp_file_name = temp_file.name
            temp_file.write(test_data)
            temp_file.close()

            filtered_results = process_shot_manifest(temp_file_name)
            if filtered_results:
                print(f"\nFound {len(filtered_results)} unique shots with their highest version:")
                print(f"{'Shot Name':<10} {'Sequence':<10} {'Version':<10} {'Status':<10} {'Artist':<10}")
                print("-" * 55)
                for shot in filtered_results:
                    print(
                        f"{shot['shot_name']:<10} "
                        f"{shot['sg_sequence']:<10} "
                        f"{shot['nuke_version']:<10} "
                        f"{shot['sg_comp_status']:<10} "
                        f"{shot['comp_artist']:<10}"
                    )
            else:
                print("No valid shots found in the manifest.")

        finally:
            if temp_file_name and os.path.exists(temp_file_name):
                os.remove(temp_file_name)