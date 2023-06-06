from __future__ import annotations
from typing import Union
from BaseContent import BaseContent
from agents.Outliner import Outliner
from agents.Researcher import Researcher
from utils.StageReturnType import Stage, StageReturnType


class Creator:
    def __init__(self, researcher: Researcher, outliner: Outliner) -> None:
        self.researcher = researcher
        self.outliner = outliner
        # self.blogWriter = blogWriter
        # self.reviewer = reviewer

    def run(self, content: BaseContent) -> None:

        stage = Stage.RESEARCH
        feedback = None

        while (stage != Stage.PUBLISH):
            print("Stage: " + str(stage))
            print(feedback)

            if (stage == Stage.RESEARCH):
                res = self.researcher.run(content, feedback)
                stage = res.stage
                content = res.content

            elif (stage == Stage.OUTLINE):
                res = self.outliner.run(content, feedback)
                stage = res.stage
                content = res.content

            elif (stage == Stage.WRITE):
                print("Done for now")
                return 
                # writeReturnType = self.blogWriter.run(content, feedback)
                # stage = writeReturnType.stage
                # content = writeReturnType.content

            elif (stage == Stage.REVIEW):
                print("Done for now")
                return
                # reviewReturnType = self.reviewer.run(content, feedback)
                # stage = reviewReturnType.stage
                # content = reviewReturnType.content

