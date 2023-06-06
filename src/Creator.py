from __future__ import annotations

from typing import List, Optional,Any, Callable, Union
from langchain import BasePromptTemplate

from pydantic import BaseModel, ValidationError

from langchain.chains.llm import LLMChain
from langchain.chat_models.base import BaseChatModel
from langchain.experimental.autonomous_agents.autogpt.output_parser import (
    AutoGPTOutputParser,
    BaseAutoGPTOutputParser,
)
from langchain.experimental.autonomous_agents.autogpt.prompt import AutoGPTPrompt
from langchain.experimental.autonomous_agents.autogpt.prompt_generator import (
    FINISH_NAME,
)
from langchain.schema import (
    AIMessage,
    BaseMessage,
    Document,
    HumanMessage,
    SystemMessage,
)
from langchain.tools.base import BaseTool
from langchain.tools.human.tool import HumanInputRun
from langchain.vectorstores.base import VectorStoreRetriever
from BaseContent import BaseContent
from enum import Enum
from pydantic import BaseModel, Field


Stage = Enum('Stage', ['RESEARCH', 'OUTLINE', 'WRITE', 'REVIEW', 'PUBLISH'])

class QuestionInput(BaseModel):
    questions: List[str] = Field(description="A list of questions you want to answer in your research")

class ResearchInput(BaseModel):
    question: str = Field(description="The question you are answering from the todo list")
    answer: str = Field(description="The answer to the question")

class FeedbackInput(BaseModel):
    feedback: str = Field(description="The feedback you want to give on why the document is incomplete for your stage")

class StageReturnType:
    stage = Stage
    content = BaseContent
    feedback = Union[str, None]

class Creator:
    def __init__(self, researcher: Researcher, outliner: Outliner, blogWriter: BlogWriter, reviewer: Reviewer) -> None:
        self.researcher = researcher
        self.outliner = outliner
        self.blogWriter = blogWriter
        self.reviewer = reviewer

    def run(self, content: BaseContent) -> None:

        stage = Stage.RESEARCH
        feedback = None

        while (stage != Stage.PUBLISH):
            if (stage == Stage.RESEARCH):
                researchReturnType = self.researcher.run(content, feedback)
                stage = researchReturnType.stage
                content = researchReturnType.content

            elif (stage == Stage.OUTLINE):
                outlineReturnType = self.outliner.run(content, feedback)
                stage = outlineReturnType.stage
                content = outlineReturnType.content

            elif (stage == Stage.WRITE):
                writeReturnType = self.blogWriter.run(content, feedback)
                stage = writeReturnType.stage
                content = writeReturnType.content

            elif (stage == Stage.REVIEW):
                reviewReturnType = self.reviewer.run(content, feedback)
                stage = reviewReturnType.stage
                content = reviewReturnType.content


class Researcher:
    pass

class Outliner:
    pass

class BlogWriter:
    pass

class Reviewer:
    pass
