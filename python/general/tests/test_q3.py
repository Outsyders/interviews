import pytest
from general.q3_csv import process_shot_manifest

MOCK_MANIFEST_CSV = """shot_name,sg_sequence,nuke_version,sg_comp_status,comp_artist
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


@pytest.fixture
def manifest_file(tmp_path):
    """Creates a temporary manifest file for use in tests."""
    file_path = tmp_path / "shots.csv"
    file_path.write_text(MOCK_MANIFEST_CSV)
    return str(file_path)

def test_successful_filtering_and_conversion_shot_context(manifest_file):
    """
    Ensures filtering isolates high-version Nuke files
    """
    result = process_shot_manifest(manifest_file)
    assert len(result) == 5
    
    shot = result[0]
    assert shot['shot_name'] == 'SH_010'
    assert shot['sg_sequence'] == 'SEQ_001'
    assert isinstance(shot['nuke_version'], int)
    assert shot['nuke_version'] == 15

def test_robustness_and_version_thresholds_shots(manifest_file):
    """
    Checks all filtering/skipping behaviors for Nuke files:
    """    
    result = process_shot_manifest(manifest_file)
    assert len(result) == 5
    
    codes = {shot['shot_name'] for shot in result}
    assert 'SH_010' in codes
    assert 'SH_020' in codes
    assert 'SH_030' in codes
    assert 'SH_040' in codes
    assert 'SH_050' in codes
    assert 'SH_060' not in codes

def test_file_not_found_error():
    """
    Test 3: Ensures the function handles a missing file path gracefully 
    by returning an empty list.
    """
    non_existent_path = "/nonexistent/path/shots_manifest.csv"
    
    result = process_shot_manifest(non_existent_path)
    
    assert result == []