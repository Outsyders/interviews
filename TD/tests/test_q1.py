from basic_python.q1_strings_and_lists import sanitize_paths

def test_normalization_and_deduplication():
    """
    Test 1: Ensures mixed separators are normalized and resulting duplicates are removed.
    The test uses sets for comparison because the output order is not guaranteed.
    """
    raw_paths = [
        "C:\\projects\\outsyders_test\\seq\\ABC\\ABC1010\\work_dir\\ABC1010_comp_v001.nk",
        "/projects/outsyders_test/seq/s010/comp/layer.exr",
        "C:/projects/outsyders_test/seq/ABC/ABC1010/work_dir/ABC1010_comp_v001.nk",
        "\\\\server\\projects\\outsyders_test\\"
    ]
    
    expected_unique_paths = {
        "C:/projects/outsyders_test/seq/ABC/ABC1010/work_dir/ABC1010_comp_v001.nk",
        "/projects/outsyders_test/seq/s010/comp/layer.exr",
        "//server/projects/outsyders_test"
    }
   
    assert set(sanitize_paths(raw_paths)) == expected_unique_paths

def test_unc_path_normalization():
    """
    Test 2: Specifically checks the proper normalization of Windows UNC paths 
    (starting with \\\\) to the cross-platform //server/ format.
    """
    raw_paths = [
        "\\\\server_name\\share\\folder",
        "//server_name/share/folder",
        "\\\\server_name\\share\\folder\\",
        "//server_name/share/folder/"
    ]
    
    expected_unique_paths = {
        "//server_name/share/folder"
    }
    
    assert set(sanitize_paths(raw_paths)) == expected_unique_paths
