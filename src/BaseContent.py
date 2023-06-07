from typing import List
import os
import pickle
from pydantic import BaseModel, Field

class ArticleInput(BaseModel):
    article: str = Field(description="Write the contents of the article in markdown format here. Cannot be empty.")

class OutlineInput(BaseModel):
    outline: str = Field(description="The contents of the outline, in markdown format. Cannot be empty")

class QuestionInput(BaseModel):
    questions: List[str] = Field(description="A list of questions you want to answer in your research")

class ResearchInput(BaseModel):
    question: str = Field(description="The question you are answering from the todo list")
    answer: str = Field(description="The answer to the question")

class FeedbackInput(BaseModel):
    feedback: str = Field(description="The feedback you want to give on why the document is incomplete for your stage")

class BaseContent: 
    filename = ""
    title = "" # title of the content -> used to name the files and the content
    outline = "" # outline for the content
    content_type = "" # type of content (article, blog post, etc)
    content = ""
    todo_questions = set() # list of questions that need to be answered
    research = {} # pairs of (question, answer)
    audience = "" # who the content is for
    goals = "" # what the content is trying to achieve
    tone = "" # what the tone of the content is

    def __init__(self, filename: str, title: str, audience: str, goals: str, tone: str) -> None:
        self.filename = filename
        self.title = title
        self.audience = audience
        self.goals = goals
        self.tone = tone

    def writeArticle(self, article: str) -> None:
        self.content = article
        if article == "":
            return "please include the content of your article in the input"
        return "success"

    def writeOutline(self, outline: str) -> None:
        self.outline = outline
        if outline == "":
            return "please include the content of your outline in the input"
        return "success"

    # when a question is added to the content we add it to the todo list
    def addQuestions(self, questions: List[str]) -> None:
        for question in questions:
            self.todo_questions.add(question)
        return "success"

    # when a question is answered we add it to the research and remove it from the todo list
    def addResearch(self, question: str, answer: str) -> None:
        if question not in self.todo_questions:
            return "Error: question not in todo list"

        if question in self.research:
            self.research[question] += answer
            return "Success: added to existing research"
        else:
            self.research[question] = answer
            self.todo_questions.remove(question)
            return "Success: added to new research"

    # when a question is not relevant to the content anymore we remove it from the research
    def removeQuestion(self, question: str) -> None:
        if question not in self.research:
            return "Error: question not in research"
        del self.research[question]
        return "Success: removed question from research"
    
    def saveToFile(self) -> None:
        # if a directory called filename doesn't exist, create it
        if not os.path.exists(self.filename):
            os.makedirs(self.filename)
            
        if self.outline != "":
            with open(f"{self.filename}/outline.txt", "w") as f:
                f.write(self.outline)
                
        if self.content != "":
            with open(f"{self.filename}/article.md", "w") as f:
                f.write(self.content)

        # save the todo questions to a file
        with open(f"{self.filename}/todo_questions.txt", "w") as f:
            for question in self.todo_questions:
                f.write(f"{question}\n")

        # save the research to a file
        with open(f"{self.filename}/research.txt", "w") as f:
            for question, answer in self.research.items():
                f.write(f"{question}\n{answer}\n\n")

        # save the object as a pickle
        with open(f"{self.filename}/content.pkl", "wb") as f:
            pickle.dump(self, f)


    # load the data from the file
    def loadFromFile(self) -> None:

        if not os.path.exists(self.filename):
            return

        # load the data if it exists
        with open(f"{self.filename}/content.pkl", "rb") as f:
            data = pickle.load(f)
            self.title = data.title
            self.outline = data.outline
            self.content_type = data.content_type
            self.todo_questions = data.todo_questions
            self.research = data.research
            self.audience = data.audience
            self.goals = data.goals
            self.tone = data.tone

    def __str__(self) -> str:
        return f"Title: {self.title}\nOutline: {self.outline}\nContent Type: {self.content_type}\nTodo Questions: {self.todo_questions}\nResearch: {self.research}\nAudience: {self.audience}\nGoals: {self.goals}\nTone: {self.tone}"

