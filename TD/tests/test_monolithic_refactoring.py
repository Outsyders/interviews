import pytest
from refactoring.monolithic import JobCreator, RenderJobValidationError 


def test_valid_job_creation_and_priority_cap():
    """
    Tests successful job creation and verifies that the priority is correctly capped at 99.
    """
    valid_options = {
        'render_output': "//projects/test/seq/shot/work_dir/render",
        'frames': '101-201',
        'priority': 150
    }

    builder = JobCreator(
        shot_name="seq_shot_comp_render", 
        version=7, 
        options=valid_options
    )
    job_instance = builder.create_job()
    

    assert job_instance.name == "seq_shot_comp_render_v7_render"
    assert job_instance.priority == 99
    assert job_instance.output_path == "//projects/test/seq/shot/work_dir/render/seq_shot_comp_render/v007"


def test_invalid_frame_range_raises_error():
    """
    Tests that job creation fails with RenderJobValidationError when frames are invalid.
    """
    invalid_options = {
        'frames': '  ', 
        'priority': 60
    }
    
    builder = JobCreator(
        shot_name="Shot_A010", 
        version=1, 
        options=invalid_options
    )

    with pytest.raises(RenderJobValidationError) as excinfo:
        builder.create_job()
        
    assert "Invalid or empty frame range provided" in str(excinfo.value)


def test_invalid_initialization_raises_value_error():
    """
    Tests that object initialization fails with a standard ValueError for bad inputs (like negative version).
    """

    with pytest.raises(ValueError) as excinfo:
        JobCreator(shot_name="TestShot", version=-1, options={})

    assert "version must be positive" in str(excinfo.value)
