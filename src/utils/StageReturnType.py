import enum
from BaseContent import BaseContent
from typing import Union

class Stage(enum.Enum):
    RESEARCH = 1
    OUTLINE = 2
    WRITE = 3
    REVIEW = 4
    PUBLISH = 5

class StageReturnType:
    def __init__(self, stage: Stage, content: BaseContent, feedback: Union[str, None]) -> None:
        self.stage = stage
        self.content = content
        self.feedback = feedback
    
    stage: Stage
    content: BaseContent
    feedback: Union[str, None]