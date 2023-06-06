from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.experimental import AutoGPT
from langchain.chat_models import ChatOpenAI
import faiss
from BaseContent import BaseContent
from agents.cResearcher import Researcher
from typing import List, Optional
from langchain.tools import StructuredTool
from langchain.tools.human.tool import HumanInputRun
from Creator import QuestionInput, ResearchInput

from dotenv import load_dotenv

load_dotenv()


baseContent = BaseContent(
    filename="project_structure",
    title = "How to structure a nextjs project with typescript, trpc, prisma, cockroach db, nextauth and chakra ui",
    audience="Founders of SaaS startups who have raised money and need to build an MVP. They have a surface understanding of technology, so keep it simple and don't use too much jargon. Explain things in a way that a non-technical person could understand.",
    goals="Convince the audience that Beavr Labs is a knowledgeable and trustworthy company that can help them build their MVP",
    tone="Professional, but not too formal. Include some humor and personality",
)
baseContent.loadFromFile() # pulling from the file instead of starting over

print("loaded from file")
print(baseContent)



search = SerpAPIWrapper()
tools = [
    Tool(
        name = "search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    ),
    WriteFileTool(),
    ReadFileTool(),
    Tool(
        name = "add_question",
        func = baseContent.addQuestions,
        description = "add research questions to your todo list of questions to answer",
        args_schema = QuestionInput
    ),
    StructuredTool.from_function(
        name = "add_research_answer",
        func = baseContent.addResearch,
        description = "add an answer to a question. Make sure the answer actually answers the question. Otherwise try another search. The question should be in your todo list. If its not, add it first",
        args_schema = ResearchInput
    ),
    Tool(
        name = "remove_research_question",
        func = baseContent.removeQuestion,
        description = "remove a research question and its answer from your researched questions because you no longer need it",
    ),
    HumanInputRun()
]


embeddings_model = OpenAIEmbeddings()
embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

agent = Researcher.from_llm_and_tools(
    tools=tools,
    llm=ChatOpenAI(model="gpt-4"),
    memory=vectorstore.as_retriever(),
)
# Set verbose to be true
agent.chain.verbose = True

agent.run(baseContent, None)