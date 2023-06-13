from __future__ import annotations
from typing import Union
from BaseContent import BaseContent
from agents.Outliner import Outliner
from agents.Researcher import Researcher
from agents.Writer import Writer
from utils.StageReturnType import Stage


class Creator:
    def __init__(self, researcher: Researcher, outliner: Outliner, writer: Writer) -> None:
        self.researcher = researcher
        self.outliner = outliner
        self.writer = writer
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
                feedback = res.feedback
                stage = res.stage
                content = res.content

            elif (stage == Stage.WRITE):
                res = self.writer.run(content, feedback)
                feedback = res.feedback
                stage = res.stage
                content = res.content

            elif (stage == Stage.REVIEW):
                print("Done for now")
                return
                # reviewReturnType = self.reviewer.run(content, feedback)
                # stage = reviewReturnType.stage
                # content = reviewReturnType.content
            

