from general.q1_strings_and_lists import sanitize_paths
from general.q2_parsing import increment_version, change_frame_padding
from general.q3_csv import process_shot_manifest


# --- q1: sanitize_paths -----------------------------------------------------
def test_sanitize_normalizes_and_dedupes():
    raw = [
        "C:\\projects\\seq\\ABC\\shot_v001.nk",
        "C:/projects/seq/ABC/shot_v001.nk",
        "\\\\server\\share\\folder\\",
        "//server/share/folder",
    ]
    assert set(sanitize_paths(raw)) == {
        "C:/projects/seq/ABC/shot_v001.nk",
        "//server/share/folder",
    }


# --- q2: version / frame parsing --------------------------------------------
def test_increment_version_keeps_padding():
    assert increment_version("shot_v099.nk") == "shot_v100.nk"


def test_increment_version_unchanged_when_absent():
    assert increment_version("asset_no_version.nk") == "asset_no_version.nk"


def test_change_frame_padding():
    assert change_frame_padding("shotA_v001.1042.exr") == "shotA_v001.####.exr"
    # No frame number -> unchanged.
    assert change_frame_padding("shotA_v001.exr") == "shotA_v001.exr"


# --- q3: shot manifest ------------------------------------------------------
MANIFEST = """shot_name,sg_sequence,nuke_version,sg_comp_status,comp_artist
SH_010,SEQ_001,15,cmp,JSmith
SH_010,SEQ_001,12,cmp,JSmith
SH_040,SEQ_002,1,ip,RKhan
SH_040,SEQ_002,WIP,ip,ASmith
SH_060,SEQ_003,NA,dep,RKhan
"""


def test_process_shot_manifest(tmp_path):
    path = tmp_path / "shots.csv"
    path.write_text(MANIFEST)

    result = process_shot_manifest(str(path))
    by_shot = {r["shot_name"]: r for r in result}

    assert by_shot["SH_010"]["nuke_version"] == 15      # highest of 15/12
    assert isinstance(by_shot["SH_010"]["nuke_version"], int)
    assert by_shot["SH_040"]["nuke_version"] == 1        # "WIP" row skipped
    assert "SH_060" not in by_shot                       # only "NA" -> dropped


def test_process_shot_manifest_missing_file():
    assert process_shot_manifest("/no/such/file.csv") == []
