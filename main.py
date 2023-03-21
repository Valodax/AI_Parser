from llama_index import GPTSQLStructStoreIndex, SQLDatabase, SimpleDirectoryReader, GPTSimpleVectorIndex
from langchain.agents import Tool, initialize_agent
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def query_database():
    db_name = input('Enter the database name and location: ')
    if db_name.endswith('.db'):
        db_name = db_name[:-3]
    if not os.path.exists(f"databases/{db_name}.db"):
        print(f"Error: {db_name}.db does not exist in databases.")
        return None
    print("Indexing all tables in the database...")
    engine = engine=create_engine(f'sqlite:///databases/{db_name}.db')

    sql_database = SQLDatabase(engine)
    index = GPTSQLStructStoreIndex(
        [],
        sql_database=sql_database, 
    )
    return index

def query_csv():
    csvs = SimpleDirectoryReader('csvs').load_data()
    index = GPTSimpleVectorIndex(csvs)
    return index

def query_document():
    documents = SimpleDirectoryReader('documents').load_data()
    index = GPTSimpleVectorIndex(documents)
    return index

def main():
    index = None
    while index is None:
        option = input('What would you like to index?:\n1) Database\n2) CSV\n3) Document\n')
        if option == '1':
            index = query_database()
        elif option == '2':
            index = query_csv()
        elif option == '3':
            index = query_document()
        else:
            print('Invalid option, please try again.')
    tools = [
        Tool(
            name = "GPT Index",
            func=lambda q: str(index.query(q)),
            description="The input to this tool should be a complete english sentence.",
            return_direct=True
        ),
    ]
    memory = ConversationBufferMemory(memory_key="chat_history")
    llm = OpenAI(temperature=0)
    agent_chain = initialize_agent(tools, llm, agent="conversational-react-description", memory=memory)
    while True:
        result = agent_chain.run(input=input("Ask a question: "))
        print(result)

if __name__ == '__main__':
    main()