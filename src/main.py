
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from agents.Researcher import Researcher
from agents.Outliner import Outliner
from agents.Writer import Writer
import faiss
from BaseContent import BaseContent
from Creator import Creator


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

embeddings_model = OpenAIEmbeddings()
embedding_size = 1536

researcher = Researcher.from_llm_and_tools(
    llm=ChatOpenAI(model="gpt-4"),
    content=baseContent,
    memory=FAISS(embeddings_model.embed_query, faiss.IndexFlatL2(embedding_size), InMemoryDocstore({}), {}).as_retriever(),
)
researcher.chain.verbose = True

outliner = Outliner.from_llm_and_tools(
    llm=ChatOpenAI(model="gpt-4"),
    content=baseContent,
    memory=FAISS(embeddings_model.embed_query, faiss.IndexFlatL2(embedding_size), InMemoryDocstore({}), {}).as_retriever(),
)
outliner.chain.verbose = True

writer = Writer.from_llm_and_tools(
    llm=ChatOpenAI(model="gpt-4"),
    content=baseContent,
    memory=FAISS(embeddings_model.embed_query, faiss.IndexFlatL2(embedding_size), InMemoryDocstore({}), {}).as_retriever(),
)
writer.chain.verbose = True

creator = Creator(
    researcher=researcher,
    outliner=outliner,
    writer=writer,
)

creator.run(baseContent)
