from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

prompt_template = "What is a good name for a company that makes {product}?"

# llm = OpenAI(temperature=0)
llm = ChatOpenAI(model="gpt-4")
llm_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(prompt_template)
)

llm_chain.verbose = True

print(llm_chain("colorful socks"))

# llm_chain.run(product = "socks")