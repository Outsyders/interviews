
"""
Refactor the following code, which prepares a render job dictionary, into a cleaner, more modular, and object-oriented design.
"""

def prepare_render_job(shot_name, version, options):
    # Part 1: Path Generation
    base_dir = options.get('render_output', "/projects/abc/seq/abc1010/comp/work_dir/renders/")
    submission_path = f"{base_dir}{shot_name}/v{version:03d}"
    
    # Part 2: Option Validation and Defaults
    render_frames = options.get('frames', '1001-1100')
    if not isinstance(render_frames, str) or not render_frames:
        raise ValueError("Invalid frame range.")
        
    priority = options.get('priority', 50)
    if priority > 99:
        priority = 99 # Cap priority
        
    # Part 3: Job Description Creation
    job_description = {
        "Name": f"{shot_name}_v{version}_render",
        "Frames": render_frames,
        "Priority": priority,
        "Output": submission_path
    }
    
    return job_description
