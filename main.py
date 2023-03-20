from llama_index import GPTSQLStructStoreIndex, SQLDatabase, SimpleDirectoryReader, GPTSimpleVectorIndex
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def query_database():
    engine = engine=create_engine(f'sqlite:///tokens.db')

    sql_database = SQLDatabase(engine,include_tables=['all_tokens'])

    index = GPTSQLStructStoreIndex(
        [],
        sql_database=sql_database, 
        table_name="all_tokens",
    )
    return index

def query_aave_db():
    engine = engine=create_engine(f'sqlite:///aave_accounts.db')

    sql_database = SQLDatabase(engine,include_tables=['my_table'])

    index = GPTSQLStructStoreIndex(
        [],
        sql_database=sql_database, 
        table_name="my_table",
    )
    return index

def main():
    index = None
    while index is None:
        option = input('Enter 1 for Tokens\nEnter 2 for AAVE: ')
        if option == '1':
            index = query_database()
        elif option == '2':
            index = query_aave_db()
        else:
            print('Invalid option, please try again.')

    query_string = input('Enter your query: ')

    response = index.query(query_string)
    print(response)

if __name__ == '__main__':
    main()