import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import (
    create_openai_functions_agent,
    AgentExecutor,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.retriever import create_retriever_tool
from .tools.chatbot_retriever_tool import get_retriever
from .prompt.system_prompt import system


load_dotenv()
openai_model = os.getenv('OPENAI_MODEL')
openai_api_key = os.getenv("OPENAI_API_KEY")
host = os.getenv('HOST')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABSE')

# Set up information for account of Mysql
DB_CONFIG = {
    "host": host,
    "user": user,
    "password": password,
    "database": database,
}

# Create tool for agent
tool = create_retriever_tool(
    retriever = get_retriever,
    name = "Search",
    description="Search the information of Vietnamese history and culture."
)
tools = [tool]

chat_model = ChatOpenAI(
    model = openai_model,
    temperature=0,
    streaming=True,
    api_key=openai_api_key,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create agent for system
chatbot_agent = create_openai_functions_agent(
    llm=chat_model,
    prompt=prompt,
    tools=tools
)
chatbot_agent_executor = AgentExecutor(
    agent=chatbot_agent,
    tools=tools,
    verbose=True,
)
