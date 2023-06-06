from enum import Enum
from BaseContent import BaseContent
from typing import Union

Stage = Enum('Stage', ['RESEARCH', 'OUTLINE', 'WRITE', 'REVIEW', 'PUBLISH'])

class StageReturnType:
    stage = Stage
    content = BaseContent
    feedback = Union[str, None]