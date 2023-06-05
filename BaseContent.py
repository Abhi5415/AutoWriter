from typing import List

class BaseContent: 
    title = "" # title of the content -> used to name the files and the content
    outline = "" # outline for the content
    content_type = "" # type of content (article, blog post, etc)
    todo_questions = set() # list of questions that need to be answered
    research = {} # pairs of (question, answer)
    audience = "" # who the content is for
    goals = "" # what the content is trying to achieve
    tone = "" # what the tone of the content is

    def __init__(self, title: str, audience: str, goals: str, tone: str) -> None:
        self.title = title
        self.audience = audience
        self.goals = goals
        self.tone = tone

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