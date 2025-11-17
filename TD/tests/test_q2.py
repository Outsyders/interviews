from basic_python.q2_parsing import increment_version, change_frame_padding

def test_version_increment_padding():
    """Test that the version increments correctly and maintains padding."""
    input_path = "shot_v099.nk"
    expected_output = "shot_v100.nk"
    
    assert increment_version(input_path) == expected_output

def test_no_version_found():
    """Test that the path is returned unchanged if no version is present."""   
    input_path = "asset_no_version.nk"
    
    assert increment_version(input_path) == input_path

def test_standard_padding():
    """
    Verifies the function handles standard 4-digit padding and normalizes backslashes.
    """
    input_path = "C:\\projects\\shotA\\render\\shotA_v001.1042.exr"
    expected_output = "C:\\projects\\shotA\\render\\shotA_v001.####.exr"
    
    assert change_frame_padding(input_path) == expected_output

def test_sample_data_path_no_padding():
    """
    Test a complex path that includes backslashes and a full directory structure.
    """
    input_path = "Y:\\projects\\dev\\seq\\TD\\TD0011\\plate\\pub_dir\\TD0011_plate_ingest_v009\\exr\\TD0011_plate_ingest_v009.exr"
    expected_output = "Y:\\projects\\dev\\seq\\TD\\TD0011\\plate\\pub_dir\\TD0011_plate_ingest_v009\\exr\\TD0011_plate_ingest_v009.exr"
    
    assert change_frame_padding(input_path) == expected_output
