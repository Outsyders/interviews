
"""
Refactor the following code, which prepares a render job dictionary, into a cleaner, more modular, and object-oriented design.

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
"""

from dataclasses import dataclass
from typing import Dict, Any

class RenderJobValidationError(Exception):
    """Custom exception for validation errors during job preparation."""
    pass

@dataclass(frozen=True) 
class RenderJob:
    """A container for render job submission data."""
    name: str
    frames: str
    priority: int
    output_path: str

class JobCreator:
    """Handles the creation and validation logic for a RenderJob."""
    
    def __init__(self, shot_name: str, version: int, options: Dict[str, Any]):
        """Initializes the job builder with core parameters."""
        if not shot_name or version <= 0:
            raise ValueError("Asset name must be provided and version must be positive.")
            
        self.shot_name = shot_name
        self.version = version
        self.options = options
        
    def _build_path(self) -> str:
        """Generating the submission path."""
        base_dir = self.options.get(
            'render_output', 
            "/projects/abc/seq/abc1010/comp/work_dir/renders/"
        )

        if base_dir and not base_dir.endswith('/'):
            base_dir += '/'
            
        return f"{base_dir}{self.shot_name}/v{self.version:03d}"
        
    def _validate_frames(self) -> str:
        """
        Validating and normalizing the frame range.
        Raises RenderJobValidationError on failure.
        """
        frames = self.options.get('frames', '1001-1100')
        if not isinstance(frames, str) or not frames.strip():
            raise RenderJobValidationError("Invalid or empty frame range provided.")
            
        return frames.strip()
        
    def _validate_priority(self) -> int:
        """
        Validating the job priority, setting the default, and capping the maximum.
        """
        priority = self.options.get('priority', 50)
        
        if not isinstance(priority, int):
            try:
                priority = int(priority)
            except ValueError:
                priority = 50 
                
        return min(priority, 99)

    def create_job(self) -> RenderJob:
        """The main factory method to assemble and return the RenderJob dataclass instance."""
        output_path = self._build_path()
        frames = self._validate_frames()
        priority = self._validate_priority()
        
        job_name = f"{self.shot_name}_v{self.version}_render"
        
        return RenderJob(
            name=job_name,
            frames=frames,
            priority=priority,
            output_path=output_path
        )
