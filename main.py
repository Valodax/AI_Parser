from llama_index import GPTSQLStructStoreIndex, SQLDatabase, SimpleDirectoryReader, GPTSimpleVectorIndex, download_loader
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

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

    query_string = input('Enter your query: ')

    response = index.query(query_string)
    print(response)

if __name__ == '__main__':
    main()